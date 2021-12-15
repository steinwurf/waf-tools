#!/usr/bin/env python
# encoding: utf-8
# Avalanche Studios 2009-2011
# Thomas Nagy 2011

"""
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. The name of the author may not be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

"""
To add this tool to your project:
def options(conf):
    opt.load('msvs')

It can be a good idea to add the sync_exec tool too.

To generate solution files:
$ waf configure msvs

To customize the outputs, provide subclasses in your wscript files:

from waflib.extras import msvs
class vsnode_target(msvs.vsnode_target):
    def get_build_command(self, props):
        # likely to be required
        return "waf.bat build"
    def collect_source(self):
        # likely to be required
        ...
class msvs_bar(msvs.msvs_generator):
    def init(self):
        msvs.msvs_generator.init(self)
        self.vsnode_target = vsnode_target

The msvs class re-uses the same build() function for reading the targets
(task generators), you may therefore specify msvs settings on the context
object:

def build(bld):
    bld.solution_name = 'foo.sln'
    bld.waf_command = 'waf.bat'
    bld.projects_dir = bld.srcnode.make_node('.depproj')
    bld.projects_dir.mkdir()

For visual studio 2008, the command is called 'msvs2008', and the classes
such as vsnode_target are wrapped by a decorator class 'wrap_2008' to
provide special functionality.

ASSUMPTIONS:
* a project can be either a directory or a target, vcxproj files are written
  only for targets that have source files
* each project is a vcxproj file, therefore the project uuid needs only to be a
  hash of the absolute path
"""

import os
import re
import sys
import uuid  # requires python 2.5
from pprint import pprint
from waflib.extras.wurf.waf_build_context import WafBuildContext
from waflib import Utils, TaskGen, Logs, Task, Context, Node, Options

HEADERS_GLOB = "**/(*.h|*.hpp|*.H|*.inl)"

PROJECT_TEMPLATE = r"""<?xml version="1.0" encoding="UTF-8"?>
<Project DefaultTargets="Build" ToolsVersion="4.0"
    xmlns="http://schemas.microsoft.com/developer/msbuild/2003">

    <ItemGroup Label="ProjectConfigurations">
        ${for b in project.build_properties}
        <ProjectConfiguration Include="${b.configuration}|${b.platform}">
            <Configuration>${b.configuration}</Configuration>
            <Platform>${b.platform}</Platform>
        </ProjectConfiguration>
        ${endfor}
    </ItemGroup>

    <ItemDefinitionGroup>
        <Link>
            <SubSystem>Console</SubSystem>
        </Link>
    </ItemDefinitionGroup>

    <PropertyGroup Label="Globals">
        <ProjectGuid>{${project.uuid}}</ProjectGuid>
        <Keyword>MakeFileProj</Keyword>
        <ProjectName>${project.name}</ProjectName>
    </PropertyGroup>
    <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />

    ${for b in project.build_properties}
    <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='${b.configuration}|${b.platform}'" Label="Configuration">
        <ConfigurationType>Makefile</ConfigurationType>
        <OutDir>build\VSProjects\$(Configuration)\</OutDir>
        <PlatformToolset>${project.platformver}</PlatformToolset>
        ${if getattr(project, 'debugger_command', None)}
        <LocalDebuggerCommand>${xml:project.debugger_command}</LocalDebuggerCommand>
        ${endif}
        ${if getattr(project, 'debugger_command_args', None)}
        <LocalDebuggerCommandArguments>${xml:project.debugger_command_args}</LocalDebuggerCommandArguments>
        ${endif}
    </PropertyGroup>
    ${endfor}

    <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
    <ImportGroup Label="ExtensionSettings">
    </ImportGroup>

    ${for b in project.build_properties}
    <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='${b.configuration}|${b.platform}'">
        <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
    </ImportGroup>
    ${endfor}

    ${for b in project.build_properties}
    <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='${b.configuration}|${b.platform}'">
        <NMakeBuildCommandLine>${xml:project.get_build_command(b)}</NMakeBuildCommandLine>
        <NMakeReBuildCommandLine>${xml:project.get_rebuild_command(b)}</NMakeReBuildCommandLine>
        <NMakeCleanCommandLine>${xml:project.get_clean_command(b)}</NMakeCleanCommandLine>
        <NMakeIncludeSearchPath>${xml:b.includes_search_path}</NMakeIncludeSearchPath>
        <NMakePreprocessorDefinitions>${xml:b.preprocessor_definitions};$(NMakePreprocessorDefinitions)</NMakePreprocessorDefinitions>
        <IntDir>build\VSProjects\$(Configuration)\</IntDir>
        <BaseIntermediateOutputPath>build\VSProjects\</BaseIntermediateOutputPath>

        ${if getattr(b, 'output_file', None)}
        <NMakeOutput>${xml:b.output_file}</NMakeOutput>
        ${endif}
        ${if getattr(b, 'working_dir', None)}
        <LocalDebuggerWorkingDirectory>${xml:b.working_dir}</LocalDebuggerWorkingDirectory>
        ${endif}
        ${if getattr(b, 'deploy_dir', None)}
        <RemoteRoot>${xml:b.deploy_dir}</RemoteRoot>
        ${endif}
    </PropertyGroup>
    ${endfor}

    ${for b in project.build_properties}
        ${if getattr(b, 'deploy_dir', None)}
    <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='${b.configuration}|${b.platform}'">
        <Deploy>
            <DeploymentType>CopyToHardDrive</DeploymentType>
        </Deploy>
    </ItemDefinitionGroup>
        ${endif}
    ${endfor}

    <ItemGroup>
        ${for x in project.source}
        <${project.get_key(x)} Include='${x.abspath()}' />
        ${endfor}
    </ItemGroup>
    <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
    <ImportGroup Label="ExtensionTargets">
    </ImportGroup>
