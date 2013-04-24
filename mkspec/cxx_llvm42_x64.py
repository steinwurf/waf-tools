#!/usr/bin/env python
# encoding: utf-8

import os, sys

# The common modules are in the ./common folder
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(CURRENT_DIR,'common'))

import clang_common

"""
Detect and setup the 64-bit Apple llvm 4.2 compiler (clang 3.2)
"""
def configure(conf):
    conf.mkspec_clang_configure(4,2)
    conf.env.CXXFLAGS += ['-m64']
