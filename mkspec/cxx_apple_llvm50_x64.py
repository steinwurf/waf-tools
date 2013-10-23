#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the 64-bit Apple llvm 5.0 compiler (clang 3.3)
"""
def configure(conf):
    if conf.is_mkspec_platform('mac'):
        conf.load_external_tool('mkspec_common', 'clang_common')
        conf.mkspec_clang_configure(5,0)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal('%s is not supported for this mkspec.' % conf.get_mkspec_platform())
