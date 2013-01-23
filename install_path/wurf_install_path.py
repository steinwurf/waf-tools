#!/usr/bin/env python
# encoding: utf-8

"""
Copies chosen targets to a specific location.

This tool is available in the external-waf-tools repository, so we have
to load it:

def options(opt):
    import waflib.extras.wurf_dependency_bundle as bundle
    import waflib.extras.wurf_dependency_resolve as resolve
    import waflib.extras.wurf_configure_output

    bundle.add_dependency(opt,
        resolve.ResolveGitMajorVersion(
            name='waf-tools',
            git_repository='git://github.com/steinwurf/external-waf-tools.git',
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
./waf --options=install_path=~/my_binaries

"""

import os
from waflib.TaskGen import feature, before_method

@feature('cxxprogram')
@before_method('apply_link')
def update_install_path(self):

    if self.bld.has_tool_option('install_path'):
        install_path = self.bld.get_tool_option('install_path')
        self.install_path = os.path.abspath(os.path.expanduser(install_path))
