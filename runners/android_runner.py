#!/usr/bin/env python
# encoding: utf-8

import os, sys, re

from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
from basic_runner import BasicRunner

class AndroidRunner(BasicRunner):
    def run(self):
        bld = self.generator.bld

        adb = bld.env['ADB']

        results = []

        dest_dir = '/data/local/tmp/'

        device_id = None
        if bld.has_tool_option('device_id'):
            device_id = bld.get_tool_option('device_id')

        adb_shell = [adb]
        if device_id:
            adb_shell += ['-s', device_id]
        adb_shell += ['shell']

        adb_push = [adb]
        if device_id:
            adb_push += ['-s', device_id]
        adb_push += ['push']

        # Push the test files
        for t in self.test_inputs:

            filename = os.path.basename(t.abspath())
            # This path is on android, hence we use '/'
            # regardless of the host platform.
            dest_file = dest_dir + filename

            result = self.run_cmd(adb_push + [t.abspath(), dest_file])

            results.append(result)
            if result['return_code'] != 0:
                self.save_result(results)
                return


        # Push the binary
        binary = str(self.inputs[0])
        adb_push_bin = adb_push + [
            self.inputs[0].abspath(),
            dest_dir + binary]

        result = self.run_cmd(adb_push_bin)
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            return

        run_binary_cmd = "./{}".format(binary)

        # If this is a benchmark and we need to retrieve the result file
        if  bld.has_tool_option('run_benchmark') \
        and bld.has_tool_option('python_result'):
            # Add the benchmark python result output filename option
            run_binary_cmd += " --pyfile={}".format(
                bld.get_tool_option("python_result"))

        # Add the given run command modifications
        run_binary_cmd = self.format_command(run_binary_cmd)

        # Echo the exit code after the shell command
        result = self.run_cmd(
            adb_shell + \
            ["cd {0};{1};echo shellexit:$?".format(dest_dir, run_binary_cmd)])

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

            adb_pull = [adb]

            if device_id:
                adb_pull += ['-s', device_id]

            adb_pull += ['pull']

            output_file = bld.get_tool_option("python_result")

            # This path is on android and not the host platform
            benchmark_result  = dest_dir + output_file

            # Remove the old benchmark if it exists
            self.run_cmd(["rm", "-f", output_file])

            result = self.run_cmd(adb_pull + [benchmark_result, output_file])
            results.append(result)

            if result['return_code'] != 0:
                self.save_result(results)
                return

        self.save_result(results)