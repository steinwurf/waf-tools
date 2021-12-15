#!/usr/bin/env python
# encoding: utf-8

"""
Set the soname of the shared libraries built to the library name itself.

Not setting the soname can cause problems, see this issue:
https://github.com/android-ndk/ndk/issues/177 as this may result in invalid
DT_NEEDED entries in the resulting binary.

According to this pull-request:
https://github.com/moritz-wundke/Boost-for-Android/issues/44, and the links to
the various discussion forums in it, Android will not support versioning in the
soname so for this reason we should not use the waf vnum feature for Android
libraries.

Instead we should simply specify the real file e.g. libfoo.so as soname.

To verify the soname is correctly specified you can use readelf:

    readelf -d build/cxx_android_gxx49_armv7/libfoo.so

The -d will show the dynamic section of the ELF binary, look for an entry in
the type column saying (SONAME) and check its Name/Value column.
"""

from waflib.TaskGen import feature, after_method


@feature("cshlib", "cxxshlib")
@after_method("apply_link")
def set_android_soname(self):
    """
    Task generator method, which will run after the apply_link method.

    The apply_link method is the one creating the link_task.
    """
    # We only set the soname if this is an Android build.
    if not self.bld.is_mkspec_platform("android"):
        return

    # Fetch the library name
    node = self.link_task.outputs[0]

    # Add the soname for the ld linker - to disable, unset env.SONAME_ST
    if self.env.SONAME_ST:
        linker_flag = self.env.SONAME_ST % node.name
        self.env.append_value("LINKFLAGS", linker_flag)
