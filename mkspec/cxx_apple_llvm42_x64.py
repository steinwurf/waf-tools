#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the 64-bit Apple llvm 4.2 compiler (clang 3.2)
"""
def configure(conf):
    if conf.is_mkspec_platform('mac'):
        conf.load_external_tool('mkspec_common', 'clang_common')
        conf.mkspec_clang_configure(4,2)
        conf.env.CXXFLAGS += ['-m64']
    else:
        conf.fatal('%s is unsupported for this mkspec.' % conf.get_mkspec_platform())