</Project>
"""

FILTER_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
    <ItemGroup>
        ${for x in project.source}
            <${project.get_key(x)} Include="${x.abspath()}">
                <Filter>${project.get_filter_name(x.parent)}</Filter>
            </${project.get_key(x)}>
        ${endfor}
    </ItemGroup>
    <ItemGroup>
        ${for x in project.dirs()}
            <Filter Include="${project.get_filter_name(x)}">
                <UniqueIdentifier>{${project.make_uuid(x.abspath())}}</UniqueIdentifier>
            </Filter>
        ${endfor}
    </ItemGroup>
</Project>
"""

PROJECT_2008_TEMPLATE = r"""<?xml version="1.0" encoding="UTF-8"?>
<VisualStudioProject ProjectType="Visual C++" Version="9,00"
    Name="${xml: project.name}" ProjectGUID="{${project.uuid}}"
    Keyword="MakeFileProj"
    TargetFrameworkVersion="196613">
    <Platforms>
        ${if project.build_properties}
        ${for b in project.build_properties}
           <Platform Name="${xml: b.platform}" />
        ${endfor}
        ${else}
           <Platform Name="Win32" />
        ${endif}
    </Platforms>
    <ToolFiles>
    </ToolFiles>
    <Configurations>
        ${if project.build_properties}
        ${for b in project.build_properties}
        <Configuration
            Name="${xml: b.configuration}|${xml: b.platform}"
            IntermediateDirectory="$(ConfigurationName)"
            OutputDirectory="${xml: b.outdir}"
            ConfigurationType="0">
            <Tool
                Name="VCNMakeTool"
                BuildCommandLine="${xml: project.get_build_command(b)}"
                ReBuildCommandLine="${xml: project.get_rebuild_command(b)}"
                CleanCommandLine="${xml: project.get_clean_command(b)}"
                ${if getattr(b, 'output_file', None)}
                Output="${xml: b.output_file}"
                ${endif}
                PreprocessorDefinitions="${xml: b.preprocessor_definitions}"
                IncludeSearchPath="${xml: b.includes_search_path}"
                ForcedIncludes=""
                ForcedUsingAssemblies=""
                AssemblySearchPath=""
                CompileAsManaged=""
            />
        </Configuration>
        ${endfor}
        ${else}
            <Configuration Name="Release|Win32" >
        </Configuration>
        ${endif}
    </Configurations>
    <References>
    </References>
    <Files>
${project.display_filter()}
    </Files>
</VisualStudioProject>
"""

