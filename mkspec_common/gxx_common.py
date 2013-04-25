#!/usr/bin/env python
# encoding: utf-8

import os

from waflib import Utils
from waflib.Configure import conf
import waflib.Tools.gxx as gxx
from os.path import abspath, expanduser

import cxx_common

@conf
def mkspec_gxx_configure(conf, major, minor):

    # Where to look
    paths = conf.mkspec_get_toolchain_paths()

    # Find the compiler
    gxx_names = conf.mkspec_get_gxx_binary_name(major, minor)

    cxx = conf.find_program(gxx_names, path_list = paths, var = 'CXX')
    cxx = conf.cmd_to_list(cxx)
    conf.env.CXX = cxx
    conf.env.CXX_NAME = os.path.basename(conf.env.get_flat('CXX'))

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
    conf.mkspec_set_gxx_cxxflags()


@conf
def mkspec_gxx_android_configure(conf, major, minor):
    conf.set_mkspec_platform('android')
    conf.mkspec_gxx_configure(major,minor)
    conf.mkspec_set_android_options()


@conf
def mkspec_set_gxx_cxxflags(conf):

    conf.env['CXXFLAGS'] += ['-O2','-ftree-vectorize',
                             '-Wextra','-Wall']

    if conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']
    else:
        conf.env['CXXFLAGS'] += ['-s']

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
def mkspec_get_gxx_binary_name(conf, major, minor):
    """
    :param major: The major version number of the g++ binary e.g. 4
    :param minor: The minor version number of the g++ binary e.g. 6
    :return: A list with names of the g++ binary we are looking for
             e.g. ['g++-4.6', 'g++-mp-4.6'] for g++ version 4.6 on
             mac/darwin
    """

    # First the default case
    binary = ['g++-{0}.{1}'.format(major, minor)]

    if conf.is_mkspec_platform('mac'):

        # If the compiler is installed using macports
        return binary + ['g++-mp-{0}.{1}'.format(major, minor)]

    if conf.is_mkspec_platform('android'):

        # Here all binaries are named the same for all NDK standalone
        # toolchains that we are aware of
        return ['arm-linux-androideabi-g++']

    if conf.is_mkspec_platform('windows'):

        # On Windows, all binaries are named the same
        # for all g++ versions
        return ['g++']

    return binary




