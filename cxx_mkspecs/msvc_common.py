#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from waflib.Logs import debug


@conf
def mkspec_check_minimum_msvc_version(conf, minimum):
    """
    :param minimum: The major version number, e.g. 11.0
    """
    if (conf.env['MSVC_VERSION'] < float(minimum)):
        conf.fatal("Compiler version: {0}, "
                   "required minimum: {1}"
                   .format(conf.env['MSVC_VERSION'], minimum))


@conf
def mkspec_msvc_configure(conf, version):

    conf.env.MSVC_VERSIONS = ['msvc %s' % version]

    # Here we suppress all the "Checking for program CL"
    # messages printed by waf when loading the msvc tool
    conf.env.stash()
    conf.start_msg('Checking for msvc %s compiler' % version)
    try:
        conf.load('msvc')
    except conf.errors.ConfigurationError as e:
        conf.env.revert()
        conf.end_msg(False)
        # The error should be raised again to make the configure step fail
        raise e
    else:
        conf.end_msg(conf.env.get_flat('CXX'))
        conf.mkspec_set_msvc_flags()


@conf
def mkspec_set_msvc_flags(conf):

    if conf.has_tool_option('cxx_debug'):
        # Use the multithread, debug version of the run-time library
        conf.env['CXXFLAGS'] += ['/MTd']
        # Include all debugging information in the .obj files.
        # No .pdb files are produced to prevent warnings.
        conf.env['CXXFLAGS'] += ['/Z7']

        conf.env['LINKFLAGS'] += ['/DEBUG']
    else:
        # Use the multithread, release version of the run-time library
        conf.env['CXXFLAGS'] += ['/MT']

    # Add various defines to suppress deprecation warnings for common
    # functions like strcpy, sprintf and socket API calls
    conf.env['CXXFLAGS'] += \
        ['/D_SCL_SECURE_NO_WARNINGS', '/D_CRT_SECURE_NO_WARNINGS',
         '/D_WINSOCK_DEPRECATED_NO_WARNINGS']

    if conf.has_tool_option('cxx_nodebug'):
        conf.env['DEFINES'] += ['NDEBUG']

    # The /EHs flag only allows standard C++ exceptions (which might also
    # originate from extern "C" functions).
    # Set _WIN32_WINNT=0x0501 (i.e. Windows XP target) to suppress warnings
    # in Boost Asio.
    # Disabled compiler warnings:
    # - C4503 that complains about the length of decorated template names.
    #   This occurs frequently as we compile heavily templated code, and
    #   we also have to enable /bigobj to allow large object files.
    # - C4312 that warns about assigning a 32-bit value to a 64-bit pointer
    #   type which is commonly used in our unit tests.
    conf.env['CXXFLAGS'] += \
        ['/O2', '/W2', '/wd4503', '/wd4312',
         '/EHs', '/D_WIN32_WINNT=0x0501', '/bigobj']

    # Do not generate .manifest files (the /MANIFEST flag is added by waf)
    conf.env['LINKFLAGS'].remove('/MANIFEST')
    conf.env['LINKFLAGS'] += ['/MANIFEST:NO']
    conf.env['MSVC_MANIFEST'] = False

    # Disable LNK4221 linker warning for empty object files
    conf.env['LINKFLAGS'] += ['/ignore:4221']  # used for LINK.exe
    conf.env['ARFLAGS'] += ['/ignore:4221']  # used for LIB.exe
