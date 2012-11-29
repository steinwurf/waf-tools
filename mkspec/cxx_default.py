#!/usr/bin/env python
# encoding: utf-8

from waflib import Utils
from waflib.Configure import conf
from waflib.Tools import compiler_cxx
from os.path import abspath, expanduser

"""
Detect and setup the default compiler for the platform
"""
def configure(conf):

    # Here we simply try to find a compiler on the current host
    # this code is mostly taken from the "compiler_cxx" tool
    build_platform = Utils.unversioned_sys_platform()
    possible_compiler_list = compiler_cxx.cxx_compiler[build_platform in cxx_compiler and build_platform or 'default']

    """
    Sometimes CXX is a list, and sometimes it is a string.
    This depends tool used to initialize the compiler.
    It is ugly but we deal with it here
    """

    CXX = ""
    if isinstance(conf.env['CXX'], list):
        assert(len(conf.env['CXX']) == 1)
        CXX = conf.env['CXX'][0]
    else:
        CXX = conf.env['CXX']

    # Note clang goes first otherwise 'g++' will be in 'clang(g++)'
    if 'clang' in CXX:
        conf.add_clang_default_flags()
    elif 'g++' in CXX:
        conf.add_gcc_default_flags()
    elif 'CL.exe' in CXX or 'cl.exe' in CXX:
        conf.add_msvc_default_cxxflags()
    else:
        raise Errors.WafError('toolchain_cxx flag for unknown compiler %s'
                              % conf.env.CXX)

@conf
def gcc_check_version(conf, version):
    """
    :param version : The version number as a tuple.
    """
    conf.get_cc_version([conf.env['CXX']], gcc=True)

    if conf.env['CC_VERSION'] != version:
        conf.fatal("Wrong version number, wanted '%r', but got '%r'."
                   % (version, conf.env['CC_VERSION']))

@conf
def get_mkspec_option(conf, option, required=True, error_msg = None):
    try:
        option = conf.env["cxx_mkspec_options"][option]
    except Exception, e:
        if required:
            if error_msg:
                conf.fatal(error_msg)
            else:
                conf.fatal("Missing mkspec-option %s."%e)
        option = None
    return option

@conf
def add_gcc_default_flags(conf):
    conf.env['CXXFLAGS'] += ['-O2','-g','-ftree-vectorize',
                             '-Wextra','-Wall','-std=c++0x']

@conf
def clang_check_version(conf, version):
    """
    Clang is compatible with the gcc way of checking the version.
    """
    conf.gcc_check_version(version)

@conf
def add_clang_default_cxxflags(conf):
    conf.env['CXXFLAGS'] += ['-O2', '-g', '-Wextra', '-Wall', '-std=c++0x']

@conf
def clang_find_binaries(conf, version):
    conf.find_program('clang++', var='CXX')

    conf.clang_check_version(version)

    conf.find_ar()
    conf.gxx_common_flags()
    conf.gxx_modifier_platform()

    conf.cxx_load_tools()
    conf.cxx_add_flags()
    conf.link_add_flags()

    conf.env['LINK_CXX'] = conf.env['CXX']

@conf
def add_android_default_cxxflags(conf):
    conf.env['CXXFLAGS'] += ['-O2','-g','-ftree-vectorize','-Wextra',
                             '-Wall','-std=gnu++0x']

@conf
def android_default_arflags(conf):
    return ['rcs']


@conf
def android_find_binaries(conf, version, path_list):
    conf.gxx_common_flags()
    conf.cxx_load_tools()

    temp_path_list = []

    for p in path_list:
        temp_path_list.append(abspath(expanduser(p)))

    path_list = temp_path_list
    
    # Setup compiler and linker
    conf.find_program('arm-linux-androideabi-g++', path_list=path_list, var='CXX')
    conf.env['LINK_CXX'] = conf.env['CXX']

    conf.gcc_check_version(version)

    conf.find_program('arm-linux-androideabi-gcc', path_list=path_list, var='CC')

    #Setup archiver and archiver flags
    conf.find_program('arm-linux-androideabi-ar', path_list=path_list, var='AR')
    conf.env['ARFLAGS'] = conf.android_default_arflags()

    #Setup android asm
    conf.find_program('arm-linux-androideabi-as', path_list=path_list, var='AS')

    #Setup android nm
    conf.find_program('arm-linux-androideabi-nm', path_list=path_list, var='NM')

    #Setup android ld
    conf.find_program('arm-linux-androideabi-ld', path_list=path_list, var='LD')

@conf
def add_msvc_default_cxxflags(conf):
    conf.env['CXXFLAGS'] += ['/O2', '/Ob2', '/W3', '/MT', '/EHs']
