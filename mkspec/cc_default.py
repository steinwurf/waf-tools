#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib.Configure import conf
from waflib.Tools.compiler_c import c_compiler
import waflib.Tools.gcc as gcc
from os.path import abspath, expanduser
import os
"""
Detect and setup the default compiler for the platform
"""
def configure(conf):

    # Here we simply try to find a compiler on the current host
    # this code is mostly taken from the "compiler_cxx" tool
    build_platform = Utils.unversioned_sys_platform()
    platform = build_platform if build_platform in c_compiler else 'default'
    possible_compiler_list = c_compiler[platform]

    for compiler in possible_compiler_list:
        conf.env.stash()
        conf.start_msg('Checking for %r (c compiler)' % compiler)
        try:
            conf.load(compiler)
        except conf.errors.ConfigurationError as e:
            conf.env.revert()
            conf.end_msg(False)
            debug('compiler_c: %r' % e)
        else:
            if conf.env['CC']:
                conf.end_msg(conf.env.get_flat('CC'))
                conf.env['COMPILER_C'] = compiler
                break
            conf.end_msg(False)
    else:
        conf.fatal('could not configure a c compiler!')

    CC = conf.env.get_flat('CC')

    # Note clang goes first otherwise 'gcc' will be in 'clang(gcc)'
    if 'clang' in CC:
        conf.mkspec_set_clang_ccflags()
    elif 'gcc' in CC:
        conf.mkspec_set_gcc_ccflags()
    elif 'CL.exe' in CC or 'cl.exe' in CC:
        conf.add_msvc_default_ccflags()
    else:
        raise Errors.WafError('toolchain_c flag for unknown compiler %s'
                              % conf.env.CC)

# @conf
# def get_mkspec_option(conf, option, required=True, error_msg = None):
#     try:
#         option = conf.env["cxx_mkspec_options"][option]
#     except Exception, e:
#         if required:
#             if error_msg:
#                 conf.fatal(error_msg)
#             else:
#                 conf.fatal("Missing mkspec-option %s."%e)
#         option = None
#     return option

