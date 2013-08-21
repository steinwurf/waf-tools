#!/usr/bin/env python
# encoding: utf-8
# Carlos Rafael Giani, 2006
# Thomas Nagy, 2010
# Script is based on the waf_unit_test tool, but has since
# been significantly rewritten.

"""
Unit testing + benchmark tool.

This tool is available in the external-waf-tools repository, so we have
to load it:

def options(opt):
    import waflib.extras.wurf_dependency_bundle as bundle
    import waflib.extras.wurf_dependency_resolve as resolve
    import waflib.extras.wurf_configure_output

    bundle.add_dependency(opt,
        resolve.ResolveGitMajorVersion(
            name='waf-tools',
            git_repository='git://github.com/steinwurf/external-waf-tools.git',
            major_version=1))

    opt.load('wurf_dependency_bundle')
    opt.load('wurf_tools')

The tool should then be loaded:

def configure(conf):
    if conf.is_toplevel():
        conf.load('wurf_dependency_bundle')
        conf.load('wurf_tools')
        conf.load_external_tool('mkspec', 'wurf_cxx_mkspec_tool')
        conf.load_external_tool('runners', 'wurf_runner')

Finally in the build step, we add 'test' as a feature:

def build(bld):
    bld.program(features = 'cxx test',
                source   = ['main.cpp'],
                target   = 'hello')

This tool also support providing test files. This is useful when writing
tests that require some input data file in order to run. The test files
will be copied to the directory where the test binary will be executed.

Test files are added by specifying them using the test_files attribute
of the build. E.g.:

def build(bld):
    bld.program(features   = 'cxx test',
                source     = ['main.cpp'],
                target     = 'hello',
                test_files = ['test_input.txt'])

"""

import os, sys, re
from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
from basic_runner import BasicRunner
from android_runner import AndroidRunner
from ios_runner import IOSRunner
from ssh_runner import SSHRunner

@feature('test')
@after_method('apply_link')
def make_test(self):
    if self.bld.has_tool_option('run_tests'):
        make_run(self, "test")

@feature('benchmark')
@after_method('apply_link')
def make_benchmark(self):
    if self.bld.has_tool_option('run_benchmarks'):
        make_run(self, "benchmark")
    elif hasattr(self, 'link_task'):
        if self.bld.has_tool_option('run_benchmark'):
            if self.bld.get_tool_option("run_benchmark") == \
               self.link_task.outputs[0].name:
                make_run(self, "benchmark")

        if self.bld.has_tool_option('print_benchmark_paths'):
            print(self.link_task.outputs[0].relpath())

def make_run(taskgen, run_type):
    """
    Create the run task. There can be only one unit test 
    task by task generator.
    """
    task = None

    if hasattr(taskgen, 'link_task'):

        taskgen.bld.add_group()
        if taskgen.bld.has_tool_option('ssh_runner'):
            task = taskgen.create_task('SSHRunner', 
                taskgen.link_task.outputs)
        elif taskgen.bld.is_mkspec_platform('android'):
            task = taskgen.create_task('AndroidRunner', 
                taskgen.link_task.outputs)
        elif taskgen.bld.is_mkspec_platform('ios'):
            task = taskgen.create_task('IOSRunner', 
                taskgen.link_task.outputs)
        else:
            task = taskgen.create_task('BasicRunner', 
                taskgen.link_task.outputs)

        # Check if the executable requires any test files
        test_files = getattr(taskgen, 'test_files', [])
        task.test_inputs = taskgen.to_nodes(test_files)

    # We are creating a new task which should run an executable after
    # a build finishes. Here we add two functions to the BuildContext
    # which prints a summary and ensures that the build fails if the
    # test fails.
    post_funs = getattr(taskgen.bld, 'post_funs', None)
    if post_funs:
        if not summary in post_funs:
            taskgen.bld.add_post_fun(summary)
        if not set_exit_code in post_funs:
            taskgen.bld.add_post_fun(set_exit_code)
    else:
        taskgen.bld.add_post_fun(summary)
        taskgen.bld.add_post_fun(set_exit_code)


def summary(bld):
    """
    Display an execution summary::

    def build(bld):
        bld(features='cxx cxxprogram test', source='main.c', target='app')
        from waflib.Tools import waf_unit_test
        bld.add_post_fun(waf_unit_test.summary)
    """
    lst = getattr(bld, 'runner_results', [])
    if lst:
        print len(lst)
        Logs.pprint('CYAN', 'execution summary')

        total = len(lst)
        fail = len([x for x in lst if x[1]])

        Logs.pprint('CYAN', '  successful runs %d/%d' % (total-fail, total))
        for (f, code, out, err) in lst:
            if not code:
                Logs.pprint('CYAN', '    %s' % f)

        Logs.pprint('CYAN', '  failed runs %d/%d' % (fail, total))
        for (f, code, out, err) in lst:
            if code:
                Logs.pprint('CYAN', '    %s' % f)

def assemble_output(out, err):
    """Helper function to assemble output message from the test results"""
    msg = []
    if out:
        msg.append('\nstdout:\n\n%s' % (out.decode('utf-8')))
    if err:
        msg.append('\nstderr:\n\n%s' % (err.decode('utf-8')))
    return msg

def set_exit_code(bld):
    """
    If any of the tests fails waf will exit with that exit code.
    This is useful if you have an automated build system which need
    to report on errors from the tests.
    You may use it like this:

    def build(bld):
        bld(features='cxx cxxprogram test', source='main.c', target='app')
        from waflib.Tools import waf_unit_test
        bld.add_post_fun(waf_unit_test.set_exit_code)
    """
    lst = getattr(bld, 'runner_results', [])
    print lst
    for (filename, return_code, stdout, stderr) in lst:
        print "filename{}".format(filename)
        print "return_code{}".format(return_code)
        print "out{}".format(stdout)
        print "stderr{}".format(stderr)
        if return_code:
            msg = assemble_output(stdout, stderr)
            bld.fatal(os.linesep.join(msg))
        elif not bld.has_tool_option('run_silent'):
            msg = assemble_output(stdout, stderr)
            Logs.pprint('WHITE', os.linesep.join(msg))

