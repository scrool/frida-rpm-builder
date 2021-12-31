#!/usr/bin/env python3
"""Majority of this code comes from Frida's code base - releng/release.py. It
was simplified to output only rpms with python 3.10 on Fedora 35 which at the
time of writing wasn't available by upstream.

Contrary to upstream rpms are placed into build/rpm directories of frida-python
and frida-tools. rpms are also not uploaded and removed but kept in place."""

import errno
import glob
import os
import subprocess
import sys


DEBUG=0

if __name__ == "__main__":
    build_dir = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
    if len(build_dir) == 1:
        build_dir = build_dir[1].rstrip("\n")
    else:
        build_dir = os.getcwd()

    frida_python_dir = os.path.join(build_dir, "frida-python")
    frida_tools_dir = os.path.join(build_dir, "frida-tools")

    raw_version = (
        subprocess.check_output(
            ["git", "describe", "--tags", "--always", "--long"], cwd=build_dir
        )
        .decode("utf-8")
        .strip()
        .replace("-", ".")
    )
    (major, minor, micro, nano, commit) = raw_version.split(".")
    version = "%d.%d.%d" % (int(major), int(minor), int(micro))

    def build_python_rpms(distro_name, package_name_prefix, interpreter, extension):
        if DEBUG:
            print("cd %s && \\" % frida_tools_dir)
        cmd = [
            "make",
        ]
        if DEBUG:
            print(f"{cmd}")
        subprocess.check_call(cmd, cwd=frida_tools_dir)

        env = {}
        env.update(os.environ)

        env.update({"PYTHON": interpreter})

        if DEBUG:
            print(f"env {env['PYTHON']=} \\")
        cmd = [
            "make",
            "python-linux-x86_64",
        ]
        if DEBUG:
            print(f"{cmd}")
        subprocess.check_call(cmd, env=env)

        env.update({"FRIDA_VERSION": version, "FRIDA_EXTENSION": extension})

        for module_dir in [frida_python_dir, frida_tools_dir]:
            output_dir = os.path.join(module_dir, "build", "rpm")
            try:
                os.makedirs(output_dir)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            # Fail early because fpm doesn't like rpms already created ahead
            rpms = glob.glob(f"{output_dir}/*.rpm")
            if len(rpms) > 0:
                raise RuntimeError(
                    f"Directory {output_dir} already contains rpms: {rpms}"
                )

            if DEBUG:
                print("cd %s && \\" % module_dir)
                print(f"env {env['FRIDA_VERSION']=} {env['FRIDA_EXTENSION']=} \\")
            cmd = [
                "fpm",
                "--package=" + output_dir,
                "--iteration=1." + distro_name,
                "--maintainer='Ole André Vadla Ravnås <oleavr@frida.re>'",
                "--vendor=Frida",
                "--python-bin=" + interpreter,
                "--python-package-name-prefix=" + package_name_prefix,
                "-s",
                "python",
                "-t",
                "rpm",
                "setup.py",
            ]
            if DEBUG:
                print("%s" % " ".join(cmd))
            subprocess.check_call(cmd, cwd=module_dir, env=env)

    build_python_rpms(
        "fc35",
        "python3",
        "/usr/bin/python3.10",
        os.path.join(
            build_dir,
            "build",
            "frida-linux-x86_64",
            "lib",
            "python3.10",
            "site-packages",
            "_frida.so",
        ),
    )
