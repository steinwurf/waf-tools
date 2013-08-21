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
    color = 'BLUE'
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
        bld = self.generator.bld

        cmd = self.format_command(self.inputs[0].abspath()).split(' ')

        # If this is a benchmark run and we have specified
        # an output file name; use it.
        if  bld.has_tool_option('run_benchmark') \
        and bld.has_tool_option('python_result'):
            cmd += ["--pyfile={}".format(
                bld.get_tool_option("python_result"))]

        # First check whether we require any test files
        for t in self.test_inputs:

            filename = os.path.basename(t.abspath())

            test_file_out = self.inputs[0].parent.find_or_declare(filename)

            Logs.debug("wr: test file {0} -> {1}".format(
                t.abspath(), test_file_out.abspath()))

            test_file_out.write(t.read('rb'), 'wb')
            if hasattr(self.generator, 'chmod'):
                os.chmod(test_file_out.abspath(), self.generator.chmod)

        result = run_cmd(cmd)

        self.save_result([result])

    def save_result(self, results):
        """
        Stores the result in the self.generator.bld.runner_results
        """
        combined_stdout = ""
        combined_stderr = ""
        combined_return_code = 0

        for result in results:
            cmd = result["cmd"]
            if not isinstance(cmd, basestring):
                cmd = " ".join(cmd)

            if result["stdout"]:
                combined_stdout += 'Running: {0}\n{1}'.format(
                    cmd, result["stdout"])
            if result["stderr"]:
                combined_stderr += 'Running: {0}\n{1}'.format(
                        cmd, result["stderr"])
            if result['return_code'] != 0: combined_return_code = -1

        combined_result = (
            self.format_command(self.inputs[0]),
            combined_return_code,
            combined_stdout,
            combined_stderr)

        testlock.acquire()
        try:
            bld = self.generator.bld
            Logs.debug("wr: %r", result)
            try:
                bld.runner_results.append(combined_result)
            except AttributeError:
                bld.runner_results = [combined_result]
        finally:
            testlock.release()

def run_cmd(cmd):
    Logs.debug("wr: running %r", cmd)

    proc = Utils.subprocess.Popen(
        cmd,
        stderr=Utils.subprocess.PIPE,
        stdout=Utils.subprocess.PIPE)
    (stdout, stderr) = proc.communicate()

    result =  {'cmd': cmd, 'return_code': proc.returncode,
               'stdout': stdout, 'stderr': stderr}

    return result