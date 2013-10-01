News for external-waf-tools
===========================

This file lists the major changes between versions. For a more detailed list
of every change, see the Git log.

2.11.0
* Minor: Added cxx_clang32_x32/64 mkspecs for clang 3.2 targets.

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



