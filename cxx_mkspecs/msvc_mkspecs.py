#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

from . import msvc_common


@conf
def cxx_msvc12_x64(conf):
    """
    Detect and setup the Microsoft Visual C++ 2013 compiler for 64-bit windows
    """
    if conf.is_mkspec_platform("windows"):
        conf.env.MSVC_TARGETS = ["x86_amd64"]
        conf.mkspec_msvc_configure("12.0")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_msvc12_x86(conf):
    """
    Detect and setup the Microsoft Visual C++ 2013 compiler for 32-bit windows
    """
    if conf.is_mkspec_platform("windows"):
        conf.env.MSVC_TARGETS = ["x86"]
        conf.mkspec_msvc_configure("12.0")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_msvc14_x64(conf):
    """
    Detect and setup the Microsoft Visual C++ 2015 compiler for 64-bit
    """
    if conf.is_mkspec_platform("windows"):
        conf.env.MSVC_TARGETS = ["x86_amd64"]
        conf.mkspec_msvc_configure("14.0")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_msvc14_x86(conf):
    """
    Detect and setup the Microsoft Visual C++ 2015 compiler for 32-bit
    """
    if conf.is_mkspec_platform("windows"):
        conf.env.MSVC_TARGETS = ["x86"]
        conf.mkspec_msvc_configure("14.0")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_msvc15_x64(conf):
    """
    Configure the Visual Studio 2017 (version 15.x) compiler for 64-bit
    """
    if conf.is_mkspec_platform("windows"):
        # The x64 native toolchain is preferred over the x86_amd64 toolchain
        # which is a 32-bit compiler that cross-compiles to 64-bit (Visual
        # Studio 2017 Express only provides x86_amd64, but other versions
        # provide both options)
        conf.env.MSVC_TARGETS = ["x64", "x86_amd64"]
        version = conf.mkspec_find_installed_msvc_version(15)
        conf.mkspec_msvc_configure(version)
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_msvc15_x86(conf):
    """
    Configure the Visual Studio 2017 (version 15.x) compiler for 32-bit
    """
    if conf.is_mkspec_platform("windows"):
        # Use the native x86 toolchain when available, future versions of
        # Visual Studio might only provide amd64_x86, which is a 64-bit
        # compiler that cross-compiles to 32-bit
        conf.env.MSVC_TARGETS = ["x86", "amd64_x86"]
        version = conf.mkspec_find_installed_msvc_version(15)
        conf.mkspec_msvc_configure(version)
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_msvc16_x64(conf):
    """
    Configure the Visual Studio 2019 (version 16.x) compiler for 64-bit
    """
    if conf.is_mkspec_platform("windows"):
        # The x64 native toolchain is preferred over the x86_amd64 toolchain
        # which is a 32-bit compiler that cross-compiles to 64-bit (Visual
        # Studio 2017 Express only provides x86_amd64, but other versions
        # provide both options)
        conf.env.MSVC_TARGETS = ["x64", "x86_amd64"]
        version = conf.mkspec_find_installed_msvc_version(16)
        conf.mkspec_msvc_configure(version)
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_msvc16_x86(conf):
    """
    Configure the Visual Studio 2019 (version 16.x) compiler for 64-bit
    """
    if conf.is_mkspec_platform("windows"):
        # The x64 native toolchain is preferred over the x86_amd64 toolchain
        # which is a 32-bit compiler that cross-compiles to 64-bit (Visual
        # Studio 2017 Express only provides x86_amd64, but other versions
        # provide both options)
        conf.env.MSVC_TARGETS = ["x86", "amd64_x86"]
        version = conf.mkspec_find_installed_msvc_version(16)
        conf.mkspec_msvc_configure(version)
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )
