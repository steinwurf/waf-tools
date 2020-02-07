#!/usr/bin/env python
# encoding: utf-8

import os

from waflib.Configure import conf

from . import gxx_common


@conf
def cxx_android_gxx49_arm(conf):
    """
    Detect and setup the Android g++ 4.9 compiler for ARM
    """
    conf.mkspec_gxx_android_configure(4, 9, 'arm-linux-androideabi')


@conf
def cxx_android_gxx49_armv7(conf):
    """
    Detect and setup the Android g++ 4.9 compiler for ARMv7
    """
    conf.mkspec_gxx_android_configure(4, 9, 'arm-linux-androideabi')
    # Specify the ARMv7 architecture and the 'softfp' float ABI to compile for
    # hardware FPU, but with software linkage (required for -mfpu=neon flag).
    # The __ARM_NEON__ macro will be defined only if the -mfloat-abi=softfp and
    # -mfpu=neon flags are used together.
    flags = ['-march=armv7-a', '-mtune=generic-armv7-a', '-mfloat-abi=softfp']
    conf.env['CFLAGS'] += flags
    conf.env['CXXFLAGS'] += flags
    # Specify the ARMv7 architecture in the LINKFLAGS to link with the
    # atomic support that is required for std::threads (without this flag,
    # the threading code might call pure virtual methods)
    conf.env['LINKFLAGS'] += ['-march=armv7-a']


@conf
def cxx_android5_gxx49_armv7(conf):
    """
    Detects and setup the Android 5.0+ g++ 4.9 compiler for ARMv7
    """
    conf.cxx_android_gxx49_armv7()
    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    conf.mkspec_add_common_flag('-fPIE')
    conf.env['LINKFLAGS'] += ['-pie']


@conf
def cxx_android5_gxx49_arm64(conf):
    """
    Detects and setup the Android 5.0+ g++ 4.9 compiler for ARM64
    """
    # Note: The arm64 platform was introduced in Android 5 (API Level 21).
    # Therefore the standalone toolchain must be created with the
    # --api=21 option (or above).
    # Only position independent executables (PIE) are supported on Android 5.
    conf.mkspec_gxx_android_configure(4, 9, 'aarch64-linux-android')
    conf.mkspec_add_common_flag('-fPIE')
    conf.env['LINKFLAGS'] += ['-pie']
    # Default "bfd" linker for the arm64 toolchain has an issue with linking
    # shared libraries: https://github.com/android-ndk/ndk/issues/148
    # Force the use of the "gold" linker until it becomes the default
    conf.env['LINKFLAGS'] += ['-fuse-ld=gold']
    conf.env['DEST_CPU'] = 'arm64'


@conf
def cxx_android_gxx49_x86(conf):
    """
    Detect and setup the Android g++ 4.9 compiler for x86
    """
    conf.mkspec_gxx_android_configure(4, 9, 'i686-linux-android')


@conf
def cxx_android5_gxx49_x86(conf):
    """
    Detect and setup the Android 5.0+ g++ 4.9 compiler for x86
    """
    conf.cxx_android_gxx49_x86()
    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    conf.mkspec_add_common_flag('-fPIE')
    conf.env['LINKFLAGS'] += ['-pie']


@conf
def cxx_android5_gxx49_x64(conf):
    """
    Detect and setup the Android 5.0+ g++ 4.9 compiler for x86_64
    """
    # Note: The x86_64 platform was introduced in Android 5 (API Level 21).
    # Therefore the standalone toolchain must be created with the
    # --api=21 option (or above).
    conf.mkspec_gxx_android_configure(4, 9, 'x86_64-linux-android')
    # The PIE binary must be the default in this case
    conf.mkspec_add_common_flag('-fPIE')
    conf.env['LINKFLAGS'] += ['-pie']


@conf
def mkspec_setup_gcov(conf, major, minor, minimum=False):
    """
    Setup g++ for coverage analysis with gcov
    """
    # Don't add any optimization flags (these might lead to incorrect results)
    conf.env['MKSPEC_DISABLE_OPTIMIZATION'] = True

    conf.mkspec_gxx_configure(major, minor, minimum=minimum)

    # Set flag to compile and link code instrumented for coverage analysis
    conf.mkspec_add_common_flag('--coverage')

    # Add flags to disable optimization and all function inlining
    flags = ['-O0', '-fPIC', '-fno-inline', '-fno-inline-small-functions',
             '-fno-default-inline']
    conf.env['CFLAGS'] += flags
    conf.env['CXXFLAGS'] += flags


@conf
def cxx_gcov_default(conf):
    """
    Configure the default g++ for coverage analysis with gcov
    """
    conf.mkspec_setup_gcov(4, 9, minimum=True)


