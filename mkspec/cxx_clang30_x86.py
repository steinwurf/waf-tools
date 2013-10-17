#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the clang 3.0 compiler for 32 bit
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'clang_common')
    conf.mkspec_clang_configure(3,0)
    conf.mkspec_add_common_flag('-m32')
