#!/usr/bin/env python
# encoding: utf-8

import os
import wurf_cxx_mkspec
import wurf_runner
import wurf_install_path
import wurf_project_generator
import wurf_android_soname

from waflib.Configure import conf


@conf
def load_external_waf_tool(ctx, name):
    """
    This helper function can be used to load an additional external tool
    from the top-level wscript of a project (if that tool is not loaded
    by default for all projects)
    :param ctx: the resolve or configuration context
    """
    import inspect
    this_file = inspect.getfile(inspect.currentframe())
    path = os.path.join(os.path.dirname(this_file))
    ctx.load([name], tooldir=[path])


def resolve(ctx):

    ctx.load('wurf_install_path')
    ctx.load('wurf_cxx_mkspec')
    ctx.load('wurf_runner')


def configure(conf):

    if not conf.env['DISABLE_WURF_CXX_MKSPEC']:
        conf.load('wurf_cxx_mkspec')

    conf.load('wurf_runner')
    conf.load('wurf_install_path')
    conf.load('wurf_project_generator')
    conf.load('wurf_android_soname')


# Required for automatic recursion
def build(bld):
    pass
