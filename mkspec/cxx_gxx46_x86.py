#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the g++ 4.6 compiler for 32 bit linux
"""
def configure(conf):
    conf.mkspec_gxx_configure(4,6)
    conf.env['CXXFLAGS'] += ['-m32']
