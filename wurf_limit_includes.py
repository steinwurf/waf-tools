#!/usr/bin/env python
# encoding: utf-8

"""
The "limit_includes" feature limits the available include paths when compiling
sources to the includes that are explicitly exported by the top-level task
generators in the "use" list. Recursive includes are disabled: if a "used"
task generator brings other includes from its dependencies, then those will
not be available in the top-level sources.

If the compiler defines any default include paths in conf.env.INCLUDES, then
these will also be available when using the "limit_includes" feature.

The "limit_includes" feature is primarily useful for top-level programs:

def build(bld):
    bld.program(features='cxx limit_includes',
                source=['main.cpp'],
                target='myprogram',
                use=['mylib1, mylib2'])

In this example, 'myprogram' can only access the include paths that are
defined in the 'export_includes' list of 'mylib1' and 'mylib2'.
"""

import os

from waflib import Errors
from waflib.TaskGen import feature, before_method, after_method


@feature("limit_includes")
@before_method("process_use")
def store_default_includes(self):
    """
    Stores the default system includes in self.env.DEFAULT_INCLUDES before
    running the "process_use" method. This is necessary for the MSVC compiler
    where the system include paths are not hardcoded.
    """
    self.env.DEFAULT_INCLUDES = self.env.INCLUDES


@feature("limit_includes")
@before_method("apply_incpaths")
@after_method("process_use")
def set_limited_includes(self):
    """
    Limits the available include paths based on the 'export_includes' list
    of the top-level task generators in the current 'use' list
    """
    # Restore the default system includes and remove all other includes that
    # were added from the dependencies during the "process_use" method
    self.env.INCLUDES = self.env.DEFAULT_INCLUDES
    self.includes = []
    # Only add the includes that are explicitly exported by the top-level
    # task generators in the "use" list
    for name in self.to_list(getattr(self, "use", [])):
        try:
            y = self.bld.get_tgen_by_name(name)
        except Errors.WafError:
            continue
        else:
            if getattr(y, "export_includes", None):
                self.includes.extend(y.to_incnodes(y.export_includes))
