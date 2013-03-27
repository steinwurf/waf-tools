#!/usr/bin/env python
# encoding: utf-8

import cc_default

"""
Detect and setup the ios gcc 4.2 compiler for arm
"""
def configure(conf):
    conf.mkspec_gcc_ios_configure(4,2)

