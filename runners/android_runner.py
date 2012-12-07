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
            combined_stdout += 'Running %(cmd)s %(stdout)s' % result
            combined_stderr += 'Running %(cmd)s %(stderr)s' % result
            if result['return_code'] != 0: combined_return_code = -1

        result = (self.format_command(self.inputs[0]), combined_return_code,
                  combined_stdout, combined_stderr)
        
        super(AndroidRunner, self).save_result(result)
    
    def run(self):

        bld = self.generator.bld
        
        adb = bld.env['ADB']

        results = []
        
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

        dest_bin = '/data/local/tmp/' + str(self.inputs[0])

        # Run the two adb commands
        adb_push = [adb, 'push', str(self.inputs[0].abspath()), dest_bin] 

        result = run_cmd(adb_push)
        results.append(result)

        if result['return_code'] != 0:
            self.save_result(results)
            return
        
        cmd = self.format_command(dest_bin)

        # Echo the exit code after the shell command
        adb_shell = [adb, 'shell', cmd + ';echo shellexit:$?']

        result = run_cmd(adb_shell)
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



