#!/usr/bin/env python
# encoding: utf-8
from waflib.Tools.gxx import gxx_common_flags
import cxx_default
import os

"""
Detect and setup the android gcc-4.6 compiler for arm
"""
def configure(conf):
    conf.default_android_configure(('4','6','0'))

