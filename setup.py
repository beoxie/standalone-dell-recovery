#!/usr/bin/python3
#
# Dell Recovery Media install script
# Copyright (C) 2008-2009, Dell Inc.
#  Author: Mario Limonciello <Mario_Limonciello@Dell.com>
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import subprocess
from distutils.core import setup
from DistUtilsExtra.command import (build_extra, 
                                   build_i18n, 
                                   build_help,
                                   build_icons,
                                   clean_i18n)

import glob, os.path, os

def files_only(directory):
    for root, dirs, files in os.walk(directory):
        if root == directory:
            array = []
            for file in files:
                array.append(os.path.join(directory, file))
            return array

I18NFILES = []
for filepath in glob.glob("po/mo/*/LC_MESSAGES/*.mo"):
    lang = filepath[len("po/mo/"):]
    targetpath = os.path.dirname(os.path.join("share/locale",lang))
    I18NFILES.append((targetpath, [filepath]))

setup(
    name="standalone-dell-recovery",
    author="Kevin Rustin Wang",
    author_email="Kevin_Rustin_Wang@Dell.com",
    maintainer="Kevin Rustin Wang",
    maintainer_email="Kevin_Rustin_Wang@Dell.com",
    url="http://linux.dell.com/",
    license="gpl",
    description="Creates a piece of standalone recovery media for Dell Factory Install",
    packages=["Dell"],
    data_files=[('share/dell/bin', ['backend/recovery-media-backend']),
                ('/etc/dbus-1/system.d/', glob.glob('backend/*.conf')),
                ('share/pixmaps', glob.glob("gtk/*.svg")),
                ('share/dbus-1/system-services', glob.glob('backend/*.service')),
                ('/lib/udev/rules.d', glob.glob('udev/*')),
                ('share/dell/scripts', glob.glob('startup/*.py')),
                ('share/dell/gtk', glob.glob('gtk/*.ui'))]+I18NFILES,

    cmdclass = { 'build_i18n': build_i18n.build_i18n,
                 "build_help" : build_help.build_help,
                 'build_icons': build_icons.build_icons,
                 'clean': clean_i18n.clean_i18n,
               }
)

