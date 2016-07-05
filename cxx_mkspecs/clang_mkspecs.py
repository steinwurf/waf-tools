#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

from . import clang_common


@conf
def cxx_android_clang34_armv7(conf):
    """
    Detect and setup the Android clang 3.4 compiler for ARMv7
    """
    conf.mkspec_clang_android_configure(3, 4, prefix='arm-linux-androideabi',
                                        target='armv7-linux-androideabi')
    conf.env['DEST_CPU'] = 'arm'

@conf
def cxx_android_clang38_armv7a(conf):
    """
    Detect and setup the Android clang 3.8 compiler for ARMv7a
    """
    conf.mkspec_clang_android_configure(3, 8, prefix='arm-linux-androideabi',
                                        target='armv7a-none-linux-android')
    conf.env['DEST_CPU'] = 'arm'

@conf
def cxx_apple_llvm70_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 7.0 compiler
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(7, 0)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


@conf
def cxx_apple_llvm73_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 7.3 compiler
    """
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(7, 3)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
            conf.get_mkspec_platform()))


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
def cxx_clang36_x64(conf):
    """
    Detect and setup the clang 3.6 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 6)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang36_x86(conf):
    """
    Detect and setup the clang 3.6 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 6)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_clang37_x64(conf):
    """
    Detect and setup the clang 3.7 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 7)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang37_x86(conf):
    """
    Detect and setup the clang 3.7 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 7)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_clang38_x64(conf):
    """
    Detect and setup the clang 3.8 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 8)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_clang38_x86(conf):
    """
    Detect and setup the clang 3.8 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 8)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_ios50_apple_llvm_armv7(conf):
    """
    Detect and setup the default Apple LLVM compiler for iOS 5.0 armv7
    """
    conf.mkspec_clang_ios_configure(6, 1, '5.0', 'armv7', minimum=True)
    conf.env['DEST_CPU'] = 'arm'


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
def cxx_clang36_address_sanitizer_x64(conf):
    """
    Configure clang 3.6 (64-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 6, '-m64')


@conf
def cxx_clang36_address_sanitizer_x86(conf):
    """
    Configure clang 3.6 (32-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 6, '-m32')


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
def cxx_clang36_memory_sanitizer_x64(conf):
    """
    Configure clang 3.6 (64-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 6, '-m64')


@conf
def cxx_clang36_memory_sanitizer_x86(conf):
    """
    Configure clang 3.6 (32-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 6, '-m32')


@conf
def mkspec_setup_clang_thread_sanitizer(conf, major, minor, arch):
    """
    http://clang.llvm.org/docs/ThreadSanitizer.html
    """
    conf.mkspec_clang_configure(major, minor, force_debug=True)
    conf.mkspec_add_common_flag(arch)

    conf.mkspec_add_common_flag('-fsanitize=thread')


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


@conf
def cxx_clang36_thread_sanitizer_x64(conf):
    """
    Configure clang 3.6 (64-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 6, '-m64')


@conf
def cxx_clang36_thread_sanitizer_x86(conf):
    """
    Configure clang 3.6 (32-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 6, '-m32')
