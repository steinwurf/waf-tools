#!/usr/bin/env python
# encoding: utf-8

import os

from waflib.Configure import conf
import waflib.Utils

from . import cxx_common


@conf
def mkspec_check_clang_version(conf, compiler, major, minor, minimum=False):
    """
    Check the exact or minimum clang version.

    :param major: The major version number, e.g. 3
    :param minor: The minor version number, e.g. 5
    :param minimum: Only check for a minimum compiler version, if true
    """
    conf.get_cc_version(cc=compiler, clang=True)
    conf.mkspec_validate_cc_version(major, minor, minimum)


@conf
def mkspec_clang_configure(conf, major, minor, prefix=None, minimum=False,
                           force_debug=False):
    """
    :param major:       The major version number of the compiler, e.g. 3
    :param minor:       The minor version number of the compiler, e.g. 4
    :param prefix:      Prefix to compiler name, e.g. 'arm-linux-androideabi'
    :param minimum:     Only check for a minimum compiler version, if true
    :param force_debug: Always compile with debugging flags, if true
    """
    # Where to look
    paths = conf.mkspec_get_toolchain_paths()

    # If the user-defined CXX variable is set, then use that compiler
    if 'CXX' in os.environ:
        cxx = waflib.Utils.to_list(os.environ['CXX'])
        conf.to_log('Using user defined environment variable CXX=%r' % cxx)
    else:
        # Find the clang++ compiler
        clangxx_names = conf.mkspec_get_clangxx_binary_name(major, minor)
        if minimum:
            clangxx_names = 'clang++'
        cxx = conf.find_program(clangxx_names, path_list=paths)
        cxx = conf.cmd_to_list(cxx)

    conf.env['CXX'] = cxx
    conf.env['CXX_NAME'] = os.path.basename(conf.env.get_flat('CXX'))

    conf.mkspec_check_clang_version(cxx, major, minor, minimum)

    # If the user-defined CC variable is set, then use that compiler
    if 'CC' in os.environ:
        cc = waflib.Utils.to_list(os.environ['CC'])
        conf.to_log('Using user defined environment variable CC=%r' % cc)
    else:
        # Find clang as the C compiler
        clang_names = conf.mkspec_get_clang_binary_name(major, minor)
        if minimum:
            clang_names = 'clang'
        cc = conf.find_program(clang_names, path_list=paths)
        cc = conf.cmd_to_list(cc)

    conf.env['CC'] = cc
    conf.env['CC_NAME'] = os.path.basename(conf.env.get_flat('CC'))

    conf.mkspec_check_clang_version(cc, major, minor, minimum)

    # Find the archiver
    ar = conf.mkspec_get_ar_binary_name(prefix)
    conf.find_program(ar, path_list=paths, var='AR')
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
    conf.mkspec_clang_configure(major, minor, prefix)
    conf.mkspec_set_android_options()

    # Specify the target architecture as required by clang
    target_flags = ['-target', target]
    conf.env['CFLAGS'] += target_flags
    conf.env['CXXFLAGS'] += target_flags
    conf.env['LINKFLAGS'] += target_flags


@conf
def mkspec_clang_ios_configure(conf, major, minor, min_ios_version, cpu,
                               minimum=False):
    conf.set_mkspec_platform('ios')
    conf.mkspec_clang_configure(major, minor, minimum=minimum)
    conf.mkspec_set_ios_options(min_ios_version, cpu)


@conf
def mkspec_set_clang_ccflags(conf, force_debug=False):

    optflag = '-O2'

    # Use -Os (optimize for size) flag on iOS, because -O2 produces unstable
    # code on this platform
    if conf.get_mkspec_platform() in ['ios']:
        optflag = '-Os'

    if not conf.env['MKSPEC_DISABLE_OPTIMIZATION']:
        conf.env['CFLAGS'] += [optflag]

    # Warning flags
    conf.env['CFLAGS'] += [optflag, '-Wextra', '-Wall']

    if conf.has_tool_option('cxx_debug') or force_debug:
        conf.env['CFLAGS'] += ['-g']

    if conf.has_tool_option('cxx_nodebug'):
        conf.env['DEFINES'] += ['NDEBUG']


@conf
def mkspec_set_clang_cxxflags(conf, force_debug=False):

    optflag = '-O2'

    # Use -Os (optimize for size) flag on iOS, because -O2 produces unstable
    # code on this platform
    if conf.get_mkspec_platform() in ['ios']:
        optflag = '-Os'

    if not conf.env['MKSPEC_DISABLE_OPTIMIZATION']:
        conf.env['CXXFLAGS'] += [optflag]

    # Warning flags
    conf.env['CXXFLAGS'] += ['-pedantic', '-Wextra', '-Wall']

    if conf.has_tool_option('cxx_debug') or force_debug:
        conf.env['CXXFLAGS'] += ['-g']
    elif not conf.get_mkspec_platform() in ['mac', 'ios']:
        conf.env['LINKFLAGS'] += ['-s']

    if conf.has_tool_option('cxx_nodebug'):
        conf.env['DEFINES'] += ['NDEBUG']

    if conf.is_mkspec_platform('linux'):
        # Use the more restrictive c++11 option for linux
        conf.env['CXXFLAGS'] += ['-std=c++11']
        # clang is currently incompatible with the Dual ABI of libstdc++ that
        # was introduced by g++ 5.1. Every library that uses libstdc++ should
        # be compiled with -D_GLIBCXX_USE_CXX11_ABI=0 until the clang
        # developers add support for the new ABI.
        # This also means that we cannot link to other system libraries (which
        # are compiled without this flag).
        # Further explanation and relevant bug reports:
        # http://allanmcrae.com/2015/06/the-case-of-gcc-5-1-and-the-two-c-abis/
        # https://llvm.org/bugs/show_bug.cgi?id=23529
        # https://bugs.launchpad.net/ubuntu/+source/llvm-toolchain-3.6/+bug/1488254
        conf.env['DEFINES'] += ['_GLIBCXX_USE_CXX11_ABI=0']
    else:
        # Other platforms might need some non-standard functions,
        # therefore we use gnu++11
        # For Android see: http://stackoverflow.com/questions/9247151
        # For MinGW: http://stackoverflow.com/questions/6312151
        conf.env['CXXFLAGS'] += ['-std=gnu++11']

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

    # The default name works fine on most other platforms
    clangxx_binary_names = ['clang++']

    if conf.is_mkspec_platform('linux'):
        # Make sure the more specific binary name is first in the list
        # e.g. ["clang-3.6", "clang"] instead of ["clang", "clang-3.6"].
        #
        # The reason is that waf's find_program code will search for the
        # binary name from the beginning of the list so if your default
        # clang is e.g. 3.8 and you try to configure with a mkspec that
        # wants 3.6 you will find the default clang first and then we will
        # fail because it does not have the required version.
        clangxx_binary_names.insert(0,'clang++-{0}.{1}'.format(major, minor))

    return clangxx_binary_names


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

    # The default name works fine on most other platforms
    clang_binary_names = ['clang']

    if conf.is_mkspec_platform('linux'):
        # See note on the binary name order in the clangxx version of this
        # function.
        clang_binary_names.insert(0, 'clang-{0}.{1}'.format(major, minor))

    return clang_binary_names
