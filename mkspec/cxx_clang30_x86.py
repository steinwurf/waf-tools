#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the clang 3.0 compiler for 32 bit
"""
def configure(conf):
    conf.mkspec_clang_configure(3,0)
    conf.env.CXXFLAGS += ['-m32']
