# -*- coding: utf-8 -*-
#
# libcnml.py - CNML library
# Copyright (C) 2012 Pablo Castellano <pablo@anche.no>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import absolute_import
import os
import six
import datetime
import warnings

from libcnml import logger

try:
    # python 3
    from urllib import request
except ImportError:
    # python 2
    import urllib as request

try:
    from lxml import etree
    from lxml.etree import XMLSyntaxError
    LXML = True
    logger.info('Using lxml which is more efficient')
except ImportError:
    import xml.dom.minidom as MD
    LXML = False
    logger.info('lxml module not found. Falling back to minidom')


def get_attribute(obj, key, cast_func=None, use_parent=False):
    if LXML:
        if use_parent:
            obj = obj.getparent()
        value = obj.get(key)
    else:
        if use_parent:
            obj = obj.parentNode
        value = obj.getAttribute(key)
    if cast_func:
        value = cast_func(value)
    return value


def get_elements(obj, key, dot=False):
    if LXML:
        if dot:
            key = './/' + key
        return obj.iterfind(key)
    else:
        return obj.getElementsByTagName(key)


class CNMLZone(object):
    """
    This CNMLZone class represents an area in the world map

    It's defined using two coordinate points: (left_bottom, right_top)
    Zones can be nested, so a zone has its own unique id and its parent id
    A zone has a title, which is the most useful for the end-users
    CNML can also provide the total amount of clients, devices, links, services... in the area
    """
    def __init__(self, zid, parentid, aps=0, box=[], nclients=0, ndevices=0, nlinks=0, nservices=0, title=''):
        self.id = zid
        self.parentzone = parentid
        self.totalAPs = aps
        self.box = box
        self.totalClients = nclients
        self.totalDevices = ndevices
        self.totalLinks = nlinks
        self.totalServices = nservices
        self.title = title
        self.subzones = dict()
        self.nodes = dict()

    # @param z: CNMLZone
    def add_subzone(self, z):
        self.subzones[z.id] = z

    # @param z: CNMLNode
    def add_node(self, n):
        self.nodes[n.id] = n

    def get_node(self, nid):
        return self.nodes[nid]

    def get_nodes(self):
        return self.nodes.values()

    def get_subzone(self, zid):
        return self.subzones[zid]

    def get_subzones(self):
        return self.subzones.values()

    @staticmethod
    def parse(z):
        zid = get_attribute(z, 'id', int)
        try:
            zparentid = get_attribute(z, 'parent_id', int)
        except:
            # guifi.net World doesn't have parent_id
            zparentid = None

        nAPs = get_attribute(z, 'access_points') or 0
        nAPs = int(nAPs)
        box = get_attribute(z, 'box').split(',')
        box = [box[:2], box[2:]]
        nclients = get_attribute(z, 'clients') or 0
        nclients = int(nclients)
        ndevices = get_attribute(z, 'devices') or 0
        ndevices = int(ndevices)
        nlinks = get_attribute(z, 'links') or 0
        nlinks = int(nlinks)
        nservices = get_attribute(z, 'services') or 0
        nservices = int(nservices)
        title = get_attribute(z, 'title')
#       nnodes = int(z.getAttribute('zone_nodes'))
#       nnodes is not useful --> len(nodes)

        newzone = CNMLZone(zid, zparentid, nAPs, box, nclients, ndevices, nlinks, nservices, title)
        return newzone

    def __str__(self):
        return 'CNMLZone({0}): {1}'.format(self.id, self.title)

    # Deprecated methods

    def addSubzone(self, z):
        warnings.warn("addSubzone() is deprecated and will be removed in the future.")
        self.add_subzone(z)

    def addNode(self, n):
        warnings.warn("addNode() is deprecated and will be removed in the future.")
        self.add_node(n)

    def getNodes(self):
        warnings.warn("getNodes() is deprecated and will be removed in the future.")
        return self.get_nodes()

    def getSubzones(self):
        warnings.warn("getSubzones() is deprecated and will be removed in the future.")
        return self.get_subzones()


