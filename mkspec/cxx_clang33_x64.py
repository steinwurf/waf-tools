#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the clang 3.3 compiler for 64 bit
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'clang_common')
    conf.mkspec_clang_configure(3,3)
    conf.mkspec_add_common_flag('-m64')
