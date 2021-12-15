#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import re
from waflib import Utils, Logs

from .basic_runner import BasicRunner


def options(opt):

    opts = opt.add_option_group("SSH/iOS runner options")

    opts.add_option(
        "--ssh_runner",
        default=None,
        dest="ssh_runner",
        action="store_true",
        help="Run the tests or benchmarks on a remote host using SSH",
    )

    opts.add_option(
        "--ssh_user",
        default=None,
        dest="ssh_user",
        help="Set the SSH username (used with --ssh_runner)",
    )

    opts.add_option(
        "--ssh_host",
        default=None,
        dest="ssh_host",
        help="Set the target SSH host (used with --ssh_runner)",
    )

    opts.add_option(
        "--ssh_dest_dir",
        default=None,
        dest="ssh_dest_dir",
        help="Set the destination folder where the binary "
        "will be copied with SCP (used with --ssh_runner)",
    )

    opts.add_option(
        "--ssh_clean_dir",
        default=None,
        dest="ssh_clean_dir",
        action="store_true",
        help="Delete all files from the destination folder "
        "before running the binary (used with --ssh_runner)",
    )

    opts.add_option(
        "--ssh_output_file",
        default=None,
        dest="ssh_output_file",
        help="Save the console output to the given file " "(used with --ssh_runner)",
    )

    opts.add_option(
        "--ssh_options",
        default=None,
        dest="ssh_options",
        help="Set extra options for SSH (used with --ssh_runner)",
    )

    opts.add_option(
        "--scp_options",
        default=None,
        dest="scp_options",
        help="Set extra options for SCP (used with --ssh_runner)",
    )


