#!/usr/bin/env python
# encoding: utf-8
# Carlos Rafael Giani, 2006
# Thomas Nagy, 2010
# Script is based on the waf_unit_test tool, but has since
# been significantly rewritten.

"""
Unit testing + benchmark tool.

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
        conf.load_external_tool('mkspec', 'wurf_cxx_mkspec_tool')
        conf.load_external_tool('runners', 'wurf_runner')    

Finally in the build step, we add 'test' as a feature:

def build(bld):
    bld.program(features = 'cxx test',
                source   = ['main.cpp'],
                target   = 'hello')    
"""

import os, sys, re
from waflib.TaskGen import feature, after_method
from waflib import Utils, Task, Logs, Options
from basic_runner import BasicRunner
from android_runner import AndroidRunner

@feature('test')
@after_method('apply_link')
def make_test(self):
    if self.bld.has_tool_option('run_tests'):
        make_run(self, "test")

@feature('benchmark')
@after_method('apply_link')
def make_benchmark(self):
    if self.bld.has_tool_option('run_benchmarks'):
        make_run(self, "benchmark")

def make_run(taskgen, run_type):
    """Create the run task. There can be only one unit test task by task generator."""
    task = None
    if getattr(taskgen, 'link_task', None):

        taskgen.bld.add_group()
        
        if taskgen.bld.is_mkspec_platform('android'):
            task = taskgen.create_task('AndroidRunner', taskgen.link_task.outputs)
        else:
            task = taskgen.create_task('BasicRunner', taskgen.link_task.outputs)
            task.run_type = run_type


    # We are creating a new task which should run a executable after
    # a build finishes. Here we add two functions to the BuildContext
    # which prints a summary and ensures that the build fails if the
    # test fails.
    post_funs = getattr(taskgen.bld, 'post_funs', None)
    if post_funs:
        if not summary in post_funs:
            taskgen.bld.add_post_fun(summary)
        if not set_exit_code in post_funs:
            taskgen.bld.add_post_fun(set_exit_code)
    else:
        taskgen.bld.add_post_fun(summary)
        taskgen.bld.add_post_fun(set_exit_code)
    

def summary(bld):
    """
    Display an execution summary::

    def build(bld):
        bld(features='cxx cxxprogram test', source='main.c', target='app')
        from waflib.Tools import waf_unit_test
        bld.add_post_fun(waf_unit_test.summary)
    """
    lst = getattr(bld, 'runner_results', [])
    if lst:
        Logs.pprint('CYAN', 'execution summary')

        total = len(lst)
        fail = len([x for x in lst if x[1]])

        Logs.pprint('CYAN', '  successful runs %d/%d' % (total-fail, total))
        for (f, code, out, err) in lst:
            if not code:
                Logs.pprint('CYAN', '    %s' % f)

        Logs.pprint('CYAN', '  failed runs %d/%d' % (fail, total))
        for (f, code, out, err) in lst:
            if code:
                Logs.pprint('CYAN', '    %s' % f)

def set_exit_code(bld):
    """
    If any of the tests fail waf will exit with that exit code.
    This is useful if you have an automated build system which need
    to report on errors from the tests.
    You may use it like this:

    def build(bld):
        bld(features='cxx cxxprogram test', source='main.c', target='app')
        from waflib.Tools import waf_unit_test
        bld.add_post_fun(waf_unit_test.set_exit_code)
    """
    lst = getattr(bld, 'runner_results', [])
    for (f, code, out, err) in lst:
        if code:
            msg = []
            if out:
                msg.append('stdout:%s%s' % (os.linesep, out.decode('utf-8')))
            if err:
                msg.append('stderr:%s%s' % (os.linesep, err.decode('utf-8')))
            bld.fatal(os.linesep.join(msg))
