#!/usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

import emscripten_common


@conf
def cxx_emscripten125(conf):
    """
    Detect and setup the em++ 1.25 compiler
    """
    conf.mkspec_emscripten_configure(1, 25)


@conf
def cxx_emscripten126(conf):
    """
    Detect and setup the em++ 1.26 compiler
    """
    conf.mkspec_emscripten_configure(1, 26)
