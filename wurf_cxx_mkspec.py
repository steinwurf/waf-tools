#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib.Configure import conf

import cxx_mkspecs.cxx_default
import cxx_mkspecs.clang_mkspecs
import cxx_mkspecs.gxx_mkspecs
import cxx_mkspecs.msvc_mkspecs
import cxx_mkspecs.emscripten_mkspecs

# Allows us to catch queries for platforms that we do not yet support
mkspec_platforms = ["windows", "linux", "android", "mac", "ios", "emscripten"]


@conf
def get_mkspec_platform(conf):
    # If the MKSPEC_PLATFORM is not set, we auto detect it.
    if not conf.env["MKSPEC_PLATFORM"]:
        platform = Utils.unversioned_sys_platform()
        if platform == "win32":
            platform = "windows"
        elif platform == "darwin":
            platform = "mac"
        conf.set_mkspec_platform(platform)

    return conf.env["MKSPEC_PLATFORM"]


@conf
def set_mkspec_platform(conf, platform):
    if conf.env["MKSPEC_PLATFORM"]:
        conf.fatal(
            "The mkspec platform could not be set to {0}, as it was "
            "already set to {1}.".format(platform, conf.env["MKSPEC_PLATFORM"])
        )

    if platform not in mkspec_platforms:
        conf.fatal(
            "The mkspec platform {0} is not supported."
            " Current platform is {1}".format(platform, conf.env["MKSPEC_PLATFORM"])
        )

    conf.env["MKSPEC_PLATFORM"] = platform


@conf
def is_mkspec_platform(conf, platform):
    return conf.get_mkspec_platform() == platform


def options(opt):

    opts = opt.add_option_group("Makespec options")

    opts.add_option(
        "--cxx_mkspec",
        default=None,
        dest="cxx_mkspec",
        help="Select a C++ make specification (which can include a specific "
        "platform, compiler and CPU architecture)",
    )

    opts.add_option(
        "--cxx_debug",
        default=None,
        dest="cxx_debug",
        action="store_true",
        help="Defines compiler flags for a debug build",
    )

    opts.add_option(
        "--cxx_nodebug",
        default=None,
        dest="cxx_nodebug",
        action="store_true",
        help='Defines the "NDEBUG" compiler flag',
    )

    opts.add_option(
        "--cflags",
        default=None,
        dest="cflags",
        help="Defines extra flags for the C compiler "
        '(use the ";" character between flags)',
    )

    opts.add_option(
        "--cxxflags",
        default=None,
        dest="cxxflags",
        help="Defines extra flags for the C++ compiler "
        '(use the ";" character between flags)',
    )

    opts.add_option(
        "--linkflags",
        default=None,
        dest="linkflags",
        help="Defines extra flags for the linker "
        '(use the ";" character between flags)',
    )

    opts.add_option(
        "--commonflags",
        default=None,
        dest="commonflags",
        help="Defines extra flags for the C/C++ compiler and the linker "
        '(use the ";" character between flags)',
    )

    opts.add_option(
        "--android_sdk_dir",
        default=None,
        dest="android_sdk_dir",
        help="Path to the Android SDK (not required if ADB is in the PATH)",
    )

    opts.add_option(
        "--android_ndk_dir",
        default=None,
        dest="android_ndk_dir",
        help="Path to the standalone Android toolchain (the standard NDK "
        "is not supported)",
    )

    opts.add_option(
        "--ios_sdk_dir",
        default=None,
        dest="ios_sdk_dir",
        help="Path to the iOS SDK (not required if XCode is installed to "
        "the default location)",
    )

    opts.add_option(
        "--ios_toolchain_dir",
        default=None,
        dest="ios_toolchain_dir",
        help="Path to the iOS toolchain (not required if XCode is installed "
        "to the default location)",
    )

    opts.add_option(
        "--emscripten_path",
        default=None,
        dest="emscripten_path",
        help="Path to the Emscripten compiler (em++)",
    )

    opts.add_option(
        "--poky_sdk_path",
        default=None,
        dest="poky_sdk_path",
        help="Path to the Yocto-based cross-compiler toolchain for the "
        "Poky distribution. Tested with the Gateworks Yocto SDK.",
    )


def configure(conf):

    # Which mkspec should we use, by default, use the cxx_default
    # that simply fallbacks to use waf auto detect of compiler etc.
    mkspec = "cxx_default"

    if conf.has_tool_option("cxx_mkspec"):
        mkspec = conf.get_tool_option("cxx_mkspec")

    conf.msg("Using the mkspec:", mkspec)

    # Additional flags for C/C++ compiler and linker
    if conf.has_tool_option("cflags"):
        conf.env["CFLAGS"] += conf.get_tool_option("cflags").split(";")
    if conf.has_tool_option("cxxflags"):
        conf.env["CXXFLAGS"] += conf.get_tool_option("cxxflags").split(";")
    if conf.has_tool_option("linkflags"):
        conf.env["LINKFLAGS"] += conf.get_tool_option("linkflags").split(";")

    # Common flags to be set for C/C++ compiler and linker
    if conf.has_tool_option("commonflags"):
        conf.env["CFLAGS"] += conf.get_tool_option("commonflags").split(";")
        conf.env["CXXFLAGS"] += conf.get_tool_option("commonflags").split(";")
        conf.env["LINKFLAGS"] += conf.get_tool_option("commonflags").split(";")

    # Find and call the mkspec function on the conf object
    if hasattr(conf, mkspec):
        getattr(conf, mkspec)()
    else:
        conf.fatal("The mkspec is not available: {0}".format(mkspec))
