#!/usr/bin/env python
# encoding: utf-8

from waflib import Errors
from waflib.Configure import conf
from waflib.Configure import ConfigurationContext


# List of supported C++ standards
cxx_standards = ["c++98", "c++03", "c++11", "c++14", "c++17", "c++20", "c++23", "c++26"]

# Map of aliases for C++ standards
cxx_standard_aliases = {
    "c++11": "c++0x",
    "c++14": "c++1y",
    "c++17": "c++1z",
    "c++20": "c++2a",
    "c++23": "c++2b",
    "c++26": "c++2c",
}


def configure(conf):
    """
    Configure the C++ standard used to build the project.
    """
    old_post_recurse = ConfigurationContext.post_recurse

    def post_recurse(self, node):
        if self.is_toplevel():
            cxx_standard = self.env["CXX_STANDARD"]
            self.start_msg("Using the {0} Standard".format(cxx_standard.upper()))

            # Check that the standard is supported by the compiler
            if cxx_standard not in self.env["CXX_SUPPORTED_STANDARDS"]:
                self.fatal(
                    "The C++ standard {0} is not supported by the {1} compiler.".format(
                        cxx_standard, self.env["COMPILER_CXX"]
                    )
                )
            else:
                self.end_msg("ok")
                self.env.CXXFLAGS += [self.env["CXX_SUPPORTED_STANDARDS"][cxx_standard]]

        old_post_recurse(self, node)

    ConfigurationContext.post_recurse = post_recurse


@conf
def check_cxx_standard(conf):
    """
    Check which C++ standard is supported by the compiler.
    This will set the CXX_STANDARD_MINIMUM and CXX_STANDARD_MAXIMUM
    in the environment.
    """
    compiler = conf.env["COMPILER_CXX"]
    major = int(conf.env["CC_VERSION"][0])

    conf.env["CXX_SUPPORTED_STANDARDS"] = {}

    # monkey patch start_msg and end_msg to avoid printing
    # the messages to the console
    def start_msg(self, *k, **kw):
        pass

    def end_msg(self, *k, **kw):
        pass

    # cache the original start_msg and end_msg
    old_start_msg = conf.start_msg
    old_end_msg = conf.end_msg

    conf.start_msg = start_msg
    conf.end_msg = end_msg

    for cxx_standard in cxx_standards:
        cxx_standard_flags = conf.get_cxx_standard_flags(compiler, major, cxx_standard)
        for cxx_standard_flag in cxx_standard_flags:
            ret = conf.check_cxx(
                cxxflags=cxx_standard_flag,
                mandatory=False,
            )
            if ret:
                conf.env["CXX_SUPPORTED_STANDARDS"][cxx_standard] = cxx_standard_flag
                break

    # restore the original start_msg and end_msg
    conf.start_msg = old_start_msg
    conf.end_msg = old_end_msg

    if conf.env["CXX_SUPPORTED_STANDARDS"] == {}:
        conf.fatal(
            "Could not determine the C++ standard supported by the compiler {0}.".format(
                compiler
            )
        )


@conf
def get_cxx_standard_flags(conf, compiler, major, cxx_standard):
    if "clang" in compiler or "g++" in compiler:
        flags = ["-std={0}".format(cxx_standard)]
        if cxx_standard in cxx_standard_aliases:
            flags.append("-std={0}".format(cxx_standard_aliases[cxx_standard]))
        return flags
    elif "msvc" in compiler or "CL.exe" in compiler or "cl.exe" in compiler:
        return ["/std:{0}".format(cxx_standard)]
    else:
        raise Errors.WafError("Unknown compiler: %s" % compiler)


@conf
def set_cxx_standard(conf, cxx_standard):
    """
    Set the C++ standard whose features are requested to build this target.

    :param cxx_standard: the minimum C++ standard to use
    """

    # If the user has specified a number then we convert it to a string
    if isinstance(cxx_standard, int):
        if cxx_standard == 3:
            cxx_standard = "c++03"
        else:
            cxx_standard = "c++{}".format(cxx_standard)

    if cxx_standard not in cxx_standards:
        conf.fatal(
            "The C++ standard {0} is not supported. "
            "Supported standards are {1}".format(cxx_standard, cxx_standards)
        )

    # If the user has specified a standard which is lower than
    # the previous standard then we keep the previous standard
    if not conf.env["CXX_STANDARD"]:
        conf.env["CXX_STANDARD"] = cxx_standard
    elif cxx_standards.index(cxx_standard) > cxx_standards.index(
        conf.env["CXX_STANDARD"]
    ):
        conf.env["CXX_STANDARD"] = cxx_standard
    elif cxx_standards.index(cxx_standard) < cxx_standards.index(
        conf.env["CXX_STANDARD"]
    ):
        conf.fatal(
            "The C++ standard {0} is lower than the "
            "previous standard {1} specified in a dependency.".format(
                cxx_standard, conf.env["CXX_STANDARD"]
            )
        )