class CNMLNode(object):
    """
    This CNMLNode class represents a node in the network

    Nodes are mainly wireless but there are a lot of different options, like fiber or ethernet cable
    It's defined using one coordinate point
    Each node has its own unique id
    A node has a title and a status, which is the most useful for the end-users
    CNML can also provide the total amount of links of this node
    """
    def __init__(self, nid, title, lat, lon, nlinks, status,
                 elevation, created, updated):
        self.id = nid
        self.title = title
        self.latitude = lat
        self.longitude = lon
        self.totalLinks = nlinks
        self.antenna_elevation = elevation
        self.created = datetime.datetime.strptime(created, '%Y%m%d %H%M')
        if updated:
            self.updated = datetime.datetime.strptime(updated, '%Y%m%d %H%M')
        else:
            self.updated = None
        self.status = status
        self.devices = dict()
        self.services = dict()
        self.zone = None

    def get_device(self, did):
        return self.devices[did]

    def get_devices(self):
        return self.devices.values()

    def get_service(self, sid):
        return self.services[sid]

    def get_services(self):
        return self.services.values()

    def add_device(self, dev):
        self.devices[dev.id] = dev

    def add_service(self, service):
        self.services[service.id] = service

    @staticmethod
    def parse(n):
        nid = get_attribute(n, 'id', int)
        lat = get_attribute(n, 'lat', float)
        lon = get_attribute(n, 'lon', float)
        title = get_attribute(n, 'title')
        #ndevices = get_attribute(n, 'devices') or 0
        #ndevices = int(ndevices)
        nlinks = get_attribute(n, 'links') or 0
        nlinks = int(nlinks)
        status = get_attribute(n, 'status')
        status = Status.str_to_status(status)
        elevation = get_attribute(n, 'antenna_elevation') or 0
        elevation = int(elevation)
        created = get_attribute(n, 'created')
        updated = get_attribute(n, 'updated')  # parse date chunga

        newnode = CNMLNode(nid, title, lat, lon, nlinks, status,
                           elevation, created, updated)
        return newnode

    def __str__(self):
        return 'CNMLNode({0}): {1} ({2})'.format(self.id, self.title, self.status)

    # Deprecated methods

    def getDevices(self):
        warnings.warn("getDevices() is deprecated and will be removed in the future.")
        return self.get_devices()

    def getServices(self):
        warnings.warn("getServices() is deprecated and will be removed in the future.")
        return self.get_services()

    def addDevice(self, dev):
        warnings.warn("addDevice() is deprecated and will be removed in the future.")
        return self.add_device(dev)

    def addService(self, service):
        warnings.warn("addService() is deprecated and will be removed in the future.")
        return self.add_service(service)


class CNMLService(object):
    """
    This CNMLService class represents a service in the network

    Services are what make networks attractive to users
    Each service has its own unique id and contains the reference to the node where it's running
    A service has a title and a status, which is the most useful for the end-users
    CNML can also provide the date when the service was created
    """
    def __init__(self, sid, title, stype, status, created, updated, parent):
        self.id = sid
        self.title = title
        self.type = stype
        self.status = status
        self.created = datetime.datetime.strptime(created, '%Y%m%d %H%M')
        if updated:
            self.updated = datetime.datetime.strptime(updated, '%Y%m%d %H%M')
        else:
            self.updated = None
        self.parentNode = parent

    @staticmethod
    def parse(s, parent):
        sid = get_attribute(s, 'id', int)
        title = get_attribute(s, 'title')
        type = get_attribute(s, 'type')
        status = get_attribute(s, 'status')
        status = Status.str_to_status(status)
        created = get_attribute(s, 'created')
        updated = get_attribute(s, 'updated')

        newservice = CNMLService(sid, title, type, status, created, updated, parent)
        return newservice

    def __str__(self):
        return 'CNMLService({}): {} ({})'.format(self.id, self.title, self.type)


