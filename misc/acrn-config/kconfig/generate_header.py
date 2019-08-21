# Copyright (C) 2018 Intel Corporation.
# SPDX-License-Identifier: BSD-3-Clause

# This script takes a Kconfig and a .config, and generates a C header file with
# all the configuration data defined as object-like macros.

import sys
import os
import re

# Kconfiglib: Copyright (c) 2011-2018, Ulf Magnusson
# SPDX-License-Identifier: ISC
# Refer to scripts/kconfig/LICENSE.kconfiglib for the permission notice.
import kconfiglib

class AcrnConfig(kconfiglib.Kconfig):
    help_regex = re.compile("64-bit[\s\n]+integer")
    def __init__(self, filename="Kconfig", warn=True, warn_to_stderr=True, encoding="utf-8"):
        kconfiglib.Kconfig.__init__(self, filename, warn, warn_to_stderr, encoding)

    def write_autoconf(self, filename,
                       header="/* Generated by Kconfiglib (https://github.com/ulfalizer/"
                       "Kconfiglib) */\n"):

        guard_begin = "#ifndef HV_KCONFIG\n#define HV_KCONFIG\n"
        guard_end = "#endif"

        with open(filename, "w") as f_autoconf:
            f_autoconf.write(header)
            f_autoconf.write(guard_begin)

            for sym in self.defined_syms:
                if sym.config_string in ("", None):
                    continue
                else:
                    val = sym.str_value
                    if sym.orig_type in (kconfiglib.BOOL, kconfiglib.TRISTATE):
                        if val != "n":
                            f_autoconf.write("#define {}{}{} 1\n"
                                    .format(self.config_prefix, sym.name,
                                            "_MODULE" if val == "m" else ""))
                    elif sym.orig_type == kconfiglib.STRING:
                        f_autoconf.write('#define {}{} "{}"\n'
                                .format(self.config_prefix, sym.name,
                                        kconfiglib.escape(val)))
                    elif sym.orig_type in (kconfiglib.INT, kconfiglib.HEX):
                        if sym.orig_type == kconfiglib.HEX:
                            val = val + "U"
                            if not val.startswith(("0x", "0X")):
                                val = "0x" + val
                        elif sym.orig_type == kconfiglib.INT and len(sym.ranges) > 0:
                            left_sym = sym.ranges[0][0]
                            right_sym = sym.ranges[0][1]
                            left_value = int(left_sym.str_value)
                            right_value = int(right_sym.str_value)
                            if left_value >= 0 and right_value >= 0:
                                val = val + "U"

                        _help = sym.nodes[0].help
                        if _help not in (None, "") and len(self.help_regex.findall(_help)) > 0:
                            val = val + "L"
                        f_autoconf.write("#define {}{} {}\n"
                                .format(self.config_prefix, sym.name, val))
                    else:
                        raise Exception(
                            'Internal error while creating C header: unknown type "{}".' \
                            .format(sym.orig_type))

            f_autoconf.write(guard_end)


def usage():
    sys.stdout.write("%s: <Kconfig file> <.config file> <path to config.h>\n" % sys.argv[0])

def main():
    if len(sys.argv) < 4:
        usage()
        sys.exit(1)

    header = "/* Generated by Kconfiglib */\n"
    kconfig_path = sys.argv[1]
    if not os.path.isfile(kconfig_path):
        sys.stderr.write("Cannot find file %s\n" % kconfig_path)
        sys.exit(1)

    config_path = sys.argv[2]
    if not os.path.isfile(config_path):
        sys.stderr.write("Cannot find file %s\n" % config_path)
        sys.exit(1)

    kconfig = AcrnConfig(kconfig_path)
    kconfig.load_config(config_path)
    kconfig.write_autoconf(sys.argv[3], header)
    sys.stdout.write("Configuration header written to %s.\n" % sys.argv[3])

if __name__ == "__main__":
    main()
