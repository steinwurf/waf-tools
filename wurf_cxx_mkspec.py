#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib.Configure import conf

import cxx_mkspecs.cxx_default
import cxx_mkspecs.clang_mkspecs
import cxx_mkspecs.gxx_mkspecs
import cxx_mkspecs.msvc_mkspecs
import cxx_mkspecs.emscripten_mkspecs

# Allows us to catch queries for platforms that we do not yet support
mkspec_platforms = ['windows', 'linux', 'android', 'mac', 'ios', 'emscripten']


@conf
def get_mkspec_platform(conf):
    # If the MKSPEC_PLATFORM is not set, we auto detect it.
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
        conf.fatal("The mkspec platform could not be set to {0}, as it was "
                   "already set to {1}.".format(
                       platform, conf.env['MKSPEC_PLATFORM']))

    if platform not in mkspec_platforms:
        conf.fatal("The mkspec platform {0} is not supported."
                   " Current platform is {1}".format(
                       platform, conf.env['MKSPEC_PLATFORM']))

    conf.env['MKSPEC_PLATFORM'] = platform


@conf
def is_mkspec_platform(conf, platform):
    return conf.get_mkspec_platform() == platform


def configure(conf):
    # Which mkspec should we use, by default, use the cxx_default
    # that simply fallbacks to use waf auto detect of compiler etc.
    mkspec = "cxx_default"

    if conf.has_tool_option('cxx_mkspec'):
        mkspec = conf.get_tool_option('cxx_mkspec')

    conf.msg('Using the mkspec:', mkspec)

    # Find and call the mkspec function on the conf object
    if hasattr(conf, mkspec):
        getattr(conf, mkspec)()
    else:
        conf.fatal("The mkspec is not available: {0}".format(mkspec))

    # Additional flags for C/C++ compiler and linker
    if conf.has_tool_option('cflags'):
        conf.env['CFLAGS'] += conf.get_tool_option('cflags').split(';')
    if conf.has_tool_option('cxxflags'):
        conf.env['CXXFLAGS'] += conf.get_tool_option('cxxflags').split(';')
    if conf.has_tool_option('linkflags'):
        conf.env['LINKFLAGS'] += conf.get_tool_option('linkflags').split(';')

    # Common flags to be set for C/C++ compiler and linker
    if conf.has_tool_option('commonflags'):
        conf.env['CFLAGS'] += conf.get_tool_option('commonflags').split(';')
        conf.env['CXXFLAGS'] += conf.get_tool_option('commonflags').split(';')
        conf.env['LINKFLAGS'] += conf.get_tool_option('commonflags').split(';')
