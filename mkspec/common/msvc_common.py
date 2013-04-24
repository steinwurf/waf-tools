#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib.Configure import conf
from os.path import abspath, expanduser
import os

@conf
def mkspec_msvc_configure(conf, version):
    conf.env.MSVC_VERSIONS = ['msvc %s' % version]

    # Here it would be nice to suppress all the extra "Checking for program CL"
    # messages printed by waf when loading the msvc tool. It looks as if we
    # have to suppress the find_program output in the get_msvc_version().
    # E.g. by using conf.in_msg = 1, anyway this is future work
    conf.load('msvc')
    conf.mkspec_set_msvc_flags()

@conf
def mkspec_set_msvc_flags(conf):

    # Set _CRT_SECURE_NO_WARNINGS and _SCL_SECURE_NO_WARNINGS to suppress
    # deprecation warnings for strcpy, sprintf, etc.
    if conf.has_tool_option('cxx_debug'):
        # Produce full-symbolic debugging information in a .pdb file
        # Use the multithread, debug version of the run-time library
        conf.env['CXXFLAGS'] += ['/Zi', '/MTd', '/D_SCL_SECURE_NO_WARNINGS']
        conf.env['LINKFLAGS'] += ['/DEBUG']
    else:
        # Use the multithread, release version of the run-time library
        conf.env['CXXFLAGS'] += ['/MT', '/D_CRT_SECURE_NO_WARNINGS']

    # Set _WIN32_WINNT=0x0501 (i.e. Windows XP target)
    # to suppress warnings in boost asio
    # Disable warning C4345 which only states that msvc follows the
    # C++ standard for initializing POD types when the () form is used
    # Treat C4100 unreferenced parameter warning as Level 3
    # instead of Level 4 to better match g++ warnings
    conf.env['CXXFLAGS'] += ['/O2', '/Ob2', '/W3', '/wd4345', '/w34100', '/EHs',
        '/D_WIN32_WINNT=0x0501']

