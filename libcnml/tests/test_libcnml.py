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
        'interfaces': (
            82381, 82382, 82387, 82389, 82390, 82391, 82392,
            82393, 82442, 82443, 82444, 82445, 82446, 82447,
            82450, 82496, 84157, 84158, 84161, 84162, 84163,
            84251, 84253,
        ),
        'links': (
            54362, 54363, 54364, 54365, 54405, 54406, 54407, 54408, 54449,
            55718, 55719, 55722, 55729, 55770,
        ),
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
        'interfaces': (
            84178, 84179, 84185, 84227, 84228, 84243, 84246, 84248, 84273,
            84274, 84275, 84276, 84319, 84328, 84459, 84460, 84462, 84463,
            84464, 84469, 84470,
        ),
        'links': (
            55732, 55735, 55754, 55763, 55767, 55784, 55785, 55789, 55797,
            55817, 55818, 55897, 55898, 55899, 55902, 55904,
        ),
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
        'interfaces': (
            77127, 81573, 82624, 82626, 82630, 82631, 82641, 82664, 83515,
            83516, 84998,
        ),
        'links': (
            54559, 54560, 54568, 54589, 55264, 55265, 55341, 56317,
        ),
        'ip': {
            'address': '10.138.53.101',
            'title': 'CanetCuba',
        },
    }
}


class EmptyFileTestCase(unittest.TestCase):
    def test_invalid(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'data/empty.cnml'
        )
        parser = libcnml.CNMLParser(filename)
        self.assertFalse(parser.loaded)


class ValidationTestCase(unittest.TestCase):
    def test_valid(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'data/54284.cnml'
        )
        parser = libcnml.CNMLParser(filename)
        self.assertTrue(parser.loaded)

    def test_invalid(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'data/54284_invalid.cnml'
        )
        parser = libcnml.CNMLParser(filename)
        self.assertFalse(parser.loaded)


class LibcnmlTestCase(unittest.TestCase):
    cnml_file = 'data/54284.cnml'
    data = DATA[54284]

    def setUp(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            self.cnml_file
        )
        self.parser = libcnml.CNMLParser(filename)

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
        for iface in interfaces:
            self.assertIn(iface.id, self.data['interfaces'])

        self.assertEqual(len(interfaces), len(self.data['interfaces']))

    def test_getLinks(self):
        links = self.parser.getLinks()
        for link in links:
            self.assertIn(link.id, self.data['links'])
        self.assertEqual(len(links), len(self.data['links']))


class Zone55284TestCase(LibcnmlTestCase):
    cnml_file = 'data/55284.cnml'
    data = DATA[55284]


class Zone2525TestCase(LibcnmlTestCase):
    cnml_file = 'data/2525.cnml'
    data = DATA[2525]

if __name__ == '__main__':
    unittest.main()
