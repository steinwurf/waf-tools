#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
import time
from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
from basic_runner import BasicRunner, run_cmd

class SSHRunner(BasicRunner):

    def run(self):

        bld = self.generator.bld

        results = []

        dest_dir = bld.get_tool_option('ssh_dest_dir')
        ssh_host = bld.get_tool_option('ssh_host')
        ssh_user = bld.get_tool_option('ssh_user')
        ssh_target = ssh_user + '@' + ssh_host

        # ssh command as a list
        ssh_cmd = ['ssh', ssh_target]

        # scp command as a list
        scp_cmd = ['scp']

        # Enumerate the test files
        file_list = [test_input.abspath() for test_input in self.test_inputs]

        # Add the binary
        binary = self.inputs[0]
        file_list.append(binary.abspath())

        # Copy all files in file_list
        result = run_cmd(scp_cmd + file_list + [ssh_target+':'+dest_dir])
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            return

        # To run the binary; cd to dest_dir, run the binary ...
        run_binary_cmd = "cd {0};./{1}".format(dest_dir, binary)

        # Wait! is this a benchmark, and if so do we need to retrieve the
        # result file?
        if  bld.has_tool_option('run_benchmark') \
        and bld.has_tool_option('python_result'):
            # ... add the benchmark python result output filename option ...
            run_binary_cmd += " --pyfile={}".format(
                bld.get_tool_option("python_result"))

        # ... finally echo the exit code
        result = run_cmd(ssh_cmd + \
            ["{};echo shellexit:$?".format(run_binary_cmd)])
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            return

        # Almost done. Look for the exit code in the output
        # and fail if non-zero
        match = re.search('shellexit:(\d+)', result['stdout'])

        if not match:
            result =  {'cmd': 'Looking for shell exit', 'return_code': -1,
                       'stdout': '', 'stderr': 'Failed to find exitcode'}

            results.append(result)
            self.save_result(results)
            return

        if match.group(1) != "0":
            result =  {'cmd': 'Shell exit indicates error',
                       'return_code': match.group(1),
                       'stdout': '',
                       'stderr': 'Exit code was %s' % match.group(1)}

            results.append(result)
            self.save_result(results)
            return

        # Everything seems to be fine, lets pull the output file if needed
        if  bld.has_tool_option('run_benchmark') \
        and bld.has_tool_option('python_result'):
            output_file = bld.get_tool_option("python_result")

            # Remove the old benchmark if it exists
            run_cmd(["rm", "-f", output_file])

            benchmark_result = os.path.join(dest_dir,output_file)

            result = run_cmd(scp_cmd + \
                ['{0}:{1}'.format(ssh_target,benchmark_result), '.'])
            results.append(result)

            if result['return_code'] != 0:
                self.save_result(results)
                return

        self.save_result(results)
