#!/usr/bin/env python
# encoding: utf-8

"""Tool for copying jni libraries to the appropriate Android app folder."""

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
    in the libs folder will be packaged in the apk. So we copy the shared libs
    we build there.
    """
    if not self.bld.is_mkspec_platform('android'):
        return

    input_librarys = self.link_task.outputs
    output_librarys = []
    for input_library in input_librarys:
        project_path = self.path.parent.abspath()
        output_library = os.path.basename(input_library.abspath())
        output_library = self.bld.root.make_node(
            os.path.abspath(os.path.join(
                project_path,
                'app',
                'src',
                'main',
                'jniLibs',
                'armeabi',
                output_library)))

        output_librarys.append(output_library)

    copy_task = self.create_task('AndroidCopyFileTask')
    copy_task.set_inputs(input_librarys)
    copy_task.set_outputs(output_librarys)
    copy_task.chmod = self.link_task.chmod


class AndroidCopyFileTask(Task.Task):
    """Perform the copying of generated files to the Android project."""

    color = 'PINK'

    def run(self):
        """Run the task."""
        for src_node, tgt_node in zip(self.inputs, self.outputs):
            src = src_node.abspath()
            tgt = tgt_node.abspath()

            # Following is for shared libs and stale inodes (-_-)
            try:
                os.remove(tgt)
            except OSError:
                pass

            # Make sure the output directories are available
            try:
                os.makedirs(os.path.dirname(tgt))
            except OSError:
                pass

            # Copy the file
            try:
                shutil.copy2(src, tgt)
                os.chmod(tgt, self.chmod)
            except IOError as e:
                Logs.error("The copy file step failed: {0}".format(e))
                try:
                    os.stat(src)
                except (OSError, IOError):
                    Logs.error('File %r does not exist' % src)
                raise Errors.WafError('Could not install the file %r' % tgt)

            Logs.info("{n}    Copied: {c}{src}{n} -> {c}{tgt}{n}".format(
                c=Logs.colors(AndroidCopyFileTask.color),
                src=src_node.relpath(),
                tgt=tgt_node.relpath(),
                n=Logs.colors.NORMAL
            ))
