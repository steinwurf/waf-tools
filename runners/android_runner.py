#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
from basic_runner import BasicRunner

class AndroidRunner(BasicRunner):

    def save_result(self, results):

        combined_stdout = ""
        combined_stderr = ""
        combined_return_code = 0

        for result in results:
            combined_stdout += 'Running {cmd}\n{stdout}\n'.format(**result)
            combined_stderr += 'Running {cmd}\n{stderr}\n'.format(**result)
            if result['return_code'] != 0: combined_return_code = -1

        result = (self.format_command(self.inputs[0]), combined_return_code,
                  combined_stdout, combined_stderr)

        super(AndroidRunner, self).save_result(result)

    def run(self):
        bld = self.generator.bld

        adb = bld.env['ADB']
        
        results = []

        dest_dir = '/data/local/tmp/'

        def run_cmd(cmd):

            Logs.debug("wr: running %r", cmd)

            proc = Utils.subprocess.Popen(
                cmd,
                stderr=Utils.subprocess.PIPE,
                stdout=Utils.subprocess.PIPE)
            (stdout, stderr) = proc.communicate()

            result =  {'cmd': cmd, 'return_code': proc.returncode,
                       'stdout': stdout, 'stderr':stderr}

            return result

        device_id = None
        if bld.has_tool_option('device_id'):
            device_id = bld.get_tool_option('device_id')

        # ADB shell command, we make it immutable using a tuple.
        adb_shell = None
        if device_id:
            adb_shell = (adb, '-s', device_id, 'shell')
        else:
            adb_shell = (adb, 'shell')

        # First we remove all files from dest_dir with rm -rf
        result = run_cmd(list(adb_shell) + ["rm {}*".format(dest_dir)])
        results.append(result)
        if result['return_code'] != 0:
            self.save_result(results)
            return

        # Run the adb commands, we make it immutable using a tuple.
        adb_push = None

        if device_id:
            adb_push = (adb, '-s', device_id, 'push')
        else:
            adb_push = (adb, 'push')

        # Push the test files
        for t in self.test_inputs:

            filename = os.path.basename(t.abspath())
            # This path is on android, hence we use '/' regardless of the host platform.
            dest_file = dest_dir + filename

            result = run_cmd(list(adb_push) + [t.abspath(), dest_file])
            
            results.append(result)
            if result['return_code'] != 0:
                self.save_result(results)
                return


        # Push the binary
        binary = str(self.inputs[0])
        adb_push_bin = list(adb_push) + [self.inputs[0].abspath(), dest_dir + binary]

        result = run_cmd(adb_push_bin)
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            return

        # We have to cd to the dir and run the binary
        run_binary_cmd = "cd {0};./{1}".format(dest_dir, binary)

        #is this a benchmark, and if so do we need to retrieve the result?
        if  bld.has_tool_option('run_benchmark') \
        and bld.has_tool_option('python_result'):
            run_binary_cmd += " --pyfile={}".format(bld.get_tool_option("python_result"))

        # Echo the exit code after the shell command
        result = run_cmd(list(adb_shell) + ["{};echo shellexit:$?".format(run_binary_cmd)])
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            return

        # Look for the exit code in the output and fail if non-zero
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

            adb_pull = None

            if device_id:
                adb_pull = (adb, '-s', device_id, 'pull')
            else:
                adb_pull = (adb, 'pull')

            output_file = bld.get_tool_option("python_result")

            # This path is on android and not the host platform
            src_file  = dest_dir + output_file
            
            dest_file = os.path.join(".","benchmark_results", output_file)

            result = run_cmd(list(adb_pull) + [src_file, dest_file])
            results.append(result)

            if result['return_code'] != 0:
                self.save_result(results)
                return

        self.save_result(results)