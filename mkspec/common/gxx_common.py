#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib.Configure import conf
import waflib.Tools.gxx as gxx
from os.path import abspath, expanduser
import os

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

    conf.mkspec_check_gxx_version(major, minor)

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
def mkspec_get_toolchain_paths(conf):
    """
    :return: the common paths where we may find the g++ binary
    """
    # The default path to search
    path_list = os.environ.get('PATH', '').split(os.pathsep)

    if conf.is_mkspec_platform('mac'):

        # If the compiler is installed using macports
        path_list += ['/opt/local/bin']

    if conf.is_mkspec_platform('android'):
        ndk = conf.get_tool_option('android_ndk_dir')
        ndk = abspath(expanduser(ndk))
        ndk_path = [ndk, os.path.join(ndk,'bin')]

        return ndk_path

    return path_list

@conf
def mkspec_set_android_options(conf):
    sdk = conf.get_tool_option('android_sdk_dir')
    sdk = abspath(expanduser(sdk))
    sdk_path = [sdk, os.path.join(sdk,'platform-tools')]

    conf.find_program('adb', path_list = sdk_path, var='ADB')

    # Set the android define - some libraries rely on this define being present
    conf.env.DEFINES += ['ANDROID']

    # Add common libraries for android
    conf.env.LIB_ANDROID = ['log', 'gnustl_static']

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


@conf
def mkspec_check_gxx_version(conf, major, minor):
    """
    :param major: The major version number of the g++ binary e.g. 4
    :param minor: The minor version number of the g++ binary e.g. 6
    """
    conf.get_cc_version(conf.env['CXX'], gcc = True)

    if (int(conf.env['CC_VERSION'][0]) != int(major) or
        int(conf.env['CC_VERSION'][1]) != int(minor)):
        conf.fatal("Wrong version number: {0}, "
                   "expected major={1} and minor={2}."
                   .format(conf.env['CC_VERSION'], major, minor))


@conf
def mkspec_get_ar_binary_name(conf):
    """
    :return: The name of the ar binary we are looking for
             e.g. 'arm-linux-androideabi-ar' for the archiver on android
    """

    if conf.is_mkspec_platform('android'):
        return 'arm-linux-androideabi-ar'
    else:
        return 'ar'

