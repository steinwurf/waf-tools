#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

import gxx_common

"""
Detect and setup the Android g++ 4.6 compiler for ARM
"""
@conf
def cxx_android_gxx46_arm(conf):
    conf.mkspec_gxx_android_configure(4, 6, 'arm-linux-androideabi')

"""
Detect and setup the g++ 4.6 cross-compiler for ARM 32-bit Linux
"""
@conf
def cxx_crosslinux_gxx46_arm(conf):
    conf.mkspec_gxx_configure(4, 6, 'arm-openwrt-linux')
    # Statically link in the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']

"""
Detect and setup the g++ 4.6 cross-compiler for 64-bit Linux
"""
@conf
def cxx_crosslinux_gxx46_x64(conf):
    conf.mkspec_gxx_configure(4, 6, 'crosslinux-gxx46-x64')
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the g++ 4.6 cross-compiler for 32-bit Linux
"""
@conf
def cxx_crosslinux_gxx46_x86(conf):
    conf.mkspec_gxx_configure(4, 6, 'crosslinux-gxx46-x86')
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the g++ 4.7 cross-compiler for MIPS 32-bit Linux
"""
@conf
def cxx_crosslinux_gxx47_mips(conf):
    conf.mkspec_gxx_configure(4, 7, 'crosslinux-gxx47-mips')
    # Statically link in the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']

"""
Detect and setup the g++ 4.6 compiler for 64 bit
"""
@conf
def cxx_gxx46_x64(conf):
    conf.mkspec_gxx_configure(4,6)
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the g++ 4.6 compiler for 32 bit linux
"""
@conf
def cxx_gxx46_x86(conf):
    conf.mkspec_gxx_configure(4,6)
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the g++ 4.7 compiler for 64 bit
"""
@conf
def cxx_gxx47_x64(conf):
    conf.mkspec_gxx_configure(4,7)
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the g++ 4.7 compiler for 32 bit
"""
@conf
def cxx_gxx47_x86(conf):
    conf.mkspec_gxx_configure(4,7)
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the g++ 4.8 compiler for 64 bit
"""
@conf
def cxx_gxx48_x64(conf):
    conf.mkspec_gxx_configure(4,8)
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the g++ 4.8 compiler for 32 bit
"""
@conf
def cxx_gxx48_x86(conf):
    conf.mkspec_gxx_configure(4,8)
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the g++ 4.7 cross-compiler for Raspberry Pi (Linux)
"""
@conf
def cxx_raspberry_gxx47_arm(conf):
    conf.mkspec_gxx_configure(4, 7, 'raspberry-gxx47-arm')