SOLUTION_TEMPLATE = """Microsoft Visual Studio Solution File, Format Version ${project.numver}
# Visual Studio ${project.vsver}
${for p in project.all_projects}
Project("{${p.ptype()}}") = "${p.name}", "${p.title}", "{${p.uuid}}"
EndProject${endfor}
Global
    GlobalSection(SolutionConfigurationPlatforms) = preSolution
        ${if project.all_projects}
        ${for (configuration, platform) in project.all_projects[0].ctx.project_configurations()}
        ${configuration}|${platform} = ${configuration}|${platform}
        ${endfor}
        ${endif}
    EndGlobalSection
    GlobalSection(ProjectConfigurationPlatforms) = postSolution
        ${for p in project.all_projects}
            ${if hasattr(p, 'source')}
            ${for b in p.build_properties}
        {${p.uuid}}.${b.configuration}|${b.platform}.ActiveCfg = ${b.configuration}|${b.platform}
            ${if getattr(p, 'is_active', None)}
        {${p.uuid}}.${b.configuration}|${b.platform}.Build.0 = ${b.configuration}|${b.platform}
            ${endif}
            ${endfor}
            ${endif}
        ${endfor}
    EndGlobalSection
    GlobalSection(SolutionProperties) = preSolution
        HideSolutionNode = FALSE
    EndGlobalSection
EndGlobal
"""

COMPILE_TEMPLATE = """def f(project):
    lst = []
    def xml_escape(value):
        return value.replace("&", "&amp;").replace('"', "&quot;").replace("'", "&apos;").replace("<", "&lt;").replace(">", "&gt;")

    %s

    #f = open('cmd.txt', 'w')
    #f.write(str(lst))
    #f.close()
    return ''.join(lst)
"""
reg_act = re.compile(
    r"(?P<backslash>\\)|(?P<dollar>\$\$)|(?P<subst>\$\{(?P<code>[^}]*?)\})", re.M
)


def compile_template(line):
    """
    Compile a template expression into a python function (like jsps, but way
    shorter)
    """
    extr = []

    def repl(match):
        g = match.group
        if g("dollar"):
            return "$"
        elif g("backslash"):
            return "\\"
        elif g("subst"):
            extr.append(g("code"))
            return "<<|@|>>"
        return None

    line2 = reg_act.sub(repl, line)
    params = line2.split("<<|@|>>")
    assert extr

    indent = 0
    buf = []
    app = buf.append

    def app(txt):
        buf.append(indent * "    " + txt)

    for x in range(len(extr)):
        if params[x]:
            app("lst.append(%r)" % params[x])

        f = extr[x]
        if f.startswith("if") or f.startswith("for"):
            app(f + ":")
            indent += 1
        elif f.startswith("py:"):
            app(f[3:])
        elif f.startswith("endif") or f.startswith("endfor"):
            indent -= 1
        elif f.startswith("else") or f.startswith("elif"):
            indent -= 1
            app(f + ":")
            indent += 1
        elif f.startswith("xml:"):
            app("lst.append(xml_escape(%s))" % f[4:])
        else:
            app("lst.append(%s)" % f)

    if extr:
        if params[-1]:
            app("lst.append(%r)" % params[-1])

    fun = COMPILE_TEMPLATE % "\n    ".join(buf)
    return Task.funex(fun)


re_blank = re.compile("(\n|\r|\\s)*\n", re.M)


def rm_blank_lines(txt):
    txt = re_blank.sub("\r\n", txt)
    return txt


BOM = "\xef\xbb\xbf"
try:
    BOM = bytes(BOM, "iso8859-1")  # python 3
except:
    pass


def stealth_write(self, data, flags="wb"):
    try:
        unicode
    except:
        data = data.encode("utf-8")  # python 3
    else:
        data = data.decode(sys.getfilesystemencoding(), "replace")
        data = data.encode("utf-8")

    if self.name.endswith(".vcproj") or self.name.endswith(".vcxproj"):
        data = BOM + data

    try:
        txt = self.read(flags="rb")
        if txt != data:
            raise ValueError("must write")
    except (IOError, ValueError):
        self.write(data, flags=flags)
    else:
        Logs.debug("msvs: skipping %s" % self.abspath())


