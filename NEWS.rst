News for external-waf-tools
===========================

This file lists the major changes between versions. For a more detailed list
of every change, see the Git log.

Latest
------
* tbd

2.32.0
------
* Minor: Added ssh_output_file option to save the test output into a file
  which is later copied to the host (to mitigate SSH truncating issues)
* Bugfix: Linux kernel modules are loaded from the correct directory

2.31.0
------
* Minor: Add ssh_clean_dir option to delete all files from the target directory
  before copying the new test binaries (to conserve free space)
* Minor: Simplify flags for cxx_crosslinux_gxx48_mips mkspec

2.30.0
------
* Minor: Add makespec for MIPS OpenWrt toolchain (cxx_crosslinux_gxx48_mips)

2.29.0
------
* Minor: Simplify ADB variable in android_runner by using env.get_flat
* Bugfix: Install path issue fixed for Python extensions (pyext)

2.28.0
------
* Minor: Added fix for supporting waf 1.8.0pre1.

2.27.0
------
* Minor: Added mkspecs cxx_apple_llvm51_x86/64 for Apple LLVM 5.1 compiler.
* Minor: Add cxx_ios50_apple_llvm51_armv7 makespec.

2.26.0
------
* Minor: Add ARMv7 makespec for Android Clang (cxx_android_clang34_armv7)
* Minor: Update minimum compiler versions in cxx_default (g++ 4.6, clang 3.4,
  msvc 12.0)

2.25.0
------
* Minor: Add ARMv7 makespec for Android GCC (cxx_android_gxx48_armv7)

2.24.0
------
* Minor: Add makespec for new OpenWrt toolchain (cxx_crosslinux_gxx47_arm)
* Minor: Add 'cxx_nodebug' option which defines NDEBUG to disable assertions

2.23.0
------
* Minor: The SSH commands are invoked with the -t flag, which ensures that the
  remote process is terminated when the SSH process is killed on the host.
* Minor: IOSRunner class is derived from SSHRunner to enhance code reuse
* Minor: Add mkspec_try_flags function to check for available compiler flags

2.22.0
------
* Bugfix: Use -Os (optimize for size) flag on iOS, because -O2 produces unstable
  code on this platform
* Minor: Introduce force_debug parameter in mkspec_clang_configure to make the
  clang sanitizer mkspecs simpler

2.21.0
------
* Minor: Add mkspecs for Visual Studio 2013: cxx_msvc12_x86 and cxx_msvc12_x64.

2.20.0
------
* Minor: Add makespecs for clang address, memory and thread sanitizers.
* Bugfix: Statically link GCC libraries to support C++ exceptions with the
  OpenWrt toolchain (cxx_crosslinux_gxx46_arm mkspec).

2.19.1
------
* Bug: Changed use of ``xrange`` to ``range`` to support python 3.x.

2.19.0
------
* Minor: cxx_default explicitly reports all configuration errors.
* Minor: The android_sdk_dir and android_ndk_dir options are not necessary if
  adb and the Android toolchain binaries are in the PATH.
* Minor: Add cxx_android_gxx48_arm makespec.
* Minor: Add cxx_clang34_x86 and cxx_clang34_x64 makespecs.

2.18.0
------
* Minor: Add support for testing Linux kernel modules with the basic_runner and
  the SSH runner.

2.17.1
------
* Bugfix: Use target option instead of ccc-host-triple in iOS builds

2.17.0
------
* Minor: Add cxx_ios50_apple_llvm50_armv7 makespec.
* Minor: Remove obsolete -s linker flag on Mac OSX

2.16.2
------
* Bugfix: Support spaces in paths in basic_runner.

2.16.1
------
* Bugfix: Remove added quotes from ssh_options and scp_options.

2.16.0
------
* Minor: Add ssh_options and scp_options for SSH runner customization.

2.15.0
------
* Minor: Combined mkspecs into single files for each compiler family.
* Minor: Added mkspec cxx_crosslinux_gxx46_arm for Linux on 32-bit ARM.
* Minor: Added cflags,cxxflags,linkflags,commonflags options

2.14.0
------
* Minor: Added mkspecs cxx_apple_llvm50_x86/64 for Apple LLVM 5.0 compiler.

2.13.0
------
* Minor: Add -m32/-m64 flag for CFLAGS/CXXFLAGS/LINKFLAGS to enable 32-bit
  compilation on 64-bit systems (applies to all g++ and clang mkspecs).

