#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import re
from waflib import Utils, Logs
from basic_runner import BasicRunner


class SSHRunner(BasicRunner):

    def run_cmd(self, cmd):

        Logs.debug("wr: running %r", cmd)

        # The pty module only works on Unix systems
        stdin_target = Utils.subprocess.PIPE
        if sys.platform != 'win32':
            import pty
            # subprocess.Popen() does not allocate a terminal for new
            # processes. We allocate a pseudo-terminal with pty.openpty() and
            # connect it to stdin. This is required if SSH is invoked with the
            # -t flag, which ensures that the remote process is terminated when
            # the SSH process is killed on the host.
            (master, slave) = pty.openpty()
            stdin_target = slave

        proc = Utils.subprocess.Popen(
            cmd,
            cwd=self.inputs[0].parent.abspath(),
            stdin=stdin_target,
            stderr=Utils.subprocess.PIPE,
            stdout=Utils.subprocess.PIPE)

        (stdout, stderr) = proc.communicate()

        result = {'cmd': cmd, 'return_code': proc.returncode,
                  'stdout': stdout, 'stderr': stderr}

        return result

    def save_result(self, results, ssh_cmd):
        # Override save_result to ensure that the kernel objects are removed

        # Unload the required kernel objects with rmmod (in reverse order)
        # Note: you have to SSH with the ROOT user!
        for ko in reversed(self.kernel_objects):
            result = self.run_cmd(ssh_cmd + ['rmmod', ko.name])
            results.append(result)

        super(SSHRunner, self).save_result(results)

    def run(self):

        bld = self.generator.bld

        dest_dir = bld.get_tool_option('ssh_dest_dir')
        ssh_host = bld.get_tool_option('ssh_host')
        ssh_user = bld.get_tool_option('ssh_user')
        ssh_target = ssh_user + '@' + ssh_host

        ssh_options = []
        if bld.has_tool_option('ssh_options'):
            ssh_options = \
                bld.get_tool_option('ssh_options').replace('"', '').split(' ')

        scp_options = []
        if bld.has_tool_option('scp_options'):
            scp_options = \
                bld.get_tool_option('scp_options').replace('"', '').split(' ')

        ssh_cmd = ['ssh', '-t'] + ssh_options + [ssh_target]
        scp_cmd = ['scp'] + scp_options

        self.run_ssh(ssh_cmd, scp_cmd, ssh_target, dest_dir)

    def run_ssh(self, ssh_cmd, scp_cmd, ssh_target, dest_dir):

        bld = self.generator.bld

        results = []

        # Delete all files from the destination folder if requested
        if bld.has_tool_option('ssh_clean_dir'):
            result = self.run_cmd(
                ssh_cmd + ["rm", "-f", "{0}/*".format(dest_dir)])
            results.append(result)

        # Enumerate the test files
        file_list = [test_input.abspath() for test_input in self.test_inputs]

        # Add the required kernel objects
        for ko in self.kernel_objects:
            file_list.append(ko.abspath())

        # Add the binary
        binary = self.inputs[0]
        file_list.append(binary.abspath())

        # Copy all files in file_list
        result = self.run_cmd(
            scp_cmd + file_list + [ssh_target + ':' + dest_dir])
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results, ssh_cmd)
            return

        # Load the required kernel objects with insmod (in the original order)
        # Note: you have to SSH with the ROOT user!
        for ko in self.kernel_objects:
            result = self.run_cmd(
                ssh_cmd + ['insmod', "{0}/{1}".format(dest_dir, ko.name)])
            results.append(result)
            if result['return_code'] != 0:
                self.save_result(results, ssh_cmd)
                return

        run_binary_cmd = "./{0}".format(binary)

        # If this is a benchmark and we need to retrieve the result file
        if bld.has_tool_option('run_benchmark') and \
           bld.has_tool_option('python_result'):
            # Add the benchmark python result output filename option
            run_binary_cmd += " --pyfile={}".format(
                bld.get_tool_option("python_result"))

        # Add the given run command modifications
        run_binary_cmd = self.format_command(run_binary_cmd)

        # Echo the exit code after the shell command
        if bld.has_tool_option('ssh_output_file'):
            output_file = bld.get_tool_option('ssh_output_file')
            result = self.run_cmd(
                ssh_cmd + ["cd {0};{1} &> {2};echo shellexit:$?;cat {2}".format(
                    dest_dir, run_binary_cmd, output_file)])
        else:
            result = self.run_cmd(
                ssh_cmd + ["cd {0};{1};echo shellexit:$?".format(
                    dest_dir, run_binary_cmd)])

        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results, ssh_cmd)
            return

        # Almost done. Look for the exit code in the output
        # and fail if non-zero
        match = re.search('shellexit:(\d+)', result['stdout'])

        if not match:
            result = {'cmd': 'Looking for shell exit', 'return_code': -1,
                      'stdout': '', 'stderr': 'Failed to find exitcode'}

            results.append(result)
            self.save_result(results, ssh_cmd)
            return

        if match.group(1) != "0":
            result = {'cmd': 'Shell exit indicates error',
                      'return_code': match.group(1),
                      'stdout': '',
                      'stderr': 'Exit code was %s' % match.group(1)}

            results.append(result)
            self.save_result(results, ssh_cmd)
            return

        # Everything seems to be fine, pull the output file if needed
        if bld.has_tool_option('run_benchmark') and \
           bld.has_tool_option('python_result'):
            output_file = bld.get_tool_option("python_result")

            # Remove the old benchmark if it exists
            self.run_cmd(["rm", "-f", output_file])

            benchmark_result = os.path.join(dest_dir, output_file)

            result = self.run_cmd(scp_cmd + ['{0}:{1}'.format(
                ssh_target, benchmark_result), '.'])
            results.append(result)

            if result['return_code'] != 0:
                self.save_result(results, ssh_cmd)
                return

        self.save_result(results, ssh_cmd)
