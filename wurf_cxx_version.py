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
    """Configure the toolset for managing C++ standard."""

    # Monkey patch the post_recurse method of the ConfigurationContext
    # This is needed to run the check for the highest C++ standard
    # needed by the project and its dependencies.
    old_post_recurse = ConfigurationContext.post_recurse

    def post_recurse(self, node):
        # Only run the check at the top level
        if self.is_toplevel():
            cxx_standard = self.env["CXX_STANDARD"]
            if not cxx_standard:
                self.msg("No C++ standard specified", "ok", color="YELLOW")
                return
            origin = conf.env["CXX_STANDARD_ORIGIN"]
            self.start_msg(f"Using {cxx_standard.upper()} (required by {origin})")

            # Check that the standard is supported by the compiler
            if cxx_standard not in self.env["CXX_SUPPORTED_STANDARDS"]:
                self.fatal(
                    f"The C++ standard {cxx_standard} is not supported by the {self.env['CXX']} compiler."
                )

            else:
                self.end_msg("ok")
                # Add the flag for the C++ standard to the list of C++ flags
                self.env.CXXFLAGS += [self.env["CXX_SUPPORTED_STANDARDS"][cxx_standard]]
        # Call the original post_recurse method
        old_post_recurse(self, node)

    ConfigurationContext.post_recurse = post_recurse


def get_cxx_standard_flags(compiler, major, cxx_standard):
    if "clang" in compiler or "g++" in compiler:
        flags = [f"-std={cxx_standard}"]
        if cxx_standard in cxx_standard_aliases:
            flags.append(f"-std={cxx_standard_aliases[cxx_standard]}")
        return flags
    elif "msvc" in compiler or "CL.exe" in compiler or "cl.exe" in compiler:
        return [f"/std:{cxx_standard}"]
    else:
        raise Errors.WafError("Unknown compiler: %s" % compiler)


@conf
def check_cxx_standard(conf):
    """
    Check which C++ standard is supported by the set compiler.
    This will populate the environment variable CXX_SUPPORTED_STANDARDS
    with the list of supported C++ standards and their corresponding flags
    for enabling them.
    """
    compiler = conf.env["CXX"][0]
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
        cxx_standard_flags = get_cxx_standard_flags(compiler, major, cxx_standard)
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
        conf.fatal(f"Could not determine the C++ standards supported by {compiler}.")


@conf
def set_cxx_standard(conf, cxx_standard):
    """
    Set the C++ standard whose features are requested to build this target.

    :param cxx_standard: the minimum C++ standard to use, this can either be
                            a string or an integer. If it is a string then it
                            must be of the following form: c++XX where XX is
                            the year of the standard.
    """

    # If the user has specified a number then we convert it to a string
    if isinstance(cxx_standard, int):
        if cxx_standard == 3:
            cxx_standard = "c++03"
        else:
            cxx_standard = "c++{}".format(cxx_standard)

    if cxx_standard not in cxx_standards:
        conf.fatal(
            f"{cxx_standard} is not supported. Supported standards are {cxx_standards}"
        )

    # If the user has specified a standard which is lower than
    # the previous standard then we keep the previous standard
    index = cxx_standards.index(cxx_standard)
    current = conf.env["CXX_STANDARD"]
    if not current or index > cxx_standards.index(current):
        conf.env["CXX_STANDARD"] = cxx_standard
        # This assumes that the name of the path
        # is the name of the project
        conf.env["CXX_STANDARD_ORIGIN"] = conf.path.name
