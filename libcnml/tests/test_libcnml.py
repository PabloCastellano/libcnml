import os
import unittest
import libcnml

DATA = {
    54284: {
        'zones': 1,
        'nodes': 7,
        'devices': 15,
        'services': 8,
        'radios': 11,
        'interfaces': 23,
        'links': 14,
        'ip': {
            'address': '10.69.12.1',
            'title': 'ANDGkPlzUdala',
        },
    },
    55284: {
        'zones': 1,
        'nodes': 3,
        'devices': 12,
        'services': 4,
        'radios': 7,
        'interfaces': 24,
        'links': 16,
        'ip': {
            'address': '10.69.28.1',
            'title': 'TOLOOiaun',
        },
    },
    2525: {
        'zones': 1,
        'nodes': 6,
        'devices': 9,
        'services': 9,
        'radios': 7,
        'interfaces': 15,
        'links': 8,
        'ip': {
            'address': '10.138.53.101',
            'title': 'CanetCuba',
        },
    }
}


class LibcnmlTestCase(unittest.TestCase):
    #cnml_file = 'data/54284.cnml'
    #data = DATA[54284]
    #cnml_file = 'data/55284.cnml'
    #data = DATA[55284]
    cnml_file = 'data/2525.cnml'
    data = DATA[2525]

    def setUp(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            self.cnml_file
        )
        self.parser = libcnml.CNMLParser(filename)

    def test_validateDTD(self):
        # TODO: validateDTD should return True of False
        pass

    def test_findNodefromIPv4(self):
        node = self.parser.findNodefromIPv4(self.data['ip']['address'])
        self.assertTrue(node is not None)
        self.assertEqual(node.title, self.data['ip']['title'])

    def test_getNodes(self):
        nodes = self.parser.getNodes()
        self.assertEqual(len(nodes), self.data['nodes'])

    def test_getZones(self):
        zones = self.parser.getZones()
        self.assertEqual(len(zones), self.data['zones'])

    def test_getDevices(self):
        devices = self.parser.getDevices()
        self.assertEqual(len(devices), self.data['devices'])

    def test_getServices(self):
        services = self.parser.getServices()
        self.assertEqual(len(services), self.data['services'])

    def test_getRadios(self):
        radios = self.parser.getRadios()
        self.assertEqual(len(radios), self.data['radios'])

    def test_getInterfaces(self):
        interfaces = self.parser.getInterfaces()
        self.assertEqual(len(interfaces), self.data['interfaces'])

    def test_getLinks(self):
        links = self.parser.getLinks()
        self.assertEqual(len(links), self.data['links'])


class Zone55284TestCase(LibcnmlTestCase):
    cnml_file = 'data/55284.cnml'
    data = DATA[55284]


class Zone2525TestCase(LibcnmlTestCase):
    cnml_file = 'data/2525.cnml'
    data = DATA[2525]

if __name__ == '__main__':
    unittest.main()
