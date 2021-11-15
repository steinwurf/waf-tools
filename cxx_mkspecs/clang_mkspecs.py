#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

from . import clang_common


@conf
def cxx_android_clang38_armv7(conf):
    """
    Detect and setup the Android clang 3.8 compiler for ARMv7
    """
    conf.mkspec_clang_android_configure(3, 8, prefix="arm-linux-androideabi")
    conf.env["DEST_CPU"] = "arm"


@conf
def cxx_android_clang50_armv7(conf):
    """
    Detect and setup the Android clang 5.0 compiler for ARMv7
    """
    conf.mkspec_clang_android_configure(5, 0, prefix="arm-linux-androideabi")
    conf.env["DEST_CPU"] = "arm"


@conf
def cxx_android_clang70_armv7(conf):
    """
    Detect and setup the Android clang 7.0 compiler for ARMv7
    """
    conf.mkspec_clang_android_configure(7, 0, prefix="arm-linux-androideabi")
    conf.env["DEST_CPU"] = "arm"
    # Note: libc++_shared.so is not available on the target platform, so
    # we force the linker to select the static version of libstdc++ (which is
    # actually libc++ in NDK r17+)
    conf.env["LINKFLAGS"] += ["-static-libstdc++"]


@conf
def cxx_android_clang80_armv7(conf):
    """
    Detect and setup the Android clang 8.0 compiler for ARMv7
    """
    conf.mkspec_clang_android_configure(8, 0, prefix="arm-linux-androideabi")
    conf.env["DEST_CPU"] = "arm"
    # Note: libc++_shared.so is not available on the target platform, so
    # we force the linker to select the static version of libstdc++ (which is
    # actually libc++ in NDK r17+)
    conf.env["LINKFLAGS"] += ["-static-libstdc++"]


@conf
def cxx_android5_clang38_armv7(conf):
    """
    Detects and setup the Android 5.0+ clang 3.8 compiler for ARMv7
    """
    conf.cxx_android_clang38_armv7()
    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]


@conf
def cxx_android5_clang50_armv7(conf):
    """
    Detects and setup the Android 5.0+ clang 5.0 compiler for ARMv7
    """
    conf.cxx_android_clang50_armv7()
    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]


@conf
def cxx_android5_clang70_armv7(conf):
    """
    Detects and setup the Android 5.0+ clang 7.0 compiler for ARMv7
    """
    conf.cxx_android_clang70_armv7()
    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]
    # Note: libc++_shared.so is not available on the target platform, so
    # we force the linker to select the static version of libstdc++ (which is
    # actually libc++ in NDK r17+)
    conf.env["LINKFLAGS"] += ["-static-libstdc++"]


@conf
def cxx_android5_clang80_armv7(conf):
    """
    Detects and setup the Android 5.0+ clang 8.0 compiler for ARMv7
    """
    conf.cxx_android_clang80_armv7()
    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]
    # Note: libc++_shared.so is not available on the target platform, so
    # we force the linker to select the static version of libstdc++ (which is
    # actually libc++ in NDK r17+)
    conf.env["LINKFLAGS"] += ["-static-libstdc++"]


@conf
def cxx_android5_clang38_arm64(conf):
    """
    Detects and setup the Android 5.0+ clang 3.8 compiler for ARM64
    """
    # Note: The arm64 platform was introduced in Android 5 (API Level 21).
    # Therefore the standalone toolchain must be created with the
    # --api=21 option (or above).
    conf.mkspec_clang_android_configure(3, 8, prefix="aarch64-linux-android")
    conf.env["DEST_CPU"] = "arm64"
    # Only position independent executables (PIE) are supported on Android 5.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]
    # Default "bfd" linker for the arm64 toolchain has an issue with linking
    # shared libraries: https://github.com/android-ndk/ndk/issues/148
    # Force the use of the "gold" linker until it becomes the default
    conf.env["LINKFLAGS"] += ["-fuse-ld=gold"]


