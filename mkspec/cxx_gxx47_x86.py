#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the g++ 4.7 compiler for 32 bit
"""
def configure(conf):
    conf.mkspec_gxx_configure(4,7)
    conf.env['CXXFLAGS'] += ['-m32']
