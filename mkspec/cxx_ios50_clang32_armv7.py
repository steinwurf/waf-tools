#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the clang 3.2 compiler for iOS 5.0 armv7
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'clang_common')
    conf.mkspec_clang_ios_configure(3, 2, '5.0', 'armv7')
