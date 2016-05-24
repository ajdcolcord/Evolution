#!/usr/bin/env python2.7

import unittest
from dealerProxy import ProxyDealer


class PlayerTests(unittest.TestCase):

    def test_parse_incoming_messages(self):
        json_msg1 = "[1, 2, 3][]"
        result = ProxyDealer.parse_incoming_messages(json_msg1)
        self.assertEquals(result[0], [1, 2, 3])
        self.assertEquals(result[1], [])