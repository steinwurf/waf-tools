#!/usr/bin/env python
# encoding: utf-8

import os
import time
from waflib import Utils, Logs
from ssh_runner import SSHRunner


class IOSRunner(SSHRunner):

    def save_result(self, results, ssh_cmd):

        # Kill the usbmux process
        if self.usbmux_proc:
            self.usbmux_proc.kill()

        super(IOSRunner, self).save_result(results, ssh_cmd)

    def run(self):

        bld = self.generator.bld
        self.usbmux_proc = None

        dest_dir = '/private/var/mobile/tmp'
        localport = '22222'
        ssh_target = 'mobile@localhost'

        def start_proc(cmd):

            Logs.debug("wr: starting %r", cmd)

            proc = Utils.subprocess.Popen(
                cmd,
                stderr=Utils.subprocess.PIPE,
                stdout=Utils.subprocess.PIPE)
            # Wait for 3 seconds so that the process can start properly
            # If the device was idle for a long time, then the connection
            # might not start for the first try
            time.sleep(3.0)

            return proc

        usbmux_dir = bld.get_tool_option('usbmux_dir')

        usbmux = os.path.join(usbmux_dir, 'tcprelay.py')
        # Use usbmux in threaded mode to handle multiple connections at once
        usbmux_cmd = [usbmux, '--threaded', '22:{}'.format(localport)]
        scp_cmd = ['scp', '-P', localport]
        ssh_cmd = ['ssh', '-t', '-p', localport, ssh_target]

        # Start the usbmux daemon to forward 'localport' to port 22 on USB
        self.usbmux_proc = start_proc(usbmux_cmd)

        # Call the 'run_ssh' method of the SSHRunner class
        super(IOSRunner, self).run_ssh(ssh_cmd, scp_cmd, ssh_target, dest_dir)
