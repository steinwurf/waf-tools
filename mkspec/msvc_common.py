#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib.Configure import conf
from waflib.Logs import debug
from os.path import abspath, expanduser
import os

@conf
def mkspec_check_minimum_msvc_version(conf, minimum):
    """
    :param minimum: The major version number, e.g. 11.0
    """
    if (conf.env['MSVC_VERSION'] < float(minimum)):
        conf.fatal("Compiler version: {0}, "
                   "required minimum: {1}"
                   .format(conf.env['MSVC_VERSION'], minimum))

@conf
def mkspec_msvc_configure(conf, version):

    conf.env.MSVC_VERSIONS = ['msvc %s' % version]

    # Here we suppress all the "Checking for program CL"
    # messages printed by waf when loading the msvc tool
    conf.env.stash()
    conf.start_msg('Checking for msvc %s compiler' % version)
    try:
        conf.load('msvc')
    except conf.errors.ConfigurationError as e:
        conf.env.revert()
        conf.end_msg(False)
        debug('msvc_common: %r' % e)
    else:
        conf.end_msg(conf.env.get_flat('CXX'))
        conf.end_msg(False)
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

    if conf.has_tool_option('cxx_nodebug'):
        conf.env['DEFINES'] += ['NDEBUG']

    # Set _WIN32_WINNT=0x0501 (i.e. Windows XP target)
    # to suppress warnings in boost asio
    # Disable warning C4345 which only states that msvc follows the
    # C++ standard for initializing POD types when the () form is used
    # Treat C4100 unreferenced parameter warning as Level 3
    # instead of Level 4 to better match g++ warnings
    conf.env['CXXFLAGS'] += ['/O2', '/Ob2', '/W3', '/wd4345', '/w34100', '/EHs',
        '/D_WIN32_WINNT=0x0501']
    # Disable LNK4221 linker warning for empty object files
    conf.env['LINKFLAGS'] += ['/ignore:4221']  # used for LINK.exe
    conf.env['ARFLAGS'] +=   ['/ignore:4221']  # used for LIB.exe


