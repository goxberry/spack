##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import sys
import inspect


class Libelf(AutotoolsPackage):
    """libelf lets you read, modify or create ELF object files in an
       architecture-independent way. The library takes care of size
       and endian issues, e.g. you can process a file for SPARC
       processors on an Intel-based system."""

    homepage = "http://www.mr511.de/software/english.html"
    url      = "http://www.mr511.de/software/libelf-0.8.13.tar.gz"

    version('0.8.13', '4136d7b4c04df68b686570afa26988ac')
    version('0.8.12', 'e21f8273d9f5f6d43a59878dc274fec7')

    provides('elf@0')

    # To build a shared library, must run autoreconf
    depends_on('m4', type='build', when='platform=darwin')
    depends_on('autoconf', type='build', when='platform=darwin')
    depends_on('automake', type='build', when='platform=darwin')
    depends_on('libtool', type='build', when='platform=darwin')
    force_autoreconf = (True if sys.platform == 'darwin' else False)

    @when('platform=darwin')
    def autoreconf(self, spec, prefix):
        with working_dir(self.configure_directory):
            m = inspect.getmodule(self)
            # This line is what is needed most of the time
            # --install, --verbose, --force
            autoreconf_args = ['-ivf']
            m.autoreconf(*autoreconf_args)

    def configure_args(self):
        args = ["--enable-shared",
                "--disable-dependency-tracking",
                "--disable-debug"]

        # Flags courtesy of NixOS:
        # https://git.mayflower.de/NixOS/nixpkgs/commit/e73d805aa9f7349cc32d5a89c20efb7a3f86eba4
        if self.spec.satisfies('platform=darwin'):
            # Configure check for dynamic lib support is broken, see
            # http://lists.uclibc.org/pipermail/uclibc-cvs/2005-August/019383.html
            # Passing this option requires running autoreconf
            args.append('mr_cv_target_elf=yes')
            # Libelf's custom NLS macros fail to determine the catalog file extension
            # on Darwin, so disable NLS for now.
            args.append('--disable-nls')

        return args

    def install(self, spec, prefix):
        make('install', parallel=False)
