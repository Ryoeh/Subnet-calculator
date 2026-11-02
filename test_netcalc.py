import unittest
import ipaddress

from main import (
    to_binary,
    get_host_info,
    split_network,
    get_required_prefix,
    allocate_vlsm
)


class TestNetCalc(unittest.TestCase):

    # ==========================================
    # BINARY CONVERSION
    # ==========================================

    def test_binary_conversion(self):

        ip = ipaddress.IPv4Address("192.168.1.1")

        result = to_binary(ip)

        expected = "11000000.10101000.00000001.00000001"

        self.assertEqual(result, expected)


    # ==========================================
    # HOST CALCULATIONS
    # ==========================================

    def test_standard_subnet(self):

        network = ipaddress.ip_network("192.168.1.0/24")

        usable, first, last = get_host_info(network)

        self.assertEqual(usable, 254)
        self.assertEqual(str(first), "192.168.1.1")
        self.assertEqual(str(last), "192.168.1.254")


    def test_point_to_point_subnet(self):

        network = ipaddress.ip_network("10.0.0.0/31")

        usable, first, last = get_host_info(network)

        self.assertEqual(usable, 2)
        self.assertEqual(str(first), "10.0.0.0")
        self.assertEqual(str(last), "10.0.0.1")


    def test_single_address_subnet(self):

        network = ipaddress.ip_network("8.8.8.8/32")

        usable, first, last = get_host_info(network)

        self.assertEqual(usable, 1)
        self.assertEqual(str(first), "8.8.8.8")
        self.assertEqual(str(last), "8.8.8.8")


    # ==========================================
    # FLSM TESTS
    # ==========================================

    def test_flsm_split(self):

        network = ipaddress.ip_network("192.168.1.0/24")

        subnets = split_network(network, 4)

        self.assertEqual(len(subnets), 4)
        self.assertEqual(subnets[0].prefixlen, 26)
        self.assertEqual(str(subnets[0]), "192.168.1.0/26")
        self.assertEqual(str(subnets[1]), "192.168.1.64/26")


    def test_flsm_rounds_up_subnet_count(self):

        network = ipaddress.ip_network("192.168.1.0/24")

        subnets = split_network(network, 5)

        self.assertEqual(len(subnets), 8)


    def test_flsm_invalid_count(self):

        network = ipaddress.ip_network("192.168.1.0/24")

        with self.assertRaises(ValueError):
            split_network(network, 0)


    # ==========================================
    # VLSM TESTS
    # ==========================================

    def test_required_prefix(self):

        self.assertEqual(get_required_prefix(100), 25)
        self.assertEqual(get_required_prefix(50), 26)
        self.assertEqual(get_required_prefix(20), 27)


    def test_vlsm_allocation(self):

        network = ipaddress.ip_network("192.168.1.0/24")

        requirements = [
            ("Office", 50),
            ("Servers", 100),
            ("Guests", 20)
        ]

        result = allocate_vlsm(network, requirements)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[0][0], "Servers")
        self.assertEqual(str(result[0][1]), "192.168.1.0/25")

        self.assertEqual(result[1][0], "Office")
        self.assertEqual(str(result[1][1]), "192.168.1.128/26")

        self.assertEqual(result[2][0], "Guests")
        self.assertEqual(str(result[2][1]), "192.168.1.192/27")


    def test_vlsm_insufficient_space(self):

        network = ipaddress.ip_network("192.168.1.0/29")

        requirements = [
            ("Servers", 10)
        ]

        with self.assertRaises(ValueError):
            allocate_vlsm(network, requirements)


    def test_vlsm_invalid_host_count(self):

        network = ipaddress.ip_network("192.168.1.0/24")

        requirements = [
            ("Servers", 0)
        ]

        with self.assertRaises(ValueError):
            allocate_vlsm(network, requirements)


if __name__ == "__main__":
    unittest.main()