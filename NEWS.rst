News for waf-tools
==================

This file lists the major changes between versions. For a more detailed list
of every change, see the Git log.

Latest
------
* tbd

4.31.0
------
* Minor: Added mkspecs for g++ 9.2.

4.30.0
------
* Minor: Allow multiple paths to be specified for ``copy_path`` option.

4.29.0
------
* Minor: Added cxx_bootlin_musl_gxx54_armv5 mspec
* Minor: Support fully static linking when passing -static as linkflag

4.28.0
------
* Minor: Changed the default ``--prefix`` to an empty string to avoid
  interference with the ``--destdir`` and ``--install_path`` options.
* Minor: Changed the default value for ``--destdir`` to install files
  into ``{project_name}_install`` in the local project folder.
  This change essentially makes the ``--install_path`` option obsolete.
* Minor: Added the following  mkspecs:
  cxx_android_clang80_armv7,
  cxx_android5_clang80_armv7,
  cxx_musl_gxx91_x86_64, and
  cxx_musl_gxx91_armv7.

4.27.0
------
* Minor: Use the -O2 flag when compiling with clang for Android and iOS.

4.26.0
------
* Minor: Added mkspecs for g++ 7.4.

4.25.1
------
* Patch: Restore the original ``--destdir`` option, since overriding its
  default value breaks our ``--install_path`` option and related functionality.

4.25.0
------
* Minor: Depend on options registry to access Git functionality during
  options.
* Minor: Changed the defaults for ``--destdir`` and ``--prefix`` to install
  in a local project folder rather than system-wide.

4.24.0
------
* Minor: Added msvs_extend_sources to allow Visual Studio project generator
  to include additional source files.

4.23.0
------
* Minor: Added mkspecs for g++ 8.3.

4.22.0
------
* Minor: Added mkspecs for clang 7.0: cxx_clang70_x86 and cxx_clang70_x64.

4.21.1
------
* Patch: Enabled libatomic support in cxx_openwrt_gxx73_armv7 and
  cxx_openwrt_gxx73_mips.

4.21.0
------
* Minor: Added the cxx_openwrt_gxx73_armv7 and cxx_openwrt_gxx73_mips mkspecs.

4.20.1
------
* Patch: Set the correct debugger working directory in the project generator
  for Visual Studio 2017.

4.20.0
------
* Minor: Added a project generator for Visual Studio 2017.

4.19.0
------
* Minor: Added the cxx_poky_gxx63_armv7 mkspec to support the Yocto-based
  Poky distribution (Gateworks Yocto SDK).

4.18.0
------
* Minor: Added versionless clang sanitizer mkspecs.

4.17.1
------
* Patch: Added missing -static-libstdc++ flag in cxx_android_clang70_armv7.

4.17.0
------
* Minor: Added mkspecs for clang 7.0 in the Android NDK r18b.

4.16.0
------
* Minor: Added the cxx_apple_llvm100_x64 mkspec (to support XCode 10.0).

4.15.1
------
* Patch: Correctly enumerate dependencies in the MSVS project generator
  to collect all available include directories.

4.15.0
------
* Minor: Added mkspecs cxx_msvc15_x86 and cxx_msvc15_x64 to support the
  Visual Studio 2017 compiler (including the VS Build Tools).

4.14.0
------
* Minor: Added mkspecs for g++ 8.1 and 8.2.

4.13.2
------
* Patch: Run wurf_runner features after process_use (waf 2.0 compatibility).

4.13.1
------
* Patch: Make wurf_runner compatible with waf 2.0.

4.13.0
------
* Minor: Added the limit_includes waf feature that is useful to constrain the
  available include paths to the export_includes of the top-level task
  generators in the program's "use" list.

4.12.0
------
* Minor: Added the -fno-omit-frame-pointer flag to g++ debug builds (this is
  needed for running various profiling tools).

4.11.0
------
* Minor: Added mkspecs for clang 4.0, 5.0, 6.0 and g++ 7.2, 7.3.

4.10.0
------
* Minor: Added the cxx_apple_llvm91_x64 mkspec (to support XCode 9.3).

4.9.1
------
* Patch: Disabled the incorrect unused-lambda-capture warning for clang 5.0
  in the Android NDK r16b.

