#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# WAF build script - this file is part of ZFS-Fuse, a port of the Solaris ZFS to Linux
#
#  Sandeep S Srinivasa <sandys(at)gmail(dot)com>
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
# $Id$

"""
This is a WAF build script (http://code.google.com/p/waf/).
It can be used as an alternative build system to autotools
for zfs-fuse. 
"""


import Build, Configure, Options, Runner, Task, Utils
import sys, os, subprocess, shutil
from distutils import version
from Logs import error, debug, warn



APPNAME = 'zfs-fuse'
VERSION = '0.6.0'

srcdir = '.'
blddir = '__build'

subdirs = """
            src/lib/libsolcompat/
            src/lib/libumem/
            src/lib/libavl/
            src/lib/libsolkerncompat/
            src/lib/libnvpair/
            src/lib/libuutil/
            src/lib/libzpool/
            src/lib/libzfs/
            src/lib/libzfscommon/
            src/zfs-fuse/
            src/cmd/zfs/
            src/cmd/zpool/
            src/cmd/zstreamdump/
            src/cmd/zdb/
            src/cmd/ztest/
          """.split()


#####
#Cmd Line Options
####
def set_options(opt):
    opt.add_option('--prefix', type='string',help='set install path prefix', dest='usr_prefix')
    opt.add_option('--debug', action='store', default='1', help='Choose \'0,1,2,3\' or any comma separated combination thereof')


def init(ctx):
    import Configure

####
#Configuration
####
def configure(conf):
#    import Options # getting the user-provided options to the configuration section
#    if Options.options.usr_prefix
#        Options.prefix = Options.options.usr_prefix


    conf.check_tool('gcc glib2')


#    conf.env.CCFLAGS = ['-Wall']
    conf.env.ASFLAGS = ["-c"]
    conf.env.LINKFLAGS = ['-pipe', '-Wall']
    conf.env.CCFLAGS = ['-pipe', '-Wall', '-std=gnu99', '-Wno-switch', '-Wno-unused', '-Wno-missing-braces', '-Wno-parentheses', '-Wno-uninitialized', '-fno-strict-aliasing', '-D_GNU_SOURCE', '-DLINUX_AIO']
    conf.env.INCLUDEDIR = ['/usr/include/']
#    conf.env['INCLUDEDIR'] = '/usr/include'
#    conf.define('_FILE_OFFSET_BITS', 64) 
#    conf.write_config_header('config.h')

    conf.check(header_name="aio.h", uselib_store='aio_defines', mandatory=True)
    conf.check(lib='aio',  uselib_store='aio_lib', mandatory=True)
    conf.check(lib='ssl',  uselib_store='openssl', mandatory=True)
    conf.check(lib='crypto',  uselib_store='crypto', mandatory=True)
    conf.check(lib='pthread',  uselib_store='pthread_lib', mandatory=True)
    conf.check_cc(lib='fuse',  uselib_store='fuse_lib',  mandatory=True)
    conf.check_cc(lib='dl',  uselib_store='dl_lib',  mandatory=True)
    conf.check_cc(lib='z',  uselib_store='z_lib',  mandatory=True)
    conf.check_cc(lib='m',  uselib_store='m_lib',  mandatory=True)
    conf.check_cc(header_name='fuse/fuse_lowlevel.h', includes=['/usr/include/'], 
            ccflags='-D_FILE_OFFSET_BITS=64', uselib_store='fuse_defines', mandatory=True)
    conf.check(
        		fragment='#include <sys/types.h>\n #include <attr/xattr.h>\nint main() { return 0; }\n',
        		define_name='xattr_defines',
        		execute=1,
        		define_ret=1,
            mandatory=True,
        		msg='Checking for <attr/xattr.h>')
    conf.check_cc(lib='rt', uselib_store='rt_lib', mandatory=True)
    conf.check_tool('gas')
    #if not conf.env.AS: conf.env.AS = conf.env.CC
    conf.env.AS = conf.env.CC


    ###################### install configuration ################

    conf.check_tool('gnu_dirs')
    warn(" setting MANDIR = %s" % conf.env.MANDIR)
    conf.env.PREFIX = '/'
    conf.env.MANDIR = '/usr/share/man/man8'
    
    debug_3 = conf.env.copy()
    debug_2 = conf.env.copy()
    debug_1 = conf.env.copy()
    debug_0 = conf.env.copy()

    
    debug_3.set_variant('debug_3')
    conf.set_env_name('debug_3', debug_3)
    #conf.setenv('debug_3')
    #sss - this is a hack. dunno why ASFLAGS dont propagate. maybe a bug
    debug_3.ASFLAGS='-c'
    debug_3.append_value('CCFLAGS', ['-ggdb', '-DDEBUG', '-finstrument-functions'])
    debug_3.append_value('LINKFLAGS', ['-ggdb'])
    
    debug_2.set_variant('debug_2')
    conf.set_env_name('debug_2', debug_2)
    #conf.setenv('debug_2')
    #sss - this is a hack. dunno why ASFLAGS dont propagate. maybe a bug
    debug_2.ASFLAGS='-c'
    debug_2.append_value('CCFLAGS',['-ggdb', '-DDEBUG'])
    debug_2.append_value('LINKFLAGS', ['-ggdb'])
    
    debug_1.set_variant('debug_1')
    conf.set_env_name('debug_1', debug_1)
    #conf.setenv('debug_1')
    #sss - this is a hack. dunno why ASFLAGS dont propagate. maybe a bug
    debug_1.ASFLAGS='-c'
    debug_1.append_value( 'CCFLAGS',['-ggdb', '-O2', '-DDEBUG'])
    debug_1.append_value('LINKFLAGS', ['-ggdb'])
    
    debug_0.set_variant('debug_0')
    conf.set_env_name('debug_0', debug_0)
    #conf.setenv('debug_0')
    #sss - this is a hack. dunno why ASFLAGS dont propagate. maybe a bug
    debug_0.ASFLAGS='-c'
    debug_0.append_value('CCFLAGS', ['-s', '-O2', '-DNDEBUG'])
    debug_0.append_value('LINKFLAGS',['-s'])

    conf.sub_config("src/lib/libumem")
####
#Build
####
def build(bld):
    bld.add_subdirs(subdirs)
    bld.includes = '/usr/include/'
    #man_list = bld.path.ant_glob('doc/*.gz')
    bld.install_files('${MANDIR}', 'doc/*.gz')
    
    # enable the debug or the release variant, depending on the one wanted
    for obj in bld.all_task_gen[:]:
      debug_3_obj = obj.clone('debug_3')
      debug_2_obj = obj.clone('debug_2')
      debug_1_obj = obj.clone('debug_1')
      debug_0_obj = obj.clone('debug_0')

      #disable "default"
      obj.posted = 1


      # disable the unwanted variant(s)
      build_type = Options.options.debug
      if build_type.find('3') < 0:
        debug_3_obj.posted = 1
      if build_type.find('2') < 0:
        debug_2_obj.posted = 1
      if build_type.find('1') < 0:
        debug_1_obj.posted = 1
      if build_type.find('0') < 0:
        debug_0_obj.posted = 1
