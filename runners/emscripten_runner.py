#!/usr/bin/env python
# encoding: utf-8

from .basic_runner import BasicRunner


class EmscriptenRunner(BasicRunner):
    def format_command_list(self, executable):
        cmd = super(EmscriptenRunner, self).format_command_list(executable)

        bld = self.generator.bld
        nodejs = bld.env["NODEJS"][0]
        cmd = [nodejs] + cmd
        return cmd
