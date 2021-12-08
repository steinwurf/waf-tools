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
from waflib import Options
from waflib.TaskGen import feature, before_method, after_method


def options(opt):

    opts = opt.add_option_group("Install path options")

    opts.add_option(
        "--install_path",
        default=None,
        dest="install_path",
        help="Copy the compiled C/C++ binaries to the specified path",
    )

    opts.add_option(
        "--install_relative",
        default=None,
        dest="install_relative",
        action="store_true",
        help="Preserve the folder structure " "when copying binaries",
    )

    opts.add_option(
        "--install_shared_libs",
        default=None,
        dest="install_shared_libs",
        action="store_true",
        help="Copy the compiled C/C++ shared libraries " "(used with --install_path)",
    )

    opts.add_option(
        "--install_static_libs",
        default=None,
        dest="install_static_libs",
        action="store_true",
        help="Copy the compiled C/C++ static libraries " "(used with --install_path)",
    )


def build(bld):
    # The install_path option only works correctly when the destdir value
    # is an empty string. Otherwise the destdir value would be prepended to
    # the install_path locations that are calculated in this file.
    if bld.has_tool_option("install_path"):
        # If the install_path option is used, then destdir must be empty
        if Options.options.destdir:
            Options.options.destdir = ""


@feature("cshlib", "cxxshlib")
@before_method("apply_link")
def update_shlib_install_path(self):
    """
    Sets the install_path attribute of shared library task generators before
    executing the apply_link method. This enables the installation of the
    compiled C and C++ shared libraries to facilitate the integration
    with other build systems.
    """
    if self.bld.has_tool_option("install_path") and self.bld.has_tool_option(
        "install_shared_libs"
    ):
        install_path = self.bld.get_tool_option("install_path")
        self.install_path = os.path.abspath(os.path.expanduser(install_path))


@feature("cstlib", "cxxstlib")
@before_method("apply_link")
def update_stlib_install_path(self):
    """
    Sets the install_path attribute of static library task generators before
    executing the apply_link method. This enables the installation of the
    compiled C and C++ static libraries to facilitate the integration
    with other build systems.
    """
    if self.bld.has_tool_option("install_path") and self.bld.has_tool_option(
        "install_static_libs"
    ):
        install_path = self.bld.get_tool_option("install_path")
        self.install_path = os.path.abspath(os.path.expanduser(install_path))


@feature("cxxprogram", "cprogram", "pyext")
@before_method("apply_link")
def update_install_path(self):
    """
    Updates the install_path variable of the task generator before
    executing the apply_link method. This will override the install_path
    otherwise used.
    """
    if self.bld.has_tool_option("install_path"):
        install_path = self.bld.get_tool_option("install_path")
        self.install_path = os.path.abspath(os.path.expanduser(install_path))


@feature("cxxprogram", "cprogram", "pyext")
@after_method("apply_link")
def change_relative_path_option(self):
    """
    Overwrite the output paths for the install_task to preserver the
    the folder structure (relative to the project root)
    """
    install_relative = self.bld.has_tool_option("install_relative")

    if getattr(self, "install_task", None) and install_relative:
        # Note that we need to manually overwrite the outputs using the
        # desired relative path, because install_task.relative_trick=True
        # does not work (the outputs are already calculated)
        dest = self.install_task.get_install_path()
        outputs = []
        for y in self.install_task.inputs:
            # Preserve the relative path from the project root within the
            # install folder
            destfile = os.path.join(dest, y.path_from(self.bld.srcnode))
            outputs.append(self.bld.root.make_node(destfile))
        self.install_task.outputs = outputs