@conf
def cxx_gxx49_x64(conf):
    """
    Detect and setup the g++ 4.9 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(4, 9)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx49_x86(conf):
    """
    Detect and setup the g++ 4.9 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(4, 9)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx52_x64(conf):
    """
    Detect and setup the g++ 5.2 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(5, 2)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx52_x86(conf):
    """
    Detect and setup the g++ 5.2 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(5, 2)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx53_x64(conf):
    """
    Detect and setup the g++ 5.3 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(5, 3)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx53_x86(conf):
    """
    Detect and setup the g++ 5.3 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(5, 3)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx54_x64(conf):
    """
    Detect and setup the g++ 5.4 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(5, 4)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx54_x86(conf):
    """
    Detect and setup the g++ 5.4 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(5, 4)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx60_x64(conf):
    """
    Detect and setup the g++ 6.0 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(6, 0)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx60_x86(conf):
    """
    Detect and setup the g++ 6.0 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(6, 0)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx61_x64(conf):
    """
    Detect and setup the g++ 6.1 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(6, 1)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx61_x86(conf):
    """
    Detect and setup the g++ 6.1 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(6, 1)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx62_x64(conf):
    """
    Detect and setup the g++ 6.2 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(6, 2)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx62_x86(conf):
    """
    Detect and setup the g++ 6.2 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(6, 2)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx63_x64(conf):
    """
    Detect and setup the g++ 6.3 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(6, 3)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx63_x86(conf):
    """
    Detect and setup the g++ 6.3 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(6, 3)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx72_x64(conf):
    """
    Detect and setup the g++ 7.2 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(7, 2)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx72_x86(conf):
    """
    Detect and setup the g++ 7.2 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(7, 2)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx73_x64(conf):
    """
    Detect and setup the g++ 7.3 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(7, 3)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx73_x86(conf):
    """
    Detect and setup the g++ 7.3 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(7, 3)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx74_x64(conf):
    """
    Detect and setup the g++ 7.4 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(7, 4)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx74_x86(conf):
    """
    Detect and setup the g++ 7.4 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(7, 4)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx81_x64(conf):
    """
    Detect and setup the g++ 8.1 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(8, 1)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx81_x86(conf):
    """
    Detect and setup the g++ 8.1 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(8, 1)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx82_x64(conf):
    """
    Detect and setup the g++ 8.2 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(8, 2)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx82_x86(conf):
    """
    Detect and setup the g++ 8.2 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(8, 2)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx83_x64(conf):
    """
    Detect and setup the g++ 8.3 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(8, 3)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx83_x86(conf):
    """
    Detect and setup the g++ 8.3 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(8, 3)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx92_x64(conf):
    """
    Detect and setup the g++ 9.2 compiler for 64 bit
    """
    conf.mkspec_gxx_configure(9, 2)
    conf.mkspec_add_common_flag('-m64')


@conf
def cxx_gxx92_x86(conf):
    """
    Detect and setup the g++ 9.2 compiler for 32 bit
    """
    conf.mkspec_gxx_configure(9, 2)
    conf.mkspec_add_common_flag('-m32')


@conf
def cxx_gxx63_armv7(conf):
    """
    Detect and setup the g++ 6.3 cross-compiler for ARM Linux running on ARMv7
    CPU with a hardware FPU. The 'g++-arm-linux-gnueabihf' Debian package
    should provide a compatible toolchain, or the standalone version can be
    downloaded from the Linaro releases:
    https://releases.linaro.org/components/toolchain/binaries/latest/arm-linux-gnueabihf/
    """
    conf.mkspec_gxx_configure(6, 3, 'arm-linux-gnueabihf')
    # Specify the ARMv7 architecture in the LINKFLAGS to link with the
    # atomic support that is required for std::threads (without this flag,
    # the threading code might call pure virtual methods)
    conf.env['LINKFLAGS'] += ['-march=armv7-a']
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']
    # Set the target CPU
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_gxx63_armv7_softfp(conf):
    """
    Detect and setup the g++ 6.3 cross-compiler for ARM Linux running on ARMv7
    CPU with a hardware FPU, but on a system where a soft-float ABI is required.
    The 'g++-arm-linux-gnueabi' Debian package should provide a compatible
    toolchain, or the standalone version can be  downloaded from the Linaro
    releases:
    https://releases.linaro.org/components/toolchain/binaries/latest/arm-linux-gnueabi/
    """
    conf.mkspec_gxx_configure(6, 3, 'arm-linux-gnueabi')
    # Specify the ARMv7 architecture and the 'softfp' float ABI to compile for
    # hardware FPU, but with software linkage (required for -mfpu=neon flag).
    # The __ARM_NEON__ macro will be defined only if the -mfloat-abi=softfp and
    # -mfpu=neon flags are used together.
    flags = ['-march=armv7-a', '-mfloat-abi=softfp']
    conf.env['CFLAGS'] += flags
    conf.env['CXXFLAGS'] += flags
    # Specify the ARMv7 architecture in the LINKFLAGS to link with the
    # atomic support that is required for std::threads (without this flag,
    # the threading code might call pure virtual methods)
    conf.env['LINKFLAGS'] += ['-march=armv7-a']
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']
    # Set the target CPU
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_raspberry_gxx49_arm(conf):
    """
    Detect and setup the g++ 4.9 cross-compiler for Raspberry Pi (Linux)
    """
    conf.mkspec_gxx_configure(4, 9, 'raspberry-gxx49-arm')
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']
    # Set the target CPU
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_raspberry_gxx49_armv7(conf):
    """
    Detect and setup the g++ 4.9 cross-compiler for Raspberry Pi (Linux)
    running on ARMv7 compatible hardware (Raspberry Pi 2)
    """
    conf.mkspec_gxx_configure(4, 9, 'raspberry-gxx49-arm')
    # atomic support that is required for std::threads (without this flag,
    # the threading code might call pure virtual methods)
    conf.env['LINKFLAGS'] += ['-march=armv7-a']
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']
    # Set the target CPU
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_musl_gxx91_armv7(conf):
    """
    Detect and setup the g++ 9.1 cross-compiler for MUSL Libc
    running on ARMv7 compatible hardware (Raspberry Pi 3)

    A toolchain can be downloaded from: https://musl.cc/
    """
    conf.mkspec_gxx_configure(9, 1, 'armv7l-linux-musleabihf')
    # atomic support that is required for std::threads (without this flag,
    # the threading code might call pure virtual methods)
    conf.env['LINKFLAGS'] += ['-march=armv7-a']
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']
    # Set the target CPU
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_musl_gxx54_armv5(conf):
    """
    Detect and setup the g++ 5.4 cross-compiler for MUSL Libc
    running on ARMv7 compatible hardware (Raspberry Pi 3)

    A toolchain can be downloaded from: https://musl.cc/
    """
    conf.mkspec_gxx_configure(5, 4, 'arm-linux')
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']
    conf.env['CXXFLAGS'] += ['-std=c++14']
    # Set the target CPU
    conf.env['DEST_CPU'] = 'arm'


