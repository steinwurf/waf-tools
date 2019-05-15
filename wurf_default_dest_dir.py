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
    group = opt.option_groups['Configuration options']
    group.remove_option('--destdir')

    default_destdir = opt.srcnode.abspath()

    group.add_option('--destdir',
                     help='installation root [default: %r]' % default_destdir,
                     default=default_destdir, dest='destdir')

    appname = getattr(waflib.Context.g_module, 'APPNAME')
    version = getattr(waflib.Context.g_module, 'VERSION')

    group.remove_option('--prefix')
    default_prefix = os.path.join(os.sep, appname + '_' + version)
    group.add_option('--prefix', dest='prefix', default=default_prefix,
                     help='installation prefix [default: %r]' % default_prefix)
