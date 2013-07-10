#!/usr/bin/env python
# encoding: utf-8

import os
##import sys

from waflib import Utils
from waflib.Configure import conf
from waflib import Logs
from waflib import Errors

##import waflib.Tools.gxx as gxx
##from os.path import abspath, expanduser

### The common modules are in the ./common folder
##CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
##sys.path.append(os.path.join(CURRENT_DIR,'common'))
##
##import clang_common
##import gxx_common
##import msvc_common

def check_minimum_cc_versions(conf, major, minor):
    # Enforce minimum version for C++ compiler
    CXX = conf.cmd_to_list(conf.env['CXX'])
    conf.mkspec_check_minimum_cc_version(CXX, major, minor)
    # Enforce minimum version for C compiler
    CC = conf.cmd_to_list(conf.env['CC'])
    conf.mkspec_check_minimum_cc_version(CC, major, minor)

def load_compiler(conf, compiler):

    # Note clang goes first otherwise 'g++' will be in 'clang(g++)'
    if 'clang' in compiler:
        # Set the CXX and CC variables manually if needed
        if not conf.env['CXX']: conf.env['CXX'] = 'clang++'
        if not conf.env['CC']: conf.env['CC'] = 'clang'
        # Use the g++ waf tool to load clang
        # as there is no tool for clang
        conf.load('g++')
        # Also load 'clang' as a C compiler using the gcc tool
        conf.load('gcc')
        conf.load_external_tool('mkspec_common', 'clang_common')
        # Enforce minimum version for compilers
        check_minimum_cc_versions(conf, 3, 0)
        conf.mkspec_set_clang_cxxflags()
        conf.mkspec_set_clang_ccflags()
    elif 'g++' in compiler:
        conf.load('g++')
        # Also load 'gcc' as a C compiler
        conf.load('gcc')
        conf.load_external_tool('mkspec_common', 'gxx_common')
        # Enforce minimum version for compilers
        check_minimum_cc_versions(conf, 4, 6)
        conf.mkspec_set_gxx_cxxflags()
        conf.mkspec_set_gcc_ccflags()
    elif 'msvc' in compiler or 'CL.exe' in compiler or 'cl.exe' in compiler:
        conf.load('msvc')
        # Note: the waf msvc tool also load msvc as a C compiler
        conf.load_external_tool('mkspec_common', 'msvc_common')
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
        'linux':  ['g++'],
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
            conf.end_msg(False)
            Logs.debug('cxx_default: %r' % e)
        else:
            if conf.env['CXX']:
                conf.end_msg(conf.env.get_flat('CXX'))
                conf.env['COMPILER_CXX'] = compiler
                break # Break from the for-cycle
            conf.end_msg(False)
    else:
        conf.fatal('Could not configure a C++ compiler!')
