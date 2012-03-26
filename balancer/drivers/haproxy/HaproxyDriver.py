# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License

import re
import sys
import os
import shutil
import logging


from balancer.drivers.BaseDriver import BaseDriver
#from balancer.drivers.haproxy.Context import Context

logger = logging.getLogger(__name__)

class HaproxyDriver(BaseDriver):
    def __init__(self):
        
        pass

    def createRServer(self, vserver, rserver,  context):
        if not bool(rserver.name): 
            return 'RSERVER NAME ERROR'
        if rserver.port == 'any':
            rserver.port = ''
        config_file  =  HaproxyConfigFile(context.tmp_config)
        config_file.AddRServer(vserver.name,  rserver.name,  rserver.address,  rserver.port)
        return True

    
    def deleteRServer(self, vserver,  context, rserver):
        if not bool(rserver.name): 
            return 'RSERVER NAME ERROR'
        config_file  = HaproxyConfigFile(context.tmp_config)
        config_file.DeleteRServer (vserver.name,  rserver.name)

    
    def createVIP(self,  context, vip,  sfarm): 
        pass
        
    
    
    def deleteVIP(self,  context,  vip):
        pass
        
        
class HaproxyFronted:
    def __init__(self):
        self.name = ""
        self.bind_address = ""
        self.bind_port= ""
        self.default_backend = ""
        self.mode = "http"

class HaproxyBackend:
    def __init__(self):
        self.name = ""
        self.mode = ""
        self.balance = "source"
   
class HaproxyRserver:
    def __init__(self):
        self.name = ""
        self.address = ""
        self.check = False
        self.cookie = ""
        self.disabled = False
        self.error_limit = 10
        self.fall = 0
        self.id = ""
        self.inter = 2000
        self.fastinter = 2000
        self.downinter = 2000
        self.maxconn = 0
        self.minconn = 0
        self.observe = ""
        self.on_error = ""
        self.port = ""
        self.redir = ""
        self.rise = 2
        self.slowstart = 0
        self.source_addres = ""
        self.source_min_port = ""
        self.source_max_port = ""
        self.track = ""
        self.weight = 1
        