Node.Node.stealth_write = stealth_write

re_quote = re.compile("[^a-zA-Z0-9-]")


def quote(s):
    return re_quote.sub("_", s)


def xml_escape(value):
    value = value.replace("&", "&amp;")
    value = value.replace('"', "&quot;")
    value = value.replace("'", "&apos;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")
    return value


def make_uuid(v, prefix=None):
    """
    simple utility function
    """
    if isinstance(v, dict):
        keys = list(v.keys())
        keys.sort()
        tmp = str([(k, v[k]) for k in keys])
    else:
        tmp = str(v)
    d = Utils.md5(tmp.encode()).hexdigest().upper()
    if prefix:
        d = "%s%s" % (prefix, d[8:])
    gid = uuid.UUID(d, version=4)
    return str(gid).upper()


def diff(node, fromnode):
    # difference between two nodes, but with "(..)" instead of ".."
    c1 = node
    c2 = fromnode

    c1h = c1.height()
    c2h = c2.height()

    lst = []
    up = 0

    while c1h > c2h:
        lst.append(c1.name)
        c1 = c1.parent
        c1h -= 1

    while c2h > c1h:
        up += 1
        c2 = c2.parent
        c2h -= 1

    while id(c1) != id(c2):
        lst.append(c1.name)
        up += 1

        c1 = c1.parent
        c2 = c2.parent

    for i in range(up):
        lst.append("(..)")
    lst.reverse()
    return tuple(lst)


class build_property(object):
    pass


class vsnode(object):

    """
    Abstract class representing visual studio elements
    We assume that all visual studio nodes have a uuid and a parent
    """

    def __init__(self, ctx):
        self.ctx = ctx  # msvs context
        self.name = ""  # string, mandatory
        # path in visual studio (name for dirs, absolute path for projects)
        self.vspath = ""
        self.uuid = ""  # string, mandatory
        self.parent = None  # parent node for visual studio nesting

    def get_waf(self):
        """
        Override in subclasses...
        """
        return 'cd /d "{}" & {}'.format(
            self.ctx.srcnode.abspath(), getattr(self.ctx, "waf_command", "python waf")
        )

    def ptype(self):
        """
        Return a special uuid for projects written in the solution file
        """
        pass

    def write(self):
        """
        Write the project file, by default, do nothing
        """
        pass

    def make_uuid(self, val):
        """
        Alias for creating uuid values easily (the templates cannot access
        global variables)
        """
        return make_uuid(val)


class vsnode_vsdir(vsnode):

    """
    Nodes representing visual studio folders (which do not match the filesystem
    tree!)
    """

    VS_GUID_SOLUTIONFOLDER = "2150E333-8FDC-42A3-9474-1A3956D46DE8"

    def __init__(self, ctx, uuid, name, vspath=""):
        vsnode.__init__(self, ctx)
        self.title = self.name = name
        self.uuid = uuid
        self.vspath = vspath or name

    def ptype(self):
        return self.VS_GUID_SOLUTIONFOLDER


