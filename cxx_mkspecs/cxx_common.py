#!/usr/bin/env python
# encoding: utf-8

import os

from waflib.Configure import conf


@conf
def mkspec_add_common_flag(conf, flag):
    """
    Add common flags.

    :param flag: The flag to be set for C/C++ compiler and linker
    """
    conf.env["CFLAGS"] += [flag]
    conf.env["CXXFLAGS"] += [flag]
    conf.env["LINKFLAGS"] += [flag]


@conf
def mkspec_try_flags(conf, flagtype, flaglist):
    """
    Check support of the given list of compiler/linker flags.

    :param flagtype: The flag type, cflags, cxxflags or linkflags
    :param flaglist: The list of flags to be checked

    :return: The list of supported flags
    """
    ret = []

    for flag in flaglist:
        conf.start_msg("Checking for %s: %s" % (flagtype, flag))
        try:
            if flagtype == "cflags":
                conf.check_cc(cflags=flag)
            elif flagtype == "cxxflags":
                conf.check_cxx(cxxflags=flag)
            elif flagtype == "linkflags":
                conf.check_cxx(linkflags=flag)
        except conf.errors.ConfigurationError:
            conf.end_msg("no", color="YELLOW")
        else:
            conf.end_msg("yes")
            ret.append(flag)

    return ret


@conf
def mkspec_validate_cc_version(conf, major, minor, minimum=False):
    """
    Check the exact or minimum CC version.

    :param major: The major version number, e.g. 4
    :param minor: The minor version number, e.g. 6
    :param minimum: Only check for a minimum compiler version, if true
    """
    cc_major = int(conf.env["CC_VERSION"][0])
    cc_minor = int(conf.env["CC_VERSION"][1])
    cc_version = ".".join(conf.env["CC_VERSION"])

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


@conf
def mkspec_get_toolchain_paths(conf):
    """
    Return the common paths where the g++ binaries are located.

    :return: the common paths where we may find the g++ binary
    """
    # The default path to search
    path_list = os.environ.get("PATH", "").split(os.pathsep)

    if conf.is_mkspec_platform("mac"):

        # If the compiler is installed using macports
        path_list += ["/opt/local/bin"]

    if conf.is_mkspec_platform("android"):
        # If specified, the android_ndk_dir option overrides the OS path
        if conf.has_tool_option("android_ndk_dir"):
            ndk = conf.get_tool_option("android_ndk_dir")
            ndk = os.path.abspath(os.path.expanduser(ndk))
            ndk_path = [ndk, os.path.join(ndk, "bin")]
            return ndk_path

    if conf.is_mkspec_platform("ios"):
        if conf.has_tool_option("ios_toolchain_dir"):
            toolchain = conf.get_tool_option("ios_toolchain_dir")
        else:
            toolchain = (
                "/Applications/Xcode.app/Contents/Developer/"
                "Toolchains/XcodeDefault.xctoolchain/usr/bin/"
            )
        toolchain = os.path.abspath(os.path.expanduser(toolchain))

        return toolchain

    if conf.has_tool_option("poky_sdk_path"):
        sdk_path = conf.get_tool_option("poky_sdk_path")
        cross_compiler = os.path.join(
            sdk_path,
            "sysroots",
            "x86_64-pokysdk-linux",
            "usr",
            "bin",
            "arm-poky-linux-gnueabi",
        )

        path_list = [cross_compiler] + path_list

    return path_list


@conf
def mkspec_set_android_options(conf):
    # The android_sdk_dir option is optional, if adb is in the OS path
    if conf.has_tool_option("android_sdk_dir"):
        sdk = conf.get_tool_option("android_sdk_dir")
        sdk = os.path.abspath(os.path.expanduser(sdk))
        sdk_path = [sdk, os.path.join(sdk, "platform-tools")]
        conf.find_program("adb", path_list=sdk_path, var="ADB")
    else:
        conf.find_program("adb", var="ADB")

    # Set the android define - some libraries rely on this define
    # being present
    conf.env.DEFINES += ["ANDROID"]

    # Add common libraries for Android here
    conf.env["LINKFLAGS"] += ["-llog"]
    # No need to specify 'gnustl_static' or 'gnustl_shared'
    # The Android toolchain will select the appropriate standard library
    # conf.env.LIB_ANDROID = ['gnustl_static']


@conf
def mkspec_set_ios_options(conf, min_ios_version, cpu):

    using_simulator = bool(cpu in ["i386", "x86_64"])

    sdk_type = "iPhoneOS"

    # If cpu is 'i386', then we are building for the iOS simulator
    if using_simulator:
        sdk_type = "iPhoneSimulator"

    if conf.has_tool_option("ios_sdk_dir"):
        sdk = conf.get_tool_option("ios_sdk_dir")
    else:
        # Use the standard location of the iOS SDK
        sdk = (
            "/Applications/Xcode.app/Contents/Developer/Platforms"
            "/{}.platform/Developer/SDKs/{}.sdk".format(sdk_type, sdk_type)
        )
    sdk = os.path.abspath(os.path.expanduser(sdk))

    # Set the IPHONE define - some libraries rely on this define being
    # present
    conf.env.DEFINES += ["IPHONE"]

    # Add common libraries for iOS here
    conf.env["LINKFLAGS"] += ["-lSystem"]  # links with libSystem.dylib

    # Define what are the necessary common compiler and linker options
    # to build for the iOS platform. We tell the ARM cross-compiler
    # to target the specified arm-apple-ios platform triplet, specify
    # the location of the iOS SDK, use the compiler's integrated
    # assembler and set the minimal supported iOS version

    triple = "{}-apple-ios{}.0".format(cpu, min_ios_version)

    ios_version_arg = "-miphoneos-version-min={}"
    if using_simulator:
        ios_version_arg = "-mios-simulator-version-min={}"

    ios_flags = [
        "-target",
        triple,
        "-integrated-as",
        "-isysroot",
        sdk,
        ios_version_arg.format(min_ios_version),
    ]

    conf.env["CFLAGS"] += ios_flags
    conf.env["CXXFLAGS"] += ios_flags
    conf.env["LINKFLAGS"] += ios_flags


@conf
def mkspec_get_ar_binary_name(conf, prefix=None):
    """
    :return: The name of the ar binary we are looking for
             e.g. 'arm-linux-androideabi-ar' for the archiver on android
    """

    binary = "ar"

    if prefix:
        # Toolchains use a specific prefix
        return ["{0}-{1}".format(prefix, binary)]

    return binary


@conf
def mkspec_get_compiler_binary_name(conf, base, major, minor, prefix):
    """
    :param base:   Base compiler name: 'gcc', 'g++', 'clang' or 'clang++'
    :param major:  The major version number of the compiler, e.g. 4
    :param minor:  The minor version number of the compiler, e.g. 8
    :param prefix: Prefix to the compiler name, e.g. 'arm-linux-androideabi'
    :return:       A list of possible compiler names that should be tested,
                   e.g. ['g++-5.4', 'g++-5', 'g++'] for g++ 5.4
    """
    if prefix:
        # Toolchains use a specific prefix, and this should be the only
        # binary name that is tested
        return ["{0}-{1}".format(prefix, base)]

    # waf will test the binary names in order, so the first candidates should
    # include the version number. The list should start with the more
    # specific binary names, e.g. ['g++-5.4', 'g++-5', 'g++']
    binary = ["{0}-{1}.{2}".format(base, major, minor), "{0}-{1}".format(base, major)]

    # The default binary should be available on all platforms, which should
    # be the last candidate after the versioned names
    return binary + [base]
