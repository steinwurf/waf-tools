#!/usr/bin/env python
# encoding: utf-8

import os
from waflib import Utils, Task, Logs
testlock = Utils.threading.Lock()

def nice_path(node):
    """
    Return the path seen from the launch directory.
    Can be used for opening files easily (copy-paste in the console).
    """
    return node.path_from(node.ctx.launch_node())


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

        src_str = ' '.join([nice_path(a) for a in self.inputs])
        tgt_str = ' '.join([nice_path(a) for a in self.outputs])
        tst_str = '\n\t'.join([nice_path(a) for a in self.test_inputs])
        kobj_str = '\n\t'.join([nice_path(a) for a in self.kernel_objects])

        if self.outputs:
            sep = ' -> '
        else:
            sep = ''

        if self.test_inputs:
            tst_str = '\ntest inputs:\n\t{}'.format(tst_str)

        if self.kernel_objects:
            kobj_str = '\nkernel objects:\n\t{}'.format(kobj_str)

        return "{name}: {source_str}{separator}{target_str}" \
            "{test_str}{kobj_str}\n".format(
                name=self.__class__.__name__.replace('_task', ''),
                source_str=self.format_command(src_str),
                separator=sep,
                target_str=tgt_str,
                test_str=tst_str,
                kobj_str=kobj_str)

    def runnable_status(self):
        """
        Always execute the test task

        If the run_modified option is present, then only the modified test
        binaries will be run.
        """
        ret = super(BasicRunner, self).runnable_status()
        if ret == Task.SKIP_ME:
            if not self.generator.bld.has_tool_option('run_modified'):
                return Task.RUN_ME

        return ret

    def format_command(self, executable):
        """
        Return a formatted command as a STRING

        We allow the user to 'modify' the command to be executed.
        E.g. by specifying --option=run_cmd='valgrind %s' this will
        replace %s with the executable name and thus run the executable
        under valgrind
        """
        cmd = ' '.join(self.format_command_list(executable))
        return cmd

    def format_command_list(self, executable):
        """
        Return a formatted command as a LIST

        We allow the user to 'modify' the command to be executed.
        E.g. by specifying --option=run_cmd='valgrind %s' this will
        replace %s with the executable name and thus run the executable
        under valgrind
        """
        executable = str(executable)
        bld = self.generator.bld
        if bld.has_tool_option('run_cmd'):
            testcmd = bld.get_tool_option('run_cmd')
            # Split the arguments BEFORE substituting the executable path
            args = testcmd.split(' ')
            # Substitute the path to the relevant element
            for i in range(len(args)):
                if '%s' in args[i]:
                    args[i] = args[i] % executable
                    break

        else:
            args = [executable]

        return args

    def run(self):
        """
        Basic runner - simply spins a subprocess to run the executable.
        The execution is always successful, but the
        results are stored on ``self.generator.bld.runner_results`` for
        post processing.
        """
        bld = self.generator.bld

        # Then command string can be safely split into a list of strings
        binary = self.inputs[0].abspath()
        cmd = self.format_command_list(binary)
        # If kernel objects are required, then run the test binary with sudo
        if self.kernel_objects:
            cmd.insert(0, 'sudo')

        # If this is a benchmark and we need to retrieve the result file
        if bld.has_tool_option('run_benchmark') and \
           bld.has_tool_option('python_result'):
            cmd += ["--pyfile={0}".format(
                bld.get_tool_option("python_result"))]

        # First check whether we require any test files
        for t in self.test_inputs:

            test_file_out = self.inputs[0].parent.get_bld().make_node([t.name])

            Logs.debug("wr: test file {0} -> {1}".format(
                t.abspath(), test_file_out.abspath()))

            test_file_out.write(t.read('rb'), 'wb')
            if hasattr(self.generator, 'chmod'):
                os.chmod(test_file_out.abspath(), self.generator.chmod)

        results = []

        # Load the required kernel objects with insmod (in the original order)
        for ko in self.kernel_objects:
            filename = ko.abspath()
            result = self.run_cmd(['sudo', 'insmod', filename])
            results.append(result)

        # Run the test binary
        result = self.run_cmd(cmd)
        results.append(result)

        # Unload the required kernel objects with rmmod (in reverse order)
        for ko in reversed(self.kernel_objects):
            result = self.run_cmd(['sudo', 'rmmod', ko.name])
            results.append(result)

        self.save_result(results)

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

            combined_stdout += 'Running: {0}\n'.format(cmd)
            if result["stdout"]:
                combined_stdout += result["stdout"].decode('utf-8')

            if result["stderr"]:
                combined_stderr += 'Running: {0}\n{1}'.format(
                    cmd, result["stderr"].decode('utf-8'))
            if result['return_code'] != 0:
                combined_return_code = -1

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
            stdin=Utils.subprocess.PIPE,
            stderr=Utils.subprocess.PIPE,
            stdout=Utils.subprocess.PIPE)

        (stdout, stderr) = proc.communicate()

        result = {'cmd': cmd, 'return_code': proc.returncode,
                  'stdout': stdout, 'stderr': stderr}

        return result
