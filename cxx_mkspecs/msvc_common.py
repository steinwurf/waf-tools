#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import json

from waflib.Configure import conf


@conf
def mkspec_check_minimum_msvc_version(conf, minimum):
    """
    :param minimum: The major version number, e.g. 11.0
    """
    if conf.env["MSVC_VERSION"] < float(minimum):
        conf.fatal(
            "Compiler version: {0}, "
            "required minimum: {1}".format(conf.env["MSVC_VERSION"], minimum)
        )


@conf
def mkspec_find_installed_msvc_version(conf, major_version):
    """
    Return the currently installed version of Visual Studio that matches
    the given major version. We only specify a major version in our mkspecs,
    but the minor version changes frequently with new updates.

    :param major:  The major version number of Visual Studio, e.g. 15
    :return:       The currently installed version, e.g. '15.8' for Visual
                   Studio 2017 (version 15.x)
    """
    current_version = "{}.0".format(major_version)

    # Determine the location of vswhere.exe and print all version info
    try:
        prg_path = os.environ.get(
            "ProgramFiles(x86)",
            os.environ.get("ProgramFiles", "C:\\Program Files (x86)"),
        )
        vswhere = os.path.join(
            prg_path, "Microsoft Visual Studio", "Installer", "vswhere.exe"
        )
        args = [vswhere, "-products", "*", "-legacy", "-format", "json"]
        txt = conf.cmd_and_log(args)
    except Exception as e:
        conf.to_log("msvc_common: vswhere.exe failed")
        conf.to_log(e)
        return current_version

    try:
        data = json.loads(txt)
        # Make sure that the latest version comes first
        data.sort(key=lambda x: x["installationVersion"], reverse=True)
        for entry in data:
            ver = entry["installationVersion"].split(".")
            # Note the first version that matches the major_version
            if int(ver[0]) == major_version:
                current_version = "{}.{}".format(ver[0], ver[1])
                break

    except Exception as e:
        conf.to_log("msvc_common: Failed to find installed version")
        conf.to_log(e)

    return current_version


@conf
def mkspec_msvc_configure(conf, version):

    conf.env.MSVC_VERSIONS = ["msvc %s" % version]

    # Here we suppress all the "Checking for program CL"
    # messages printed by waf when loading the msvc tool
    conf.env.stash()
    conf.start_msg("Checking for msvc %s compiler" % version)
    try:
        conf.load("msvc")
    except conf.errors.ConfigurationError as e:
        conf.env.revert()
        conf.end_msg(False)
        # The error should be raised again to make the configure step fail
        raise e
    else:
        conf.end_msg(conf.env.get_flat("CXX"))
        conf.mkspec_set_msvc_flags()


@conf
def mkspec_set_msvc_flags(conf):

    if conf.has_tool_option("cxx_debug"):
        # Use the multithread, debug version of the run-time library
        conf.env["CXXFLAGS"] += ["/MTd"]
        # Include all debugging information in the .obj files.
        # No .pdb files are produced to prevent warnings.
        conf.env["CXXFLAGS"] += ["/Z7"]

        conf.env["LINKFLAGS"] += ["/DEBUG"]

        # Don't add any optimization flags
        conf.env["MKSPEC_DISABLE_OPTIMIZATION"] = True
    else:
        # Use the multithread, release version of the run-time library
        conf.env["CXXFLAGS"] += ["/MT"]

    # Optimization flags
    optflags = ["/O2"]

    if not conf.env["MKSPEC_DISABLE_OPTIMIZATION"]:
        conf.env["CXXFLAGS"] += optflags

    # Add various defines to suppress deprecation warnings for common
    # functions like strcpy, sprintf and socket API calls
    conf.env["CXXFLAGS"] += [
        "/D_SCL_SECURE_NO_WARNINGS",
        "/D_CRT_SECURE_NO_WARNINGS",
        "/D_WINSOCK_DEPRECATED_NO_WARNINGS",
    ]

    if conf.has_tool_option("cxx_nodebug"):
        conf.env["DEFINES"] += ["NDEBUG"]

    # The /EHs flag only allows standard C++ exceptions (which might also
    # originate from extern "C" functions).
    # Set _WIN32_WINNT=0x0600 (i.e. Windows Vista target) to suppress warnings
    # in Boost Asio.
    # Disabled compiler warnings:
    # - C4503 that complains about the length of decorated template names.
    #   This occurs frequently as we compile heavily templated code, and
    #   we also have to enable /bigobj to allow large object files.
    # - C4312 that warns about assigning a 32-bit value to a 64-bit pointer
    #   type which is commonly used in our unit tests.
    conf.env["CXXFLAGS"] += [
        "/W2",
        "/wd4503",
        "/wd4312",
        "/EHs",
        "/D_WIN32_WINNT=0x0600",
        "/bigobj",
    ]

    # Do not generate .manifest files (the /MANIFEST flag is added by waf)
    conf.env["LINKFLAGS"].remove("/MANIFEST")
    conf.env["LINKFLAGS"] += ["/MANIFEST:NO"]
    conf.env["MSVC_MANIFEST"] = False

    # Disable LNK4221 linker warning for empty object files
    conf.env["LINKFLAGS"] += ["/ignore:4221"]  # used for LINK.exe
    conf.env["ARFLAGS"] += ["/ignore:4221"]  # used for LIB.exe