class CNMLDevice(object):
    """
    This CNMLDevice class represents a device of a node in the network
    """
    def __init__(self, did, name, firmware, status, title, dtype, parent, mainipv4):
        self.id = did
        self.name = name
        self.firmware = firmware
        self.status = status
        self.title = title
        self.type = dtype
        self.services = dict()
        self.radios = dict()
        self.interfaces = dict()
        self.parentNode = parent
        self.mainipv4 = mainipv4
        # self.ssid = ssid

    def get_radio(self, rid):
        return self.radios[rid]

    def get_radios(self):
        return self.radios.values()

    def get_interface(self, iid):
        return self.interfaces[iid]

    def get_interfaces(self):
        return self.interfaces.values()

    def get_service(self, sid):
        return self.services[sid]

    def get_services(self):
        return self.services.values()

    def add_radio(self, radio):
        self.radios[radio.id] = radio

    def add_interface(self, interface):
        self.interfaces[interface.id] = interface

    def add_service(self, service):
        self.services[service.id] = service

    @staticmethod
    def parse(d, parent):
        did = get_attribute(d, 'id', int)
        name = get_attribute(d, 'name')
        firmware = get_attribute(d, 'firmware')
        status = get_attribute(d, 'status')
        status = Status.str_to_status(status)
        title = get_attribute(d, 'title')
        dtype = get_attribute(d, 'type')
        mainipv4 = get_attribute(d, 'mainipv4')
        # ssid = get_attribute(d, 'ssid')
        #nlinks = get_attribute(d, 'links) or 0
        #nlinks = int(nlinks)
        #por qué no tiene un atributo radios="2" en lugar de links="2"??

        newdevice = CNMLDevice(did, name, firmware, status, title, dtype, parent, mainipv4)
        return newdevice

    def __str__(self):
        return 'CNMLDevice({0}): {1}'.format(self.id, self.title)

    # Deprecated methods

    def getRadios(self):
        warnings.warn("getRadios() is deprecated and will be removed in the future.")
        return self.get_radios()

    def getInterfaces(self):
        warnings.warn("getInterfaces() is deprecated and will be removed in the future.")
        return self.get_interfaces()

    def addRadio(self, radio):
        warnings.warn("addRadio() is deprecated and will be removed in the future.")
        self.add_radio(radio)

    def addInterface(self, interface):
        warnings.warn("addInterface() is deprecated and will be removed in the future.")
        self.add_interface(interface)


class CNMLRadio(object):
    """
    This CNMLRadio class represents a radio of a device in the network
    """
    def __init__(self, rid, protocol, snmp_name, snmp_index, ssid, mode, gain, angle, channel, clients, parent):
        self.id = rid
        self.protocol = protocol
        self.snmp_name = snmp_name
        self.snmp_index = snmp_index
        self.ssid = ssid
        self.mode = mode
        self.antenna_gain = gain
        self.antenna_angle = angle
        self.channel = channel
        self.clients_accepted = clients
        self.interfaces = dict()
        self.parentDevice = parent

    def get_interface(self, iid):
        return self.interfaces[iid]

    def get_interfaces(self):
        return self.interfaces.values()

    def add_interface(self, iface):
        self.interfaces[iface.id] = iface

    @staticmethod
    def parse(r, parent):
        #radio ids are 0, 1, 2...
        rid = get_attribute(r, 'id', int)
        protocol = get_attribute(r, 'protocol')
        snmp_name = get_attribute(r, 'snmp_name')
        snmp_index = get_attribute(r, 'snmp_index')
        ssid = get_attribute(r, 'ssid')
        mode = get_attribute(r, 'mode')
        antenna_gain = get_attribute(r, 'antenna_gain')
        antenna_angle = get_attribute(r, 'antenna_angle')
        channel = get_attribute(r, 'channel') or 0
        channel = int(channel)
        clients = get_attribute(r, 'clients_accepted') == 'Yes'

        #falta atributo interfaces="2"
        #sobra atributo device_id

        newradio = CNMLRadio(rid, protocol, snmp_name, snmp_index, ssid, mode, antenna_gain, antenna_angle, channel, clients, parent)
        return newradio

    def __str__(self):
        return 'CNMLRadio({0}): {1}'.format(self.id, self.ssid)

    # Deprecated methods

    def getInterfaces(self):
        warnings.warn("getInterfaces() is deprecated and will be removed in the future.")
        return self.get_interfaces()

    def addInterface(self, iface):
        warnings.warn("addInterface() is deprecated and will be removed in the future.")
        self.add_interface(iface)


