#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib import Context
from waflib import Options
from waflib import Errors

from waflib.Configure import conf
from waflib.Tools.compiler_cxx import cxx_compiler
import waflib.Tools.gxx as gxx
from os.path import abspath, expanduser
import os


# Allows us to catch queries for platforms that we do not yet support

mkspec_platforms = ['windows','linux', 'android', 'mac']

# If we ever need to do special things on specific platforms:
"""
mkspec_platform_specializations = { 'windows' : ['windows xp',
                                                 'windows vista',
                                                 'windows 7',
                                                 'windows 8'],
                                    'linux'   : ['ubuntu 12.04',
                                                 'debian wheezy'],
                                    'android' : ['android 2.3',
                                                 'android 4.1'],
                                    'mac'     : ['mac 10.8']
                                   }
"""


@conf
def get_mkspec_platform(conf):
    #If the MKSPEC_PLATFORM is not set, we auto detect it.
    if not conf.env['MKSPEC_PLATFORM']:
        platform = Utils.unversioned_sys_platform()
        if platform == 'win32':
            platform = 'windows'
        elif platform == 'darwin':
            platform = 'mac'
        conf.set_mkspec_platform(platform)

    return conf.env['MKSPEC_PLATFORM']


@conf
def set_mkspec_platform(conf, platform):
    if conf.env['MKSPEC_PLATFORM']:
        conf.fatal(("The mkspec platform could not be set to %s, as it was "
                   "already set to %s.") %
                   (platform, conf.env['MKSPEC_PLATFORM']))

    if not platform in mkspec_platforms:
        conf.fatal(("The mkspec platform %s is not supported"
                   " supported is %s") % (platform, conf.env['MKSPEC_PLATFORM']))

    conf.env['MKSPEC_PLATFORM'] = platform


@conf
def is_mkspec_platform(conf, platform):
    return conf.get_mkspec_platform() == platform


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
def mkspec_set_android_common(conf):
    sdk = conf.get_tool_option('android_sdk_dir')
    sdk = abspath(expanduser(sdk))
    sdk_path = [sdk, os.path.join(sdk,'platform-tools')]

    conf.find_program('adb', path_list = sdk_path, var='ADB')

    # Set the android define - some libraries rely on this define being present
    conf.env.DEFINES += ['ANDROID']

#### UNTESTED!
@conf
def mkspec_set_ios_common(conf):
    sdk = conf.get_tool_option('ios_sdk_dir')
    sdk = abspath(expanduser(sdk))
    sdk_path = [sdk]

    conf.env.DEFINES += ['IOS']
