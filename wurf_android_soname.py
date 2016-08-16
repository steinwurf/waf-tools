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


#def resolve(ctx):
#
#    opts = ctx.opt.add_option_group('Install path options')
#
#    opts.add_option(
#        '--install_path', default=None, dest='install_path',
#        help="Copy the compiled C/C++ binaries to the specified path")
#
#    opts.add_option(
#        '--install_relative', default=None, dest='install_relative',
#        action='store_true', help="Preserve the folder structure "
#                                  "when copying binaries")
#
#    opts.add_option(
#        '--install_shared_libs', default=None, dest='install_shared_libs',
#        action='store_true', help="Copy the compiled C/C++ shared libraries "
#                                  "(used with --install_path)")
#
#    opts.add_option(
#        '--install_static_libs', default=None, dest='install_static_libs',
#        action='store_true', help="Copy the compiled C/C++ static libraries "
#                                  "(used with --install_path)")


@feature('cshlib', 'cxxshlib')
@before_method('apply_link')
def set_andoid_soname(self):
    """

    """

    if not bld.is_mkspec_platform('android'):
        return

    print("LINK " + self.link_task.outputs[0].relpath())