class CNMLInterface(object):
    """
    This CNMLInterface class represents a interface associated to a radio of a device in the network
    """
    def __init__(self, iid, ipv4, mask, mac, itype, parent):
        self.id = iid
        self.ipv4 = ipv4
        self.mask = mask
        self.mac = mac
        self.type = itype
        self.links = dict()
        self.parent = parent  # It can be a CNMLDevice or a CNMLRadio

    def get_link(self, lid):
        return self.links[lid]

    def get_links(self):
        return self.links.values()

    def add_link(self, link):
        self.links[link.id] = link

    @staticmethod
    def parse(i, parent):
        iid = get_attribute(i, 'id', int)
        ipv4 = get_attribute(i, 'ipv4')
        mac = get_attribute(i, 'mac')
        #checkMac
        mask = get_attribute(i, 'mask')
        itype = get_attribute(i, 'type')  # wLan/Lan

        newiface = CNMLInterface(iid, ipv4, mask, mac, itype, parent)
        return newiface

    def __str__(self):
        return 'CNMLInterface({0}): {1} [{2}]'.format(self.id, self.ipv4, self.type)

    # Deprecated methods

    def getLinks(self):
        warnings.warn("getLinks() is deprecated and will be removed in the future.")
        return self.get_links()

    def addLink(self, link):
        warnings.warn("addLink() is deprecated and will be removed in the future.")
        self.add_link(link)


# Note that for two connected nodes there's just one link, that is,
# two different links (different linked dev/if/node) but same id
# Given a device link, how to difference which is the linked device, A or B?
# FIXME
class CNMLLink(object):
    """
    This CNMLLink class represents a link between two nodes in the network
    """
    def __init__(self, lid, status, ltype, ldid, liid, lnid, parent):
        self.id = lid
        self.status = status
        self.type = ltype
        #self.linked_device = {ldid:None}
        #self.linked_interface = {liid:None}
        #self.linked_node = {lnid:None}
        self.parentInterface = parent
        self.nodeA = lnid
        self.deviceA = ldid
        self.interfaceA = liid
        self.nodeB = None
        self.deviceB = None
        self.interfaceB = None

    def get_linked_nodes(self):
        return [self.nodeA, self.nodeB]

    def get_linked_devices(self):
        return [self.deviceA, self.deviceB]

    def get_linked_interfaces(self):
        return [self.interfaceA, self.interfaceB]

    def _parse_link_b(self, l):
        self.nodeB = get_attribute(l, 'linked_node_id', int)
        self.deviceB = get_attribute(l, 'linked_device_id', int)
        self.interfaceB = get_attribute(l, 'linked_interface_id', int)

    def _set_linked_parameters(self, devs, ifaces, nodes):
        didA = self.deviceA
        iidA = self.interfaceA
        nidA = self.nodeA
        didB = self.deviceB
        iidB = self.interfaceB
        nidB = self.nodeB

        if self.nodeB is None:
            #logger.info("Couldn't find linked node (%d) in link %d. It may be defined in a different CNML zone." % (self.nodeA, self.id))
            return

        if didA in devs:
            self.deviceA = devs[didA]
        else:
            logger.warning('Device id %d not found' % self.deviceA)

        if didB in devs:
            self.deviceB = devs[didB]
        else:
            logger.warning('Device id %d not found' % self.deviceB)

        if iidA in ifaces:
            self.interfaceA = ifaces[iidA]
        else:
            logger.warning('Interface id %d not found' % self.interfaceA)

        if iidB in ifaces:
            self.interfaceB = ifaces[iidB]
        else:
            logger.warning('Interface id %d not found' % self.interfaceB)

        if nidA in nodes:
            self.nodeA = nodes[nidA]
        else:
            logger.warning('Node id %d not found' % self.nodeA)

        if nidB in nodes:
            self.nodeB = nodes[nidB]
        else:
            logger.warning('Node id %d not found' % self.nodeB)

    # Cambiar nombres:
    # link_status -> status
    # link_type -> type
    # linked_device_id -> device_id
    # linked_interface_id -> interface_id
    # linked_node_id -> node_id
    @staticmethod
    def parse(l, parent):
        lid = get_attribute(l, 'id', int)
        status = get_attribute(l, 'link_status')
        status = Status.str_to_status(status)
        ltype = get_attribute(l, 'link_type')
        ldid = get_attribute(l, 'linked_device_id', int)
        liid = get_attribute(l, 'linked_interface_id', int)
        lnid = get_attribute(l, 'linked_node_id', int)

        newlink = CNMLLink(lid, status, ltype, ldid, liid, lnid, parent)
        return newlink

    def __str__(self):
        return 'CNMLLink({0}): [{1}<-->{2}] ({3})'.format(self.id, self.interfaceA, self.interfaceB, self.type)

    # Deprecated methods

    def getLinkedNodes(self):
        warnings.warn("getLinkedNodes() is deprecated and will be removed in the future.")
        return self.get_linked_nodes()

    def getLinkedDevices(self):
        warnings.warn("getLinkedDevices() is deprecated and will be removed in the future.")
        return self.get_linked_devices()

    def getLinkedInterfaces(self):
        warnings.warn("getLinkedInterfaces() is deprecated and will be removed in the future.")
        return self.get_linked_interfaces()

    def parseLinkB(self, l):
        warnings.warn("parseLinkB() is deprecated and will be removed in the future.")
        self._parse_link_b(l)

    def setLinkedParameters(self, devs, ifaces, nodes):
        warnings.warn("setLinkedParameters() is deprecated and will be removed in the future.")
        self._set_linked_parameters(devs, ifaces, nodes)