class vsnode_project(vsnode):

    """
    Abstract class representing visual studio project elements
    A project is assumed to be writable, and has a node representing the file
    to write to
    """

    VS_GUID_VCPROJ = "8BC9CEB8-8B4A-11D0-8D11-00A0C91BC942"

    def ptype(self):
        return self.VS_GUID_VCPROJ

    def __init__(self, ctx, node):
        vsnode.__init__(self, ctx)
        self.path = node
        self.uuid = make_uuid(node.abspath())
        self.name = node.name
        self.platformver = ctx.platformver
        self.title = self.path.relpath()
        self.srcnode = ctx.srcnode
        self.source = []  # list of node objects
        # list of properties (nmake commands, output dir, etc)
        self.build_properties = []

    def dirs(self):
        """
        Get the list of parent folders of the source files (header files
        included) for writing the filters
        """
        lst = []

        def add(x):
            if x.height() > self.srcnode.height() and x not in lst:
                lst.append(x)
                if x.parent:
                    add(x.parent)

        for x in self.source:
            add(x.parent)
        return lst

    def write(self):
        Logs.debug("msvs: creating %r" % self.path)

        # first write the project file
        template1 = compile_template(PROJECT_TEMPLATE)
        proj_str = template1(self)
        proj_str = rm_blank_lines(proj_str)
        self.path.stealth_write(proj_str)

        # then write the filter
        template2 = compile_template(FILTER_TEMPLATE)
        filter_str = template2(self)
        filter_str = rm_blank_lines(filter_str)
        tmp = self.path.parent.make_node(self.path.name + ".filters")
        tmp.stealth_write(filter_str)

    def get_key(self, node):
        """
        required for writing the source files
        """
        name = node.name
        if name.endswith(".cpp") or name.endswith(".c"):
            return "ClCompile"
        return "ClInclude"

    def collect_properties(self):
        """
        Returns a list of triplet (configuration, platform, output_directory)
        """
        ret = []
        for c in self.ctx.configurations:
            for p in self.ctx.platforms:
                x = build_property()
                x.outdir = ""

                x.configuration = c
                x.platform = p

                x.preprocessor_definitions = ""
                x.includes_search_path = ""

                # can specify "deploy_dir" too
                ret.append(x)
        self.build_properties = ret

    def get_build_params(self, props):
        ##        opt = '--execsolution=%s' % self.ctx.get_solution_node().abspath()
        # return (self.get_waf(), opt)
        return self.get_waf()

    def get_build_command(self, props):
        return "%s build" % self.get_build_params(props)

    def get_clean_command(self, props):
        return "%s clean" % self.get_build_params(props)

    def get_rebuild_command(self, props):
        return "%s clean build" % self.get_build_params(props)

    def get_filter_name(self, node):
        # Create project tree relative to the project file
        lst = diff(node, self.srcnode)
        return "\\".join(lst) or "."
        return self.name


class vsnode_alias(vsnode_project):
    def __init__(self, ctx, node, name):
        vsnode_project.__init__(self, ctx, node)
        self.name = name
        self.output_file = ""


class vsnode_build_all(vsnode_alias):

    """
    Fake target used to emulate the behavior of "make all" (starting one
    process by target is slow). This is the only alias enabled by default.
    """

    def __init__(self, ctx, node, name="build_all_projects"):
        vsnode_alias.__init__(self, ctx, node, name)
        self.is_active = True


class vsnode_install_all(vsnode_alias):

    """
    Fake target used to emulate the behavior of "make install"
    """

    def __init__(self, ctx, node, name="install_all_projects"):
        vsnode_alias.__init__(self, ctx, node, name)

    def get_build_command(self, props):
        return "%s build install" % self.get_build_params(props)

    def get_clean_command(self, props):
        return "%s clean" % self.get_build_params(props)

    def get_rebuild_command(self, props):
        return "%s clean build install" % self.get_build_params(props)


class vsnode_project_view(vsnode_alias):

    """
    Fake target used to emulate a file system view
    """

    def __init__(self, ctx, node, name="project_view"):
        vsnode_alias.__init__(self, ctx, node, name)
        self.tg = self.ctx()  # fake one, cannot remove
        self.exclude_files = (
            Node.exclude_regs
            + """
waf-1.7.*
waf3-1.7.*/**
.waf-1.7.*
.waf3-1.7.*/**
**/*.sdf
**/*.suo
**/*.ncb
**/{}
        """.format(
                Options.lockfile
            )
        )

    def collect_source(self):
        # this is likely to be slow
        self.source = self.ctx.srcnode.ant_glob("**", excl=self.exclude_files)

    def get_build_command(self, props):
        params = self.get_build_params(props) + (self.ctx.cmd,)
        return "%s %s %s" % params

    def get_clean_command(self, props):
        return ""

    def get_rebuild_command(self, props):
        return self.get_build_command(props)


