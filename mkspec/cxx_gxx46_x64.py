#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the g++ 4.6 compiler for 64 bit
"""
def configure(conf):
    conf.mkspec_gxx_configure(4,6)
    conf.env['CXXFLAGS'] += ['-m64']

