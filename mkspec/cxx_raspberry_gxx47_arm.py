#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the g++ 4.7 cross-compiler for Raspberry Pi (Linux)
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'gxx_common')
    conf.mkspec_gxx_configure(4, 7, 'raspberry-gxx47-arm')
