#!/usr/bin/env python
# encoding: utf-8

import os, sys

# The common modules are in the ./common folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR,'common'))

import gxx_common

"""
Detect and setup the g++ 4.6 compiler for 32 bit linux
"""
def configure(conf):
    conf.mkspec_gxx_configure(4,6)
    conf.env['CXXFLAGS'] += ['-m32']
