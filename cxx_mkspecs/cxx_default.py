#!/usr/bin/env python
# encoding: utf-8

import os

from waflib import Errors
from waflib import Logs
from waflib import Utils
from waflib.Configure import conf

from . import clang_mkspecs
from . import gxx_mkspecs
from . import msvc_mkspecs


def load_compiler(conf, compiler, arch):
    # Note clang goes first otherwise 'g++' will be in 'clang++'
    #                                  ¯¯¯                  ¯¯¯
    if "clang" in compiler:
        conf.mkspec_clang_configure(3, 6, minimum=True)
    elif "g++" in compiler:
        conf.mkspec_gxx_configure(4, 9, minimum=True)
    elif "msvc" in compiler or "CL.exe" in compiler or "cl.exe" in compiler:
        if arch == "x86":
            conf.env.MSVC_TARGETS = ["x86"]
        elif arch == "x64":
            conf.env.MSVC_TARGETS = ["x64", "x86_amd64"]

        conf.load("msvc")
        # Note: the waf msvc tool also loads msvc as a C compiler
        conf.mkspec_check_minimum_msvc_version(14.0)
        conf.mkspec_set_msvc_flags()
    else:
        raise Errors.WafError("Unknown compiler: %s" % compiler)

    if ("clang" in compiler or "g++" in compiler) and arch:
        if arch == "x86":
            conf.mkspec_add_common_flag("-m32")
        elif arch == "x64":
            conf.mkspec_add_common_flag("-m64")


@conf
def cxx_default(conf, arch=None):
    """
    Detect and setup the default compiler for the platform
    """
    # If the user-defined CXX variable is set
    # then use that compiler as the first option
    if "CXX" in os.environ:
        compiler = os.environ["CXX"]
        conf.start_msg("Checking C++ compiler %r" % compiler)
        load_compiler(conf, compiler, arch)
        if conf.env["CXX"]:
            conf.end_msg(conf.env.get_flat("CXX"))
            conf.env["COMPILER_CXX"] = compiler
            return  # Compiler configured successfully
        else:
            conf.end_msg(False)
            conf.fatal("Could not configure a C++ compiler!")

    # Otherwise we try to find a compiler on the current host
    # based on the following compiler list
    cxx_compilers = {
        "win32": ["msvc", "g++"],
        "linux": ["g++", "clang++"],
        "darwin": ["clang++"],
        "cygwin": ["g++"],
        "default": ["g++"],
    }

    sys_platform = Utils.unversioned_sys_platform()
    platform = "default"
    # Check if we have a specific list for the current system
    if sys_platform in cxx_compilers:
        platform = sys_platform

    # The list of the compilers to be checked
    possible_compiler_list = cxx_compilers[platform]

    for compiler in possible_compiler_list:
        conf.env.stash()
        conf.start_msg("Checking for %r (C++ compiler)" % compiler)
        try:
            load_compiler(conf, compiler, arch)
        except conf.errors.ConfigurationError as e:
            conf.env.revert()
            conf.end_msg(e, color="YELLOW")
            Logs.debug("cxx_default: %r" % e)
        else:
            if conf.env["CXX"]:
                conf.end_msg(conf.env.get_flat("CXX"))
                conf.env["COMPILER_CXX"] = compiler
                break  # Break from the for-cycle
            conf.end_msg(False)
    else:
        conf.fatal("Could not configure a C++ compiler!")


@conf
def cxx_default_x86(conf):
    """
    Detect and setup the default compiler forcing 32-bit architecture.
    """
    conf.cxx_default("x86")


@conf
def cxx_default_x64(conf):
    """
    Detect and setup the default compiler forcing 64-bit architecture.
    """
    conf.cxx_default("x64")
