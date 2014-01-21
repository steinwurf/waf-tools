#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

import clang_common

"""
Detect and setup the 64-bit Apple llvm 4.2 compiler (clang 3.2)
"""
@conf
def cxx_apple_llvm42_x64(conf):
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(4,2)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
                    conf.get_mkspec_platform()))

"""
Detect and setup the 32-bit Apple llvm 4.2 compiler (clang 3.2)
"""
@conf
def cxx_apple_llvm42_x86(conf):
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(4,2)
        conf.mkspec_add_common_flag('-m32')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
                    conf.get_mkspec_platform()))

"""
Detect and setup the 64-bit Apple llvm 5.0 compiler (clang 3.3)
"""
@conf
def cxx_apple_llvm50_x64(conf):
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(5,0)
        conf.mkspec_add_common_flag('-m64')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
                    conf.get_mkspec_platform()))

"""
Detect and setup the 32-bit Apple llvm 5.0 compiler (clang 3.3)
"""
@conf
def cxx_apple_llvm42_x86(conf):
    if conf.is_mkspec_platform('mac'):
        conf.mkspec_clang_configure(5,0)
        conf.mkspec_add_common_flag('-m32')
    else:
        conf.fatal("This mkspec is not supported on {0}.".format(
                    conf.get_mkspec_platform()))

"""
Detect and setup the clang 3.0 compiler for 64 bit
"""
@conf
def cxx_clang30_x64(conf):
    conf.mkspec_clang_configure(3,0)
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the clang 3.0 compiler for 32 bit
"""
@conf
def cxx_clang30_x86(conf):
    conf.mkspec_clang_configure(3,0)
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the clang 3.1 compiler for 64 bit
"""
@conf
def cxx_clang31_x64(conf):
    conf.mkspec_clang_configure(3,1)
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the clang 3.1 compiler for 32 bit
"""
@conf
def cxx_clang31_x86(conf):
    conf.mkspec_clang_configure(3,1)
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the clang 3.2 compiler for 64 bit
"""
@conf
def cxx_clang32_x64(conf):
    conf.mkspec_clang_configure(3,2)
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the clang 3.2 compiler for 32 bit
"""
@conf
def cxx_clang32_x86(conf):
    conf.mkspec_clang_configure(3,2)
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the clang 3.3 compiler for 64 bit
"""
@conf
def cxx_clang33_x64(conf):
    conf.mkspec_clang_configure(3,3)
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the clang 3.3 compiler for 32 bit
"""
@conf
def cxx_clang33_x86(conf):
    conf.mkspec_clang_configure(3,3)
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the clang 3.4 compiler for 64 bit
"""
@conf
def cxx_clang34_x64(conf):
    conf.mkspec_clang_configure(3,4)
    conf.mkspec_add_common_flag('-m64')

"""
Detect and setup the clang 3.4 compiler for 32 bit
"""
@conf
def cxx_clang34_x86(conf):
    conf.mkspec_clang_configure(3,4)
    conf.mkspec_add_common_flag('-m32')

"""
Detect and setup the Apple LLVM 4.2 compiler for iOS 5.0 armv7
"""
@conf
def cxx_ios50_apple_llvm42_armv7(conf):
    conf.mkspec_clang_ios_configure(4, 2, '5.0', 'armv7')

"""
Detect and setup the Apple LLVM 5.0 compiler for iOS 5.0 armv7
"""
@conf
def cxx_ios50_apple_llvm50_armv7(conf):
    conf.mkspec_clang_ios_configure(5, 0, '5.0', 'armv7')

"""
Detect and setup the clang 3.2 compiler for iOS 5.0 armv7
"""
@conf
def cxx_ios50_clang32_armv7(conf):
    conf.mkspec_clang_ios_configure(3, 2, '5.0', 'armv7')

"""
Detect and setup the clang 3.4 compiler for 32 bit and use thread sanitizer
"""
@conf
def cxx_clang34_thread_sanitizer_x86(conf):
    """
    http://clang.llvm.org/docs/ThreadSanitizer.html
    """
    conf.mkspec_clang_configure(3,4)
    conf.mkspec_add_common_flag('-m32')

    if not conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']

    conf.env['CXXFLAGS'] += ['-fsanitize=thread']

"""
Detect and setup the clang 3.4 compiler for 64 bit and use thread sanitizer
"""
@conf
def cxx_clang34_thread_sanitizer_x64(conf):
    """
    http://clang.llvm.org/docs/ThreadSanitizer.html
    """
    conf.mkspec_clang_configure(3,4)
    conf.mkspec_add_common_flag('-m64')

    if not conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']

    conf.env['CXXFLAGS'] += ['-fsanitize=thread']

"""
Detect and setup the clang 3.4 compiler for 32 bit and use memory sanitizer
"""
@conf
def cxx_clang34_memory_sanitizer_x86(conf):
    """
    To get a reasonable performance add -O1 or higher. To get meaningful
    stack traces in error messages add -fno-omit-frame-pointer. To get perfect
    stack traces you may need to disable inlining (just use -O1) and tail call
    elimination (-fno-optimize-sibling-calls).
    http://clang.llvm.org/docs/MemorySanitizer.html
    """

    conf.mkspec_clang_configure(3,4)
    conf.mkspec_add_common_flag('-m32')

    if not conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']

    conf.env['CXXFLAGS'] += ['-fsanitize=memory']

"""
Detect and setup the clang 3.4 compiler for 64 bit and use memory sanitizer
"""
@conf
def cxx_clang34_memory_sanitizer_x64(conf):
    """
    To get a reasonable performance add -O1 or higher. To get meaningful
    stack traces in error messages add -fno-omit-frame-pointer. To get perfect
    stack traces you may need to disable inlining (just use -O1) and tail call
    elimination (-fno-optimize-sibling-calls).
    http://clang.llvm.org/docs/MemorySanitizer.html
    """

    conf.mkspec_clang_configure(3,4)
    conf.mkspec_add_common_flag('-m64')

    if not conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']

    conf.env['CXXFLAGS'] += ['-fsanitize=memory']

"""
Detect and setup the clang 3.4 compiler for 32 bit and use address sanitizer
"""
@conf
def cxx_clang34_address_sanitizer_x86(conf):
    """
    To get a reasonable performance add -O1 or higher. To get nicer stack traces
    in error messages add -fno-omit-frame-pointer. To get perfect stack traces
    you may need to disable inlining (just use -O1) and tail call elimination
    (-fno-optimize-sibling-calls).
    http://clang.llvm.org/docs/AddressSanitizer.html
    """

    conf.mkspec_clang_configure(3,4)
    conf.mkspec_add_common_flag('-m32')

    if not conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']

    conf.env['CXXFLAGS'] += ['-fsanitize=address']

"""
Detect and setup the clang 3.4 compiler for 64 bit and use address sanitizer
"""
@conf
def cxx_clang34_address_sanitizer_x64(conf):
    """
    To get a reasonable performance add -O1 or higher. To get nicer stack traces
    in error messages add -fno-omit-frame-pointer. To get perfect stack traces
    you may need to disable inlining (just use -O1) and tail call elimination
    (-fno-optimize-sibling-calls).
    http://clang.llvm.org/docs/AddressSanitizer.html
    """

    conf.mkspec_clang_configure(3,4)
    conf.mkspec_add_common_flag('-m64')

    if not conf.has_tool_option('cxx_debug'):
        conf.env['CXXFLAGS'] += ['-g']

    conf.env['CXXFLAGS'] += ['-fsanitize=address']