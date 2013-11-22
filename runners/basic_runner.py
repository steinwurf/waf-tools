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
        tst_str = '\n\t'.join([a.nice_path() for a in self.test_inputs])

        if self.outputs: sep = ' -> '
        else: sep = ''

        if self.test_inputs:
            tst_str = 'test input:\n\t{}'.format(tst_str)

        return '{name}: {source_str}{seperator}{target_str}{test_str}\n'.format(
            name = self.__class__.__name__.replace('_task', ''),
            source_str = self.format_command(src_str),
            seperator = sep,
            target_str = tgt_str,
            test_str = tst_str)


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
            cmd = executable

        return cmd

    def run(self):
        """
        Basic runner - simply spins a subprocess to run the executable.
        The execution is always successful, but the
        results are stored on ``self.generator.bld.runner_results`` for
        post processing.
        """
        bld = self.generator.bld

        # It is enough to use the basename of the binary, because it is always
        # executed in its parent folder
        binary = self.inputs[0].name
        # Prefix the binary with ./ if the platform is not Windows
        if not bld.is_mkspec_platform('windows'):
            binary = './' + binary
        # Then command string can be safely split into a list of strings
        cmd = self.format_command(binary).split(' ')

        # If this is a benchmark and we need to retrieve the result file
        if bld.has_tool_option('run_benchmark') and \
           bld.has_tool_option('python_result'):
            cmd += ["--pyfile={0}".format(bld.get_tool_option("python_result"))]

        # First check whether we require any test files
        for t in self.test_inputs:

            filename = os.path.basename(t.abspath())

            test_file_out = self.inputs[0].parent.find_or_declare(filename)

            Logs.debug("wr: test file {0} -> {1}".format(
                t.abspath(), test_file_out.abspath()))

            test_file_out.write(t.read('rb'), 'wb')
            if hasattr(self.generator, 'chmod'):
                os.chmod(test_file_out.abspath(), self.generator.chmod)

        result = self.run_cmd(cmd)

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
            if not isinstance(cmd, str):
                cmd = " ".join(cmd)

            if result["stdout"]:
                combined_stdout += 'Running: {0}\n{1}'.format(
                    cmd, result["stdout"].decode('utf-8'))
            if result["stderr"]:
                combined_stderr += 'Running: {0}\n{1}'.format(
                        cmd, result["stderr"].decode('utf-8'))
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

    def run_cmd(self, cmd):

        Logs.debug("wr: running %r", cmd)

        proc = Utils.subprocess.Popen(
            cmd,
            cwd=self.inputs[0].parent.abspath(),
            stderr=Utils.subprocess.PIPE,
            stdout=Utils.subprocess.PIPE)

        (stdout, stderr) = proc.communicate()

        result =  {'cmd': cmd, 'return_code': proc.returncode,
                   'stdout': stdout, 'stderr': stderr}

        return result