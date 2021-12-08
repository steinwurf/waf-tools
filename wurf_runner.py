#!/usr/bin/env python
# encoding: utf-8
# Carlos Rafael Giani, 2006
# Thomas Nagy, 2010
# Script is based on the waf_unit_test tool, but has since
# been significantly rewritten.

"""
Tool for running unit tests and benchmarks on various platforms.

This tool is loaded automatically in the wscript of "waf-tools".

The '--run_tests' option will run the programs that use the 'test' feature:

def build(bld):
    bld.program(features = 'cxx test',
                source   = ['main.cpp'],
                target   = 'hello')

The '--run_benchmarks' and '--run_benchmark=...' options are used to run
programs that define the 'benchmark' feature:

def build(bld):
    bld.program(features = 'cxx benchmark',
                source   = ['main.cpp'],
                target   = 'my_benchmark')

This tool can also copy test files. This is useful when writing
tests that require some input data files in order to run. The test files
will be copied to the directory where the test binary will be executed.

Test files can be added with the 'test_files' attribute:

def build(bld):
    bld.program(features   = 'cxx test',
                source     = ['main.cpp'],
                target     = 'hello',
                test_files = ['test_input.txt'])
"""

import os

from waflib import Errors
from waflib import Logs
from waflib import Utils
from waflib.TaskGen import feature, after_method

from runners.android_runner import AndroidRunner
from runners.basic_runner import BasicRunner
from runners.ios_runner import IOSRunner
from runners.ssh_runner import SSHRunner
from runners.emscripten_runner import EmscriptenRunner

# We keep a list of the run tasks so that we can execute them sequentially
run_tasks = []


def options(opt):

    opts = opt.add_option_group("Runner options")

    opts.add_option(
        "--run_tests",
        default=None,
        dest="run_tests",
        action="store_true",
        help="Run all unit tests",
    )

    opts.add_option(
        "--run_silent",
        default=None,
        dest="run_silent",
        action="store_true",
        help="Do not print the test output on success " "(used with --run_tests)",
    )

    opts.add_option(
        "--run_benchmarks",
        default=None,
        dest="run_benchmarks",
        action="store_true",
        help="Run all benchmarks",
    )

    opts.add_option(
        "--run_benchmark",
        default=None,
        dest="run_benchmark",
        help="Run a specific benchmark",
    )

    opts.add_option(
        "--print_benchmarks",
        default=None,
        dest="print_benchmarks",
        action="store_true",
        help="Print the names of the defined benchmarks",
    )

    opts.add_option(
        "--print_benchmark_paths",
        default=None,
        dest="print_benchmark_paths",
        action="store_true",
        help="Print the paths to the benchmark binaries",
    )

    opts.add_option(
        "--run_cmd",
        default=None,
        dest="run_cmd",
        help="Run the target executable with a custom command " '(e.g. "valgrind %s")',
    )

    opts.add_option(
        "--result_file",
        default=None,
        dest="result_file",
        help="Copy the specified result file to the host",
    )

    opts.add_option(
        "--result_folder",
        default=None,
        dest="result_folder",
        help="Copy the result file to the given folder on the host "
        "(used with --result_file)",
    )

    opts.add_option(
        "--device_id",
        default=None,
        dest="device_id",
        help="Specify the ID of the target Android device "
        "(used with ADB when multiple devices are available)",
    )

    opts.add_option(
        "--test_filter",
        default=None,
        dest="test_filter",
        help="Only compile the test source files that include the specified "
        "substring (wildcards are allowed)",
    )

    opt.load("runners.ssh_runner")


@feature("test")
@after_method("process_use")
@after_method("apply_link")
def make_test(self):
    if self.bld.has_tool_option("run_tests"):
        make_run(self, "test")


@feature("benchmark")
@after_method("process_use")
@after_method("apply_link")
def make_benchmark(self):
    if self.bld.has_tool_option("run_benchmarks"):
        make_run(self, "benchmark")
    elif hasattr(self, "link_task"):
        if self.bld.has_tool_option("run_benchmark"):
            # Compare the benchmark name ignoring the file extension
            if (
                self.bld.get_tool_option("run_benchmark")
                == os.path.splitext(self.link_task.outputs[0].name)[0]
            ):
                make_run(self, "benchmark")

        if self.bld.has_tool_option("print_benchmark_paths"):
            print(self.link_task.outputs[0].relpath())
        if self.bld.has_tool_option("print_benchmarks"):
            print(self.link_task.outputs[0].name)


def to_source_nodes(lst, path):
    """
    Convert the input list into a list of source nodes.
    It is used to only find original source files, as opposed to the
    task_gen.to_nodes() method that prefers files in the build folder.

    :param lst: input list (of string or node)
    :param path: path from which to search the nodes
    """
    tmp = []

    # either a list or a string, convert to a list of nodes
    for x in Utils.to_list(lst):
        if isinstance(x, str):
            node = path.find_node(x)
        else:
            node = x
        if not node:
            raise Errors.WafError("Source not found: %r in %r" % (x, path))
        tmp.append(node)
    return tmp


