#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib.Configure import conf
#import waflib.Tools.gxx as gxx
from os.path import abspath, expanduser
import os


@conf
def mkspec_check_cc_version(conf, compiler, major, minor):
    """
    :param major: The major version number of the g++ binary e.g. 4
    :param minor: The minor version number of the g++ binary e.g. 6
    """
    conf.get_cc_version(compiler, gcc = True)

    if (int(conf.env['CC_VERSION'][0]) != int(major) or
        int(conf.env['CC_VERSION'][1]) != int(minor)):
        conf.fatal("Wrong version number: {0}, "
                   "expected major={1} and minor={2}."
                   .format(conf.env['CC_VERSION'], major, minor))

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

    if conf.is_mkspec_platform('ios'):
        if conf.has_tool_option('ios_toolchain_dir'):
            toolchain = conf.get_tool_option('ios_toolchain_dir')
        else:
            toolchain = "/Applications/Xcode.app/Contents/Developer/" \
                        "Toolchains/XcodeDefault.xctoolchain/usr/bin/"
        toolchain = abspath(expanduser(toolchain))
        #toolchain_path = [toolchain, os.path.join(toolchain,'bin')]

        return toolchain

    return path_list

@conf
def mkspec_set_android_options(conf):
    sdk = conf.get_tool_option('android_sdk_dir')
    sdk = abspath(expanduser(sdk))
    sdk_path = [sdk, os.path.join(sdk,'platform-tools')]

    conf.find_program('adb', path_list = sdk_path, var='ADB')

    # Set the android define - some libraries rely on this define being present
    conf.env.DEFINES += ['ANDROID']

    # Add common libraries for Android here
    conf.env['LINKFLAGS'] += ['-llog']
    # No need to specify 'gnustl_static' or 'gnustl_shared'
    # The Android toolchain will select the appropriate standard library
    #conf.env.LIB_ANDROID = ['gnustl_static']


@conf
def mkspec_set_ios_options(conf, min_ios_version, cpu):
    sdk = conf.get_tool_option('ios_sdk_dir')
    sdk = abspath(expanduser(sdk))

    # Define what are the necessary common compiler and linker options to build
    # for the iOS platform. Here, tell the ARM cross-compiler to target the
    # specified arm-apple-ios platform triplet, specify the location of the iOS SDK,
    # use the compiler's integrated assembler and set the minimal supported iOS version
    
    triple = "{}-apple-ios{}.0".format(cpu, min_ios_version)

    conf.env['CXXFLAGS'] += [ "-ccc-host-triple", triple, "-integrated-as", "-isysroot", sdk,
                              "-miphoneos-version-min={}".format(min_ios_version) ]

    # Set the IPHONE define - some libraries rely on this define being present
    conf.env.DEFINES += ['IPHONE']

    # Add common libraries for iOS here
    conf.env['LINKFLAGS'] += ['-lSystem'] # links with libSystem.dylib



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

