#! /usr/bin/env python
# encoding: utf-8

"""
This tool is a container that bundles various project generators.

The available generators:

    wurf_msvs:  Generates Visual Studio 2008, 2010 or 2012 solutions
                Exported Waf commands:
                    msvs2008
                    msvs2010
                    msvs2012


To use this external tool, simply load it in configure:

def configure(conf):

    if conf.is_toplevel():
        conf.load_external_tool('project_gen', 'wurf_project_generator')

Then you can invoke the tool together with configure:

$ python waf configure msvs2012
"""

import project_generators.msvs