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
def mkspec_clang_configure(conf, major, minor, prefix = None, minimum = False,
                           force_debug = False):
    """
    :param major:       The major version number of the compiler, e.g. 3
    :param minor:       The minor version number of the compiler, e.g. 4
    :param prefix:      Prefix to compiler name, e.g. 'arm-linux-androideabi'
    :param minimum:     Only check for a minimum compiler version, if true
    :param force_debug: Always compile with debugging flags, if true
    """
    # Where to look
    paths = conf.mkspec_get_toolchain_paths()

    # Find the clang++ compiler
    clangxx_names = conf.mkspec_get_clangxx_binary_name(major, minor)
    if minimum:
        clangxx_names = 'clang++'
    cxx = conf.find_program(clangxx_names, path_list = paths)
    cxx = conf.cmd_to_list(cxx)
    conf.env['CXX'] = cxx
    conf.env['CXX_NAME'] = os.path.basename(conf.env.get_flat('CXX'))
    # waf's gxx tool for checking version number might also work for clang
    # TODO: write a proper tool for this
    if minimum:
        conf.mkspec_check_minimum_cc_version(cxx, major, minor)
    else:
        conf.mkspec_check_cc_version(cxx, major, minor)

    # Find clang as the C compiler
    clang_names = conf.mkspec_get_clang_binary_name(major, minor)
    if minimum:
        clang_names = 'clang'
    cc = conf.find_program(clang_names, path_list = paths)
    cc = conf.cmd_to_list(cc)
    conf.env['CC'] = cc
    conf.env['CC_NAME'] = os.path.basename(conf.env.get_flat('CC'))
    # TODO: write a proper tool for this
    if minimum:
        conf.mkspec_check_minimum_cc_version(cc, major, minor)
    else:
        conf.mkspec_check_cc_version(cc, major, minor)

    # Find the archiver
    ar = conf.mkspec_get_ar_binary_name(prefix)
    conf.find_program(ar, path_list = paths, var = 'AR')
    conf.env.ARFLAGS = 'rcs'

    # Set up C++ tools and flags
    conf.gxx_common_flags()
    conf.gxx_modifier_platform()
    conf.cxx_load_tools()
    conf.cxx_add_flags()

    # Also set up C tools and flags
    conf.gcc_common_flags()
    conf.gcc_modifier_platform()
    conf.cc_load_tools()
    conf.cc_add_flags()

    # Add linker flags
    conf.link_add_flags()

    # Add our own cxx flags
    conf.mkspec_set_clang_cxxflags(force_debug)
    # Add our own cc flags
    conf.mkspec_set_clang_ccflags(force_debug)

@conf
def mkspec_clang_android_configure(conf, major, minor, prefix, target):
    conf.set_mkspec_platform('android')
    conf.mkspec_clang_configure(major, minor)
    conf.mkspec_set_android_options()

    # Specify the target architecture as required by clang
    target_flags = ['-target', target]
    conf.env['CFLAGS'] += target_flags
    conf.env['CXXFLAGS'] += target_flags
    conf.env['LINKFLAGS'] += target_flags

@conf
def mkspec_clang_ios_configure(conf, major, minor, min_ios_version, cpu):
    conf.set_mkspec_platform('ios')
    conf.mkspec_clang_configure(major, minor)
    conf.mkspec_set_ios_options(min_ios_version, cpu)

@conf
def mkspec_set_clang_ccflags(conf, force_debug = False):

    optflag = '-O2'
    # Use -Os (optimize for size) flag on iOS, because -O2 produces unstable
    # code on this platform
    if conf.get_mkspec_platform() == 'ios': optflag = '-Os'
    conf.env['CFLAGS'] += [optflag, '-Wextra', '-Wall']

    if conf.has_tool_option('cxx_debug') or force_debug:
        conf.env['CFLAGS'] += ['-g']

    if conf.has_tool_option('cxx_nodebug'):
        conf.env['DEFINES'] += ['NDEBUG']

@conf
def mkspec_set_clang_cxxflags(conf, force_debug = False):

    optflag = '-O2'
    # Use -Os (optimize for size) flag on iOS, because -O2 produces unstable
    # code on this platform
    if conf.get_mkspec_platform() == 'ios': optflag = '-Os'
    conf.env['CXXFLAGS'] += [optflag, '-Wextra', '-Wall']

    if conf.has_tool_option('cxx_debug') or force_debug:
        conf.env['CXXFLAGS'] += ['-g']
    elif not conf.get_mkspec_platform() in ['mac', 'ios']:
        conf.env['LINKFLAGS'] += ['-s']

    if conf.has_tool_option('cxx_nodebug'):
        conf.env['DEFINES'] += ['NDEBUG']

    # Use the more restrictive c++0x option for linux
    if conf.is_mkspec_platform('linux'):
        conf.env['CXXFLAGS'] += ['-std=c++0x']
    else:
        # Other platforms might need some non-standard functions
        # therefore we use gnu++0x
        # For Android see: http://stackoverflow.com/questions/9247151
        # For MinGW: http://stackoverflow.com/questions/6312151
        conf.env['CXXFLAGS'] += ['-std=gnu++0x']

    # To enable the latest standard on Mac OSX
    #conf.env['CXXFLAGS'] += ['-std=gnu++11']

    # Use clang's own C++ standard library on Mac OSX and iOS
    # Add other platforms when the library becomes stable there
    if conf.get_mkspec_platform() in ['mac', 'ios']:
        conf.env['CXXFLAGS'] += ['-stdlib=libc++']
        conf.env['LINKFLAGS'] += ['-lc++']

@conf
def mkspec_get_clangxx_binary_name(conf, major, minor):
    """
    :param major:  The major version number of the clang binary e.g. 3
    :param minor:  The minor version number of the clang binary e.g. 4
    :return:       A list with names of the clang++ binary we are looking for,
                   e.g. ['clang34++'] for clang++ 3.4 on Android
    """

    if conf.is_mkspec_platform('android'):
        # The numbered clang is the only real binary in the Android toolchain
        return ['clang{0}{1}++'.format(major, minor)]

    # The default case works fine on all other platforms
    return ['clang++']

@conf
def mkspec_get_clang_binary_name(conf, major, minor):
    """
    :param major:  The major version number of the clang binary e.g. 3
    :param minor:  The minor version number of the clang binary e.g. 4
    :return:       A list with names of the clang binary we are looking for,
                   e.g. ['clang34'] for clang 3.4 on Android
    """

    if conf.is_mkspec_platform('android'):
        # The numbered clang is the only real binary in the Android toolchain
        return ['clang{0}{1}'.format(major, minor)]

    # The default case works fine on all other platforms
    return ['clang']
