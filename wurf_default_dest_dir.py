#!/usr/bin/env python
# encoding: utf-8

import os

"""
As a default we would like binaries to be installed in the project folder.
Typically our libraries are not consumed by system package managers but just
developers that need easy access to the .so, .a and includes.
"""


def options(opt):
    group = opt.option_groups['Configuration options']
    group.remove_option('--destdir')
    default_destdir = os.path.join(opt.srcnode.abspath(), 'build_output')
    group.add_option('--destdir',
                     help='installation root [default: %r]' % default_destdir,
                     default=default_destdir, dest='destdir')

    group.remove_option('--prefix')
    default_prefix = ''
    group.add_option('--prefix', dest='prefix', default=default_prefix,
                     help='installation prefix [default: %r]' % default_prefix)
