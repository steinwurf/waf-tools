#!/usr/bin/env python
# encoding: utf-8

import os

from waflib.Configure import conf

import cxx_common


@conf
def mkspec_emscripten_configure(conf, force_debug=False):
    """
    :param force_debug: Always compile with debugging flags, if true
    """
    # Where to look
    paths = conf.get_tool_option('emscripten_path')

    # Find the clang++ compiler
    cxx = conf.find_program(['em++'], path_list=paths)
    cxx = conf.cmd_to_list(cxx)
    conf.env['CXX'] = cxx
    conf.env['CXX_NAME'] = os.path.basename(conf.env.get_flat('CXX'))

    #conf.mkspec_check_minimum_cc_version(cxx, major, minor)

    # Find clang as the C compiler
    cc = conf.find_program(['emcc'], path_list=paths)
    cc = conf.cmd_to_list(cc)
    conf.env['CC'] = cc
    conf.env['CC_NAME'] = os.path.basename(conf.env.get_flat('CC'))

    #conf.mkspec_check_minimum_cc_version(cc, major, minor)

    # Find the archiver
    conf.find_program('emar', path_list=paths, var='AR')
    conf.env.ARFLAGS = 'rcs'

    # Set up C++ tools and flags
    conf.gxx_common_flags()
    #conf.gxx_modifier_platform()
    conf.cxx_load_tools()
    conf.cxx_add_flags()

    # Also set up C tools and flags
    conf.gcc_common_flags()
    #conf.gcc_modifier_platform()
    conf.cc_load_tools()
    conf.cc_add_flags()

    # Add linker flags
    conf.link_add_flags()

    # Add our own cxx flags
    conf.env['CXXFLAGS'] += ['-O2', '-Wextra', '-Wall']

    if conf.has_tool_option('cxx_debug') or force_debug:
        conf.env['CXXFLAGS'] += ['-g']
        conf.env['LINKFLAGS'] += ['-s']

    if conf.has_tool_option('cxx_nodebug'):
        conf.env['DEFINES'] += ['NDEBUG']

    conf.env['CXXFLAGS'] += ['-std=c++0x']

    # Add our own cc flags
    conf.env['CFLAGS'] += ['-O2', '-Wextra', '-Wall']

    if conf.has_tool_option('cxx_debug') or force_debug:
        conf.env['CFLAGS'] += ['-g']

    if conf.has_tool_option('cxx_nodebug'):
        conf.env['DEFINES'] += ['NDEBUG']