@conf
def cxx_android5_clang50_arm64(conf):
    """
    Detects and setup the Android 5.0+ clang 5.0 compiler for ARM64
    """
    # Note: The arm64 platform was introduced in Android 5 (API Level 21).
    # Therefore the standalone toolchain must be created with the
    # --api=21 option (or above).
    conf.mkspec_clang_android_configure(5, 0, prefix="aarch64-linux-android")
    conf.env["DEST_CPU"] = "arm64"
    # Only position independent executables (PIE) are supported on Android 5.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]
    # Default "bfd" linker for the arm64 toolchain has an issue with linking
    # shared libraries: https://github.com/android-ndk/ndk/issues/148
    # Force the use of the "gold" linker until it becomes the default
    conf.env["LINKFLAGS"] += ["-fuse-ld=gold"]


@conf
def cxx_android5_clang70_arm64(conf):
    """
    Detects and setup the Android 5.0+ clang 7.0 compiler for ARM64
    """
    # Note: The arm64 platform was introduced in Android 5 (API Level 21).
    # Therefore the standalone toolchain must be created with the
    # --api=21 option (or above).
    conf.mkspec_clang_android_configure(7, 0, prefix="aarch64-linux-android")
    conf.env["DEST_CPU"] = "arm64"
    # Only position independent executables (PIE) are supported on Android 5.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]
    # Default "bfd" linker for the arm64 toolchain has an issue with linking
    # shared libraries: https://github.com/android-ndk/ndk/issues/148
    # Force the use of the "gold" linker until it becomes the default
    conf.env["LINKFLAGS"] += ["-fuse-ld=gold"]
    # Note: libc++_shared.so is not available on the target platform, so
    # we force the linker to select the static version of libstdc++ (which is
    # actually libc++ in NDK r17+)
    conf.env["LINKFLAGS"] += ["-static-libstdc++"]


@conf
def cxx_android5_clang38_x86(conf):
    """
    Detects and setup the Android 5.0+ clang 3.8 compiler for x86
    """
    conf.mkspec_clang_android_configure(3, 8, prefix="i686-linux-android")

    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]


@conf
def cxx_android5_clang50_x86(conf):
    """
    Detects and setup the Android 5.0+ clang 5.0 compiler for x86
    """
    conf.mkspec_clang_android_configure(5, 0, prefix="i686-linux-android")

    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]


@conf
def cxx_android5_clang70_x86(conf):
    """
    Detects and setup the Android 5.0+ clang 7.0 compiler for x86
    """
    conf.mkspec_clang_android_configure(7, 0, prefix="i686-linux-android")

    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]
    # Note: libc++_shared.so is not available on the target platform, so
    # we force the linker to select the static version of libstdc++ (which is
    # actually libc++ in NDK r17+)
    conf.env["LINKFLAGS"] += ["-static-libstdc++"]


@conf
def cxx_android5_clang38_x64(conf):
    """
    Detects and setup the Android 5.0+ clang 3.8 compiler for x64
    """
    # Note: The x86_64 platform was introduced in Android 5 (API Level 21).
    # Therefore the standalone toolchain must be created with the
    # --api=21 option (or above).
    conf.mkspec_clang_android_configure(3, 8, prefix="x86_64-linux-android")

    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]


@conf
def cxx_android5_clang50_x64(conf):
    """
    Detects and setup the Android 5.0+ clang 5.0 compiler for x64
    """
    # Note: The x86_64 platform was introduced in Android 5 (API Level 21).
    # Therefore the standalone toolchain must be created with the
    # --api=21 option (or above).
    conf.mkspec_clang_android_configure(5, 0, prefix="x86_64-linux-android")

    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]


@conf
def cxx_android5_clang70_x64(conf):
    """
    Detects and setup the Android 5.0+ clang 7.0 compiler for x64
    """
    # Note: The x86_64 platform was introduced in Android 5 (API Level 21).
    # Therefore the standalone toolchain must be created with the
    # --api=21 option (or above).
    conf.mkspec_clang_android_configure(7, 0, prefix="x86_64-linux-android")

    # Only position independent executables (PIE) are supported on Android 5
    # and above. The oldest version that can run a PIE binary is Android 4.1,
    # so the binary will segfault on all older platforms.
    # The -fPIC flag is automatically enabled for Android, so we only have to
    # add the -pie flag. This is only necessary when building programs.
    conf.env["LINKFLAGS_cprogram"] = ["-pie"]
    conf.env["LINKFLAGS_cxxprogram"] = ["-pie"]
    # Note: libc++_shared.so is not available on the target platform, so
    # we force the linker to select the static version of libstdc++ (which is
    # actually libc++ in NDK r17+)
    conf.env["LINKFLAGS"] += ["-static-libstdc++"]