4.9.0
-----
* Minor: Added mkspecs for Android x86_64: cxx_android5_clang38_x64 and
  cxx_android5_clang50_x64.

4.8.0
-----
* Minor: Added the test_filter option to only compile a part of the test source
  files. This is useful in a project with a lot of test files.

4.7.0
-----
* Minor: Added the cxx_apple_llvm90_x64 mkspec (to support XCode 9.0).

4.6.0
-----
* Minor: Added the cxx_emscripten137 mkspec.

4.5.1
-----
* Patch: The tests should only run after building the required kernel modules.

4.5.0
-----
* Minor: Added mkspecs for Android x86: cxx_android5_clang38_x86 and
  cxx_android5_clang50_x86.

4.4.0
-----
* Minor: The test runners now produce live output instead of capturing all
  lines and only displaying them at the end. The live output is especially
  useful if the test process gets stuck at a certain point.

4.3.0
-----
* Minor: Added mkspecs for clang 5.0 in the Android NDK r15.
* Minor: Added the cxx_apple_llvm81_x64 mkspec.

4.2.0
-----
* Minor: Added mkspecs for clang 3.9 sanitizers.
* Minor: Added cxx_gxx63_armv7 and cxx_gxx63_armv7_softfp mkspecs to target
  generic cross-compilers for ARMv7 systems.

4.1.1
-----
* Patch: Use the gold linker for 64-bit ARM Android targets to fix issues
  with linking shared libraries.

4.1.0
-----
* Minor: Added cxx_android5_gxx49_arm64 and cxx_android5_clang38_arm64 mkspecs
  for 64-bit ARM Android targets.

4.0.4
-----
* Patch: Fixed emscripten_common to work with the new waf.

4.0.3
-----
* Patch: Handle projects without a top-level program in the MSVS project
  generator (the debugging command should be set manually in this case).

4.0.2
-----
* Patch: Fixed the SSHRunner to avoid a non-zero return code when the
  ssh_clean_dir option is used to clean a folder that contains another folder.

4.0.1
-----
* Patch: Reimplemented the install_relative option to work with the new
  version of waf.

4.0.0
-----
* Major: Changed the option definitions to work with the new waf resolver.
* Major: Updated the MSVS project generator to support the new waf.
* Major: Removed the mkspecs that are no longer supported.
* Minor: Added wurf_configure_output.py that was previously in the waf repo.

3.19.1
------
* Patch: Removed the unnecessary -fPIE flag from cxx_android5_clang38_armv7,
  so the mkspec can be used to build both shared libraries and executables.

3.19.0
------
* Minor: Added mkspecs for g++ 6.3.

3.18.0
------
* Minor: Added mkspecs for clang 3.9.

3.17.2
------
* Patch: Allow both str and Node objects as copy_path in wurf_copy_binary.

3.17.1
------
* Patch: Use a waf Node object for the copy_path parameter in wurf_copy_binary.

3.17.0
------
* Minor: Added wurf_copy_binary.py. A tool for copying binaries to a
  configurable folder.

3.16.0
------
* Minor: Added mkspecs for clang 3.8 sanitizers.
* Minor: Removed the temporary _GLIBCXX_USE_CXX11_ABI=0 define in clang_common,
  since the libstdc++ incompatibility issue was fixed in clang 3.8.

3.15.0
------
* Minor: Added the cxx_apple_llvm80_x64 mkspec (to support XCode 8.0).

3.14.1
------
* Patch: If ssh_output_file used, then append the shellexit line to the
  output file. This is useful if the SSH output is truncated from some reason.
* Patch: The configure step should fail when the specified version of msvc
  is not found.

3.14.0
------
* Minor: Enabled the -std=c++14 flag for clang and g++.
* Minor: Set the minimum required compiler versions to g++ 4.9, clang 3.6 and
  msvc 14.0 (Visual Studio 2015).
* Patch: Properly handle missing taskgen properties in wurf_runner.

3.13.0
------
* Minor: Added mkspecs for g++ 6.2.
* Minor: Added the cxx_openwrt_gxx53_arm and cxx_openwrt_gxx53_mips mkspecs.

3.12.1
------
* Patch: Remove print statement in Android mkspecs

3.12.0
------
* Minor: Added wurf_android_soname.py. For Android builds sets the soname of the
  shared libraries built to the library name itself.

3.11.0
------
* Minor: Added mkspecs for g++ 5.4.

