#!/usr/bin/env python
# encoding: utf-8
from waflib.Tools.gxx import gxx_common_flags
import cxx_default

# @conf
# def android_test_runner(bld, bin):
#     return (bin, 0, "ok", "ok")

"""
Detect and setup the android gcc-4.6 compiler for arm
"""
def configure(conf):
    conf.set_mkspec_platform('android')

    ndk = conf.get_tool_option('NDK_DIR')

    conf.android_find_binaries(('4','6','0'), [ndk])

    # Set the android define - some libraries rely on this define being present
    conf.env.DEFINES += ['ANDROID']
    conf.add_android_default_cxxflags()