@conf
def cxx_apple_llvm80_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 8.0 compiler
    """
    if conf.is_mkspec_platform("mac"):
        conf.mkspec_clang_configure(8, 0)
        conf.mkspec_add_common_flag("-m64")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_apple_llvm81_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 8.1 compiler
    """
    if conf.is_mkspec_platform("mac"):
        conf.mkspec_clang_configure(8, 1)
        conf.mkspec_add_common_flag("-m64")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_apple_llvm90_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 9.0 compiler
    """
    if conf.is_mkspec_platform("mac"):
        conf.mkspec_clang_configure(9, 0)
        conf.mkspec_add_common_flag("-m64")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_apple_llvm91_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 9.1 compiler
    """
    if conf.is_mkspec_platform("mac"):
        conf.mkspec_clang_configure(9, 1)
        conf.mkspec_add_common_flag("-m64")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_apple_llvm100_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 10.0 compiler
    """
    if conf.is_mkspec_platform("mac"):
        conf.mkspec_clang_configure(10, 0)
        conf.mkspec_add_common_flag("-m64")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_apple_llvm120_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 12.0 compiler
    """
    if conf.is_mkspec_platform("mac"):
        conf.mkspec_clang_configure(12, 0)
        conf.mkspec_add_common_flag("-m64")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_apple_llvm130_x64(conf):
    """
    Detect and setup the 64-bit Apple LLVM 13.0 compiler
    """
    if conf.is_mkspec_platform("mac"):
        conf.mkspec_clang_configure(13, 0)
        conf.mkspec_add_common_flag("-m64")
    else:
        conf.fatal(
            "This mkspec is not supported on {0}.".format(conf.get_mkspec_platform())
        )


@conf
def cxx_clang36_x64(conf):
    """
    Detect and setup the clang 3.6 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 6)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang36_x86(conf):
    """
    Detect and setup the clang 3.6 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 6)
    conf.mkspec_add_common_flag("-m32")


@conf
def cxx_clang37_x64(conf):
    """
    Detect and setup the clang 3.7 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 7)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang37_x86(conf):
    """
    Detect and setup the clang 3.7 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 7)
    conf.mkspec_add_common_flag("-m32")


@conf
def cxx_clang38_x64(conf):
    """
    Detect and setup the clang 3.8 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 8)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang38_x86(conf):
    """
    Detect and setup the clang 3.8 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 8)
    conf.mkspec_add_common_flag("-m32")


@conf
def cxx_clang39_x64(conf):
    """
    Detect and setup the clang 3.9 compiler for 64 bit
    """
    conf.mkspec_clang_configure(3, 9)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang39_x86(conf):
    """
    Detect and setup the clang 3.9 compiler for 32 bit
    """
    conf.mkspec_clang_configure(3, 9)
    conf.mkspec_add_common_flag("-m32")


@conf
def cxx_clang40_x64(conf):
    """
    Detect and setup the clang 4.0 compiler for 64 bit
    """
    conf.mkspec_clang_configure(4, 0)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang40_x86(conf):
    """
    Detect and setup the clang 4.0 compiler for 32 bit
    """
    conf.mkspec_clang_configure(4, 0)
    conf.mkspec_add_common_flag("-m32")


@conf
def cxx_clang50_x64(conf):
    """
    Detect and setup the clang 5.0 compiler for 64 bit
    """
    conf.mkspec_clang_configure(5, 0)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang50_x86(conf):
    """
    Detect and setup the clang 5.0 compiler for 32 bit
    """
    conf.mkspec_clang_configure(5, 0)
    conf.mkspec_add_common_flag("-m32")


