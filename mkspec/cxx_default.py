#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from waflib import Utils
from waflib.Configure import conf
from waflib.Logs import debug
import waflib.Tools.gxx as gxx
from os.path import abspath, expanduser

# The common modules are in the ./common folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR,'common'))

import clang_common
import gxx_common
import msvc_common

"""
Detect and setup the default compiler for the platform
"""
def configure(conf):

    cxx_compilers = \
    {
        'win32':  ['msvc', 'g++'],
        'linux':  ['g++'],
        'darwin': ['clang++', 'g++'],
        'cygwin': ['g++'],
        'default': ['g++']
    }

    # Here we try to find a compiler on the current host
    # based on the compiler list above
    sys_platform = Utils.unversioned_sys_platform()
    platform = 'default'
    # Check if we have a specific list for the current system
    if sys_platform in cxx_compilers:
        platform = sys_platform
    possible_compiler_list = cxx_compilers[platform]

    for compiler in possible_compiler_list:
        conf.env.stash()
        conf.start_msg('Checking for %r (C++ compiler)' % compiler)
        try:
            if compiler == 'clang++':
                # Set the CXX variable manually
                conf.env['CXX'] = 'clang++'
                # Use the g++ waf tool to load clang
                # as there is no tool for clang
                conf.load('g++')
            else:
                conf.load(compiler)
        except conf.errors.ConfigurationError as e:
            conf.env.revert()
            conf.end_msg(False)
            debug('cxx_default: %r' % e)
        else:
            if conf.env['CXX']:
                conf.end_msg(conf.env.get_flat('CXX'))
                conf.env['COMPILER_CXX'] = compiler
                break # Break from the for-cycle
            conf.end_msg(False)
    else:
        conf.fatal('Could not configure a C++ compiler!')

    CXX = conf.env.get_flat('CXX')

    # Note clang goes first otherwise 'g++' will be in 'clang(g++)'
    if 'clang' in CXX:
        conf.mkspec_set_clang_cxxflags()
    elif 'g++' in CXX:
        conf.mkspec_set_gxx_cxxflags()
    elif 'CL.exe' in CXX or 'cl.exe' in CXX:
        conf.mkspec_set_msvc_flags()
    else:
        raise Errors.WafError('toolchain_cxx flag for unknown compiler %s'
                              % conf.env.CXX)

