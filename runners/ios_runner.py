#!/usr/bin/env python
# encoding: utf-8

import os
import time
from waflib import Utils, Logs

from .ssh_runner import SSHRunner


class IOSRunner(SSHRunner):
    def run(self):

        bld = self.generator.bld

        dest_dir = "/private/var/mobile/tmp"
        localport = "22222"
        ssh_target = "mobile@localhost"

        ssh_options = []
        if bld.has_tool_option("ssh_options"):
            ssh_options = bld.get_tool_option("ssh_options").replace('"', "").split(" ")

        scp_options = []
        if bld.has_tool_option("scp_options"):
            scp_options = bld.get_tool_option("scp_options").replace('"', "").split(" ")

        ssh_cmd = ["ssh", "-t", "-p", localport] + ssh_options + [ssh_target]
        scp_cmd = ["scp", "-P", localport] + scp_options

        # Call the 'run_ssh' method of the SSHRunner class
        super(IOSRunner, self).run_ssh(ssh_cmd, scp_cmd, ssh_target, dest_dir)