class Status(object):
    """
    This Status class represents the many status a node can be
    Note that only one of those is possible at a time
    """
    PLANNED = 1
    WORKING = 2
    TESTING = 3
    BUILDING = 4
    RESERVED = 5
    DROPPED = 6
    INACTIVE = 7

    @staticmethod
    def get_status_list():
        return (Status.PLANNED, Status.WORKING, Status.TESTING, Status.BUILDING, Status.RESERVED, Status.DROPPED, Status.INACTIVE)

    @staticmethod
    def str_to_status(status):
        if status.lower() == "planned":
            st = Status.PLANNED
        elif status.lower() == "working":
            st = Status.WORKING
        elif status.lower() == "testing":
            st = Status.TESTING
        elif status.lower() == "building":
            st = Status.BUILDING
        elif status.lower() == "reserved":
            st = Status.RESERVED
        elif status.lower() == "dropped":
            st = Status.DROPPED
        elif status.lower() == "inactive":
            st = Status.INACTIVE
        else:
            logger.debug('Value: %s (%d)' % (status, len(status)))
            raise ValueError

        return st

    @staticmethod
    def status_to_str(status):
        if status == Status.PLANNED:
            st = 'Planned'
        elif status == Status.WORKING:
            st = 'Working'
        elif status == Status.TESTING:
            st = 'Testing'
        elif status == Status.BUILDING:
            st = 'Building'
        elif status == Status.RESERVED:
            st = 'Reserved'
        elif status == Status.DROPPED:
            st = 'Dropped'
        elif status == Status.INACTIVE:
            st = 'Inactive'
        else:
            raise ValueError

        return st

    # Deprecated methods

    @staticmethod
    def strToStatus(status):
        warnings.warn("strToStatus() is deprecated and will be removed in the future.")
        return Status.str_to_status(status)

    @staticmethod
    def statusToStr(status):
        warnings.warn("statusToStr() is deprecated and will be removed in the future.")
        return Status.status_to_str(status)


