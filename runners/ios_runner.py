#!/usr/bin/env python
# encoding: utf-8

import os, sys, re
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

        dest_dir = '/var/mobile/tmp/'
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
                       'stdout': stdout, 'stderr':stderr}

            return result

        usbmux_dir = None
        if bld.has_tool_option('usbmux_dir'):
            usbmux_dir = bld.get_tool_option('usbmux_dir')
        else:
            bld.fatal('usbmux_dir is not specified')

        # Run the scp command
        scp_cmd = []

        if device_id:
            scp_cmd += ['scp', '-P', localport]


        # Copy the test files
        for t in self.tst_inputs:

            filename = os.path.basename(t.abspath())
            dest_file = os.path.join(dest_dir, filename)

            scp_cmd_file = scp_cmd + [t.abspath(), dest_file]

            result = run_cmd(scp_cmd_file)
            results.append(result)

            if result['return_code'] != 0:
                self.save_result(results)
                return


        # Copy the binary
        binary = str(self.inputs[0])
        dest_bin = dest_dir + binary

        scp_cmd_bin = scp_cmd + [self.inputs[0].abspath(), dest_bin]

        result = run_cmd(scp_cmd_bin)
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            return

        cmd = self.format_command(dest_bin)

        ssh_cmd = ['ssh', '-p', localport]

        # We have to cd to the dir
        # Echo the exit code after the shell command
        ssh_cmd += ["cd %s;./%s;echo shellexit:$?" % (dest_dir, binary)]

        result = run_cmd(ssh_cmd)
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
            result =  {'cmd': 'Shell exit indicate error',
                       'return_code': match.group(1),
                       'stdout': '',
                       'stderr': 'Exit code was %s' % match.group(1)}

            results.append(result)
            self.save_result(results)
            return

        self.save_result(results)



