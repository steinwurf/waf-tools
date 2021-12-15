#!/usr/bin/env python
# encoding: utf-8

import os

from waflib.Configure import conf
import waflib.Tools.gcc
import waflib.Tools.gxx
import waflib.Utils

from . import cxx_common


@conf
def mkspec_check_gcc_version(conf, compiler, major, minor, minimum=False):
    """
    Check the exact or minimum gcc version.

    :param major: The major version number, e.g. 4
    :param minor: The minor version number, e.g. 6
    :param minimum: Only check for a minimum compiler version, if true
    """
    conf.get_cc_version(cc=compiler, gcc=True)
    conf.mkspec_validate_cc_version(major, minor, minimum)


@conf
def mkspec_gxx_configure(conf, major, minor, prefix=None, minimum=False):
    """
    :param major:   The major version number of the compiler, e.g. 4
    :param minor:   The minor version number of the compiler, e.g. 6
    :param prefix:  Prefix to the compiler name, e.g. 'arm-linux-androideabi'
    :param minimum: Only check for a minimum compiler version, if true
    """
    # Where to look for the compiler
    paths = conf.mkspec_get_toolchain_paths()

    # If the user-defined CXX variable is set, then use that compiler
    if "CXX" in os.environ:
        cxx = waflib.Utils.to_list(os.environ["CXX"])
        conf.to_log("Using user defined environment variable CXX=%r" % cxx)
    else:
        # Find g++ first
        gxx_names = conf.mkspec_get_compiler_binary_name("g++", major, minor, prefix)
        if minimum:
            gxx_names = "g++"
        cxx = conf.find_program(gxx_names, path_list=paths)
        cxx = conf.cmd_to_list(cxx)

    conf.env["CXX"] = cxx
    conf.env["CXX_NAME"] = os.path.basename(conf.env.get_flat("CXX"))

    conf.mkspec_check_gcc_version(cxx, major, minor, minimum)

    # If the user-defined CC variable is set, then use that compiler
    if "CC" in os.environ:
        cc = waflib.Utils.to_list(os.environ["CC"])
        conf.to_log("Using user defined environment variable CC=%r" % cc)
    else:
        # Also find gcc
        gcc_names = conf.mkspec_get_compiler_binary_name("gcc", major, minor, prefix)
        if minimum:
            gcc_names = "gcc"
        cc = conf.find_program(gcc_names, path_list=paths)
        cc = conf.cmd_to_list(cc)

    conf.env["CC"] = cc
    conf.env["CC_NAME"] = os.path.basename(conf.env.get_flat("CC"))

    conf.mkspec_check_gcc_version(cc, major, minor, minimum)

    # Find the archiver
    ar = conf.mkspec_get_ar_binary_name(prefix)
    conf.find_program(ar, path_list=paths, var="AR")
    conf.env.ARFLAGS = "rcs"

    # Set up C++ tools and flags
    conf.gxx_common_flags()
    conf.gxx_modifier_platform()
    conf.cxx_load_tools()
    conf.cxx_add_flags()

    # Also set up C tools and flags
    conf.gcc_common_flags()
    conf.gcc_modifier_platform()
    conf.cc_load_tools()
    conf.cc_add_flags()

    # Add linker flags
    conf.link_add_flags()

    # Add our own cxx flags
    conf.mkspec_set_gxx_cxxflags()
    # Add our own cc flags
    conf.mkspec_set_gcc_ccflags()


@conf
def mkspec_gxx_android_configure(conf, major, minor, prefix):
    conf.set_mkspec_platform("android")
    conf.mkspec_gxx_configure(major, minor, prefix)
    conf.mkspec_set_android_options()


@conf
def mkspec_set_gcc_ccflags(conf):

    if conf.has_tool_option("cxx_debug"):
        conf.env["CFLAGS"] += ["-g", "-fno-omit-frame-pointer"]

        # Don't add any optimization flags
        conf.env["MKSPEC_DISABLE_OPTIMIZATION"] = True

    # Optimization flags
    optflags = ["-O2", "-ftree-vectorize", "-finline-functions"]

    if not conf.env["MKSPEC_DISABLE_OPTIMIZATION"]:
        conf.env["CFLAGS"] += optflags

    # Warning flags
    conf.env["CFLAGS"] += ["-Wextra", "-Wall"]

    if conf.has_tool_option("cxx_nodebug"):
        conf.env["DEFINES"] += ["NDEBUG"]


@conf
def mkspec_set_gxx_cxxflags(conf):

    # Warning flags
    conf.env["CXXFLAGS"] += ["-Wextra", "-Wall"]

    if conf.has_tool_option("cxx_debug"):
        conf.env["CXXFLAGS"] += ["-g", "-fno-omit-frame-pointer"]

        # Don't add any optimization flags
        conf.env["MKSPEC_DISABLE_OPTIMIZATION"] = True
    elif not conf.get_mkspec_platform() in ["mac", "ios"]:
        conf.env["LINKFLAGS"] += ["-s"]

    # Optimization flags
    optflags = ["-O2", "-ftree-vectorize", "-finline-functions"]

    if not conf.env["MKSPEC_DISABLE_OPTIMIZATION"]:
        conf.env["CXXFLAGS"] += optflags

    if conf.has_tool_option("cxx_nodebug"):
        conf.env["DEFINES"] += ["NDEBUG"]

    # Disable dynamic linking if -static is passed
    if "-static" in conf.env["LINKFLAGS"]:
        conf.env["SHLIB_MARKER"] = []

    # Use the C++14 language features
    conf.env["CXXFLAGS"] += ["-std=c++14"]
