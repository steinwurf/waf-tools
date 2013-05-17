#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the Apple LLVM 4.2 compiler for iOS 5.0 armv7
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'clang_common')
    conf.mkspec_clang_ios_configure(4, 2, '5.0', 'armv7')