class SSHRunner(BasicRunner):
    def run_cmd(self, cmd):

        bld = self.generator.bld
        run_silent = bld.has_tool_option("run_silent")

        print("Running: {}\n".format(cmd))

        # The pty module only works on Unix systems
        stdin_target = Utils.subprocess.PIPE
        if sys.platform != "win32":
            import pty

            # subprocess.Popen() does not allocate a terminal for new
            # processes. We allocate a pseudo-terminal with pty.openpty() and
            # connect it to stdin. This is required if SSH is invoked with the
            # -t flag, which ensures that the remote process is terminated when
            # the SSH process is killed on the host.
            (master, slave) = pty.openpty()
            stdin_target = slave

        proc = Utils.subprocess.Popen(
            cmd,
            cwd=self.inputs[0].parent.abspath(),
            universal_newlines=True,
            stdin=stdin_target,
            stdout=Utils.subprocess.PIPE,
            # stderr should go into the same handle as stdout:
            stderr=Utils.subprocess.STDOUT,
        )

        all_stdout = []
        # iter() is used to read lines as soon as they are written to
        # work around the read-ahead bug in Python 2:
        # https://bugs.python.org/issue3907
        for line in iter(proc.stdout.readline, ""):
            all_stdout.append(line)
            if not run_silent:
                print(line.rstrip())
                sys.stdout.flush()

        proc.stdout.close()
        return_code = proc.wait()

        if return_code:
            print("\nReturn code: {}\n".format(return_code))

        stdout = "".join(all_stdout)
        if hasattr(stdout, "decode"):
            # This is needed in Python 2 to allow unicode output
            stdout = stdout.decode("utf-8")

        result = {"cmd": cmd, "return_code": return_code, "stdout": stdout}

        return result

    def save_result(self, results, ssh_cmd):
        # Override save_result to ensure that the kernel objects are removed

        # Unload the required kernel objects with rmmod (in reverse order)
        # Note: you have to SSH with the ROOT user!
        for ko in reversed(self.kernel_objects):
            result = self.run_cmd(ssh_cmd + ["rmmod", ko.name])
            results.append(result)

        super(SSHRunner, self).save_result(results)

    def run(self):

        bld = self.generator.bld

        dest_dir = bld.get_tool_option("ssh_dest_dir")
        ssh_host = bld.get_tool_option("ssh_host")
        ssh_user = bld.get_tool_option("ssh_user")
        ssh_target = ssh_user + "@" + ssh_host

        ssh_options = []
        if bld.has_tool_option("ssh_options"):
            ssh_options = bld.get_tool_option("ssh_options").replace('"', "").split(" ")

        scp_options = []
        if bld.has_tool_option("scp_options"):
            scp_options = bld.get_tool_option("scp_options").replace('"', "").split(" ")

        ssh_cmd = ["ssh", "-t"] + ssh_options + [ssh_target]
        scp_cmd = ["scp"] + scp_options

        self.run_ssh(ssh_cmd, scp_cmd, ssh_target, dest_dir)

    def run_ssh(self, ssh_cmd, scp_cmd, ssh_target, dest_dir):

        bld = self.generator.bld

        results = []

        # Delete all files from the destination folder if requested
        if bld.has_tool_option("ssh_clean_dir"):
            result = self.run_cmd(ssh_cmd + ["rm", "-rf", "{0}/*".format(dest_dir)])
            results.append(result)

        # Make sure the destination folder exists
        result = self.run_cmd(ssh_cmd + ["mkdir", "-p", "{0}".format(dest_dir)])
        results.append(result)

        # Enumerate the test files
        file_list = [test_input.abspath() for test_input in self.test_inputs]

        # Add the required kernel objects
        for ko in self.kernel_objects:
            file_list.append(ko.abspath())

        # Add the binary
        binary = self.inputs[0]
        file_list.append(binary.abspath())

        # Copy all files in file_list
        result = self.run_cmd(scp_cmd + file_list + [ssh_target + ":" + dest_dir])
        results.append(result)

        if result["return_code"] != 0:
            self.save_result(results, ssh_cmd)
            return

        # Load the required kernel objects with insmod (in the original order)
        # Note: you have to SSH with the ROOT user!
        for ko in self.kernel_objects:
            result = self.run_cmd(
                ssh_cmd + ["insmod", "{0}/{1}".format(dest_dir, ko.name)]
            )
            results.append(result)
            if result["return_code"] != 0:
                self.save_result(results, ssh_cmd)
                return

        run_binary_cmd = "./{0}".format(binary.name)

        # Format the run command
        run_binary_cmd = self.format_command(run_binary_cmd)

        # Some SSH servers may truncate long outputs, so a workaround is used:
        # the output is saved to a file on the target device, and this file is
        # transferred to the host if the 'ssh_output_file' option is specified
        if bld.has_tool_option("ssh_output_file"):
            # Run the target binary and capture its output
            output_file = bld.get_tool_option("ssh_output_file")
            result = self.run_cmd(
                ssh_cmd
                + [
                    "cd {0};{1} &> {2};echo shellexit:$? >> {2}".format(
                        dest_dir, run_binary_cmd, output_file
                    )
                ]
            )
            results.append(result)
            failed_run = result["return_code"] != 0

            # Copy the output file to the host
            result = self.run_cmd(
                scp_cmd + ["{0}:{1}".format(ssh_target, output_file), "."]
            )
            results.append(result)
            failed_run = failed_run or (result["return_code"] != 0)

            # Print the contents of the output file to stdout
            output_basename = os.path.basename(output_file)
            result = self.run_cmd(["cat", output_basename])
            results.append(result)
            failed_run = failed_run or (result["return_code"] != 0)

            # Abort execution if any of the previous steps failed
            if failed_run:
                self.save_result(results, ssh_cmd)
                return
        else:
            # Echo the exit code after the shell command
            result = self.run_cmd(
                ssh_cmd
                + ["cd {0};{1};echo shellexit:$?".format(dest_dir, run_binary_cmd)]
            )
            results.append(result)

            if result["return_code"] != 0:
                self.save_result(results, ssh_cmd)
                return

        # Almost done. Look for the exit code in the output
        # and fail if non-zero
        match = re.search("shellexit:(\d+)", result["stdout"])

        if not match:
            error_msg = "Failed to find return code in output!\n"
            print(error_msg)

            result = {
                "cmd": "Looking for shell exit",
                "return_code": -1,
                "stdout": error_msg,
            }

            results.append(result)
            self.save_result(results, ssh_cmd)
            return

        if match.group(1) != "0":
            error_msg = "Command return code:{}\n".format(match.group(1))
            print(error_msg)

            result = {
                "cmd": "Checking return code for command",
                "return_code": match.group(1),
                "stdout": error_msg,
            }

            results.append(result)
            self.save_result(results, ssh_cmd)
            return

        # Pull the result file if needed
        if bld.has_tool_option("result_file"):

            result_file = bld.get_tool_option("result_file")

            result_folder = "."
            result_on_host = result_file
            if bld.has_tool_option("result_folder"):
                result_folder = bld.get_tool_option("result_folder")
                # Make sure that the result folder exists on the host
                if not os.path.exists(result_folder):
                    os.makedirs(result_folder)
                result_on_host = os.path.join(result_folder, result_file)

            # Remove the old result file if it exists
            self.run_cmd(["rm", "-f", result_on_host])

            # This works if the path separators are compatible on the host
            # and the target device
            result_on_device = os.path.join(dest_dir, result_file)

            result = self.run_cmd(
                scp_cmd
                + ["{0}:{1}".format(ssh_target, result_on_device), result_folder]
            )
            results.append(result)

            if result["return_code"] != 0:
                self.save_result(results, ssh_cmd)
                return

        self.save_result(results, ssh_cmd)
