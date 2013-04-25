#!/usr/bin/env python
# encoding: utf-8

import os

from waflib import Utils
from waflib.Configure import conf
import waflib.Tools.gxx as gxx
from os.path import abspath, expanduser

import cxx_common

@conf
def mkspec_clang_configure(conf, major, minor):

    # Where to look
    paths = conf.mkspec_get_toolchain_paths()

    # Find the compiler
    clang_names = conf.mkspec_get_clang_binary_name(major, minor)

    cxx = conf.find_program(clang_names, path_list = paths, var = 'CXX')
    cxx = conf.cmd_to_list(cxx)
    conf.env.CXX = cxx
    conf.env.CXX_NAME = os.path.basename(conf.env.get_flat('CXX'))

    # waf's gxx tool for checking version number also works for clang
    # so we just use it
    conf.mkspec_check_cc_version(conf.env['CXX'], major, minor)

    # Find the archiver
    ar = conf.mkspec_get_ar_binary_name()
    conf.find_program(ar, path_list = paths, var = 'AR')
    conf.env.ARFLAGS = 'rcs'

    conf.gxx_common_flags()
    conf.gxx_modifier_platform()
    conf.cxx_load_tools()
    conf.cxx_add_flags()
    conf.link_add_flags()

    # Add our own cxx flags
    conf.mkspec_set_clang_cxxflags()

@conf
def mkspec_clang_android_configure(conf, major, minor):
    conf.set_mkspec_platform('android')
    conf.mkspec_clang_configure(major,minor)
    conf.mkspec_set_android_options()


@conf
def mkspec_set_clang_cxxflags(conf):

    conf.env['CXXFLAGS'] += ['-O2', '-Wextra','-Wall']

    if conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']

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

    # Use clang's own C++ standard library on mac osx only
    # Add other platforms when the library becomes stable there
    if conf.is_mkspec_platform('mac'):
        conf.env['CXXFLAGS'] += ['-stdlib=libc++']
        conf.env['LINKFLAGS'] += ['-lc++']

@conf
def mkspec_get_clang_binary_name(conf, major, minor):
    """
    :param major: The major version number of the clang binary e.g. 3
    :param minor: The minor version number of the clang binary e.g. 1
    :return: A list with names of the g++ binary we are looking for
             e.g. ['clang31++'] for clang++ version 3.1 on
             android
    """

    return ['clang{0}{1}++'.format(major, minor), 'clang++']

@conf
def mkspec_check_clang_version(conf, major, minor):
    """
    :param major: The major version number of the clang++ binary e.g. 4
    :param minor: The minor version number of the clang++ binary e.g. 6
    """
    conf.get_cc_version(conf.env['CXX'], gcc = True)

    if (int(conf.env['CC_VERSION'][0]) != int(major) or
        int(conf.env['CC_VERSION'][1]) != int(minor)):
        conf.fatal("Wrong version number: {0}, "
                   "expected major={1} and minor={2}."
                   .format(conf.env['CC_VERSION'], major, minor))