@conf
def mkspec_get_toolchain_paths(conf):
    """
    :return: the common paths where we may find the gcc binary
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
def mkspec_get_gcc_binary_name(conf, major, minor):
    """
    :param major: The major version number of the gcc binary e.g. 4
    :param minor: The minor version number of the gcc binary e.g. 6
    :return: A list with names of the gcc binary we are looking for
             e.g. ['gcc-4.6', 'gcc-mp-4.6'] for gcc version 4.6 on
             mac/darwin
    """

    # First the default case
    binary = ['gcc-{0}.{1}'.format(major, minor)]

    if conf.is_mkspec_platform('mac'):

        # If the compiler is installed using macports
        return binary + ['gcc-mp-{0}.{1}'.format(major, minor)]

    if conf.is_mkspec_platform('android'):

        # Here all binaries are named the same for all NDK standalone
        # toolchains that we are aware of
        return ['arm-linux-androideabi-gcc']

    return binary


@conf
def mkspec_check_gcc_version(conf, major, minor):
    """
    :param major: The major version number of the gcc binary e.g. 4
    :param minor: The minor version number of the gcc binary e.g. 6
    """
    conf.get_cc_version(conf.env['CC'], gcc = True)

    if (int(conf.env['CC_VERSION'][0]) != int(major) or
        int(conf.env['CC_VERSION'][1]) != int(minor)):
        conf.fatal("Wrong version number, wanted version={0}, "
                   "but got major={1} and minor={2}."
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


@conf
def mkspec_gcc_configure(conf, major, minor):

    # Where to look
    paths = conf.mkspec_get_toolchain_paths()

    # Find the compiler
    gcc_names = conf.mkspec_get_gcc_binary_name(major, minor)

    # ccc = conf.find_program(gxx_names, path_list = paths, var = 'CXX')
    # cxx = conf.cmd_to_list(cxx)

    # Not sure if below 2 lines are correctly modified.
    # Above 2 lines are original cxx code
    ccc = conf.find_program(gcc_names, path_list = paths, var = 'CC')
    cc = conf.cmd_to_list(ccc)

    conf.env.CC = cc
    conf.env.CC_NAME = os.path.basename(conf.env.get_flat('CC'))

    conf.mkspec_check_gcc_version(major, minor)

    # Find the archiver
    ar = conf.mkspec_get_ar_binary_name()

    conf.find_program(ar, path_list = paths, var = 'AR')
    conf.env.ARFLAGS = 'rcs'

    conf.gcc_common_flags()
    conf.gcc_modifier_platform()
    conf.cc_load_tools()
    conf.cc_add_flags()
    conf.link_add_flags()

    # Add our own cxx flags
    conf.mkspec_set_gcc_ccflags()



@conf
def mkspec_set_gcc_ccflags(conf):

    conf.env['CCFLAGS'] += ['-O2','-g','-ftree-vectorize',
                             '-Wextra','-Wall']

    # Below does not seem necessary
    # if conf.is_mkspec_platform('android'):
        # http://stackoverflow.com/questions/9247151
        # conf.env['CCFLAGS'] += ['-std=gnu++0x']
    # else:
        # conf.env['CCFLAGS'] += ['-std=c++0x']

@conf
def gcc_check_version(conf, version):
    """
    :param version : The version number as a tuple.
    """
    conf.get_cc_version([conf.env['CC']], gcc=True)

    if conf.env['CC_VERSION'] != version:
        conf.fatal("Wrong version number, wanted '%r', but got '%r'."
                   % (version, conf.env['CC_VERSION']))

@conf
def mkspec_get_clang_binary_name(conf, major, minor):
    """
    :param major: The major version number of the clang binary e.g. 3
    :param minor: The minor version number of the clang binary e.g. 1
    :return: A list with names of the gcc binary we are looking for
             e.g. ['clang31'] for clang version 4.6 on
             android
    """

    return ['clang{0}{1}'.format(major, minor), 'clang']



@conf
def mkspec_clang_configure(conf, major, minor):

    # Where to look
    paths = conf.mkspec_get_toolchain_paths()

    # Find the compiler
    clang_names = conf.mkspec_get_clang_binary_name(major, minor)

    cc = conf.find_program(clang_names, path_list = paths, var = 'CC')
    cxx = conf.cmd_to_list(cc)
    conf.env.CC = cc
    conf.env.CC_NAME = os.path.basename(conf.env.get_flat('CC'))

    # waf's gxx tool for checking version number also works for clang
    # so we just use it
    conf.mkspec_check_gcc_version(major, minor)

    # Find the archiver
    ar = conf.mkspec_get_ar_binary_name()

    conf.find_program(ar, path_list = paths, var = 'AR')
    conf.env.ARFLAGS = 'rcs'

    conf.gcc_common_flags()
    conf.gcc_modifier_platform()
    conf.cc_load_tools()
    conf.cc_add_flags()
    conf.link_add_flags()

    # Add our own cxx flags
    conf.mkspec_set_clang_ccflags()


@conf
def mkspec_set_clang_ccflags(conf):
    conf.env['CCFLAGS'] += ['-O2', '-g', '-Wextra', '-Wall']


@conf
def mkspec_clang_android_configure(conf, major, minor):
    conf.set_mkspec_platform('android')
    conf.mkspec_clang_configure(major,minor)
    conf.mkspec_set_android_common()


@conf
def mkspec_gcc_android_configure(conf, major, minor):
    ### This should be fixed:
    if not conf.get_mkspec_platform() == 'android':
        conf.set_mkspec_platform('android')
    conf.mkspec_gcc_configure(major,minor)
    conf.mkspec_set_android_common()

@conf
def mkspec_set_android_common(conf):
    sdk = conf.get_tool_option('android_sdk_dir')
    sdk = abspath(expanduser(sdk))
    sdk_path = [sdk, os.path.join(sdk,'platform-tools')]

    conf.find_program('adb', path_list = sdk_path, var='ADB')

    # Set the android define - some libraries rely on this define being present
    conf.env.DEFINES += ['ANDROID']


@conf
def add_msvc_default_ccflags(conf):
    conf.env['CCFLAGS'] += ['/O2', '/Ob2', '/W3', '/MT', '/EHs']
