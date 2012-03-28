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
#    under the License.
import unittest

from balancer.core.serializeable import Serializeable
from balancer.core.uniqueobject import UniqueObject

from balancer.drivers.cisco_ace.ace_5x_driver import AceDriver
from balancer.drivers.cisco_ace.Context import Context
from balancer.drivers.cisco_ace.XmlSender import XmlSender
from balancer.loadbalancers.realserver import RealServer
from balancer.loadbalancers.serverfarm import ServerFarm
from balancer.loadbalancers.probe import *
from balancer.loadbalancers.virtualserver import VirtualServer

test_context = Context('10.4.15.30', '10443', 'admin', 'cisco123')
driver = AceDriver()

rs = RealServer()
rs.name = 'LB_test_rs01'
rs.address = '172.250.250.250'
rs.description = "RS for test"
rs.weight = 7
#rs.rateBandwidth = 500
#rs.rateConnection = 50
#Next var for AddRStoSFarm
rs.port = "80"
rs.backupRS = ""
rs.backupRSport = ""
#rs.cookieStr = "stringcookie"
#rs.failOnAll = True
rs.probes = ["icmp"]

probe = HTTPprobe()
probe.name = "LB_test_ProbeHTTP"
probe.type="HTTP"
probe.requestHTTPurl = "cisco.com" #Change default value in Probe class !
probe.probeInterval = 16
probe.passDetectInterval = 61
probe.failDetect = 4
probe.passDetectCount = 5
probe.receiveTimeout = 11
probe.isRouted = True
probe.tcpConnTerm = True
probe.appendPortHostTag = True
probe.openTimeout = 2
probe.userName = "uzver"
probe.password = "password"

sf = ServerFarm()
sf.type = "Host"
sf.name = "LB_test_sfarm01"
sf.description = "description"
sf.predictor = "roundrobin"
sf.failAction = "purge"
sf.inbandHealthCheck = "Remove"
sf.connFailureThreshCount = 5
sf.resetTimeout = 200
sf.resumeService = 40
#sf.failOnAll = True
sf._probes = ["ICMP"]
sf.transparent = True
sf.dynamicWorkloadScale = "Local"
sf.partialThreshPercentage = 11
sf.backInservice = 22

vs = VirtualServer()
vs.name = "LB_test_VIP1"
vs.address = "10.250.250.250"
vs.VLAN=[2]
vs.port="80"

class Ace_5x_DriverTestCase(unittest.TestCase):
    """def test_01_createRServer(self):
        print driver.createRServer(test_context, rs)
    
    def test_02_createProbe(self):
        driver.createProbe(test_context, probe)
    
    def test_03_createServerFarm(self):
        driver.createServerFarm(test_context, sf)
    
    def test_04_addRServerToSF(self):
        driver.addRServerToSF(test_context, sf,  rs)
    
    def test_05_addProbeToSF(self):
        driver.addProbeToSF(test_context, sf,  probe)"""
    
    def test_06_createVIP(self):
        driver.createVIP(test_context, vs,  sf)
    
    """def test_07_suspendRServer(self):
        driver.suspendRServer(test_context, sf, rs)
    
    def test_08_activateRServer(self):
        driver.activateRServer(test_context, sf, rs)
    
    def test_09_deleteVIP(self):
        driver.deleteVIP(test_context, vs)

    def test_10_deleteProbeFromSF(self):
        driver.deleteProbeFromSF(test_context, sf,  probe)
    
    def test_11_deleteRServerFromSF(self):
        driver.deleteRServerFromSF(test_context, sf,  rs)
    
    def test_12_deleteServerFarm(self):
        driver.deleteServerFarm(test_context, sf)
    
    def test_13_deleteProbe(self):
        driver.deleteProbe(test_context, probe)
    
    def test_14_deleteRServer(self):
        driver.deleteRServer(test_context, rs)"""