3.10.1
------
* Patch: Fixed the test_files property in wurf_runner, so that the input files
  are always located in the source folder. Previously the files in the build
  folder had priority, and these files might be out-of-date.

3.10.0
------
* Minor: Added the cxx_android_gxx49_armv7, cxx_android5_gxx49_armv7,
  cxx_android_clang38_armv7, cxx_android5_clang38_armv7 mkspecs to support
  g++ 4.9 and clang 3.8 in the Android NDK r12b. The clang mkspecs are still
  experimental: runtime failures are expected when using std::thread.

3.9.0
-----
* Minor: Added the cxx_raspberry_gxx49_armv7 mkspec (for Raspberry Pi 2)

3.8.1
-----
* Patch: Fixed invalid parameter in mkspec_setup_gcov.

3.8.0
-----
* Minor: Added cxx_gcov_default to configure gcov with the default g++.
* Patch: Changed search order for clang binaries such that the more specific
  version is used first.

3.7.0
-----
* Minor: Added mkspecs for clang 3.6 sanitizers.

3.6.1
-----
* Patch: Added the _GLIBCXX_USE_CXX11_ABI=0 define in clang_common to fix
  linking issues with clang on recent Linux systems where libstdc++ has an
  incompatible dual ABI.

3.6.0
-----
* Minor: Added mkspecs for clang 3.8, g++ 6.0 and g++ 6.1.

3.5.1
-----
* Patch: Use the /Z7 flag for MSVC debug builds to include all debugging
  information in the .obj files.

3.5.0
-----
* Minor: Re-enabled the -O2 flag on OSX. This produces 15x faster code for
  the binary field.

3.4.1
-----
* Patch: The test runner supports utf-8 characters printed on stdout/stderr.

3.4.0
-----
* Minor: Added mkspecs for clang 3.7 and g++ 5.3.
* Minor: Added the cxx_apple_llvm73_x64 mkspec (to support XCode 7.3).

3.3.0
-----
* Minor: Added mkspecs for the x86 and x86_64 architectures on Android:
  cxx_android_gxx49_x86, cxx_android5_gxx49_x86 and cxx_android5_gxx49_x64.
* Minor: Consolidated msvc compiler flags and warnings.

3.2.0
-----
* Minor: Added cxx_android5_gxx48_armv7 mkspec to support Android 5.0+ where
  only position independent executables (PIE) can be executed.

3.1.3
-----
* Patch: Use both `use` and `uselib` to find the needed the shared libraries.

3.1.2
-----
* Patch: Revert the change made in 3.1.1.

3.1.1
-----
* Patch: Use `use` instead of `uselib` to find the needed the shared libraries.

3.1.0
-----
* Minor: The test runner automatically copies the compiled shared libraries
  next to the test binaries (no need to specify these as test_files).

3.0.2
-----
* Patch: Added missing emscripten_path option.

3.0.1
-----
* Patch: Added missing property to the ssh_clean_dir option which does not
  take a value.

3.0.0
-----
* Major: Changed the folder structure so that the main tools are located
  in the root folder and their submodules are in the corresponding subfolders.
* Major: Defined all tool options in the resolve step to work with the
  recursive option resolution. The tool options are now standalone, and they
  are described in the waf help.
* Major: Removed the mkspecs that are no longer supported.

2.54.0
------
* Minor: Added cxx_apple_llvm70_x64 mkspec (to support XCode 7.0).

2.53.1
------
* Patch: Ensure that the result_folder exists in SSHRunner and AndroidRunner.

2.53.0
------
* Minor: Ignore the file extension when running a specific benchmark with
  the run_benchmark option.

2.52.0
------
* Minor: Added the result_file and result_folder options to all runners to
  copy a generated file to the specified folder on the host.

2.51.0
------
* Minor: Allow alternative names for node.js binary on all platforms.

2.50.0
------
* Minor: Force the sequential execution of run tasks (tests and benchmarks)
  in wurf_runner. The run tasks are executed in the same order as they are
  defined in the wscripts.

2.49.0
------
* Minor: Added mkspecs for clang 3.6 and g++ 5.2.

2.48.0
------
* Minor: Added cxx_msvc14_x86 and cxx_msvc14_x64 mkspecs and adjusted compiler
  flags to support the Visual Studio 2015 compiler (MSVC 14.0).

