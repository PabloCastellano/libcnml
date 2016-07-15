import os
import unittest
import libcnml
import datetime


DATA = {
    54284: {
        'zones': 1,
        'nodes': 29,
        'devices': 49,
        'services': 5,
        'radios': 45,
        'interfaces': (
            101085, 101159, 101160, 102429, 102431, 102436, 102437, 102442, 102716,
            102718, 102890, 102891, 108647, 126097, 127016, 127925, 132688, 134455,
            134456, 134457, 134778, 135000, 135633, 136954, 137582, 139291, 139295,
            139297, 139302, 140559, 141248, 142603, 142898, 143505, 153752, 157618,
            159096, 160653, 162731, 162785, 165682, 82382, 82389, 82390, 82391,
            82392, 82393, 82443, 82444, 82445, 82450, 82496, 86317, 86326, 86327,
            87464, 87465, 87466, 87467, 87473, 88596, 88598, 88602, 93284, 96778, 97141,
        ),
        'links': (
            121882, 122468, 122570, 122663, 122909, 123391, 123628, 124201, 124205,
            124624, 124894, 125364, 125468, 125700, 128438, 130604, 130964, 131126,
            131705, 132413, 132439, 133491, 54362, 54363, 54364, 54365, 54408,
            54449, 57313, 57320, 58265, 58271, 59133, 59137, 65799, 69092, 70212,
            70214, 70216, 70220, 70400, 70402, 70551, 70552, 74307, 79959, 80238, 80531,
        ),
        'ip': {
            'address': '10.69.12.1',
            'title': 'ANDGkPlzUdala',
        },
    },
    55284: {
        'zones': 1,
        'nodes': 4,
        'devices': 24,
        'services': 4,
        'radios': 17,
        'interfaces': (
            150351, 150353, 150408, 150409, 150410, 150411, 150412, 150413, 150415,
            150425, 150472, 150846, 150859, 150861, 150862, 150863, 150864, 150865,
            150874, 150875, 150888, 150894, 150895, 150897, 150898, 150910, 150913,
            150927, 150929, 150931, 150957, 150971, 150972, 150973, 150974, 151025,
            151512, 151645, 151646, 151647, 151648, 161569,
        ),
        'links': (
            127995, 128014, 128015, 128016, 128017, 128018, 128019, 128020, 128024,
            128037, 128161, 128163, 128164, 128165, 128166, 128167, 128171, 128180,
            128185, 128186, 128187, 128195, 128198, 128202, 128215, 128253, 128256,
            128267, 128277, 128337, 128385, 128386, 128387, 128388, 128468, 132043,
            132421,
        ),
        'ip': {
            'address': '10.69.24.3',
            'title': 'TOLOOllaun',
        },
    },
    2525: {
        'zones': 1,
        'nodes': 17,
        'devices': 13,
        'services': 8,
        'radios': 10,
        'interfaces': (
            77127, 81573, 82624, 82626, 82630, 82631, 82641, 82664, 83515,
            83516, 84998, 86420, 86955, 102790, 120315
        ),
        'links': (
            54559, 54560, 54568, 54589, 55264, 55265, 55341, 56317, 57394, 57846, 70459, 78121
        ),
        'ip': {
            'address': '10.138.53.101',
            'title': 'CanetCuba',
        },
    },
    56604: {
        'zones': 0,
        'nodes': 1,
        'devices': 8,
        'services': 0,
        'radios': 6,
        'interfaces': (
            101234, 101660, 106637, 106638, 106640, 111332, 125851, 129608, 142178, 98582
        ),
        'links': (
            125220, 73466, 75203, 80555, 81054
        ),
        'ip': {
            'address': '10.1.66.97',
            'title': 'BCNUPFp9',
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

    def test_find_node_from_ipv4(self):
        node = self.parser.find_node_from_ipv4(self.data['ip']['address'])
        self.assertTrue(node is not None)
        self.assertEqual(node.title, self.data['ip']['title'])

    def test_get_nodes(self):
        nodes = self.parser.get_nodes()
        self.assertEqual(len(nodes), self.data['nodes'])

    def test_get_zones(self):
        zones = self.parser.get_zones()
        self.assertEqual(len(zones), self.data['zones'])

    def test_get_devices(self):
        devices = self.parser.get_devices()
        self.assertEqual(len(devices), self.data['devices'])

    def test_get_services(self):
        services = self.parser.get_services()
        self.assertEqual(len(services), self.data['services'])

    def test_get_radios(self):
        radios = self.parser.get_radios()
        self.assertEqual(len(radios), self.data['radios'])

    def test_get_interfaces(self):
        interfaces = self.parser.get_interfaces()
        for iface in interfaces:
            self.assertIn(iface.id, self.data['interfaces'])

        self.assertEqual(len(interfaces), len(self.data['interfaces']))

    def test_get_links(self):
        links = self.parser.get_links()
        for link in links:
            self.assertIn(link.id, self.data['links'])
        self.assertEqual(len(links), len(self.data['links']))


class LibcnmlUrlTestCase(LibcnmlTestCase):
    """
    Same as LibcnmlTestCase but get CNML from URL
    instead of from local file
    """
    cnml_url = 'https://raw.githubusercontent.com/PabloCastellano/libcnml/master/libcnml/tests/data/54284.cnml'

    def setUp(self):
        self.parser = libcnml.CNMLParser(self.cnml_url)
        if not self.parser.loaded:
            raise ValueError('could not load CNMLParser')


class LibcnmlNodeAttributesTestCase(LibcnmlTestCase):
    cnml_file = 'data/54284.cnml'

    def setUp(self):
        filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            self.cnml_file
        )
        self.parser = libcnml.CNMLParser(filename)

    def test_node_title(self):
        node = self.parser.get_node(48441)
        self.assertEqual(node.title, 'ANDBerria38')

    def test_node_antenna_elevation(self):
        node = self.parser.get_node(48441)
        self.assertEqual(node.antenna_elevation, 12)

    def test_node_created(self):
        node = self.parser.get_node(48441)
        self.assertIsInstance(node.created, datetime.datetime)
        self.assertEqual(node.created.strftime('%Y-%m-%d %H:%M'), '2012-05-23 06:47')

    def test_node_updated(self):
        node = self.parser.get_node(48441)
        self.assertIsInstance(node.updated, datetime.datetime)
        self.assertEqual(node.updated.strftime('%Y-%m-%d %H:%M'), '2014-11-20 11:35')


class Zone55284TestCase(LibcnmlTestCase):
    cnml_file = 'data/55284.cnml'
    data = DATA[55284]

    def test_get_service(self):
        service = self.parser.get_service(80470)
        self.assertEqual(service.id, 80470)
        self.assertEqual(service.title, 'TOLO28Kanala-proxy')
        self.assertEqual(service.type, 'Proxy')
        self.assertEqual(service.status, libcnml.Status.BUILDING)
        self.assertEqual(service.created, datetime.datetime(2015, 8, 3, 6, 56))
        self.assertEqual(service.updated, datetime.datetime(2015, 8, 3, 7, 0))

        device = self.parser.get_device(78855)
        service = device.get_service(80470)

        self.assertEqual(service.id, 80470)
        self.assertEqual(service.title, 'TOLO28Kanala-proxy')
        self.assertEqual(service.type, 'Proxy')
        self.assertEqual(service.status, libcnml.Status.BUILDING)
        self.assertEqual(service.created, datetime.datetime(2015, 8, 3, 6, 56))
        self.assertEqual(service.updated, datetime.datetime(2015, 8, 3, 7, 0))


class Zone2525TestCase(LibcnmlTestCase):
    cnml_file = 'data/2525.cnml'
    data = DATA[2525]


class Node56604TestCase(LibcnmlTestCase):
    cnml_file = 'data/56604_node.cnml'
    data = DATA[56604]


if __name__ == '__main__':
    unittest.main()
