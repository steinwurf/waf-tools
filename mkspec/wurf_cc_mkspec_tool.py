#!/usr/bin/env python
# encoding: utf-8

import os, sys, inspect, ast

from waflib import Utils
from waflib import Context
from waflib import Options
from waflib import Errors

from waflib.Configure import conf

import mkspec_common

def configure(conf):
    # Which mkspec should we use, by default, use the cxx_default
    # that simply fallbacks to use waf auto detect of compiler etc.
    mkspec = "cc_default"

    if conf.has_tool_option('cc_mkspec'):
        mkspec = conf.get_tool_option('cc_mkspec')

    conf.msg('Using the mkspec:', mkspec)
    conf.load_external_tool('mkspec', mkspec)
