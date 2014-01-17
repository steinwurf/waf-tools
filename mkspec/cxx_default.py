#!/usr/bin/env python
# encoding: utf-8

import os

from waflib import Utils
from waflib.Configure import conf
from waflib import Logs
from waflib import Errors

import clang_common
import gxx_common
import msvc_common


def load_compiler(conf, compiler):

    # Note clang goes first otherwise 'g++' will be in 'clang(g++)'
    if 'clang' in compiler:
        conf.mkspec_clang_configure(3, 0, minimum = True)

    elif 'g++' in compiler:
        conf.mkspec_gxx_configure(4, 6, minimum = True)

    elif 'msvc' in compiler or 'CL.exe' in compiler or 'cl.exe' in compiler:
        conf.load('msvc')
        # Note: the waf msvc tool also load msvc as a C compiler
        conf.mkspec_check_minimum_msvc_version(11.0)
        conf.mkspec_set_msvc_flags()
    else:
        raise Errors.WafError('Unknown compiler: %s' % compiler)

"""
Detect and setup the default compiler for the platform
"""
def configure(conf):

    # If the user-defined CXX variable is set
    # then use that compiler as the first option
    if 'CXX' in os.environ:
        compiler = os.environ['CXX']
        conf.start_msg('Checking C++ compiler %r' % compiler)
        load_compiler(conf, compiler)
        if conf.env['CXX']:
            conf.end_msg(conf.env.get_flat('CXX'))
            conf.env['COMPILER_CXX'] = compiler
            return # Compiler configured successfully
        else:
            conf.end_msg(False)
            conf.fatal('Could not configure a C++ compiler!')

    # Otherwise we try to find a compiler on the current host
    # based on the following compiler list
    cxx_compilers = \
    {
        'win32':  ['msvc', 'g++'],
        'linux':  ['g++', 'clang++'],
        'darwin': ['clang++', 'g++'],
        'cygwin': ['g++'],
        'default': ['g++']
    }

    sys_platform = Utils.unversioned_sys_platform()
    platform = 'default'
    # Check if we have a specific list for the current system
    if sys_platform in cxx_compilers:
        platform = sys_platform

    # The list of the compilers to be checked
    possible_compiler_list = cxx_compilers[platform]

    for compiler in possible_compiler_list:
        conf.env.stash()
        conf.start_msg('Checking for %r (C++ compiler)' % compiler)
        try:
            load_compiler(conf, compiler)
        except conf.errors.ConfigurationError as e:
            conf.env.revert()
            conf.end_msg(e, color='YELLOW')
            Logs.debug('cxx_default: %r' % e)
        else:
            if conf.env['CXX']:
                conf.end_msg(conf.env.get_flat('CXX'))
                conf.env['COMPILER_CXX'] = compiler
                break # Break from the for-cycle
            conf.end_msg(False)
    else:
        conf.fatal('Could not configure a C++ compiler!')