class vsnode_target(vsnode_project):

    """
    Visual studio project representing a target (programs, libraries, etc)
    """

    def __init__(self, ctx, name):
        """
        A project is more or less equivalent to a file/folder
        """
        base = getattr(ctx, "projects_dir", None)
        # the project file as a Node
        node = base.make_node(quote(name) + ctx.project_extension)
        vsnode_project.__init__(self, ctx, node)
        self.name = quote(name)
        self.include_dirs = set()  # set of dirs for includes search path
        self.target_found = False

        # Additonal directory to look for sources in
        self.msvs_extend_sources = getattr(ctx, "msvs_extend_sources", [])

    def get_build_params(self, props):
        """
        Override the default to add the target name
        """
        return self.get_waf()

    def set_includes_search_path(self):

        print("INCLUDE SEARCH PATH:")
        lst = sorted(self.include_dirs)
        pprint(lst, indent=2)
        # Create a string from the list of include dirs
        inc_str = ";".join(lst)
        for x in self.build_properties:
            x.includes_search_path = inc_str

    def collect_source(self):

        exclude_files = (
            Node.exclude_regs
            + """
waf
waf-*
waf3-*
.waf-*
.waf3-*
.lock-*
**/*.pyc
build
build_current
resolve_symlinks
resolved_dependencies
**/.vs
**/*.sln
**/*.vcxproj*
**/*.sdf
**/*.suo
**/*.ncb
**/*.bat
**/*.log
        """
        )

        # Try to include all existing files in the project
        self.source = self.ctx.srcnode.ant_glob("**", excl=exclude_files)

        for srcnode in self.msvs_extend_sources:
            self.source += srcnode.ant_glob("**", excl=exclude_files)

        self.source.sort(key=lambda x: x.abspath())

    def collect_include_dirs(self, tg):
        # print('TARGET INCLUDES: ')
        includes = tg.to_list(getattr(tg, "includes", []))
        # pprint(includes, indent=2)
        for include in includes:
            # Skip include dirs in the 'build' directory
            if isinstance(include, Node.Node) and not include.is_child_of(
                self.ctx.bldnode
            ):
                self.include_dirs.add(include.abspath())

    def collect_properties(self, tg):
        """
        Visual studio projects are associated with platforms and configurations
        (for building especially)
        """
        super(vsnode_target, self).collect_properties()
        for x in self.build_properties:
            x.outdir = self.path.parent.abspath()
            x.preprocessor_definitions = ""
            x.includes_search_path = ""

            try:
                tsk = tg.link_task
            except AttributeError:
                pass
            else:
                self.target_found = True
                print("OUTPUT PATH:\n\t" + tsk.outputs[0].abspath())
                x.output_file = tsk.outputs[0].abspath()
                x.working_dir = tsk.outputs[0].parent.abspath()
                x.preprocessor_definitions = ";".join(tsk.env.DEFINES)


