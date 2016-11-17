#!/usr/bin/env python
# encoding: utf-8

"""
Tool for copying binaries to a given folder.

The folder must be provided by the build in the form of an option called
copy_path.
This means a build with the feature copy_binary should look similar
to this:

    bld(features='... copy_binary',
        ...
        copy_path='app/src/main/jniLibs/armeabi',
        ...)

Note the copy_path is relative to the wscript or wscript_build file.
"""

import os
import shutil
from waflib.TaskGen import feature
from waflib.TaskGen import after_method

from waflib import Task, Errors, Logs


@feature('copy_binary')
@after_method('apply_link')
def copy_binary(self):
    """Copy binary created by the link task to a given location."""
    if not hasattr(self, 'copy_path'):
        raise Errors.WafError(
            '{} build missing required "copy_path" option.'.format(self.name))

    input_libraries = self.link_task.outputs
    output_libraries = []
    for input_library in input_libraries:
        output_library = self.bld.root.make_node(os.path.join(
            self.path.abspath(),
            self.copy_path,
            os.path.basename(input_library.abspath())))
        output_libraries.append(output_library)

    copy_task = self.create_task('CopyFileTask')
    copy_task.set_inputs(input_libraries)
    copy_task.set_outputs(output_libraries)
    copy_task.chmod = self.link_task.chmod


class CopyFileTask(Task.Task):
    """Perform the copying of generated files."""

    color = 'PINK'

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
                    Logs.error('File %r does not exist' % source)
                raise Errors.WafError('Could not install the file %r' % target)

            Logs.info("{n}{s}Copying {c}{source}{n} -> {c}{target}{n}".format(
                c=Logs.colors(CopyFileTask.color),
                s=' ' * 10,
                source=os.path.basename(source_node.abspath()),
                target=target_node.relpath(),
                n=Logs.colors.NORMAL
            ))
