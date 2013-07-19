#!/usr/bin/env python
# encoding: utf-8

"""
Detect and setup the android g++ 4.6 compiler for arm
"""
def configure(conf):
    conf.load_external_tool('mkspec_common', 'gxx_common')
    conf.mkspec_gxx_android_configure(4, 6, 'arm-linux-androideabi')
