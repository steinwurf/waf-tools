#!/usr/bin/env python
# encoding: utf-8
# Carlos Rafael Giani, 2006
# Thomas Nagy, 2010

"""
Unit testing system for C/C++/D providing test execution:

* in parallel, by using ``waf -j``
* partial (only the tests that have changed) or full (by using ``waf --alltests``)

The tests are declared by adding the **test** feature to programs::

def options(opt):
    opt.load('compiler_cxx waf_unit_test')
def configure(conf):
    conf.load('compiler_cxx waf_unit_test')
def build(bld):
    bld(features='cxx cxxprogram test', source='main.cpp', target='app')
    # or
    bld.program(features='test', source='main2.cpp', target='app2')

When the build is executed, the program 'test' will be built and executed without arguments.
The success/failure is detected by looking at the return code. The status and the standard output/error
are stored on the build context.

The results can be displayed by registering a callback function. Here is how to call
the predefined callback::

def build(bld):
    bld(features='cxx cxxprogram test', source='main.c', target='app')
    from waflib.Tools import waf_unit_test
    bld.add_post_fun(waf_unit_test.summary)
"""

import os, sys
from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
testlock = Utils.threading.Lock()

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

def make_run(taskgen, run_type):
    """Create the run task. There can be only one unit test task by task generator."""
    task = None
    if getattr(taskgen, 'link_task', None):
        if taskgen.bld.is_mkspec_platform('android'):
            task = taskgen.create_task('AndroidRunner', taskgen.link_task.outputs)
        else:
            task = taskgen.create_task('BasicRunner', taskgen.link_task.outputs)
            task.run_type = run_type

class BasicRunner(Task.Task):
    """
    Execute a unit test
    """
    color = 'PINK'
    after = ['vnum', 'inst']
    run_type = ''
    vars = []

    def runnable_status(self):
        """
        Always execute the task if `waf --options=run_always` was used
        """

        ret = super(BasicRunner, self).runnable_status()
        if ret == Task.SKIP_ME:
            if self.generator.bld.has_tool_option('run_always'):
                return Task.RUN_ME
        return ret

    def setup_path(self):
        """
        Execute the test. The execution is always successful, but the
        results are stored on ``self.generator.bld.utest_results`` for
        postprocessing.
        """
        try:
            fu = getattr(self.generator.bld, 'all_test_paths')
        except AttributeError:
            fu = os.environ.copy()
            self.generator.bld.all_test_paths = fu

            lst = []
            for g in self.generator.bld.groups:
                for tg in g:
                    if getattr(tg, 'link_task', None):
                        lst.append(tg.link_task.outputs[0].parent.abspath())

            def add_path(dct, path, var):
                dct[var] = os.pathsep.join(Utils.to_list(path) + [os.environ.get(var, '')])

            if Utils.is_win32:
                add_path(fu, lst, 'PATH')
            elif Utils.unversioned_sys_platform() == 'darwin':
                add_path(fu, lst, 'DYLD_LIBRARY_PATH')
                add_path(fu, lst, 'LD_LIBRARY_PATH')
            else:
                add_path(fu, lst, 'LD_LIBRARY_PATH')

                return fu


        def run(self):
            fu = self.setup_path()
            executable = self.inputs[0].abspath()
            cwd = self.inputs[0].parent.abspath()

            cmd = getattr(Options.options, 'testcmd', False)
            if cmd:
                cmd = cmd % executable
            else:
                cmd  = executable

            Logs.debug("wr: running %r", cmd)

            proc = Utils.subprocess.Popen(
                cmd,
                cwd=cwd,
                env=fu,
                stderr=Utils.subprocess.PIPE,
                stdout=Utils.subprocess.PIPE)
            (stdout, stderr) = proc.communicate()

            result = (executable, proc.return_code, stdout, stderr)
            self.save_result(result)

        def save_result(self, result):
            testlock.acquire()
            try:
                bld = self.generator.bld
                Logs.debug("wr: %r", result)
                try:
                    bld.runner_results.append(result)
                except AttributeError:
                    bld.runner_results = [result]
            finally:
                testlock.release()

class AndroidRunner(BasicRunner):
    def run(self):
        print "running on android"

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

def set_exit_code(bld):
    """
    If any of the tests fail waf will exit with that exit code.
    This is useful if you have an automated build system which need
    to report on errors from the tests.
    You may use it like this:

    def build(bld):
        bld(features='cxx cxxprogram test', source='main.c', target='app')
        from waflib.Tools import waf_unit_test
        bld.add_post_fun(waf_unit_test.set_exit_code)
    """
    lst = getattr(bld, 'runner_results', [])
    for (f, code, out, err) in lst:
        if code:
            msg = []
            if out:
                msg.append('stdout:%s%s' % (os.linesep, out.decode('utf-8')))
            if err:
                msg.append('stderr:%s%s' % (os.linesep, err.decode('utf-8')))
            bld.fatal(os.linesep.join(msg))