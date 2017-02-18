#!/usr/bin/env python
# encoding: utf-8

"""
Copies chosen targets to the specified install path.

The install path can be set with the install_path option:
    python waf --install_path="~/my_binaries"

If you also pass the install_relative option waf will preserve the folder
structure when installing, e.g.:
    python waf --install_path="~/my_binaries" --install_relative
"""

import os
from waflib.TaskGen import feature, before_method, after_method


def options(opt):

    opts = opt.add_option_group('Install path options')

    opts.add_option(
        '--install_path', default=None, dest='install_path',
        help="Copy the compiled C/C++ binaries to the specified path")

    opts.add_option(
        '--install_relative', default=None, dest='install_relative',
        action='store_true', help="Preserve the folder structure "
                                  "when copying binaries")

    opts.add_option(
        '--install_shared_libs', default=None, dest='install_shared_libs',
        action='store_true', help="Copy the compiled C/C++ shared libraries "
                                  "(used with --install_path)")

    opts.add_option(
        '--install_static_libs', default=None, dest='install_static_libs',
        action='store_true', help="Copy the compiled C/C++ static libraries "
                                  "(used with --install_path)")


@feature('cshlib', 'cxxshlib')
@before_method('apply_link')
def update_shlib_install_path(self):
    """
    Sets the install_path attribute of shared library task generators before
    executing the apply_link method. This enables the installation of the
    compiled C and C++ shared libraries to facilitate the integration
    with other build systems.
    """

    if self.bld.has_tool_option('install_path') and \
       self.bld.has_tool_option('install_shared_libs'):
        install_path = self.bld.get_tool_option('install_path')
        self.install_path = os.path.abspath(os.path.expanduser(install_path))


@feature('cstlib', 'cxxstlib')
@before_method('apply_link')
def update_stlib_install_path(self):
    """
    Sets the install_path attribute of static library task generators before
    executing the apply_link method. This enables the installation of the
    compiled C and C++ static libraries to facilitate the integration
    with other build systems.
    """

    if self.bld.has_tool_option('install_path') and \
       self.bld.has_tool_option('install_static_libs'):
        install_path = self.bld.get_tool_option('install_path')
        self.install_path = os.path.abspath(os.path.expanduser(install_path))


@feature('cxxprogram', 'cprogram', 'pyext')
@before_method('apply_link')
def update_install_path(self):
    """
    Updates the install_path variable of the task generator before
    executing the apply_link method. This will override the install_path
    otherwise used.
    """

    if self.bld.has_tool_option('install_path'):
        install_path = self.bld.get_tool_option('install_path')
        self.install_path = os.path.abspath(os.path.expanduser(install_path))


@feature('cxxprogram', 'cprogram', 'pyext')
@after_method('apply_link')
def change_relative_path_option(self):
    """
    If an install_task exists this will update the relative_trick
    options, which will make waf preserve the folder structure
    """

    install_relative = self.bld.has_tool_option('install_relative')

    if getattr(self, 'install_task', None):
        self.install_task.relative_trick = install_relative