def make_run(taskgen, run_type):
    """
    Create the run task.

    There can be only one unit test task by task generator.
    """
    if hasattr(taskgen, "link_task"):

        if taskgen.bld.has_tool_option("ssh_runner"):
            task = taskgen.create_task("SSHRunner", taskgen.link_task.outputs)
        elif taskgen.bld.is_mkspec_platform("android"):
            task = taskgen.create_task("AndroidRunner", taskgen.link_task.outputs)
        elif taskgen.bld.is_mkspec_platform("ios"):
            task = taskgen.create_task("IOSRunner", taskgen.link_task.outputs)
        elif taskgen.bld.is_mkspec_platform("emscripten"):
            task = taskgen.create_task("EmscriptenRunner", taskgen.link_task.outputs)
        else:
            task = taskgen.create_task("BasicRunner", taskgen.link_task.outputs)

        # Check if the executable requires any test files
        test_files = getattr(taskgen, "test_files", [])
        task.test_inputs = to_source_nodes(test_files, taskgen.path)

        # Locate any shared libs that are needed to run this binary, and
        # add these to the test_inputs list
        uselib = getattr(taskgen, "uselib", [])
        use = getattr(taskgen, "use", [])
        for lib_name in set(uselib + use):
            # We are only concerned with the shared libs that are generated by
            # this waf process, so e.g. the pthread shared lib should be
            # already available on the system.
            lib_task_gen = taskgen.bld.task_gen_cache_names.get(lib_name, None)
            if (
                lib_task_gen
                and lib_task_gen.target
                and hasattr(lib_task_gen, "link_task")
            ):
                # Some lib found, now determine if it is a shared lib.
                lib_node = lib_task_gen.link_task.outputs[0]

                # We substitute the target name into the cshlib_PATTERN
                shared_lib_name = taskgen.env["cshlib_PATTERN"] % lib_task_gen.target

                # If the output name matches the shared lib pattern, then
                # we assume that it is a shared lib
                if lib_node.name == shared_lib_name:
                    # Add the library to the test inputs
                    task.test_inputs.append(lib_node)

        # Make sure that this newly created task is executed after the
        # previously defined run task (if there is such a task)
        if len(run_tasks) > 0:
            task.set_run_after(run_tasks[-1])
        # Store this task in the run_tasks list
        run_tasks.append(task)

        # Check if the executable requires any kernel modules
        kernel_modules = getattr(taskgen, "kernel_modules", [])
        task.kernel_objects = []

        for module in kernel_modules:
            # Find the task that builds the module
            module_task = taskgen.bld.get_tgen_by_name(module).tasks[0]
            # Get the first target of the task (i.e. the kernel object)
            task.kernel_objects.append(module_task.outputs[0])
            # Make sure that the tests run after building the kernel module
            task.set_run_after(module_task)

    # We are creating a new task which should run an executable after
    # a build finishes. Here we add two functions to the BuildContext
    # which prints a summary and ensures that the build fails if the
    # test fails.
    post_funs = getattr(taskgen.bld, "post_funs", None)
    if post_funs:
        if set_exit_code not in post_funs:
            taskgen.bld.add_post_fun(set_exit_code)
        if summary not in post_funs:
            taskgen.bld.add_post_fun(summary)
    else:
        taskgen.bld.add_post_fun(set_exit_code)
        taskgen.bld.add_post_fun(summary)


def summary(bld):
    """
    Display an execution summary:

    def build(bld):
        bld(features='cxx cxxprogram test', source='main.c', target='app')
        from waflib.Tools import waf_unit_test
        bld.add_post_fun(waf_unit_test.summary)
    """
    lst = getattr(bld, "runner_results", [])
    if lst:
        Logs.pprint("CYAN", "Execution Summary:")

        total = len(lst)
        fail = len([x for x in lst if x[1]])

        Logs.pprint("CYAN", "  successful runs %d/%d" % (total - fail, total))
        for (filename, return_code, stdout) in lst:
            if return_code == 0:
                Logs.pprint("CYAN", "    %s" % filename)

        if fail != 0:
            Logs.pprint("CYAN", "  failed runs %d/%d" % (fail, total))
            for (filename, return_code, stdout) in lst:
                if return_code != 0:
                    Logs.pprint("CYAN", "     %s" % filename)


def set_exit_code(bld):
    """
    If any of the tests fails, waf will output the corresponding exit code.
    This is useful if you have an automated build system which need
    to report on errors from the tests.
    You may use it like this:

    def build(bld):
        bld(features='cxx cxxprogram test', source='main.c', target='app')
        from waflib.Tools import waf_unit_test
        bld.add_post_fun(waf_unit_test.set_exit_code)
    """
    lst = getattr(bld, "runner_results", [])
    for (cmd, return_code, stdout) in lst:
        if return_code:
            # If this was a "silent" run, we should print the full output
            if bld.has_tool_option("run_silent"):
                Logs.pprint("RED", stdout)
            bld.fatal(
                'Command "{}" failed with return code: {}'.format(cmd, return_code)
            )
