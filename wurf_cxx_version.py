#!/usr/bin/env python
# encoding: utf-8

from waflib import Errors
from waflib.Configure import conf
from waflib.Configure import ConfigurationContext


# List of supported C++ stds
cxx_stds = ["c++98", "c++03", "c++11", "c++14", "c++17", "c++20", "c++23", "c++26"]

# Map of aliases for C++ stds
cxx_std_aliases = {
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
            cxx_std = self.env["CXX_STD"]
            if not cxx_std:
                self.msg("No C++ standard specified", "ok", color="YELLOW")
                return
            origin = conf.env["CXX_STD_ORIGIN"]
            self.start_msg(f"Using {cxx_std.upper()} (required by {origin})")

            # Check that the std is supported by the compiler
            if cxx_std not in self.env["CXX_SUPPORTED_STDS"]:
                self.fatal(
                    f"The C++ standard {cxx_std} is not supported by the {self.env['CXX']} compiler."
                )

            else:
                self.end_msg("ok")
                # Add the flag for the C++ standard to the list of C++ flags
                self.env.CXXFLAGS += [self.env["CXX_SUPPORTED_STDS"][cxx_std]]
        # Call the original post_recurse method
        old_post_recurse(self, node)

    ConfigurationContext.post_recurse = post_recurse


def get_cxx_std_flags(compiler, version, cxx_std):
    if "clang" in compiler or "g++" in compiler:
        flags = [f"-std={cxx_std}"]
        if cxx_std in cxx_std_aliases:
            flags.append(f"-std={cxx_std_aliases[cxx_std]}")
        return flags
    elif "msvc" in compiler or "CL.exe" in compiler or "cl.exe" in compiler:
        return [f"/std:{cxx_std}"]
    else:
        raise Errors.WafError(f"Unknown compiler: {compiler} {version}")


@conf
def check_cxx_std(conf):
    """
    Check which C++ standard is supported by the set compiler.
    This will populate the environment variable CXX_SUPPORTED_STDS
    with the list of supported C++ standards and their corresponding flags
    for enabling them.
    """
    compiler = conf.env["CXX"][0]
    version = conf.env["CC_VERSION"]

    conf.env["CXX_SUPPORTED_STDS"] = {}

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

    for cxx_std in cxx_stds:
        cxx_std_flags = get_cxx_std_flags(compiler, version, cxx_std)
        for cxx_std_flag in cxx_std_flags:
            ret = conf.check_cxx(
                cxxflags=cxx_std_flag,
                mandatory=False,
            )
            if ret:
                conf.env["CXX_SUPPORTED_STDS"][cxx_std] = cxx_std_flag
                break

    # restore the original start_msg and end_msg
    conf.start_msg = old_start_msg
    conf.end_msg = old_end_msg

    if conf.env["CXX_SUPPORTED_STDS"] == {}:
        conf.fatal(
            f"Could not determine the C++ standards supported by {compiler} {version}."
        )


@conf
def set_cxx_std(conf, cxx_std):
    """
    Set the C++ standard whose features are requested to build this target.

    :param cxx_std: the C++ standard to use, this can either be
                    a string or an integer. If it is a string then it
                    must be of the following form: c++XX where XX is
                    the year of the standard.
                    If a dependency requests a C++ standard which is
                    higher than the one requested by the project then
                    the higher standard will be used.
    """

    # If the user has specified a number then we convert it to a string
    if isinstance(cxx_std, int):
        if cxx_std == 3:
            cxx_std = "c++03"
        else:
            cxx_std = "c++{}".format(cxx_std)

    if cxx_std not in cxx_stds:
        conf.fatal(f"{cxx_std} is not supported. Supported standards are {cxx_stds}")

    # If the user has specified a standard which is lower than
    # the previous standard then we keep the previous standard
    index = cxx_stds.index(cxx_std)
    current = conf.env["CXX_STD"]
    if not current or index > cxx_stds.index(current):
        conf.env["CXX_STD"] = cxx_std
        # This assumes that the name of the path
        # is the name of the project
        conf.env["CXX_STD_ORIGIN"] = conf.path.name
