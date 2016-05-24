#!/usr/bin/env python2.7

import unittest
from traitCard import TraitCard
from constants import *

class TraitCardTests(unittest.TestCase):

    def testEquals(self):
        trait1 = TraitCard(CARNIVORE, 3)
        trait2 = TraitCard(CARNIVORE, 3)
        trait3 = TraitCard(AMBUSH, 3)
        trait4 = TraitCard(CARNIVORE, 4)

        self.assertTrue(trait1 == trait2)
        self.assertFalse(trait1 == trait3)
        self.assertFalse(trait1 == trait4)

    def testFromJson(self):
        json_trait1 = [3, CARNIVORE]
        trait1 = TraitCard(CARNIVORE, 3)

        self.assertEquals(TraitCard.from_json(json_trait1), trait1)

        with self.assertRaises(Exception):
            TraitCard.from_json([CARNIVORE, 3])

        with self.assertRaises(Exception):
            TraitCard.from_json([3, CARNIVORE, 2])

        with self.assertRaises(Exception):
            TraitCard.from_json([3, "nonsense"])

    def testToJson(self):
        json_trait1 = [3, CARNIVORE]
        trait1 = TraitCard(CARNIVORE, 3)

        self.assertEquals(trait1.to_json(), json_trait1)

    def test_is_valid_food(self):
        json_trait1 = [5, CARNIVORE]
        json_trait2 = [2, LONG_NECK]
        bad_trait1 = [-9, CARNIVORE]
        bad_trait2 = [4, AMBUSH]

        self.assertTrue(TraitCard.is_valid_food(json_trait1))
        self.assertTrue(TraitCard.is_valid_food(json_trait2))
        self.assertFalse(TraitCard.is_valid_food(bad_trait1))
        self.assertFalse(TraitCard.is_valid_food(bad_trait2))

if __name__ == "__main__":
    unittest.main()