class msvs_generator(WafBuildContext):

    """generates a Visual Studio 2010 solution"""

    cmd = "msvs2010"
    fun = "build"

    def init(self):
        """
        Some data that needs to be present
        """
        if not getattr(self, "numver", None):
            self.numver = "11.00"
        if not getattr(self, "vsver", None):
            self.vsver = "2010"
        if not getattr(self, "platformver", None):
            self.platformver = "v100"

        if not getattr(self, "configurations", None):
            self.configurations = ["Release"]  # LocalRelease, RemoteDebug, etc
        if not getattr(self, "platforms", None):
            self.platforms = ["Win32"]
        if not getattr(self, "all_projects", None):
            self.all_projects = []
        if not getattr(self, "project_extension", None):
            self.project_extension = "_2010.vcxproj"
        if not getattr(self, "solution_name", None):
            self.solution_name = (
                getattr(Context.g_module, Context.APPNAME, "project") + "_2010.sln"
            )
        if not getattr(self, "projects_dir", None):
            self.projects_dir = self.srcnode

        # bind the classes to the object, so that subclass can provide custom
        # generators
        if not getattr(self, "vsnode_vsdir", None):
            self.vsnode_vsdir = vsnode_vsdir
        if not getattr(self, "vsnode_target", None):
            self.vsnode_target = vsnode_target
        if not getattr(self, "vsnode_build_all", None):
            self.vsnode_build_all = vsnode_build_all
        if not getattr(self, "vsnode_install_all", None):
            self.vsnode_install_all = vsnode_install_all
        if not getattr(self, "vsnode_project_view", None):
            self.vsnode_project_view = vsnode_project_view

        if not getattr(self, "main_project", None):
            self.main_project = self.vsnode_target(
                self, getattr(Context.g_module, Context.APPNAME, "project")
            )

    def pre_recurse(self, node):

        super(msvs_generator, self).pre_recurse(node)

        # Call build() in all dependencies before executing build()
        # in the top-level wscript: this allows us to go through all
        # task generators from the dependencies and save all available
        # include directories for the main project's includes_search_path
        if self.is_toplevel():
            self.recurse_dependencies()

    def execute(self):
        """
        Entry point
        """
        self.restore()
        if not self.all_envs:
            self.load_envs()
        self.recurse([self.run_dir])

        # user initialization
        self.init()

        # two phases for creating the solution:
        # add project objects into "self.all_projects"
        self.collect_projects()
        # write the corresponding project and solution files
        self.write_files()

    def collect_projects(self):
        """
        Fill the list self.all_projects with project objects
        Fill the list of build targets
        """

        self.collect_targets()
        self.main_project.collect_source()
        self.main_project.set_includes_search_path()
        self.all_projects.append(self.main_project)

    def write_files(self):
        """
        Write the project and solution files from the data collected
        so far. It is unlikely that you will want to change this
        """
        for p in self.all_projects:
            p.write()

        # and finally write the solution file
        node = self.get_solution_node()
        node.parent.mkdir()
        Logs.warn("Creating %r" % node)
        template1 = compile_template(SOLUTION_TEMPLATE)
        sln_str = template1(self)
        sln_str = rm_blank_lines(sln_str)
        node.stealth_write(sln_str)

    def get_solution_node(self):
        """
        The solution filename is required when writing the .vcproj files
        return self.solution_node and if it does not exist, make one
        """
        try:
            return self.solution_node
        except:
            pass

        solution_name = getattr(self, "solution_name", None)

        if os.path.isabs(solution_name):
            self.solution_node = self.root.make_node(solution_name)
        else:
            self.solution_node = self.srcnode.make_node(solution_name)
        return self.solution_node

    def project_configurations(self):
        """
        Helper that returns all the pairs (config,platform)
        """
        ret = []
        for c in self.configurations:
            for p in self.platforms:
                ret.append((c, p))
        return ret

    def collect_targets(self):
        """
        Process the list of task generators
        """
        for g in self.groups:
            for tg in g:
                if not isinstance(tg, TaskGen.task_gen):
                    continue

                print(str.format("Processing: {}", tg))

                tg.post()

                # Load include dirs from all active taskgens
                self.main_project.collect_include_dirs(tg)

                if not getattr(tg, "link_task", None):
                    continue
                # Skip any taskgens that are outside the project directory
                if not tg.path.is_child_of(self.srcnode):
                    continue
                # Also skip the taskgens in the 'resolve_symlinks' directory
                if "resolve_symlinks" in tg.path.abspath():
                    continue

                # pprint(tg.__dict__, indent=2)

                if not self.main_project.target_found:
                    type = getattr(tg, "typ", None)
                    if type == "program":
                        print("MAIN PROGRAM FOUND:\n\t{}".format(tg))
                        self.main_project.collect_properties(tg)

        # If no main program was found, then create a build configuration
        # with an empty taskgen
        if not self.main_project.target_found:
            self.main_project.collect_properties(None)
            # Set the default debugger command to "python waf --run_tests"
            self.main_project.debugger_command = "python.exe"
            self.main_project.debugger_command_args = "waf --run_tests"


