#!/usr/bin/env python
# encoding: utf-8

"""
Tool for copying binaries to a given folder.

The folder is specified with the copy_path option, and it must be a string or
a waf Node object.

If copy_path is a string, then it denotes a path relative to the wscript or
wscript_build file where the build task is defined:

    bld(features='... copy_binary',
        ...
        copy_path='../app/src/main/jniLibs/armeabi',
        ...)

If copy_path is a Node, then the usual waf methods can be used to specify the
target folder. To specify a path relative to the current top-level wscript
(i.e. the root folder of the top-level project), you can use bld.srcnode
like this (find_or_declare makes sure that the folder is created if needed):

    bld(features='... copy_binary',
        ...
        copy_path=bld.srcnode.find_or_declare('app/src/main/jniLibs/armeabi'),
        ...)
"""

import os
import shutil
from waflib.TaskGen import feature
from waflib.TaskGen import after_method

from waflib import Task, Errors, Node, Logs


def to_base_path(ctx, copy_path):

    if isinstance(copy_path, str):
        return os.path.join(ctx.path.abspath(), copy_path)
    elif isinstance(copy_path, Node.Node):
        return copy_path.abspath()
    else:
        raise Errors.WafError(
            "{}: copy_path must be an str or Node object.".format(ctx.name)
        )


@feature("copy_binary")
@after_method("apply_link")
def copy_binary(self):
    """Copy binary created by the link task to a given location."""

    if not hasattr(self, "copy_path"):
        raise Errors.WafError(
            '{}: missing required "copy_path" option.'.format(self.name)
        )

    if isinstance(self.copy_path, list):
        base_paths = []
        for p in self.copy_path:
            base_paths.append(to_base_path(self, p))
    else:
        base_paths = [to_base_path(self, self.copy_path)]

    if len(base_paths) == 0:
        raise Errors.WafError(
            "{}: copy_path must be at least one path.".format(self.name)
        )

    for base_path in base_paths:
        input_libraries = self.link_task.outputs
        output_libraries = []
        for input_library in input_libraries:
            output_library = self.bld.root.make_node(
                os.path.join(base_path, input_library.name)
            )
            output_libraries.append(output_library)

        copy_task = self.create_task("CopyFileTask")
        copy_task.set_inputs(input_libraries)
        copy_task.set_outputs(output_libraries)
        copy_task.chmod = self.link_task.chmod


class CopyFileTask(Task.Task):
    """Perform the copying of generated files."""

    color = "PINK"

    def run(self):
        """Run the task."""
        for source_node, target_node in zip(self.inputs, self.outputs):
            source = source_node.abspath()
            target = target_node.abspath()

            # Following is for shared libs and stale inodes (-_-)
            try:
                os.remove(target)
            except OSError:
                pass

            # Make sure the output directories are available
            try:
                os.makedirs(os.path.dirname(target))
            except OSError:
                pass

            # Copy the file
            try:
                shutil.copy2(source, target)
                os.chmod(target, self.chmod)
            except IOError as e:
                Logs.error("The copy file step failed: {0}".format(e))
                try:
                    os.stat(source)
                except (OSError, IOError):
                    Logs.error("File %r does not exist" % source)
                raise Errors.WafError("Could not copy the file %r" % target)

            Logs.info(
                "{n}{s}Copying {c}{source}{n} -> {c}{target}{n}".format(
                    c=Logs.colors(CopyFileTask.color),
                    s=" " * 10,
                    source=source_node.name,
                    target=target_node.relpath(),
                    n=Logs.colors.NORMAL,
                )
            )
