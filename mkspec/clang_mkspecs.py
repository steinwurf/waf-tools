#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

import clang_common


@conf
def cxx_android_clang34_armv7(conf):
    """
    Detect and setup the Android clang 3.4 compiler for ARMv7
    """
    conf.mkspec_clang_android_configure(3, 4, prefix='arm-linux-androideabi',
                                        target='armv7-linux-androideabi')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_apple_llvm42_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 4.2 compiler (clang 3.2)
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(4, 2)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_apple_llvm42_x86(conf):
    """
    Detect and setup the 32-bit Apple LLVM 4.2 compiler (clang 3.2)
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(4, 2)
        conf.mkspec_add_common_flag('-m32')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_apple_llvm50_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 5.0 compiler (clang 3.3)
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(5, 0)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_apple_llvm50_x86(conf):
    """
    Detect and setup the 32-bit Apple LLVM 5.0 compiler (clang 3.3)
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(5, 0)
        conf.mkspec_add_common_flag('-m32')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_apple_llvm51_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 5.1 compiler (clang 3.4)
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(5, 1)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_apple_llvm51_x86(conf):
    """
    Detect and setup the 32-bit Apple LLVM 5.1 compiler (clang 3.4)
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(5, 1)
        conf.mkspec_add_common_flag('-m32')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_apple_llvm60_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 6.0 compiler (clang 3.5)
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(6, 0)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_apple_llvm61_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 6.1 compiler (LLVM 3.6)
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(6, 1)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_clang30_x64(conf):
    """
    Detect and setup the clang 3.0 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 0)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang30_x86(conf):
    """
    Detect and setup the clang 3.0 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 0)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_clang31_x64(conf):
    """
    Detect and setup the clang 3.1 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 1)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang31_x86(conf):
    """
    Detect and setup the clang 3.1 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 1)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_clang32_x64(conf):
    """
    Detect and setup the clang 3.2 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 2)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang32_x86(conf):
    """
    Detect and setup the clang 3.2 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 2)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_clang33_x64(conf):
    """
    Detect and setup the clang 3.3 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 3)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang33_x86(conf):
    """
    Detect and setup the clang 3.3 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 3)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_clang34_x64(conf):
    """
    Detect and setup the clang 3.4 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 4)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang34_x86(conf):
    """
    Detect and setup the clang 3.4 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 4)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_clang35_x64(conf):
    """
    Detect and setup the clang 3.5 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 5)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang35_x86(conf):
    """
    Detect and setup the clang 3.5 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 5)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_ios50_apple_llvm42_armv7(conf):
    """
    Detect and setup the Apple LLVM 4.2 compiler for iOS 5.0 armv7
    """
    conf.mkspec_clang_ios_configure(4, 2, '5.0', 'armv7')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios50_apple_llvm50_armv7(conf):
    """
    Detect and setup the Apple LLVM 5.0 compiler for iOS 5.0 armv7
    """
    conf.mkspec_clang_ios_configure(5, 0, '5.0', 'armv7')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios50_apple_llvm51_armv7(conf):
    """
    Detect and setup the Apple LLVM 5.1 compiler for iOS 5.0 armv7
    """
    conf.mkspec_clang_ios_configure(5, 1, '5.0', 'armv7')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios50_apple_llvm60_armv7(conf):
    """
    Detect and setup the Apple LLVM 6.0 compiler for iOS 5.0 armv7
    """
    conf.mkspec_clang_ios_configure(6, 0, '5.0', 'armv7')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios50_apple_llvm_armv7(conf):
    """
    Detect and setup the default Apple LLVM compiler for iOS 5.0 armv7
    """
    conf.mkspec_clang_ios_configure(6, 1, '5.0', 'armv7', minimum=True)
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios50_clang32_armv7(conf):
    """
    Detect and setup the clang 3.2 compiler for iOS 5.0 armv7
    """
    conf.mkspec_clang_ios_configure(3, 2, '5.0', 'armv7')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios70_apple_llvm60_armv7(conf):
    """
    Detect and setup the Apple LLVM 6.0 compiler for iOS 7.0 armv7
    """
    conf.mkspec_clang_ios_configure(6, 0, '7.0', 'armv7')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios70_apple_llvm60_armv7s(conf):
    """
    Detect and setup the Apple LLVM 6.0 compiler for iOS 7.0 armv7s
    """
    conf.mkspec_clang_ios_configure(6, 0, '7.0', 'armv7s')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios70_apple_llvm60_arm64(conf):
    """
    Detect and setup the Apple LLVM 6.0 compiler for iOS 7.0 arm64
    """
    conf.mkspec_clang_ios_configure(6, 0, '7.0', 'arm64')
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios70_apple_llvm60_i386(conf):
    """
    Detect and setup the Apple LLVM 6.0 compiler for iOS 7.0 i386 (simulator)
    """
    conf.mkspec_clang_ios_configure(6, 0, '7.0', 'i386')


@conf
def cxx_ios70_apple_llvm60_x86_64(conf):
    """
    Detect and setup the Apple LLVM 6.0 compiler for iOS 7.0 x86_64 (simulator)
    """
    conf.mkspec_clang_ios_configure(6, 0, '7.0', 'x86_64')


@conf
def cxx_ios70_apple_llvm_armv7(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 armv7
    """
    conf.mkspec_clang_ios_configure(6, 1, '7.0', 'armv7', minimum=True)
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios70_apple_llvm_armv7s(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 armv7s
    """
    conf.mkspec_clang_ios_configure(6, 1, '7.0', 'armv7s', minimum=True)
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios70_apple_llvm_arm64(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 arm64
    """
    conf.mkspec_clang_ios_configure(6, 1, '7.0', 'arm64', minimum=True)
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_ios70_apple_llvm_i386(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 i386 (simulator)
    """
    conf.mkspec_clang_ios_configure(6, 1, '7.0', 'i386', minimum=True)


@conf
def cxx_ios70_apple_llvm_x86_64(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 x86_64 (simulator)
    """
    conf.mkspec_clang_ios_configure(6, 1, '7.0', 'x86_64', minimum=True)


@conf
def mkspec_setup_clang_address_sanitizer(conf, major, minor, arch):
    """
    To get a reasonable performance add -O1 or higher. To get nicer
    stack traces in error messages add -fno-omit-frame-pointer. To get
    perfect stack traces you may need to disable inlining (just use
    -O1) and tail call elimination (-fno-optimize-sibling-calls).
    http://clang.llvm.org/docs/AddressSanitizer.html
    """
    conf.mkspec_clang_configure(major, minor, force_debug=True)
    conf.mkspec_add_common_flag(arch)

    conf.mkspec_add_common_flag('-fsanitize=address')
    conf.mkspec_add_common_flag('-fno-omit-frame-pointer')
    conf.mkspec_add_common_flag('-fno-optimize-sibling-calls')


@conf
def cxx_clang34_address_sanitizer_x64(conf):
    """
    Configure clang 3.4 (64-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 4, '-m64')


@conf
def cxx_clang34_address_sanitizer_x86(conf):
    """
    Configure clang 3.4 (32-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 4, '-m32')


@conf
def cxx_clang35_address_sanitizer_x64(conf):
    """
    Configure clang 3.5 (64-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 5, '-m64')


@conf
def cxx_clang35_address_sanitizer_x86(conf):
    """
    Configure clang 3.5 (32-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 5, '-m32')


@conf
def mkspec_setup_clang_memory_sanitizer(conf, major, minor, arch):
    """
    To get a reasonable performance add -O1 or higher. To get
    meaningful stack traces in error messages add
    -fno-omit-frame-pointer. To get perfect stack traces you may need
    to disable inlining (just use -O1) and tail call elimination
    (-fno-optimize-sibling-calls).
    http://clang.llvm.org/docs/MemorySanitizer.html
    """

    conf.mkspec_clang_configure(major, minor, force_debug=True)
    conf.mkspec_add_common_flag(arch)

    conf.mkspec_add_common_flag('-fsanitize=memory')
    conf.mkspec_add_common_flag('-fsanitize-memory-track-origins')
    conf.mkspec_add_common_flag('-fno-omit-frame-pointer')
    conf.mkspec_add_common_flag('-fno-optimize-sibling-calls')


@conf
def cxx_clang34_memory_sanitizer_x64(conf):
    """
    Configure clang 3.4 (64-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 4, '-m64')


@conf
def cxx_clang34_memory_sanitizer_x86(conf):
    """
    Configure clang 3.4 (32-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 4, '-m32')


@conf
def cxx_clang35_memory_sanitizer_x64(conf):
    """
    Configure clang 3.5 (64-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 5, '-m64')


@conf
def cxx_clang35_memory_sanitizer_x86(conf):
    """
    Configure clang 3.5 (32-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 5, '-m32')


@conf
def mkspec_setup_clang_thread_sanitizer(conf, major, minor, arch):
    """
    http://clang.llvm.org/docs/ThreadSanitizer.html
    """
    conf.mkspec_clang_configure(major, minor, force_debug=True)
    conf.mkspec_add_common_flag(arch)

    conf.mkspec_add_common_flag('-fsanitize=thread')


@conf
def cxx_clang34_thread_sanitizer_x64(conf):
    """
    Configure clang 3.4 (64-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 4, '-m64')


@conf
def cxx_clang34_thread_sanitizer_x86(conf):
    """
    Configure clang 3.4 (32-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 4, '-m32')


@conf
def cxx_clang35_thread_sanitizer_x64(conf):
    """
    Configure clang 3.5 (64-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 5, '-m64')


@conf
def cxx_clang35_thread_sanitizer_x86(conf):
    """
    Configure clang 3.5 (32-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 5, '-m32')
