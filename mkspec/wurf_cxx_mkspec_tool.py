#!/usr/bin/env python
# encoding: utf-8

import os, sys, inspect, ast

from waflib import Utils
from waflib import Context
from waflib import Options
from waflib import Errors

from waflib.Configure import conf
from waflib.Configure import ConfigurationContext

###############################
# ToolchainConfigurationContext
###############################

class ToolchainConfigurationContext(ConfigurationContext):
    '''configures the project'''
    cmd='configure'

    def init_dirs(self):
        # Waf calls this function to set the output directory.
        # Waf sets the output dir in the following order
        # 1) Check whether the -o option has been specified
        # 2) Check whether the wscript has an out varialble defined
        # 3) Fallback and use the name of the lock-file
        #
        # In order to not suprise anybody we will disallow the out variable
        # but allow our output dir to be overwritten by using the -o option

        assert(getattr(Context.g_module,Context.OUT,None) == None)

        if not Options.options.out:
            if Options.options.cxx_mkspec:
                self.out_dir = "build/"+Options.options.cxx_mkspec
            else:
                build_platform = Utils.unversioned_sys_platform()
                self.out_dir = "build/" + build_platform

        super(ToolchainConfigurationContext, self).init_dirs()


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
                   " supported is %s") % (platform, mkspec_platform))

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
    conf.load_external_tool('mkspec', mkspec)



