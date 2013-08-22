#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
import time
from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
from basic_runner import BasicRunner, run_cmd

class IOSRunner(BasicRunner):
    def save_result(self, results, usbmux_proc):
        # Kill the usbmux process
        usbmux_proc.kill()

        super(IOSRunner, self).save_result(results)

    def run(self):

        bld = self.generator.bld

        results = []

        dest_dir = '/private/var/mobile/tmp'
        localport = '22222'
        ssh_target = 'mobile@localhost'

        def start_proc(cmd):

            Logs.debug("wr: starting %r", cmd)

            proc = Utils.subprocess.Popen(
                cmd,
                stderr=Utils.subprocess.PIPE,
                stdout=Utils.subprocess.PIPE)
            # Wait for a second so that the process can start
            time.sleep(1.0)

            return proc

        usbmux_dir = bld.get_tool_option('usbmux_dir')

        usbmux = os.path.join(usbmux_dir, 'tcprelay.py')

        usbmux_cmd = [usbmux, '22:{}'.format(localport)]
        scp_cmd = ['scp', '-P', localport]
        ssh_cmd = ['ssh', '-p', localport, ssh_target]

        # Start the usbmux daemon to forward 'localport' to port 22 on USB
        usbmux_proc = start_proc(usbmux_cmd)
        
        # Enumerate the test files
        file_list = [test_input.abspath() for test_input in self.test_inputs]

        # Add the binary
        binary = self.inputs[0]
        file_list.append(binary.abspath())

        # Copy all files in file_list
        result = run_cmd(scp_cmd + file_list + [ssh_target+':'+dest_dir])
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results, usbmux_proc)
            return
                  
        run_binary_cmd = "./{1}".format(dest_dir, binary)

        # if this is a benchmark and we need to retrieve the result file
        if  bld.has_tool_option('run_benchmark') \
        and bld.has_tool_option('python_result'):
            # Add the benchmark python result output filename option
            run_binary_cmd += " --pyfile={}".format(
                bld.get_tool_option("python_result"))

        # Add the given run command modifications
        run_binary_cmd = self.format_command(run_binary_cmd)

        # Finally echo the exit code
        result = run_cmd(
            ssh_cmd + \
            ["cd {0};{1};echo shellexit:$?".format(dest_dir, run_binary_cmd)])

        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results, usbmux_proc)
            return

        # Almost done. Look for the exit code in the output
        # and fail if nonzero
        match = re.search('shellexit:(\d+)', result['stdout'])

        if not match:
            result =  {'cmd': 'Looking for shell exit', 'return_code': -1,
                       'stdout': '', 'stderr': 'Failed to find exitcode'}

            results.append(result)
            self.save_result(results, usbmux_proc)
            return

        if match.group(1) != "0":
            result =  {'cmd': 'Shell exit indicates error',
                       'return_code': match.group(1),
                       'stdout': '',
                       'stderr': 'Exit code was %s' % match.group(1)}

            results.append(result)
            self.save_result(results, usbmux_proc)
            return

        # Everything seems to be fine, lets pull the output file if needed
        if  bld.has_tool_option('run_benchmark') \
        and bld.has_tool_option('python_result'):
            output_file = bld.get_tool_option("python_result")

            # Remove the old benchmark if it exists
            run_cmd(["rm", "-f", output_file])

            benchmark_result = os.path.join(dest_dir,output_file)
            
            result = run_cmd(list(scp_cmd) + ['{0}:{1}'.format(
                ssh_target,benchmark_result), '.'])
            results.append(result)

            if result['return_code'] != 0:
                self.save_result(results,usbmux_proc)
                return

        self.save_result(results, usbmux_proc)
