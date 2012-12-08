#!/usr/bin/env python
# encoding: utf-8

import cxx_default

"""
Detect and setup the android g++ 4.6 compiler for arm
"""
def configure(conf):
    conf.mkspec_gxx_android_configure(4,6)



