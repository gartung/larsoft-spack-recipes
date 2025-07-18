# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.fnal_art.packages.fnal_github_package.package import *


class Larbatch(CMakePackage, FnalGithubPackage):
    """package for batch job submission featuring project.py"""

    repo = "LArSoft/larbatch"
    version_patterns = ["v01_00_00"]

    version("01.60.01", sha256="81fab1ead869b4d45751d215685e97878b7796daeada2dbbe699b38f5ae9dade")
    version("01.59.04", sha256="8158d2e1b5f208d1014b3745c347d49e3e3449c240842af5361c67fd3b269dff")
    version("develop", branch="develop", get_full_repo=True)

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("sam-web-client", type=("run"))
    depends_on("python", type=("run"))
    depends_on("cetmodules", type="build")

    @run_before("cmake")
    def patch_version(self):
        print("filtering version in CMakeLists.txt")
        filter_file(
            r"project\(larbatch .*\)",
            "project(larbatch VERSION {})".format(self.spec.version),
            "CMakeLists.txt",
        )

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("PYTHONPATH", self.prefix.bin)
        env.prepend_path("PYTHONPATH", self.prefix.python)
        env.prepend_path(
            "PYTHONPATH",
            str(self.prefix.larbatch.v) + str(self.spec.version.underscored) + "/python",
        )