class CNMLParser(object):
    """
    This CNMLParser class is used to parse a CNML file and build the data structure
    """
    def __init__(self, filename, lazy=False, validate=True):
        self.filename = filename
        self.rootzone = 0

        self.nodes = None
        self.zones = None
        self.devices = None
        self.services = None
        self.radios = None
        self.ifaces = None
        self.links = None
        self.innerlinks = None
        self.outerlinks = None

        if not lazy:
            self.loaded = self.load(validate=validate)
            # TODO: raise exception if load failed so that the user interface can show a messagebox
        else:
            self.loaded = False

    def validate(self, tree):
        logger.info('Validating file "%s"...' % self.filename)

        validation = True
        if LXML:
            dtdfile = os.path.join(os.path.dirname(__file__), 'cnml.dtd')
            try:
                with open(dtdfile, 'rb') as dtdfp:
                    dtd = etree.DTD(dtdfp)

                logger.info('DTD validation: %s' % dtd.validate(tree))
                errors = dtd.error_log.filter_from_errors()
                if len(errors) > 0:
                    logger.warning('%d errors found:' % len(errors))
                    logger.warning(errors)
                    validation = False

            except IOError:
                logger.error('DTD Validation failed: %s file not found' % dtdfile)
                validation = False

        else:
            logger.warn('DTD validation is not implemented with Minidom API')
            validation = False

        return validation

    def find_node_from_ipv4(self, ipv4):
        for i in self.get_interfaces():
            if i.ipv4 == ipv4:
                parent = i.parent
                if isinstance(parent, CNMLRadio):
                    node = parent.parentDevice.parentNode
                else:
                    # parent of radio is already a device
                    node = parent.parentNode
                return node
        return None

    def get_node(self, nid):
        if not self.loaded:
            self.load()
        return self.nodes[nid]

    def get_nodes(self):
        return self.nodes.values()

    def get_zone(self, zid):
        if not self.loaded:
            self.load()
        return self.zones[zid]

    def get_zones(self):
        return self.zones.values()

    def get_device(self, did):
        if not self.loaded:
            self.load()
        return self.devices[did]

    def get_devices(self):
        return self.devices.values()

    def get_service(self, sid):
        if not self.loaded:
            self.load()
        return self.services[sid]

    def get_services(self):
        return self.services.values()

    def get_radio(self, did, rid):
        return self.radios[(did, rid)]

    def get_radios(self):
        return self.radios.values()

    def get_interface(self, iid):
        if not self.loaded:
            self.load()
        return self.ifaces[iid]

    def get_interfaces(self):
        return self.ifaces.values()

    def get_link(self, lid):
        if not self.loaded:
            self.load()
        return self.links[lid]

    def get_links(self):
        return self.links.values()

    def get_inner_links(self):
        return self.innerlinks.values()

    def get_outer_links(self):
        return self.outerlinks.values()

    def get_nodes_from_zone(self, zid):
        if not self.loaded:
            self.load()
        return self.zones[zid].nodes.values()

    def get_subzones_from_zone(self, zid):
        if not self.loaded:
            self.load()
        return self.zones[zid].subzones.values()

    def get_zones_names(self):
        if not self.loaded:
            self.load()

        return [z.title for z in self.get_zones()]

    def get_titles(self):
        if not self.loaded:
            self.load()

        return [n.title for n in self.get_nodes()]

    # FIXME: filename not loaded
    def get_filename(self):
        return self.filename

    def _parse_zones(self, tree):
        # --zones--
        zones = get_elements(tree, 'zone', dot=True)

        # Save root zone id
        if LXML:
            self.rootzone = int(tree.find('.//zone[1]').get('id'))
        else:
            self.rootzone = int(zones[0].getAttribute("id"))

        for z in zones:
            zid = get_attribute(z, 'id', int)
            newzone = CNMLZone.parse(z)
            self.zones[zid] = newzone
            zparentid = newzone.parentzone

            if zid != self.rootzone and zparentid is not None:
                self.zones[zparentid].add_subzone(newzone)

    def _parse_nodes(self, tree, add_zones=True):
        nodes_tree = get_elements(tree, 'node', dot=True)

        for n in nodes_tree:
            newnode = CNMLNode.parse(n)
            self.nodes[newnode.id] = newnode

            if add_zones:
                zid = get_attribute(n, 'id', int, use_parent=True)
                self.zones[zid].add_node(newnode)
                self.nodes[newnode.id].zone = self.zones[zid]

            #assert n.parentNode.localName == u'zone'
            #assert(ndevices == len(devicestree))

            # --devices--
            devices_tree = get_elements(n, 'device')

            for d in devices_tree:
                self._parse_device(d, newnode)

    def _parse_device(self, d, newnode):
        newdevice = CNMLDevice.parse(d, newnode)
        self.devices[newdevice.id] = newdevice
        self.nodes[newnode.id].add_device(newdevice)

        # --interfaces--
        # If there's a working service in this device, it has interfaces (and it's not a son of a radio!)
        interfaces_tree = get_elements(d, 'interface')

        for i in interfaces_tree:
            self._parse_interface(i, newdevice)

        # --services--
        services_tree = get_elements(d, 'service')

        for s in services_tree:
            newservice = self._parse_service(s, newdevice)
            self.nodes[newnode.id].add_service(newservice)
            self.devices[newdevice.id].add_service(newservice)

        # --radios--
        radios_tree = get_elements(d, 'radio')

        for r in radios_tree:
            self._parse_radio(r, newdevice)

    def _parse_radio(self, r, newdevice):
        newradio = CNMLRadio.parse(r, newdevice)
        self.radios[(newdevice.id, newradio.id)] = newradio
        self.devices[newdevice.id].add_radio(newradio)

        # --interfaces--
        interfaces_tree = get_elements(r, 'interface')

        for i in interfaces_tree:
            self._parse_interface(i, newradio)

    def _parse_interface(self, i, parent):
        newiface = CNMLInterface.parse(i, parent)
        self.ifaces[newiface.id] = newiface

        if isinstance(parent, CNMLDevice):
            self.devices[parent.id].add_interface(newiface)
        elif isinstance(parent, CNMLRadio):
            parent.add_interface(newiface)
        else:
            raise ValueError

        # --links--
        links_tree = get_elements(i, 'link')

        for l in links_tree:
            newlink = self._parse_link(l, newiface)
            self.ifaces[newiface.id].add_link(newlink)

    def _parse_link(self, l, newiface):
        lid = get_attribute(l, 'id')

        if lid in self.links:
            self.links[lid]._parse_link_b(l)
        else:
            newlink = CNMLLink.parse(l, newiface)
            self.links[lid] = newlink
        return self.ifaces[newiface.id]

    def _parse_service(self, s, newdevice):
        newservice = CNMLService.parse(s, newdevice)
        self.services[newservice.id] = newservice
        return newservice

    def _get_cnml_type(self, tree):
        klass = get_elements(tree, 'class')
        if LXML:
            klass = next(klass)
        else:
            klass = klass[0]

        if get_attribute(klass, 'network_description'):
            self.cnml_type = 'detail'
        else:
            if get_attribute(klass, 'node_description'):
                self.cnml_type = 'node'
            else:
                raise ValueError

    def _loadLxml(self, validate=True):
        try:
            if not self.url_contents:
                tree = etree.parse(self.filename)
            else:
                tree = etree.fromstring(self.url_contents)

        except XMLSyntaxError as e:
            logger.error('Error reading CNML file: %s' % e)
            logger.error('The file might be corrupted.')
            return False

        if validate:
            logger.info('Validating file "%s"...' % self.filename)
            if not self.validate(tree):
                return False

        self._get_cnml_type(tree)
        add_zones = self.cnml_type == 'detail'

        if add_zones:
            self._parse_zones(tree)
        self._parse_nodes(tree, add_zones=add_zones)
        return True

    def _loadMinidom(self, validate=True):
        if not self.url_contents:
            tree = MD.parse(self.filename)
        else:
            tree = MD.parseString(self.url_contents)

        if validate:
            logger.info('Validating file "%s"...' % self.filename)
            #Don't check for validation, as minidom doesn't support it
            self.validate(tree)

        self._get_cnml_type(tree)
        add_zones = self.cnml_type == 'detail'

        if add_zones:
            self._parse_zones(tree)
        self._parse_nodes(tree, add_zones=add_zones)

        # Fix: return False
        return True

    def load(self, validate=True):
        self.zones = dict()
        self.nodes = dict()
        self.devices = dict()
        self.services = dict()
        self.radios = dict()
        self.ifaces = dict()
        self.links = dict()
        self.innerlinks = {}
        self.outerlinks = {}
        self.url_contents = None

        # if URL has been passed, get the contents
        if isinstance(self.filename, six.string_types) and self.filename.startswith('http'):
            self.url_contents = request.urlopen(self.filename).read()
            # decode response if needed
            if not isinstance(self.url_contents, six.string_types):
                self.url_contents = self.url_contents.decode()

        if LXML:
            loaded = self._loadLxml(validate=validate)
        else:
            try:
                loaded = self._loadMinidom(validate=validate)
            except:
                loaded = False

        if loaded:
            logger.info('Loaded "%s" successfully' % self.filename)

            # Replace None by true reference of nodes/devices/interfaces
            # Note that if they belong to a different zone they might not be defined in the CNML file
            for link in self.get_links():
                link._set_linked_parameters(self.devices, self.ifaces, self.nodes)
                if isinstance(link.nodeA, CNMLNode) and isinstance(link.nodeB, CNMLNode):
                    # inner
                    self.innerlinks[link.id] = link
                else:
                    self.outerlinks[link.id] = link
        else:
            logger.error('There were some errors loading "%s"' % self.filename)

        self.loaded = loaded
        return loaded

    # Deprecated methods

    def findNodefromIPv4(self, ipv4):
        warnings.warn("findNodefromIPv4() is deprecated and will be removed in the future.")
        return self.find_node_from_ipv4(ipv4)

    def getNodes(self):
        warnings.warn("getNodes() is deprecated and will be removed in the future.")
        return self.get_nodes()

    def getZones(self):
        warnings.warn("getZones() is deprecated and will be removed in the future.")
        return self.get_zones()

    def getDevices(self):
        warnings.warn("getDevices() is deprecated and will be removed in the future.")
        return self.get_devices()

    def getServices(self):
        warnings.warn("getServices() is deprecated and will be removed in the future.")
        return self.get_services()

    def getRadios(self):
        warnings.warn("getRadios() is deprecated and will be removed in the future.")
        return self.get_radios()

    def getInterfaces(self):
        warnings.warn("getInterfaces() is deprecated and will be removed in the future.")
        return self.get_interfaces()

    def getLinks(self):
        warnings.warn("getLinks() is deprecated and will be removed in the future.")
        return self.get_links()

    def getNodesFromZone(self, zid):
        warnings.warn("getNodesFromZone() is deprecated and will be removed in the future.")
        return self.get_nodes_from_zone(zid)

    def getSubzonesFromZone(self, zid):
        warnings.warn("getSubzonesFromZone() is deprecated and will be removed in the future.")
        return self.get_subzones_from_zone(zid)

    def getInterface(self, iid):
        warnings.warn("getInterface() is deprecated and will be removed in the future.")
        return self.get_interface(iid)

    def getNode(self, nid):
        warnings.warn("getNode() is deprecated and will be removed in the future.")
        return self.get_node(nid)

    def getZone(self, zid):
        warnings.warn("getZone() is deprecated and will be removed in the future.")
        return self.get_zone(zid)

    def getLink(self, lid):
        warnings.warn("getLink() is deprecated and will be removed in the future.")
        return self.get_link(lid)

    def getDevice(self, did):
        warnings.warn("getDevice() is deprecated and will be removed in the future.")
        return self.get_device(did)

    def getZonesNames(self):
        warnings.warn("getZonesNames() is deprecated and will be removed in the future.")
        return self.get_zones_names()

    def getTitles(self):
        warnings.warn("getTitles() is deprecated and will be removed in the future.")
        return self.get_titles()

    def getFilename(self):
        warnings.warn("getFilename() is deprecated and will be removed in the future.")
        return self.get_filename()

    def validateDTD(self, tree):
        warnings.warn("validateDTD() is deprecated and will be removed in the future.")
        return self.validate(tree)

    def __str__(self):
        return 'CNMLParser: {1}'.format(self.filename)