@conf
def cxx_musl_gxx91_x86_64(conf):
    """
    Detect and setup the g++ 9.1 compiler for MUSL Libc
    running on x86-64

    A toolchain can be downloaded from: https://musl.cc/
    """
    conf.mkspec_gxx_configure(9, 1, 'x86_64-linux-musl')
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']


@conf
def cxx_openwrt_gxx53_arm(conf):
    """
    Detect and setup the g++ 5.3 cross-compiler for OpenWRT ARM
    """
    conf.mkspec_gxx_configure(5, 3, 'arm-openwrt-linux')
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']


@conf
def cxx_openwrt_gxx53_mips(conf):
    """
    Detect and setup the g++ 5.3 cross-compiler for OpenWRT MIPS
    """
    conf.mkspec_gxx_configure(5, 3, 'mips-openwrt-linux')
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']


@conf
def cxx_openwrt_gxx73_armv7(conf):
    """
    Detect and setup the g++ 7.3 cross-compiler for OpenWRT ARM
    """
    conf.mkspec_gxx_configure(7, 3, 'arm-openwrt-linux')
    # Enable atomic support (without these flags, the linker might have
    # undefined references to atomic functions)
    conf.env['LINKFLAGS'] += ['-march=armv7-a', '-latomic']
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']


@conf
def cxx_openwrt_gxx73_mips(conf):
    """
    Detect and setup the g++ 7.3 cross-compiler for OpenWRT MIPS
    """
    conf.mkspec_gxx_configure(7, 3, 'mips-openwrt-linux')
    # Enable atomic support (without these flags, the linker might have
    # undefined references to atomic functions)
    conf.env['LINKFLAGS'] += ['-latomic']
    # Note: libstdc++ might not be available on the target platform
    # Statically link with the C++ standard library
    conf.env['LINKFLAGS'] += ['-static-libstdc++']


@conf
def cxx_poky_gxx63_armv7(conf):
    """
    Detect and setup the g++ 6.3 cross compiler for the
    Yocto based Poky distribution.
    """

    conf.mkspec_gxx_configure(
        major=6, minor=3, prefix='arm-poky-linux-gnueabi')

    # Note: A static version of libstdc++ is not available in the
    # poky SDK so we cannot use -static-libstdc++ for statically
    # linking.

    flags = ['-march=armv7-a', '-marm', '-mfpu=neon',
             '-mfloat-abi=hard', '-mcpu=cortex-a9']

    if conf.has_tool_option('poky_sdk_path'):
        sdk_path = conf.get_tool_option('poky_sdk_path')

        sysroot = os.path.join(
            sdk_path, 'sysroots', 'cortexa9hf-neon-poky-linux-gnueabi')

        flags.append('--sysroot=%s' % sysroot)

    conf.env['LINKFLAGS'] += flags
    conf.env['CXXFLAGS'] += flags

    # Set the target CPU
    conf.env['DEST_CPU'] = 'arm'
