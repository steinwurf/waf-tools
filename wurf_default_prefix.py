#!/usr/bin/env python
# encoding: utf-8

import os
import waflib

"""
As a default, we would like binaries to be installed in the project folder.
Typically our libraries are not consumed by system package managers, but just
developers who need easy access to the compiled libraries and includes.
"""


def options(opt):

    # By default, we install to the "{PROJECT_NAME}_install" folder in
    # the local project folder.
    #
    # The user can change this using the --destdir option, e.g.:
    #
    #    python waf install --destdir=/path/to/target/folder

    group = opt.option_groups["Configuration options"]

    # First, we override the default destdir value
    project_dir = opt.srcnode.abspath()
    appname = getattr(waflib.Context.g_module, "APPNAME")
    default_destdir = os.path.join(project_dir, appname + "_install")

    group.remove_option("--destdir")
    group.add_option(
        "--destdir",
        help="installation root [default: %r]" % default_destdir,
        default=default_destdir,
        dest="destdir",
    )

    # Second, we set the default prefix value to ''
    # Any non-empty prefix would interfere with the custom destdir, and
    # the prefix value can only be changed during the waf configure step,
    # since waf determines the installation path as follows:
    #    target_path = Options.options.destdir + self.env.PREFIX + dest
    # Therefore, it is best to use an empty prefix.
    default_prefix = ""
    group.remove_option("--prefix")
    group.add_option(
        "--prefix",
        dest="prefix",
        default=default_prefix,
        help="installation prefix [default: %r]" % default_prefix,
    )