2.47.0
------
* Minor: Added cxx_apple_llvm61_x64 mkspec (to support XCode 6.4).
* Minor: Added default iOS mkspecs where we only check for a minimum version
  of the Apple LLVM compiler: cxx_ios70_apple_llvm_armv7,
  cxx_ios70_apple_llvm_armv7s, cxx_ios70_apple_llvm_arm64,
  cxx_ios70_apple_llvm_i386, cxx_ios70_apple_llvm_x86_64.
* Minor: Added cxx_emscripten134 mkspec.
* Patch: Corrected the check for the minimum version of the emscripten compiler.

2.46.0
------
* Minor: Updated the minimum versions in cxx_default to g++ 4.8 and clang 3.5.
* Minor: Switched to the -std=c++11 flag for g++ and clang.

2.45.0
------
* Minor: Added mkspecs for new cross-compiler toolchains:
  cxx_raspberry_gxx49_arm, cxx_openwrt_gxx48_arm.

2.44.0
------
* Minor: Added the cxx_gcov_gxx49_x64 mkspec for code coverage analysis
  with gcov.
* Minor: Added -pedantic and -finline-functions flags for g++ and clang.
* Minor: Disabled the unnecessary manifest files for msvc.

2.43.0
------
* Minor: Added the cxx_default_emscripten mkspec that only checks for a
  required minimum version of the emscripten compiler.
* Minor: Added mkspecs for emscripten: cxx_emscripten127 and cxx_emscripten130.

2.42.0
------
* Minor: The usbmux process is not started and stopped in IosRunner. The
  process will run permanently as a system service. This change is done to
  alleviate connection issues with iOS devices.
* Minor: Allow SSH and SCP options in IOSRunner to set additional flags.

2.41.0
------
* Minor: Prepared for waf version 1.8.8.
* Patch: Fixed issue with Ubuntu clang installation.

2.40.2
------
* Patch: Use the threaded mode of usbmux in IOSRunner to mitigate the
  connection startup problems on idle iOS devices.

2.40.1
------
* Patch: Allow the user to override the compiler with the CXX/CC environment
  variables.

2.40.0
------
* Minor: Added iOS mkspec for 64-bit simulator: cxx_ios70_apple_llvm60_x86_64

2.39.0
------
* Minor: Added install_shared_libs option to enable installation of shared libs.
* Minor: Added iOS mkspecs: cxx_ios70_apple_llvm60_armv7,
  cxx_ios70_apple_llvm60_armv7s, cxx_ios70_apple_llvm60_arm64 and
  cxx_ios70_apple_llvm60_i386.

2.38.0
------
* Minor: Only install static libs if the install_static_libs option is used.

2.37.0
------
* Minor: Added support for the emscripten compiler.
* Minor: Added emscripten mkspecs: cxx_emscripten126 and cxx_emscripten125.

2.36.1
------
* Patch: The default binary names, g++ and gcc are added as secondary options
  in the gxx mkspecs (the versioned compiler binaries are not available on
  certain Linux systems, such as ArchLinux and Fedora)

2.36.0
------
* Minor: The generated C and C++ static libraries are now copied to the given
  install_path to facilitate integration with other build systems

2.35.0
------
* Minor: Added mkspecs cxx_apple_llvm60_x64 and cxx_ios50_apple_llvm60_armv7
* Minor: Make ios_sdk_dir an optional parameter for iOS mkspecs, since the
  standard location of the iOS SDK does not include a version number
* Patch: Changed the optimizer flag for clang on OS X from -O2 to -Os,
  since -O2 causes excessive memory consumption.

2.34.0
------
* Minor: Added mkspecs for g++ 4.9 and clang 3.5
* Patch: Specify ARMv7 architecture in cxx_android_gxx48_armv7 LINKFLAGS to
  avoid runtime issues with std threads and atomics

2.33.2
------
* Patch: The ssh-runner now makes sure that the destination directory
  exists before running scp to copy the files.

2.33.1
------
* Patch: Test files are now allowed to be in the source directory when using
  the BasicRunner.

2.33.0
------
* Minor: Added mkspecs to pick architecture without specifying compiler;
  cxx_default_x86 and cxx_default_x64.

2.32.1
------
* Patch: Fixed msvc .pdb file access issue with parallel compiler processes

