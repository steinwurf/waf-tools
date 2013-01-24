News for external-waf-tools
===========================

This file lists the major changes between versions. For a more detailed list
of every change, see the Git log.

Latest
------
* tbd

1.2.1
-----
* Fix indentation error for python3

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
* Fixed protobuf tools to use new waf load_external_tool(..) function

1.0.4
-----
* Fixed bug in android runner

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
* Initial release



