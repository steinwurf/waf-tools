#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from waflib.Utils import subprocess
from waflib.Configure import conf

from . import cxx_common


@conf
def mkspec_emscripten_configure(conf, major, minor, minimum=False, force_debug=False):
    """
    :param force_debug: Always compile with debugging flags, if true
    """
    conf.set_mkspec_platform("emscripten")

    # The path to the emscripten compiler
    paths = conf.get_tool_option("emscripten_path")

    # The node.js binary can be "nodejs" or simply "node"
    conf.find_program(["nodejs", "node"], var="NODEJS")

    # Find the clang++ compiler
    cxx = conf.find_program(["em++"], path_list=paths)
    cxx = conf.cmd_to_list(cxx)
    conf.env["CXX"] = cxx
    conf.env["CXX_NAME"] = os.path.basename(conf.env.get_flat("CXX"))

    conf.check_emscripten_version(cxx, major, minor, minimum)

    # Find clang as the C compiler
    cc = conf.find_program(["emcc"], path_list=paths)
    cc = conf.cmd_to_list(cc)
    conf.env["CC"] = cc
    conf.env["CC_NAME"] = os.path.basename(conf.env.get_flat("CC"))

    conf.check_emscripten_version(cc, major, minor, minimum)

    # Find the archiver
    conf.find_program("emar", path_list=paths, var="AR")
    conf.env.ARFLAGS = ["rcs"]

    # Set up C++ tools and flags
    conf.gxx_common_flags()
    conf.cxx_load_tools()
    conf.cxx_add_flags()

    # Also set up C tools and flags
    conf.gcc_common_flags()
    conf.cc_load_tools()
    conf.cc_add_flags()

    # Add linker flags
    conf.link_add_flags()

    # Add the special flags required for emscripten
    conf.env.cshlib_PATTERN = "%s.js"
    conf.env.cxxshlib_PATTERN = "%s.js"
    conf.env.cstlib_PATTERN = "%s.a"
    conf.env.cxxstlib_PATTERN = "%s.a"
    conf.env.cprogram_PATTERN = conf.env.cxxprogram_PATTERN = "%s.js"
    conf.env.CXX_TGT_F = ["-c", "-o", ""]
    conf.env.CC_TGT_F = ["-c", "-o", ""]
    conf.env.CXXLNK_TGT_F = ["-o", ""]
    conf.env.CCLNK_TGT_F = ["-o", ""]
    conf.env.append_value("LINKFLAGS", ["-Wl,--enable-auto-import"])

    # Add our own cxx flags
    conf.env["CXXFLAGS"] += ["-Wextra", "-Wall", "-Wno-warn-absolute-paths"]

    if conf.has_tool_option("cxx_debug") or force_debug:
        conf.env["CXXFLAGS"] += ["-g"]
        conf.env["LINKFLAGS"] += ["-s"]

        # Don't add any optimization flags
        conf.env["MKSPEC_DISABLE_OPTIMIZATION"] = True

    cxxoptflags = ["-O2"]

    if not conf.env["MKSPEC_DISABLE_OPTIMIZATION"]:
        conf.env["CXXFLAGS"] += cxxoptflags

    if conf.has_tool_option("cxx_nodebug"):
        conf.env["DEFINES"] += ["NDEBUG"]

    conf.env["CXXFLAGS"] += ["-std=c++11"]

    if conf.has_tool_option("cxx_debug") or force_debug:
        conf.env["CFLAGS"] += ["-g"]
        # Don't add any optimization flags
        conf.env["MKSPEC_DISABLE_OPTIMIZATION"] = True

    coptflags = ["-O2"]

    if not conf.env["MKSPEC_DISABLE_OPTIMIZATION"]:
        conf.env["CFLAGS"] += coptflags

    # Add our own cc flags
    conf.env["CFLAGS"] += ["-Wextra", "-Wall", "-Wno-warn-absolute-paths"]

    if conf.has_tool_option("cxx_nodebug"):
        conf.env["DEFINES"] += ["NDEBUG"]


@conf
def check_emscripten_version(conf, emscripten_cc, major, minor, minimum):
    try:
        p = subprocess.Popen(
            emscripten_cc + ["--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out = p.communicate()[0]
        cc_major, cc_minor, _ = [int(v) for v in out.split()[4].split(".")]
    except Exception as e:
        conf.fatal("Could not determine the compiler version: {}".format(e))

    cc_version = "{}.{}".format(cc_major, cc_minor)

    if minimum:
        if cc_major < major or (cc_major == major and cc_minor < minor):
            conf.fatal(
                "Compiler version: {0}, "
                "required minimum version: {1}.{2}".format(cc_version, major, minor)
            )
    else:
        if cc_major != major or cc_minor != minor:
            conf.fatal(
                "Wrong compiler version: {0}, "
                "expected version: {1}.{2}".format(cc_version, major, minor)
            )
