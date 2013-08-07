#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
import time
from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
from basic_runner import BasicRunner

class IosRunner(BasicRunner):

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

        super(IosRunner, self).save_result(result)

    def run(self):

        bld = self.generator.bld

        #adb = bld.env['ADB']

        results = []

        dest_dir = '/private/var/mobile/tmp'
        localport = '22222'
        ssh_target = 'mobile@localhost'

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

        def start_proc(cmd):

            Logs.debug("wr: starting %r", cmd)

            proc = Utils.subprocess.Popen(
                cmd,
                stderr=Utils.subprocess.PIPE,
                stdout=Utils.subprocess.PIPE)
            # Wait for a second so that the process can start
            time.sleep(1.0)

            return proc



        usbmux_dir = None
        if bld.has_tool_option('usbmux_dir'):
            usbmux_dir = bld.get_tool_option('usbmux_dir')
        else:
            bld.fatal('usbmux_dir is not specified')

        usbmux = os.path.join(usbmux_dir, 'tcprelay.py')
        usbmux_cmd = [usbmux, '22:{}'.format(localport)]

        # Start the usbmux daemon to forward 'localport' to port 22 on USB
        usbmux_proc = start_proc(usbmux_cmd)

        # First we remove all files from dest_dir with rm -rf
        ssh_cmd = ['ssh', '-p', localport, ssh_target]
        
        result = run_cmd(ssh_cmd + ['rm -rf {}/*'.format(dest_dir)])
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            return

        # Run the scp command
        scp_cmd = ['scp', '-P', localport]
        file_list = []

        # Enumerate the test files
        for t in self.test_inputs:
            filename = t.abspath()
            file_list += [filename]
        
        file_list += [self.inputs[0].abspath()]

        # Copy all files in file_list
        scp_all_files = scp_cmd + file_list + [ssh_target+':'+dest_dir]

        result = run_cmd(scp_all_files)
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            usbmux_proc.kill()
            return

        # Add the binary
        binary = str(self.inputs[0])

        #!!!!!!!BUGBUGBUGBUGBUG THIS IS NOT USED!!!!!!!!!
        #cmd = self.format_command(binary)
                         
        run_binary_cmd = "cd {0};./{1}".format(dest_dir, binary)
        #is this a benchmark, and if so do we need to retrieve the result?
        if  bld.has_tool_option('run_benchmark') \
        and bld.has_tool_option('benchmark_python_result'):
            run_binary_cmd += " --pyfile={}".format(bld.get_tool_option("benchmark_python_result"))

        # We have to cd to dest_dir and run the binary
        # Echo the exit code after the shell command
        result = run_cmd(ssh_cmd + ["{};echo shellexit:$?".format(run_binary_cmd)])
        results.append(result)

        # Kill the usbmux process
        usbmux_proc.kill()

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
        and bld.has_tool_option('benchmark_python_result'):
            # Run the scp command
            benchmark_result_folder = "benchmark_results"
            scp_cmd = ['scp', '-P', localport]

            # scp fails if the destination folder doesn't exist.
            run_cmd(["mkdir","-p",benchmark_result_folder])

            output_file = bld.get_tool_option("benchmark_python_result")

            benchmark_result = os.path.join(dest_dir,output_file)
            scp_file = scp_cmd + ['{0}:{1}'.format(ssh_target,benchmark_result), benchmark_result_folder]

            result = run_cmd(scp_file)
            results.append(result)

            if result['return_code'] != 0:
                self.save_result(results)
                usbmux_proc.kill()
                return

        self.save_result(results)
