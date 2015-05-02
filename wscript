#!/usr/bin/env python
# encoding: utf-8

import os

from waflib.Configure import conf
from waflib.Configure import ConfigurationContext

APPNAME = 'waf-tools'
VERSION = '2.34.0'

@conf
def load_external_waf_tool(ctx, name):
    import inspect
    this_file = inspect.getfile(inspect.currentframe())
    path = os.path.join(os.path.dirname(this_file))
    ctx.load([name], tooldir=[path])


def resolve(ctx):

    ctx.load_external_waf_tool('wurf_cxx_mkspec')
    ctx.load_external_waf_tool('wurf_runner')


def configure(conf):

    conf.load_external_waf_tool('wurf_cxx_mkspec')
    conf.load_external_waf_tool('wurf_runner')
    conf.load_external_waf_tool('wurf_install_path')
    conf.load_external_waf_tool('wurf_project_generator')


# Required for automatic recursion
def build(bld):
    pass
