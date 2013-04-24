#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the 64-bit Apple llvm 4.2 compiler
"""
def configure(conf):
    conf.mkspec_clang_configure(4,2)
    conf.env.CXXFLAGS += ['-m64']
