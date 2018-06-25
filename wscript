#!/usr/bin/env python
# encoding: utf-8

import os

import wurf_cxx_mkspec
import wurf_configure_output
import wurf_runner
import wurf_install_path
import wurf_project_generator
import wurf_android_soname
import wurf_copy_binary
import wurf_limit_includes

from waflib import Options
from waflib.Configure import conf


@conf
def load_external_waf_tool(ctx, name):
    """
    Load an additional external tool from the top-level wscript of a project.

    :param ctx: the resolve, build or configuration context
    """
    import inspect
    this_file = inspect.getfile(inspect.currentframe())
    path = os.path.join(os.path.dirname(this_file))
    ctx.load([name], tooldir=[path])


@conf
def get_tool_option(conf, option):
    # Options can be specified in 2 ways:
    # 1) Passed with the currently executed command
    # 2) Stored during the configure step
    current = Options.options.__dict__
    stored = conf.env.stored_options

    if option in current and current[option] != None:
        return current[option]
    elif option in stored and stored[option] != None:
        return stored[option]
    else:
        conf.fatal('Missing option: %s' % option)


@conf
def has_tool_option(conf, option):
    current = Options.options.__dict__
    stored = conf.env.stored_options

    if option in current and current[option] != None:
        return True
    elif option in stored and stored[option] != None:
        return True
    else:
        return False


def options(opt):

    opt.load('wurf_install_path')
    opt.load('wurf_cxx_mkspec')
    opt.load('wurf_runner')


def configure(conf):

    # Store the options that are specified during the configure step
    conf.env["stored_options"] = Options.options.__dict__.copy()

    if not conf.env['DISABLE_WURF_CXX_MKSPEC']:
        conf.load('wurf_cxx_mkspec')

    conf.load('wurf_runner')
    conf.load('wurf_install_path')
    conf.load('wurf_project_generator')
