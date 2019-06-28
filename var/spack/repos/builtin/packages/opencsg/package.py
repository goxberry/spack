# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Opencsg(QMakePackage):
    """OpenCSG is a library that does image-based CSG rendering using OpenGL."""

    homepage = "http://www.opencsg.org/"
    url      = "http://www.opencsg.org/OpenCSG-1.4.2.tar.gz"

    version('1.4.2', 'd4369f96c2ff671b58f58cc1e894848dde3fdabdb31520f1dc45d754a577c559')

    depends_on('glew')

    def qmake_args(self):
        # Need to figure out how to do two things:
        # 1) inject include directory for GLEW (could I append to INCPATH?)
        # 2) inject lib directory for GLEW via SUBLIBS
        args = ["SUBLIBS=-L%s" % spec['glew'].prefix.lib]
        return args
