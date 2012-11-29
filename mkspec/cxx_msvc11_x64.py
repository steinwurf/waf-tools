#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the MicroSoft Visual C++ 2012 compiler for 64 bit windows
"""
def configure(conf):
    if conf.is_mkspec_platform('windows'):
        conf.env.MSVC_VERSIONS = ['msvc 11.0']
        conf.env.MSVC_TARGETS  = ['x86_amd64']
        # Here it would be nice to suppress all the extra "Checking for program CL"
        # messages printed by waf when loading the msvc tool. It looks as if we
        # have to suppress the find_program output in the get_msvc_version().
        # E.g. by using conf.in_msg = 1, anyway this is future work
        conf.load('msvc')
        conf.add_msvc_default_cxxflags()
    else:
        conf.fatal('%s is unsupported for this mkspec.' % conf.get_mkspec_platform())