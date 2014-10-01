#!/usr/bin/env python
# encoding: utf-8

"""
Copies chosen targets to a specific location.

This tool is available in the waf-tools repository, so we have
to load it:

def options(opt):
    import waflib.extras.wurf_dependency_bundle as bundle
    import waflib.extras.wurf_dependency_resolve as resolve
    import waflib.extras.wurf_configure_output

    bundle.add_dependency(opt,
        resolve.ResolveGitMajorVersion(
            name='waf-tools',
            git_repository='git://github.com/steinwurf/waf-tools.git',
            major_version=1))

    opt.load('wurf_dependency_bundle')
    opt.load('wurf_tools')

The tool should then be loaded:

def configure(conf):
    if conf.is_toplevel():
        conf.load('wurf_dependency_bundle')
        conf.load('wurf_tools')
        conf.load_external_tool('install_path', 'wurf_install_path')


The install path may now be updated by passing the install_path options. E.g.
python waf --options=install_path="~/my_binaries"

If you also pass the install_relative option waf will preserve the folder
structure when installing e.g.:
    python waf --options=install_path="~/my_binaries",install_relative

"""

import os
from waflib.TaskGen import feature, before_method, after_method

# Also install the C and C++ static libraries to facilitate the integration
# with other build systems
from waflib.Tools.c import cstlib
from waflib.Tools.cxx import cxxstlib
cstlib.inst_to = '${LIBDIR}'
cxxstlib.inst_to = '${LIBDIR}'


@feature('cxxprogram', 'cprogram', 'pyext', 'cstlib', 'cxxstlib')
@before_method('apply_link')
def update_install_path(self):
    """
    Updates the install_path variable of the task generator before
    executing the apply_link method. This will override the install_path
    otherwise used.
    """

    if self.bld.has_tool_option('install_path'):
        install_path = self.bld.get_tool_option('install_path')
        self.install_path = os.path.abspath(os.path.expanduser(install_path))


@feature('cxxprogram', 'cprogram', 'pyext')
@after_method('apply_link')
def change_relative_path_option(self):
    """
    If an install_task exists this will update the relative_trick
    options, which will make waf preserve the folder structure
    """

    install_relative = self.bld.has_tool_option('install_relative')

    if getattr(self, 'install_task', None):
        self.install_task.relative_trick = install_relative