class HaproxyConfigFile:
    def __init__(self, haproxy_config_file_path = '/tmp/haproxy.cfg',  test_config=''):
        if test_config != '':  shutil.copyfile (test_config, "/tmp/haproxy.cfg")
        self.haproxy_config_file_path = haproxy_config_file_path
        
    def GetHAproxyConfigFileName(self):
        return self.haproxy_config_file_path
    def DeleteListenBlock (self,  ListenBlockName):
        self.haproxy_config_file = open (self.haproxy_config_file_path,  "r")
        block_start=False
        new_config_file = []
        for line in  self.haproxy_config_file :
            if  not line.strip(): continue
            if line.find('listen' ) == 0 and  line.find(ListenBlockName) > 0:
                block_start = True
                continue
            elif line.find('listen' ) == -1 and block_start == True:
                continue
            elif  line.find('listen' ) == 0 and block_start == True:
                block_start = False
            new_config_file.append(line.rstrip())
        self.haproxy_config_file.close()
        self.haproxy_config_file = open (self.haproxy_config_file_path,  "w")
        for out_line in new_config_file:
            self.haproxy_config_file.write("%s\n" % out_line)
        self.haproxy_config_file.close()
        return ListenBlockName
 
    def DeleteRServerFromListenBlockName (self, ListenBlockName, RServerName):
        self.haproxy_config_file = open (self.haproxy_config_file_path,  "r")
        block_start=False
        new_config_file = []
        for line in  self.haproxy_config_file :
            if  not line.strip(): continue
            if line.find('listen' ) == 0 and  line.find(ListenBlockName) > 0:
                block_start = True
                new_config_file.append(line.rstrip())
                continue
            elif line.find('server') >= 0 and block_start == True and line.find(RServerName) > 0:
                continue
            elif  line.find('listen' ) == 0 and block_start == True:
                block_start = False
            new_config_file.append(line.rstrip())
            #print  line.rstrip()
        self.haproxy_config_file.close()
        self.haproxy_config_file  = open (self.haproxy_config_file_path,  "w")
        for out_line in new_config_file:
            self.haproxy_config_file.write("%s\n" % out_line)
        self.haproxy_config_file.close()
        return ListenBlockName
    
    def AddRServerToListenBlockName (self,  ListenBlockName, RServerName, RServerIP,  RServerPort):
        self.haproxy_config_file = open (self.haproxy_config_file_path,  "r")
        block_start=False
        new_config_file = []
        for line in  self.haproxy_config_file :
            if  not line.strip(): continue
            if line.find('listen' ) == 0 and  line.find(ListenBlockName) > 0:
                block_start = True
                new_config_file.append(line.rstrip())
                continue
            elif  line.find('listen' ) == 0 and block_start == True:
                new_config_file.append("\tserver\t%s %s:%s check inter 2000 rise 2 fall 5" % (RServerName, RServerIP,  RServerPort) )
                block_start = False
            new_config_file.append(line.rstrip())
            #print  line.rstrip()
        self.haproxy_config_file.close()
        self.haproxy_config_file  = open (self.haproxy_config_file_path,  "w")
        for out_line in new_config_file:
            self.haproxy_config_file.write("%s\n" % out_line)
        self.haproxy_config_file.close()
        return ListenBlockName       
        
    def AddListenBlock(self,  ListenBlockName,  VIPServerIP,  VIPServerPort):
        self.haproxy_config_file = open (self.haproxy_config_file_path,  "r")
        new_config_file = []
        for line in  self.haproxy_config_file :
            if  not line.strip(): continue
            new_config_file.append(line.rstrip())
        self.haproxy_config_file.close()
        new_config_file.append("listen %s %s:%s" % (ListenBlockName, VIPServerIP,  VIPServerPort))
        new_config_file.append("\tmode http")
        new_config_file.append("\tbalance roundrobin")
        new_config_file.append("\toption httpclose")
        self.haproxy_config_file  = open (self.haproxy_config_file_path,  "w")
        for out_line in new_config_file:
            self.haproxy_config_file.write("%s\n" % out_line)
        self.haproxy_config_file.close()
        return ListenBlockName
    
    def _ReadConfigFile(self):
        self.haproxy_config_file = open (self.haproxy_config_file_path,  "r")
        config_file = []
        for line in  self.haproxy_config_file :
            if  not line.strip(): continue
            config_file.append(line.rstrip())
        self.haproxy_config_file.close()
        return config_file
   
    def _WriteConfigFile(self, config_file):
        self.haproxy_config_file  = open (self.haproxy_config_file_path,  "w")
        for out_line in config_file:
            self.haproxy_config_file.write("%s\n" % out_line)
        self.haproxy_config_file.close()
   
        
    def AddFronted(self,  HaproxyFronted):
        """
            Add frontend section to haproxy config file
        """
        new_config_file = self._ReadConfigFile()
        if HaproxyFronted.name =="":
            logger.error("Empty fronted name")
            return "FRONTEND NAME ERROR"
        if HaproxyFronted.bind_address =="" or HaproxyFronted.bind_port == "":
            logger.error("Empty  bind adrress or port")
            return "FRONTEND ADDRESS OR PORT ERROR"
        logger.debug("Adding frontend")
        new_config_file.append("frontend %s" % HaproxyFronted.name )
        new_config_file.append("\tbind %s:%s" % (HaproxyFronted.bind_address,  HaproxyFronted.bind_port))
        #new_config_file.append("\tdefault_backend %s" % HaproxyFronted.default_backend)
        new_config_file.append("\tmode %s" % HaproxyFronted.mode)
        self._WriteConfigFile(new_config_file)
        return  HaproxyFronted.name  
    
    def AddBackend(self,  HaproxyBackend):
        """
            Add backend section to haproxy config file
        """
        if HaproxyBackend.name =="":
            logger.error("Empty backend name")
            return "BACKEND NAME ERROR"
        if HaproxyFronted.bind_address =="" or HaproxyFronted.bind_port == "":
            logger.error("Empty  bind adrress or port")
            return "FRONTEND ADDRESS OR PORT ERROR"
        logger.debug("Adding frontend")
        self.haproxy_config_file = open (self.haproxy_config_file_path,  "r")
        new_config_file = []
        for line in  self.haproxy_config_file :
            if  not line.strip(): continue
            new_config_file.append(line.rstrip())
        self.haproxy_config_file.close()
        new_config_file.append("frontend %s" % HaproxyFronted.name )
        new_config_file.append("\tbind %s:%s" % (HaproxyFronted.bind_address,  HaproxyFronted.bind_port))
        #new_config_file.append("\tdefault_backend %s" % HaproxyFronted.default_backend)
        new_config_file.append("\tmode %s" % HaproxyFronted.mode)
        self.haproxy_config_file  = open (self.haproxy_config_file_path,  "w")
        for out_line in new_config_file:
            self.haproxy_config_file.write("%s\n" % out_line)
        self.haproxy_config_file.close()
        return  HaproxyFronted.name     
        
    def AddRServerToBackend (self,  BackendName, RServerName, RServerIP,  RServerPort):
        
        self.haproxy_config_file = open (self.haproxy_config_file_path,  "r")
        block_start=False
        new_config_file = []
        for line in  self.haproxy_config_file :
            if  not line.strip(): continue
            if line.find('backend' ) == 0 and  line.find(ListenBlockName) > 0:
                block_start = True
                new_config_file.append(line.rstrip())
                continue
            elif  line.find('listen' ) == 0 and block_start == True:
                new_config_file.append("\tserver\t%s %s:%s check inter 2000 rise 2 fall 5" % (RServerName, RServerIP,  RServerPort) )
                block_start = False
            new_config_file.append(line.rstrip())
        self.haproxy_config_file.close()
        self.haproxy_config_file  = open (self.haproxy_config_file_path,  "w")
        for out_line in new_config_file:
            self.haproxy_config_file.write("%s\n" % out_line)
        self.haproxy_config_file.close()
        return ListenBlockName  
        
if __name__ == '__main__':
    config = HaproxyConfigFile('/tmp/haproxy.cfg', '../../tests/unit/testfiles/haproxy.cfg')
    config.DeleteListenBlock("appli2-insert")

    #config.DeleteRServer("appli1-rewrite", "app1_2" )
    #config.AddRServer("appli1-rewrite", "new_server", "1.1.1.1", "80"  )
    #config.AddListenBlock("new_block", "12.12.12.12", "80" )