2.32.0
------
* Minor: Added ssh_output_file option to save the test output into a file
  which is later copied to the host (to mitigate SSH truncating issues)
* Patch: Linux kernel modules are loaded from the correct directory

2.31.0
------
* Minor: Add ssh_clean_dir option to delete all files from the target directory
  before copying the new test binaries (to conserve free space)
* Minor: Simplify flags for cxx_crosslinux_gxx48_mips mkspec

2.30.0
------
* Minor: Add mkspec for MIPS OpenWrt toolchain (cxx_crosslinux_gxx48_mips)

2.29.0
------
* Minor: Simplify ADB variable in android_runner by using env.get_flat
* Patch: Install path issue fixed for Python extensions (pyext)

2.28.0
------
* Minor: Added fix for supporting waf 1.8.0pre1.

2.27.0
------
* Minor: Added mkspecs cxx_apple_llvm51_x86/64 for Apple LLVM 5.1 compiler.
* Minor: Add cxx_ios50_apple_llvm51_armv7 mkspec.

2.26.0
------
* Minor: Add ARMv7 mkspec for Android Clang (cxx_android_clang34_armv7)
* Minor: Update minimum compiler versions in cxx_default (g++ 4.6, clang 3.4,
  msvc 12.0)

2.25.0
------
* Minor: Add ARMv7 mkspec for Android GCC (cxx_android_gxx48_armv7)

2.24.0
------
* Minor: Add mkspec for new OpenWrt toolchain (cxx_crosslinux_gxx47_arm)
* Minor: Add 'cxx_nodebug' option which defines NDEBUG to disable assertions

2.23.0
------
* Minor: The SSH commands are invoked with the -t flag, which ensures that the
  remote process is terminated when the SSH process is killed on the host.
* Minor: IOSRunner class is derived from SSHRunner to enhance code reuse
* Minor: Add mkspec_try_flags function to check for available compiler flags

2.22.0
------
* Patch: Use -Os (optimize for size) flag on iOS, because -O2 produces unstable
  code on this platform
* Minor: Introduce force_debug parameter in mkspec_clang_configure to make the
  clang sanitizer mkspecs simpler

2.21.0
------
* Minor: Add mkspecs for Visual Studio 2013: cxx_msvc12_x86 and cxx_msvc12_x64.

2.20.0
------
* Minor: Add mkspecs for clang address, memory and thread sanitizers.
* Patch: Statically link GCC libraries to support C++ exceptions with the
  OpenWrt toolchain (cxx_crosslinux_gxx46_arm mkspec).

2.19.1
------
* Patch: Changed use of ``xrange`` to ``range`` to support python 3.x.

2.19.0
------
* Minor: cxx_default explicitly reports all configuration errors.
* Minor: The android_sdk_dir and android_ndk_dir options are not necessary if
  adb and the Android toolchain binaries are in the PATH.
* Minor: Add cxx_android_gxx48_arm mkspec.
* Minor: Add cxx_clang34_x86 and cxx_clang34_x64 mkspecs.

2.18.0
------
* Minor: Add support for testing Linux kernel modules with the basic_runner and
  the SSH runner.

2.17.1
------
* Patch: Use target option instead of ccc-host-triple in iOS builds

2.17.0
------
* Minor: Add cxx_ios50_apple_llvm50_armv7 mkspec.
* Minor: Remove obsolete -s linker flag on Mac OSX

2.16.2
------
* Patch: Support spaces in paths in basic_runner.

2.16.1
------
* Patch: Remove added quotes from ssh_options and scp_options.

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
* Patch: Fixed pull command bug in the android runner.

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
* Patch: Android and iOS runners will remove all previous test files
          from the device before running a new test.

2.1.0
-----
* Minor: New mkspec for iOS 5.0 (cxx_ios50_apple_llvm42_armv7).
* Minor: Added ios_runner for automated testing on iOS.
* Minor: mkspecs for clang++ and Apple LLVM will also load clang as a C compiler.

2.0.0
-----
* Major: mkspecs restructured, common functions moved to modules in mkspec_common.
* Major: gxx45 and msvc10 mkspecs removed.
* Major: Android mkspec renamed to cxx_android_gxx46_arm.
* Minor: Loading g++ in a mkspec will also load gcc to compile C code.
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
