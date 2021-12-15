#!/usr/bin/env python
# encoding: utf-8

import os
import re

from .basic_runner import BasicRunner


class AndroidRunner(BasicRunner):
    def run(self):

        bld = self.generator.bld

        adb = bld.env.get_flat("ADB")

        results = []

        dest_dir = "/data/local/tmp/"

        device_id = None
        if bld.has_tool_option("device_id"):
            device_id = bld.get_tool_option("device_id")

        adb_shell = [adb]
        if device_id:
            adb_shell += ["-s", device_id]
        adb_shell += ["shell"]

        adb_push = [adb]
        if device_id:
            adb_push += ["-s", device_id]
        adb_push += ["push"]

        # Push the test files
        for t in self.test_inputs:

            filename = os.path.basename(t.abspath())
            # This path is on android, hence we use '/'
            # regardless of the host platform.
            dest_file = dest_dir + filename

            result = self.run_cmd(adb_push + [t.abspath(), dest_file])

            results.append(result)
            if result["return_code"] != 0:
                self.save_result(results)
                return

        # Push the binary
        binary = str(self.inputs[0].name)
        adb_push_bin = adb_push + [self.inputs[0].abspath(), dest_dir + binary]

        result = self.run_cmd(adb_push_bin)
        results.append(result)

        if result["return_code"] != 0:
            self.save_result(results)
            return

        run_binary_cmd = "./{0}".format(binary)

        # Format the run command
        run_binary_cmd = self.format_command(run_binary_cmd)

        # Echo the exit code after the shell command
        result = self.run_cmd(
            adb_shell
            + ["cd {0};{1};echo shellexit:$?".format(dest_dir, run_binary_cmd)]
        )

        results.append(result)

        if result["return_code"] != 0:
            self.save_result(results)
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
            self.save_result(results)
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
            self.save_result(results)
            return

        # Pull the result file if needed
        if bld.has_tool_option("result_file"):

            adb_pull = [adb]

            if device_id:
                adb_pull += ["-s", device_id]

            adb_pull += ["pull"]

            result_file = bld.get_tool_option("result_file")

            # This path is on android and not the host platform
            result_on_device = dest_dir + result_file

            result_on_host = result_file
            if bld.has_tool_option("result_folder"):
                result_folder = bld.get_tool_option("result_folder")
                # Make sure that the result folder exists on the host
                if not os.path.exists(result_folder):
                    os.makedirs(result_folder)
                result_on_host = os.path.join(result_folder, result_file)

            # Remove the old result file if it exists
            self.run_cmd(["rm", "-f", result_on_host])

            result = self.run_cmd(adb_pull + [result_on_device, result_on_host])
            results.append(result)

            if result["return_code"] != 0:
                self.save_result(results)
                return

        self.save_result(results)