@conf
def cxx_clang60_x64(conf):
    """
    Detect and setup the clang 6.0 compiler for 64 bit
    """
    conf.mkspec_clang_configure(6, 0)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang60_x86(conf):
    """
    Detect and setup the clang 6.0 compiler for 32 bit
    """
    conf.mkspec_clang_configure(6, 0)
    conf.mkspec_add_common_flag("-m32")


@conf
def cxx_clang70_x64(conf):
    """
    Detect and setup the clang 7.0 compiler for 64 bit
    """
    conf.mkspec_clang_configure(7, 0)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang70_x86(conf):
    """
    Detect and setup the clang 7.0 compiler for 32 bit
    """
    conf.mkspec_clang_configure(7, 0)
    conf.mkspec_add_common_flag("-m32")


@conf
def cxx_clang100_x64(conf):
    """
    Detect and setup the clang 10.0 compiler for 64 bit
    """
    conf.mkspec_clang_configure(10, 0)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_clang130_x64(conf):
    """
    Detect and setup the clang 13.0 compiler for 64 bit
    """
    conf.mkspec_clang_configure(13, 0)
    conf.mkspec_add_common_flag("-m64")


@conf
def cxx_ios70_apple_llvm_armv7(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 armv7
    """
    conf.mkspec_clang_ios_configure(6, 1, "7.0", "armv7", minimum=True)
    conf.env["DEST_CPU"] = "arm"


@conf
def cxx_ios70_apple_llvm_armv7s(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 armv7s
    """
    conf.mkspec_clang_ios_configure(6, 1, "7.0", "armv7s", minimum=True)
    conf.env["DEST_CPU"] = "arm"


@conf
def cxx_ios70_apple_llvm_arm64(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 arm64
    """
    conf.mkspec_clang_ios_configure(6, 1, "7.0", "arm64", minimum=True)
    conf.env["DEST_CPU"] = "arm64"


@conf
def cxx_ios70_apple_llvm_i386(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 i386 (simulator)
    """
    conf.mkspec_clang_ios_configure(6, 1, "7.0", "i386", minimum=True)


@conf
def cxx_ios70_apple_llvm_x86_64(conf):
    """
    Detect and setup the Apple LLVM compiler for iOS 7.0 x86_64 (simulator)
    """
    conf.mkspec_clang_ios_configure(6, 1, "7.0", "x86_64", minimum=True)


@conf
def mkspec_setup_clang_address_sanitizer(conf, major, minor, arch, minimum=False):
    """
    To get a reasonable performance add -O1 or higher. To get nicer
    stack traces in error messages add -fno-omit-frame-pointer. To get
    perfect stack traces you may need to disable inlining (just use
    -O1) and tail call elimination (-fno-optimize-sibling-calls).
    http://clang.llvm.org/docs/AddressSanitizer.html
    """
    conf.mkspec_clang_configure(major, minor, minimum=minimum, force_debug=True)
    conf.mkspec_add_common_flag(arch)

    conf.mkspec_add_common_flag("-fsanitize=address")
    conf.mkspec_add_common_flag("-fno-omit-frame-pointer")
    conf.mkspec_add_common_flag("-fno-optimize-sibling-calls")


@conf
def cxx_clang_address_sanitizer_x64(conf):
    """
    Configure clang (64-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 6, "-m64", minimum=True)


@conf
def cxx_clang_address_sanitizer_x86(conf):
    """
    Configure clang (32-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 6, "-m32", minimum=True)


@conf
def cxx_clang38_address_sanitizer_x64(conf):
    """
    Configure clang 3.8 (64-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 8, "-m64")


@conf
def cxx_clang38_address_sanitizer_x86(conf):
    """
    Configure clang 3.8 (32-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 8, "-m32")


@conf
def cxx_clang39_address_sanitizer_x64(conf):
    """
    Configure clang 3.9 (64-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 9, "-m64")


@conf
def cxx_clang39_address_sanitizer_x86(conf):
    """
    Configure clang 3.9 (32-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(3, 9, "-m32")


@conf
def cxx_clang10_address_sanitizer_x64(conf):
    """
    Configure clang 10.0 (64-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(10, 0, "-m64")


@conf
def cxx_clang13_address_sanitizer_x64(conf):
    """
    Configure clang 13.0 (64-bit) using the address sanitizer
    """
    conf.mkspec_setup_clang_address_sanitizer(13, 0, "-m64")


@conf
def mkspec_setup_clang_memory_sanitizer(conf, major, minor, arch, minimum=False):
    """
    To get a reasonable performance add -O1 or higher. To get
    meaningful stack traces in error messages add
    -fno-omit-frame-pointer. To get perfect stack traces you may need
    to disable inlining (just use -O1) and tail call elimination
    (-fno-optimize-sibling-calls).
    http://clang.llvm.org/docs/MemorySanitizer.html
    """
    conf.mkspec_clang_configure(major, minor, minimum=minimum, force_debug=True)
    conf.mkspec_add_common_flag(arch)

    conf.mkspec_add_common_flag("-fsanitize=memory")
    conf.mkspec_add_common_flag("-fsanitize-memory-track-origins")
    conf.mkspec_add_common_flag("-fno-omit-frame-pointer")
    conf.mkspec_add_common_flag("-fno-optimize-sibling-calls")


@conf
def cxx_clang_memory_sanitizer_x64(conf):
    """
    Configure clang (64-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 6, "-m64", minimum=True)


@conf
def cxx_clang_memory_sanitizer_x86(conf):
    """
    Configure clang (32-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 6, "-m32", minimum=True)


@conf
def cxx_clang38_memory_sanitizer_x64(conf):
    """
    Configure clang 3.8 (64-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 8, "-m64")


@conf
def cxx_clang38_memory_sanitizer_x86(conf):
    """
    Configure clang 3.8 (32-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 8, "-m32")


@conf
def cxx_clang39_memory_sanitizer_x64(conf):
    """
    Configure clang 3.9 (64-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 9, "-m64")


@conf
def cxx_clang39_memory_sanitizer_x86(conf):
    """
    Configure clang 3.9 (32-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(3, 9, "-m32")


@conf
def cxx_clang10_memory_sanitizer_x64(conf):
    """
    Configure clang 10.0 (64-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(10, 0, "-m64")


@conf
def cxx_clang13_memory_sanitizer_x64(conf):
    """
    Configure clang 13.0 (64-bit) using the memory sanitizer
    """
    conf.mkspec_setup_clang_memory_sanitizer(13, 0, "-m64")


@conf
def mkspec_setup_clang_thread_sanitizer(conf, major, minor, arch, minimum=False):
    """
    http://clang.llvm.org/docs/ThreadSanitizer.html
    """
    conf.mkspec_clang_configure(major, minor, minimum=minimum, force_debug=True)
    conf.mkspec_add_common_flag(arch)

    conf.mkspec_add_common_flag("-fsanitize=thread")


@conf
def cxx_clang_thread_sanitizer_x64(conf):
    """
    Configure clang (64-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 6, "-m64", minimum=True)


@conf
def cxx_clang_thread_sanitizer_x86(conf):
    """
    Configure clang (32-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 6, "-m32", minimum=True)


@conf
def cxx_clang38_thread_sanitizer_x64(conf):
    """
    Configure clang 3.8 (64-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 8, "-m64")


@conf
def cxx_clang38_thread_sanitizer_x86(conf):
    """
    Configure clang 3.8 (32-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 8, "-m32")


@conf
def cxx_clang39_thread_sanitizer_x64(conf):
    """
    Configure clang 3.9 (64-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 9, "-m64")


@conf
def cxx_clang39_thread_sanitizer_x86(conf):
    """
    Configure clang 3.9 (32-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(3, 9, "-m32")


@conf
def cxx_clang10_thread_sanitizer_x64(conf):
    """
    Configure clang 10.0 (64-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(10, 0, "-m64")


@conf
def cxx_clang13_thread_sanitizer_x64(conf):
    """
    Configure clang 13.0 (64-bit) using the thread sanitizer
    """
    conf.mkspec_setup_clang_thread_sanitizer(13, 0, "-m64")
