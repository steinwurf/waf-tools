#!/usr/bin/env python
# encoding: utf-8

import os

from waflib import Utils
from waflib.Configure import conf
import waflib.Tools.gxx as gxx
import waflib.Tools.gcc as gcc
from os.path import abspath, expanduser

import cxx_common

@conf
def mkspec_gxx_configure(conf, major, minor, prefix = None):

    # Where to look
    paths = conf.mkspec_get_toolchain_paths()

    # Find g++ first
    gxx_names = conf.mkspec_get_gnu_binary_name('g++', major, minor, prefix)
    cxx = conf.find_program(gxx_names, path_list = paths)
    cxx = conf.cmd_to_list(cxx)
    conf.env['CXX'] = cxx
    conf.env['CXX_NAME'] = os.path.basename(conf.env.get_flat('CXX'))
    conf.mkspec_check_cc_version(cxx, major, minor)

    # Also find gcc
    gcc_names = conf.mkspec_get_gnu_binary_name('gcc', major, minor, prefix)
    cc = conf.find_program(gcc_names, path_list = paths)
    cc = conf.cmd_to_list(cc)
    conf.env['CC'] = cc
    conf.env['CC_NAME'] = os.path.basename(conf.env.get_flat('CC'))
    conf.mkspec_check_cc_version(cc, major, minor)

    # Find the archiver
    ar = conf.mkspec_get_ar_binary_name(prefix)
    conf.find_program(ar, path_list = paths, var = 'AR')
    conf.env.ARFLAGS = 'rcs'

    # Set up C++ tools and flags
    conf.gxx_common_flags()
    if not conf.is_mkspec_platform('android'):
        conf.gxx_modifier_platform()
    conf.cxx_load_tools()
    conf.cxx_add_flags()

    # Also set up C tools and flags
    conf.gcc_common_flags()
    if not conf.is_mkspec_platform('android'):
        conf.gcc_modifier_platform()
    conf.cc_load_tools()
    conf.cc_add_flags()

    # Add linker flags
    conf.link_add_flags()

    # Add our own cxx flags
    conf.mkspec_set_gxx_cxxflags()
    # Add our own cc flags
    conf.mkspec_set_gcc_ccflags()


@conf
def mkspec_gxx_android_configure(conf, major, minor, prefix):
    conf.set_mkspec_platform('android')
    conf.mkspec_gxx_configure(major, minor, prefix)
    conf.mkspec_set_android_options()

@conf
def mkspec_set_gcc_ccflags(conf):

    conf.env['CCFLAGS'] += ['-O2','-ftree-vectorize',
                             '-Wextra','-Wall']

    if conf.has_tool_option('cxx_debug'):
        conf.env['CCFLAGS'] += ['-g']

@conf
def mkspec_set_gxx_cxxflags(conf):

    conf.env['CXXFLAGS'] += ['-O2','-ftree-vectorize',
                             '-Wextra','-Wall']

    if conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']
    else:
        conf.env['LINKFLAGS'] += ['-s']

    # Use the more restrictive c++0x option for linux
    if conf.is_mkspec_platform('linux'):
        conf.env['CXXFLAGS'] += ['-std=c++0x']
    else:
        # Other platforms might need some non-standard functions
        # therefore we use gnu++0x
        # For Android see: http://stackoverflow.com/questions/9247151
        # For MinGW: http://stackoverflow.com/questions/6312151
        conf.env['CXXFLAGS'] += ['-std=gnu++0x']

    # To enable the latest standard on g++ 4.7
    #conf.env['CXXFLAGS'] += ['-std=c++11']

@conf
def mkspec_get_gnu_binary_name(conf, base, major, minor, prefix = None):
    """
    :param base:  'gcc' or 'g++'
    :param major: The major version number of the g++/gcc binary e.g. 4
    :param minor: The minor version number of the g++/gcc binary e.g. 6
    :return: A list with names of the g++ binary we are looking for
             e.g. ['g++-4.6', 'g++-mp-4.6'] for g++ version 4.6 on
             mac/darwin
    """

    # First the default case
    binary = ['{0}-{1}.{2}'.format(base, major, minor)]

    if prefix != None:
        # Toolchains use a specific prefix
        return ['{0}-{1}'.format(prefix, base)]

    if conf.is_mkspec_platform('mac'):

        # If the compiler is installed using macports
        return binary + ['{0}-mp-{1}.{2}'.format(base, major, minor)]

    if conf.is_mkspec_platform('windows'):

        # On Windows, all binaries are named the same
        # for all g++ versions
        return [base]

    return binary




