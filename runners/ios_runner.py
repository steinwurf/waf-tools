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
            combined_stdout += 'Running %(cmd)s %(stdout)s' % result
            combined_stderr += 'Running %(cmd)s %(stderr)s' % result
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

        # First we remove all files from dest_dir
        ssh_cmd = ['ssh', '-p', localport, ssh_target]
        ssh_cmd += ["'rm {}/*'".format(dest_dir)]
        # Note: this will return an error code if there are no files in dest_dir
        # We can safely ignore this
        result = run_cmd(ssh_cmd)
        results.append(result)

        # Run the scp command
        scp_cmd = ['scp', '-P', localport]
        file_list = []

        # Enumerate the test files
        for t in self.tst_inputs:
            filename = os.path.basename(t.abspath())
            file_list += filename

        # Add the binary
        binary = str(self.inputs[0])
        #dest_bin = dest_dir + binary
        file_list += self.inputs[0].abspath()

        # Copy all files in file_list
        scp_all_files = scp_cmd + file_list + [ssh_target+':'+dest_dir]

        result = run_cmd(scp_all_files)
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            usbmux_proc.kill()
            return

        cmd = self.format_command(dest_bin)


        ssh_cmd = ['ssh', '-p', localport, ssh_target]

        # We have to cd to the dir
        # Then we remove all files from the target dir with rm -rf
        # Echo the exit code after the shell command
        ssh_cmd += ["'cd %s;./%s;echo shellexit:$?'" % (dest_dir, binary)]

        result = run_cmd(ssh_cmd)
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
            result =  {'cmd': 'Shell exit indicate error',
                       'return_code': match.group(1),
                       'stdout': '',
                       'stderr': 'Exit code was %s' % match.group(1)}

            results.append(result)
            self.save_result(results)
            return

        self.save_result(results)



