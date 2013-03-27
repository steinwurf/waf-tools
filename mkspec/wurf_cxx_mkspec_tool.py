#!/usr/bin/env python
# encoding: utf-8

import os, sys, inspect, ast

from waflib import Utils
from waflib import Context
from waflib import Options
from waflib import Errors

from waflib.Configure import conf

import mkspec_common

## Moved to mkspec_common.py
# # Allows us to catch queries for platforms that we do not yet support

# mkspec_platforms = ['windows','linux', 'android', 'mac']

# # If we ever need to do special things on specific platforms:
# """
# mkspec_platform_specializations = { 'windows' : ['windows xp',
#                                                  'windows vista',
#                                                  'windows 7',
#                                                  'windows 8'],
#                                     'linux'   : ['ubuntu 12.04',
#                                                  'debian wheezy'],
#                                     'android' : ['android 2.3',
#                                                  'android 4.1'],
#                                     'mac'     : ['mac 10.8']
#                                    }
# """

## Moved to mkspec_common.py
# @conf
# def get_mkspec_platform(conf):
#     #If the MKSPEC_PLATFORM is not set, we auto detect it.
#     if not conf.env['MKSPEC_PLATFORM']:
#         platform = Utils.unversioned_sys_platform()
#         if platform == 'win32':
#             platform = 'windows'
#         elif platform == 'darwin':
#             platform = 'mac'
#         conf.set_mkspec_platform(platform)

#     return conf.env['MKSPEC_PLATFORM']

## Moved to mkspec_common.py
# @conf
# def set_mkspec_platform(conf, platform):
#     if conf.env['MKSPEC_PLATFORM']:
#         conf.fatal(("The mkspec platform could not be set to %s, as it was "
#                    "already set to %s.") %
#                    (platform, conf.env['MKSPEC_PLATFORM']))

#     if not platform in mkspec_platforms:
#         conf.fatal(("The mkspec platform %s is not supported"
#                    " supported is %s") % (platform, conf.env['MKSPEC_PLATFORM']))

#     conf.env['MKSPEC_PLATFORM'] = platform

## Moved to mkspec_common.py
# @conf
# def is_mkspec_platform(conf, platform):
#     return conf.get_mkspec_platform() == platform

def configure(conf):
    # Which mkspec should we use, by default, use the cxx_default
    # that simply fallbacks to use waf auto detect of compiler etc.
    mkspec = "cxx_default"

    if conf.has_tool_option('cxx_mkspec'):
        mkspec = conf.get_tool_option('cxx_mkspec')

    conf.msg('Using the mkspec:', mkspec)
    conf.load_external_tool('mkspec', mkspec)