def wrap_2008(cls):
    class dec(cls):
        def __init__(self, *k, **kw):
            cls.__init__(self, *k, **kw)
            self.project_template = PROJECT_2008_TEMPLATE

        def display_filter(self):

            root = build_property()
            root.subfilters = []
            root.sourcefiles = []
            root.source = []
            root.name = ""

            @Utils.run_once
            def add_path(lst):
                if not lst:
                    return root
                child = build_property()
                child.subfilters = []
                child.sourcefiles = []
                child.source = []
                child.name = lst[-1]

                par = add_path(lst[:-1])
                par.subfilters.append(child)
                return child

            for x in self.source:
                # this crap is for enabling subclasses to override
                # get_filter_name
                tmp = self.get_filter_name(x.parent)
                tmp = tmp != "." and tuple(tmp.split("\\")) or ()
                par = add_path(tmp)
                par.source.append(x)

            def display(n):
                buf = []
                for x in n.source:
                    buf.append(
                        '<File RelativePath="%s" FileType="%s"/>\n'
                        % (xml_escape(x.abspath()), self.get_key(x))
                    )
                for x in n.subfilters:
                    buf.append('<Filter Name="%s">' % xml_escape(x.name))
                    buf.append(display(x))
                    buf.append("</Filter>")
                return "\n".join(buf)

            return display(root)

        def get_key(self, node):
            """
            If you do not want to let visual studio use the default file
            extensions, override this method to return a value:
            0: C/C++ Code, 1: C++ Class, 2: C++ Header File, 3: C++ Form,
            4: C++ Control, 5: Text File, 6: DEF File, 7: IDL File,
            8: Makefile, 9: RGS File, 10: RC File, 11: RES File, 12: XSD File,
            13: XML File, 14: HTML File, 15: CSS File, 16: Bitmap, 17: Icon,
            18: Resx File, 19: BSC File, 20: XSX File, 21: C++ Web Service,
            22: ASAX File, 23: Asp Page, 24: Document, 25: Discovery File,
            26: C# File, 27: eFileTypeClassDiagram, 28: MHTML Document,
            29: Property Sheet, 30: Cursor, 31: Manifest, 32: eFileTypeRDLC
            """
            return ""

        def write(self):
            Logs.debug("msvs: creating %r" % self.path)
            template1 = compile_template(self.project_template)
            proj_str = template1(self)
            proj_str = rm_blank_lines(proj_str)
            self.path.stealth_write(proj_str)

    return dec


class msvs_2008_generator(msvs_generator):

    """generates a Visual Studio 2008 solution"""

    cmd = "msvs2008"
    fun = msvs_generator.fun

    def init(self):
        self.numver = "10.00"
        self.vsver = "2008"
        self.platformver = "v90"

        if not getattr(self, "project_extension", None):
            self.project_extension = "_2008.vcproj"
        if not getattr(self, "solution_name", None):
            self.solution_name = (
                getattr(Context.g_module, Context.APPNAME, "project") + "_2008.sln"
            )

        if not getattr(self, "vsnode_target", None):
            self.vsnode_target = wrap_2008(vsnode_target)
        if not getattr(self, "vsnode_build_all", None):
            self.vsnode_build_all = wrap_2008(vsnode_build_all)
        if not getattr(self, "vsnode_install_all", None):
            self.vsnode_install_all = wrap_2008(vsnode_install_all)
        if not getattr(self, "vsnode_project_view", None):
            self.vsnode_project_view = wrap_2008(vsnode_project_view)

        msvs_generator.init(self)


class msvs_2012_generator(msvs_generator):

    """generates a Visual Studio 2012 solution"""

    cmd = "msvs2012"
    fun = msvs_generator.fun

    def init(self):
        self.numver = "12.00"
        self.vsver = "2012"
        self.platformver = "v110"

        if not getattr(self, "project_extension", None):
            self.project_extension = "_2012.vcxproj"
        if not getattr(self, "solution_name", None):
            self.solution_name = (
                getattr(Context.g_module, Context.APPNAME, "project") + "_2012.sln"
            )

        msvs_generator.init(self)


class msvs_2017_generator(msvs_generator):

    """generates a Visual Studio 2017 solution"""

    cmd = "msvs2017"
    fun = msvs_generator.fun

    def init(self):
        self.numver = "12.00"
        self.vsver = "15"
        self.platformver = "v141"

        if not getattr(self, "project_extension", None):
            self.project_extension = "_2017.vcxproj"
        if not getattr(self, "solution_name", None):
            self.solution_name = (
                getattr(Context.g_module, Context.APPNAME, "project") + "_2017.sln"
            )

        msvs_generator.init(self)
