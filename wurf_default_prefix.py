#!/usr/bin/env python
# encoding: utf-8

import os
import waflib

"""
As a default we would like binaries to be installed in the project folder.
Typically our libraries are not consumed by system package managers but just
developers that need easy access to the .so, .a and includes.
"""


def options(opt):

    # Determine the default prefix. We would like to avoid installing
    # "incompatible" versions of the libraries into the same folders.
    #
    # To achieve this goal, we have choosen the following strategy:
    #
    # 1. If we are in a git repository use the following:
    #    a. If on a tag (released version) use the version number
    #    b. Otherwise use the SHA1
    # 2. If not in a git repository, we use the postfix "_install".
    #
    # To do the above we require a recent version of our Waf build tool.
    # If this is not available we fallback to "_install".

    version = "install"
    project_dir = opt.srcnode.abspath()

    # These operations might fail if our waf API changes in some way
    try:
        git = opt.registry.require('git')

        if git.is_git_repository(cwd=project_dir):
            version = git.current_tag(cwd=project_dir)

            if not version:
                # Use the first 8 characters of the current commit
                version = git.current_commit(cwd=project_dir)[:8]

    except Exception:
        pass

    appname = getattr(waflib.Context.g_module, 'APPNAME')

    group = opt.option_groups['Configuration options']
    group.remove_option('--prefix')
    default_prefix = os.path.join(os.sep, appname + '_' + version)
    group.add_option('--prefix', dest='prefix', default=default_prefix,
                     help='installation prefix [default: %r]' % default_prefix)