2.12.0
------
* Minor: Added mkspecs cxx_gxx48_x86/64 for g++ 4.8 compiler.
* Minor: Added cxx_clang31_x86/64 and cxx_clang33_x86/64 mkspecs.

2.11.0
------
* Minor: Added cxx_clang32_x86/64 mkspecs for clang 3.2 compiler.

2.10.1
------
* Bug: Fixed pull command bug in the android runner.

2.10.0
------
* Minor: Added cxx_crosslinux_gxx47_mips mkspec for MIPS targets.

2.9.0
-----
* Minor: Improved support for the run_cmd option.
* Minor: Refactored the different runners.

2.8.0
-----
* Minor: Added cxx_raspberry_gxx47_arm mkspec for Raspberry Pi toolchain.
* Minor: Added SSH runner to run binaries on remote hosts via SSH.

2.7.0
-----
* Minor: Changed the output of print_benchmark_paths command.

2.6.0
-----
* Minor: Added additional benchmarking capabilities.
* Minor: Refactored the different runners.

2.5.0
-----
* Minor: Added new mkspecs for cross-compiler toolchains targeting
  legacy Linux versions (cxx_crosslinux_gxx46_x86, cxx_crosslinux_gxx46_x64).
* Minor: Strip all debugging symbols from g++ and clang release builds (-s flag).

2.4.0
-----
* Minor: Updated cxx_default.py to automatically load gcc and clang as C compilers.

2.3.0
-----
* Minor: Updated wurf_install_path.py tool to also work for cprograms.

2.2.0
-----
* Minor: cxx_default explicitly checks for minimum versions of the compilers.
* Minor: User-defined CXX variable can be used to specify compiler.
* Minor: The test runner prints test results also on success (disable with
  run_silent option).
* Minor: Disable MSVC LNK4221 linker warning for empty object files.

2.1.1
-----
* Bugfix: Android and iOS runners will remove all previous test files
          from the device before running a new test.

2.1.0
-----
* Minor: New mkspec for iOS 5.0 (cxx_ios50_apple_llvm42_armv7).
* Minor: Added ios_runner for automated testing on iOS.
* Minor: Makespecs for clang++ and Apple LLVM will also load clang as a C compiler.

2.0.0
-----
* Major: Makespecs restructured, common functions moved to modules in mkspec_common.
* Major: gxx45 and msvc10 mkspecs removed.
* Major: Android mkspec renamed to cxx_android_gxx46_arm.
* Minor: Loading g++ in a makespec will also load gcc to compile C code.
* Minor: mkspec added for Apple LLVM 4.2: cxx_apple_llvm42_x64.

1.5.1
-----
* Fixing default compiler flags on Windows.

1.5.0
-----
* Added automatic project generator for Visual Studio 2008, 2010 and 2012.
* Support for debugging in Visual Studio with the cxx_debug option.
* Spurious warnings removed on win32.

1.4.0
-----
* Updated default cxxflags to build stripped release versions of the libraries.
* Possibility to use cxx_debug option when a debug build is desired.
* Added mkspec for msvc11_x86.

1.3.1
-----
* Fix problem handling paths to test_files nodes.

1.3.0
-----
* Adding support for the test_files attribute in tests and benchmarks. Using
  this attribute one may supply the test or benchmark with test files e.g.
  containing test data or similar. Test files are copied by the runners to
  the location where the test binary is executed.

1.2.1
-----
* Fix indentation error for python3.

1.2.0
-----
* Updated the install_path tool to allow the relative_trick variable to be
  updated. This allows the folder structure to be preserved when installing
  files.

1.1.0
-----
* Adding new install_path tool, which allows the install path of binaries
  to be controlled.

1.0.6
-----
* In Android runner change folder before running binary. This ensures
  that the binary is executed from a writable folder.

1.0.5
-----
* Fixed protobuf tools to use new waf load_external_tool(..) function.

1.0.4
-----
* Fixed bug in android runner.

1.0.3
-----
* Simplified cxx_mkspecs which allows more re-use of existing
  functionality.

1.0.2
-----
* Updating runner tool option from 'runcmd' to 'run_cmd', for more
  consistency in the options.

1.0.1
-----
* Android runner supports device_id=DEVICE option, which make it
  possible to run code on a specific device (when multiple are
  connected).

1.0.0
-----
* Initial release.



