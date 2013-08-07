#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
testlock = Utils.threading.Lock()


class BasicRunner(Task.Task):
    """
    Execute a unit test
    """
    color = 'PINK'
    after = ['vnum', 'inst']
    run_type = ''
    vars = []

    def __str__(self):
        "string to display to the user"

        env = self.env
        src_str = ' '.join([a.nice_path() for a in self.inputs])
        tgt_str = ' '.join([a.nice_path() for a in self.outputs])
        tst_str = ' '.join([a.nice_path() for a in self.test_inputs])

        if self.outputs: sep = ' -> '
        else: sep = ''

        if self.test_inputs: tst_str = ' {test input: %s} ' % tst_str

        return '%s: %s%s%s%s\n' % (
            self.__class__.__name__.replace('_task', ''),
            src_str, sep, tgt_str, tst_str)


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
        Adds some common paths to the environment in which
        the executable will run.
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

    def format_command(self, executable):
        """
        We allow the user to 'modify' the command to be executed.
        E.g. by specifying --option=run_cmd='valgrind %s' this will
        replace %s with the executable name and thus run the executable
        under valgrind
        """
        bld = self.generator.bld

        if bld.has_tool_option('run_cmd'):
            testcmd = bld.get_tool_option('run_cmd')
            cmd = testcmd % executable
        else:
            cmd  = executable

        return cmd

    def run(self):
        """
        Basic runner - simply spins a subprocess to run the executable.
        The execution is always successful, but the
        results are stored on ``self.generator.bld.runner_results`` for
        post processing.
        """

        fu = self.setup_path()
        cwd = self.inputs[0].parent.abspath()
        cmd = self.format_command(self.inputs[0].abspath()).split(' ')

        # First check whether we require any test files
        for t in self.test_inputs:

            filename = os.path.basename(t.abspath())

            test_file_out = self.inputs[0].parent.find_or_declare(filename)

            Logs.debug("wr: test file {0} -> {1}".format(
                t.abspath(), test_file_out.abspath()))

            test_file_out.write(t.read('rb'), 'wb')
            if getattr(self.generator, 'chmod', None):
                os.chmod(test_file_out.abspath(), self.generator.chmod)


        Logs.debug("wr: running %r in %s" % (cmd, str(cwd)))

        proc = Utils.subprocess.Popen(
            cmd,
            cwd=cwd,
            env=fu,
            stderr=Utils.subprocess.PIPE,
            stdout=Utils.subprocess.PIPE)

        (stdout, stderr) = proc.communicate()

        result = (cmd, proc.returncode, stdout, stderr)
        self.save_result(result)

    def save_result(self, result):
        """
        Stores the result in the self.generator.bld.runner_results
        """
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

