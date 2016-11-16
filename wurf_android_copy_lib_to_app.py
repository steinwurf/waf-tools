#!/usr/bin/env python
# encoding: utf-8

"""
Tool for copying jni libraries to the appropriate Android app folder.

The app folder must be provided by the build in the form of an option called
copy_path.
This means a build with the feature android_copy_lib_to_app should look similar
to this:

    bld(features='... android_copy_lib_to_app',
        ...
        copy_path='app/src/main/jniLibs/armeabi',
        ...)

Note the copy_path is relative to the project.
"""

import os
import shutil
from waflib.TaskGen import feature
from waflib.TaskGen import after_method

from waflib import Task, Errors, Logs


@feature('android_copy_lib_to_app')
@after_method('apply_link')
def android_copy_lib_to_app(self):
    """
    Copy library to Android application.

    When building an Android application from the IDE native libraries placed
    in the libs folder will be packaged in the APK. So we copy the shared libs
    we build there.
    """
    if not self.bld.is_mkspec_platform('android'):
        return

    if 'copy_path' not in dir(self):
        raise Errors.WafError(
            'android_copy_lib_to_app build missing required '
            '"copy_path" option.')

    input_libraries = self.link_task.outputs
    output_libraries = []
    for input_library in input_libraries:
        project_path = self.path.parent.abspath()
        output_library = os.path.basename(input_library.abspath())
        output_library = self.bld.root.make_node(
            os.path.abspath(os.path.join(
                project_path,
                self.copy_path,
                output_library)))
        output_libraries.append(output_library)

    copy_task = self.create_task('AndroidCopyFileTask')
    copy_task.set_inputs(input_libraries)
    copy_task.set_outputs(output_libraries)
    copy_task.chmod = self.link_task.chmod


class AndroidCopyFileTask(Task.Task):
    """Perform the copying of generated files to the Android project."""

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

            Logs.info("{n}    Copied: {c}{src}{n} -> {c}{tgt}{n}".format(
                c=Logs.colors(AndroidCopyFileTask.color),
                src=source_node.relpath(),
                tgt=target_node.relpath(),
                n=Logs.colors.NORMAL
            ))
