#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the clang 3.0 compiler for 32 bit
"""
def configure(conf):
    if conf.is_mkspec_platform('linux'):
        conf.clang_find_binaries(('3','0','0'))
        conf.add_clang_default_cxxflags()
        conf.env.CXXFLAGS += ['-m32']
    else:
        conf.fatal('%s is unsupported for this mkspec.' % conf.get_mkspec_platform())