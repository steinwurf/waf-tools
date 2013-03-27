#!/usr/bin/env python
# encoding: utf-8

import cc_default

"""
Detect and setup the android gcc 4.6 compiler for arm
"""
def configure(conf):
    conf.mkspec_gcc_android_configure(4,6)

