#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

import gxx_common


@conf
def cxx_android_gxx46_arm(conf):
    """
    Detect and setup the Android g++ 4.6 compiler for ARM
    """
    conf.mkspec_gxx_android_configure(4, 6, 'arm-linux-androideabi')


@conf
def cxx_android_gxx48_arm(conf):
    """
    Detect and setup the Android g++ 4.8 compiler for ARM
    """
    conf.mkspec_gxx_android_configure(4, 8, 'arm-linux-androideabi')


@conf
def cxx_android_gxx48_armv7(conf):
    """
    Detect and setup the Android g++ 4.8 compiler for ARMv7
    """
    conf.mkspec_gxx_android_configure(4, 8, 'arm-linux-androideabi')
    # Specify the ARMv7 architecture and the 'softfp' float ABI to compile for
    # hardware FPU, but with software linkage (required for -mfpu=neon flag).
    # The __ARM_NEON__ macro will be defined only if the -mfloat-abi=softfp and
    # -mfpu=neon flags are used together.
    flags = ['-march=armv7-a', '-mtune=generic-armv7-a', '-mfloat-abi=softfp']
    conf.env['CFLAGS'] += flags
    conf.env['CXXFLAGS'] += flags
    # Specify the ARMv7 architecture in the LINKFLAGS to link with the
    # atomic support that is required for std::threads (without this flag,
    # the threading code might call pure virtual methods)
    conf.env['LINKFLAGS'] += ['-march=armv7-a']


@conf
def cxx_crosslinux_gxx46_arm(conf):
    """
    Detect and setup the g++ 4.6 cross-compiler for ARM 32-bit Linux
    """
    conf.mkspec_gxx_configure(4, 6, 'arm-openwrt-linux')
    # Note: libstdc++ might not be available on the target platform
    # Statically link the GCC runtime and the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libgcc', '-static-libstdc++']
    # The GCC runtime does not contain the C++ exception handling functions,
    # so libgcc_eh.a should also be statically linked
    conf.env['STLIB'] += ['gcc_eh']


@conf
def cxx_crosslinux_gxx47_arm(conf):
    """
    Detect and setup the g++ 4.7 cross-compiler for ARM 32-bit Linux
    """
    conf.mkspec_gxx_configure(4, 7, 'arm-openwrt-linux')
    # Note: libstdc++ might not be available on the target platform
    # Statically link the GCC runtime and the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libgcc', '-static-libstdc++']
    # The GCC runtime does not contain the C++ exception handling functions,
    # so libgcc_eh.a should also be statically linked
    conf.env['STLIB'] += ['gcc_eh']


@conf
def cxx_crosslinux_gxx46_x64(conf):
    """
    Detect and setup the g++ 4.6 cross-compiler for 64-bit Linux
    """
    conf.mkspec_gxx_configure(4, 6, 'crosslinux-gxx46-x64')
    conf.mkspec_add_common_flag('-m64')
    # Note: libstdc++ might not be available on the target platform
    # Statically link the GCC runtime and the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libgcc', '-static-libstdc++']


@conf
def cxx_crosslinux_gxx46_x86(conf):
    """
    Detect and setup the g++ 4.6 cross-compiler for 32-bit Linux
    """
    conf.mkspec_gxx_configure(4, 6, 'crosslinux-gxx46-x86')
    conf.mkspec_add_common_flag('-m32')
    # Note: libstdc++ might not be available on the target platform
    # Statically link the GCC runtime and the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libgcc', '-static-libstdc++']


@conf
def cxx_crosslinux_gxx47_mips(conf):
    """
    Detect and setup the g++ 4.7 cross-compiler for MIPS 32-bit Linux
    """
    conf.mkspec_gxx_configure(4, 7, 'crosslinux-gxx47-mips')
    # Statically link in the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']


@conf
def cxx_gcov_gxx49_x64(conf):
    """
    Configure g++ 4.9 (64 bit) for coverage analysis with gcov
    """
    # Don't add any optimization flags (these might lead to incorrect results)
    conf.env['MKSPEC_DISABLE_OPTIMIZATION'] = True

    conf.mkspec_gxx_configure(4, 9)
    conf.mkspec_add_common_flag('-m64')

    # Set flag to compile and link code instrumented for coverage analysis
    conf.mkspec_add_common_flag('--coverage')

    # Add flags to disable optimization and all function inlining
    flags = ['-O0', '-fPIC', '-fno-inline', '-fno-inline-small-functions',
             '-fno-default-inline']
    conf.env['CFLAGS'] += flags
    conf.env['CXXFLAGS'] += flags


@conf
def cxx_gxx46_x64(conf):
    """
    Detect and setup the g++ 4.6 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(4, 6)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx46_x86(conf):
    """
    Detect and setup the g++ 4.6 compiler for 32 bit linux
    """
    conf.mkspec_gxx_configure(4, 6)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx47_x64(conf):
    """
    Detect and setup the g++ 4.7 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(4, 7)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx47_x86(conf):
    """
    Detect and setup the g++ 4.7 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(4, 7)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx48_x64(conf):
    """
    Detect and setup the g++ 4.8 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(4, 8)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx48_x86(conf):
    """
    Detect and setup the g++ 4.8 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(4, 8)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx49_x64(conf):
    """
    Detect and setup the g++ 4.9 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(4, 9)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx49_x86(conf):
    """
    Detect and setup the g++ 4.9 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(4, 9)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx52_x64(conf):
    """
    Detect and setup the g++ 4.9 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(5, 2)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx52_x86(conf):
    """
    Detect and setup the g++ 5.2 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(5, 2)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_raspberry_gxx47_arm(conf):
    """
    Detect and setup the g++ 4.7 cross-compiler for Raspberry Pi (Linux)
    """
    conf.mkspec_gxx_configure(4, 7, 'raspberry-gxx47-arm')


@conf
def cxx_raspberry_gxx49_arm(conf):
    """
    Detect and setup the g++ 4.9 cross-compiler for Raspberry Pi (Linux)
    """
    conf.mkspec_gxx_configure(4, 9, 'raspberry-gxx49-arm')
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']


@conf
def cxx_openwrt_gxx48_arm(conf):
    """
    Detect and setup the g++ 4.8 cross-compiler for 32-bit ARM OpenWRT
    """
    conf.mkspec_gxx_configure(4, 8, 'arm-openwrt-linux')
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']


@conf
def cxx_openwrt_gxx48_mips(conf):
    """
    Detect and setup the g++ 4.8 cross-compiler for 32-bit MIPS OpenWRT
    """
    conf.mkspec_gxx_configure(4, 8, 'mips-openwrt-linux')
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']
