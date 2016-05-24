#!/usr/bin/env python2.7

import unittest
from feedAction import FeedAction
from noFeedAction import NoFeedAction
from vegFeedAction import VegFeedAction
from fatStoreAction import FatStoreAction
from carnFeedAction import CarnFeedAction
from dealer import Dealer
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'feeding'))
from playerState import PlayerState
from species import Species
from traitCard import TraitCard
from constants import *

class FeedActionTests(unittest.TestCase):
    def setUp(self):
        self.species1 = Species(3, 4, 5)
        self.species2 = Species(3, 3, 3)
        self.species3 = Species(1, 2, 3)
        self.species4 = Species(1, 2, 3)
        self.fatSpecies = Species(3, 3, 3, [TraitCard(FAT_TISSUE)], 2)
        self.carnSpecies = Species(1, 3, 5, [TraitCard(CARNIVORE)], 2)


        self.speciesList1 = [self.species1, self.species2]
        self.speciesList2 = [self.species3, self.species4]
        self.speciesListWithFat = [self.fatSpecies, self.species2, self.species1]
        self.speciesListWithCarn = [self.carnSpecies, self.species3]

        self.player1 = PlayerState(1, 0, self.speciesList1, [])
        self.player2 = PlayerState(2, 2, self.speciesList2, [])
        self.player_with_fat = PlayerState(1, 0, self.speciesListWithFat, [])
        self.player_with_carn = PlayerState(1, 0, self.speciesListWithCarn, [])

        self.dealer = Dealer([self.player1, self.player2], 4, [])
        self.dealer_with_fat_player = Dealer([self.player_with_fat, self.player2], 4, [])
        self.dealer_with_carn_player = Dealer([self.player_with_carn, self.player2], 4, [])

    def tearDown(self):
        del self.species1
        del self.species2
        del self.species3
        del self.species4
        del self.fatSpecies
        del self.speciesList1
        del self.speciesList2
        del self.player1
        del self.player2
        del self.player_with_fat
        del self.dealer
        del self.dealer_with_fat_player


    def test_parse_feed_action(self):
        no_feed = FeedAction.parse_food_action(False)
        self.assertTrue(issubclass(no_feed.__class__, FeedAction))
        self.assertEquals(no_feed.__class__, NoFeedAction)
        self.assertFalse(no_feed.__class__ == VegFeedAction)
        self.assertFalse(no_feed.__class__ == FatStoreAction)
        self.assertFalse(no_feed.__class__ == CarnFeedAction)

        veg_feed = FeedAction.parse_food_action(3)
        self.assertTrue(issubclass(veg_feed.__class__, FeedAction))
        self.assertEquals(veg_feed.__class__, VegFeedAction)
        self.assertFalse(veg_feed.__class__ == NoFeedAction)
        self.assertFalse(veg_feed.__class__ == FatStoreAction)
        self.assertFalse(veg_feed.__class__ == CarnFeedAction)

        fat_store = FeedAction.parse_food_action([3, 3])
        self.assertTrue(issubclass(fat_store.__class__, FeedAction))
        self.assertEquals(fat_store.__class__, FatStoreAction)
        self.assertFalse(fat_store.__class__ == NoFeedAction)
        self.assertFalse(fat_store.__class__ == VegFeedAction)
        self.assertFalse(fat_store.__class__ == CarnFeedAction)

        carn_feed = FeedAction.parse_food_action([3, 3, 3])
        self.assertTrue(issubclass(carn_feed.__class__, FeedAction))
        self.assertEquals(carn_feed.__class__, CarnFeedAction)
        self.assertFalse(carn_feed.__class__ == VegFeedAction)
        self.assertFalse(carn_feed.__class__ == FatStoreAction)
        self.assertFalse(carn_feed.__class__ == NoFeedAction)

        with self.assertRaises(Exception):
            FeedAction.parse_food_action([3, 3, 3, 3])

        with self.assertRaises(Exception):
            FeedAction.parse_food_action(True)

    def test_to_json(self):
        no_feed = NoFeedAction()
        self.assertEquals(no_feed.to_json(), False)

        veg_feed = VegFeedAction(3)
        self.assertEquals(veg_feed.to_json(), 3)

        fat_feed = FatStoreAction(2, 1)
        self.assertEquals(fat_feed.to_json(), [2, 1])

        carn_feed = CarnFeedAction(2, 3, 1)
        self.assertEquals(carn_feed.to_json(), [2, 3, 1])


    def test_no_feed_action(self):
        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.species4.food, 1)
        self.assertEquals(self.dealer.wateringHole, 4)

        no_feed = FeedAction.parse_food_action(False)

        no_feed.feed(self.dealer)

        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.species4.food, 1)
        self.assertEquals(self.dealer.wateringHole, 4)

    def test_veg_feed_action(self):
        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.species4.food, 1)
        self.assertEquals(self.dealer.wateringHole, 4)

        veg_feed = FeedAction.parse_food_action(1)

        veg_feed.feed(self.dealer)

        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.species4.food, 1)
        self.assertEquals(self.dealer.wateringHole, 4)

        veg_feed = FeedAction.parse_food_action(0)

        veg_feed.feed(self.dealer)

        self.assertEquals(self.species1.food, 4)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.species4.food, 1)
        self.assertEquals(self.dealer.wateringHole, 3)

    def test_fat_store_action(self):
        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.dealer_with_fat_player.wateringHole, 4)
        self.assertEquals(self.fatSpecies.food, 3)
        self.assertEquals(self.fatSpecies.fatFood, 2)

        fat_store = FeedAction.parse_food_action([0, 1])

        fat_store.feed(self.dealer_with_fat_player)

        self.assertEquals(self.fatSpecies.fatFood, 3)
        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.fatSpecies.food, 3)
        self.assertEquals(self.dealer_with_fat_player.wateringHole, 3)

    def test_carn_feed_action(self):
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.species4.food, 1)
        self.assertEquals(self.carnSpecies.food, 1)
        self.assertEquals(self.dealer_with_carn_player.wateringHole, 4)
        self.assertEquals(self.carnSpecies.population, 5)
        self.assertEquals(self.species2.population, 3)
        self.assertEquals(self.species3.population, 3)
        self.assertEquals(self.species4.population, 3)

        carn_feed = FeedAction.parse_food_action([0, 0, 1])

        carn_feed.feed(self.dealer_with_carn_player)

        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.species3.food, 1)
        self.assertEquals(self.species4.food, 1)
        self.assertEquals(self.carnSpecies.food, 2)
        self.assertEquals(self.dealer_with_carn_player.wateringHole, 3)
        self.assertEquals(self.carnSpecies.population, 5)
        self.assertEquals(self.species2.population, 3)
        self.assertEquals(self.species3.population, 3)
        self.assertEquals(self.species4.population, 2)


if __name__ == "__main__":
    unittest.main()