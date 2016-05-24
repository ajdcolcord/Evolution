#!/usr/bin/env python2.7

import sys, os
import unittest
from playerState import PlayerState
from traitCard import TraitCard
from species import Species
from player import Player
from constants import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dealer'))
from playerAction import PlayerAction
from growBody import GrowBody
from growPopulation import GrowPopulation
from boardTrade import BoardTrade
from replaceTrait import ReplaceTrait
from vegFeedAction import VegFeedAction
from noFeedAction import NoFeedAction
from carnFeedAction import CarnFeedAction
from fatStoreAction import FatStoreAction


class PlayerTests(unittest.TestCase):

    def test_start(self):
        ps = PlayerState(1, 1, [])
        player = Player(1)

        self.assertEquals(player.playerState, PlayerState(1, 0, [], []))
        player.start(ps, 0)
        self.assertEquals(player.playerState, ps)

    def test_choose(self):
        hand4 = [TraitCard(CARNIVORE), TraitCard(FAT_TISSUE), TraitCard(SCAVENGER), TraitCard(HERDING)]
        hand5 = [TraitCard(CARNIVORE), TraitCard(FAT_TISSUE), TraitCard(SCAVENGER), TraitCard(HERDING),
                TraitCard(LONG_NECK)]
        hand6 = [TraitCard(CARNIVORE), TraitCard(FAT_TISSUE), TraitCard(SCAVENGER), TraitCard(HERDING),
                TraitCard(LONG_NECK), TraitCard(FERTILE)]
        hand7 = [TraitCard(FAT_TISSUE), TraitCard(SCAVENGER), TraitCard(HERDING),
                TraitCard(LONG_NECK), TraitCard(FERTILE), TraitCard(WARNING_CALL), TraitCard(CARNIVORE)]

        traits2 = [TraitCard(AMBUSH, -1), TraitCard(AMBUSH, 0), TraitCard(AMBUSH, 1), TraitCard(CARNIVORE, -1),
                   TraitCard(CARNIVORE), TraitCard(CARNIVORE, 1), TraitCard(LONG_NECK), TraitCard(LONG_NECK, 1),
                         TraitCard(WARNING_CALL), TraitCard(WARNING_CALL, 1)]

        play_act2 = PlayerAction(0, [GrowPopulation(0, 3)], [GrowBody(0, 4)], [BoardTrade(1, [2])],
                                    [ReplaceTrait(0, 0, 5)])

        ps4 = PlayerState(1, 1, [], hand4)
        ps5 = PlayerState(1, 1, [], hand5)
        ps6 = PlayerState(1, 1, [], hand6)
        ps7 = PlayerState(1, 1, [], hand7)
        ps8 = PlayerState(1, 1, [], traits2)
        player = Player(1)

        player.start(ps8, 0)
        self.assertEquals(player.playerState, ps8)
        self.assertEquals(player.choose([], []).to_json_action_4(), play_act2.to_json_action_4())

        player.start(ps4, 0)
        self.assertEquals(player.playerState, ps4)
        self.assertEquals(player.choose([], []), PlayerAction(0, [GrowPopulation(0, 2)], [], [BoardTrade(1, [3])], []))

        player.start(ps5, 0)
        self.assertEquals(player.playerState, ps5)
        self.assertEquals(player.choose([], []), PlayerAction(0, [GrowPopulation(0, 4)], [GrowBody(0, 2)],
                                                              [BoardTrade(1, [3])], []))

        player.start(ps6, 0)
        self.assertEquals(player.playerState, ps6)
        self.assertEquals(player.choose([], []), PlayerAction(0, [GrowPopulation(0, 3)], [GrowBody(0, 4)],
                                                              [BoardTrade(1, [5])], [ReplaceTrait(0, 0, 2)]))

        player.start(ps7, 0)
        self.assertEquals(player.playerState, ps7)
        self.assertEquals(player.choose([], []), PlayerAction(6, [GrowPopulation(0, 2)], [GrowBody(0, 3)],
                                                              [BoardTrade(0, [4])], [ReplaceTrait(0, 0, 1)]))

    def testSortSpecies(self):
        big = Species(5, 1, 6, [TraitCard(FAT_TISSUE), TraitCard(CARNIVORE)], 0)
        aCarnivore = Species(1, 2, 4, [TraitCard(CARNIVORE)])
        fedVeg = Species(3, 4, 3)
        smallerVeg = Species(1, 4, 2)
        smallerFatTissue = Species(0, 4, 2, [TraitCard(FAT_TISSUE)])

        ourAlreadySortedIndexedSpecies = [(0, big), (1, aCarnivore), (2, fedVeg), (3, smallerVeg), (4, smallerFatTissue)]
        ourSortedIndexedSpecies = [(0, big), (1, aCarnivore), (2, fedVeg), (3, smallerVeg), (4, smallerFatTissue)]

        outOfOrderIndexedSpecies = [(0, smallerFatTissue), (1, aCarnivore), (2, big), (3, fedVeg), (4, smallerVeg)]
        secondSortedIndexedSpecies = [(2, big), (1, aCarnivore), (3, fedVeg), (4, smallerVeg), (0, smallerFatTissue)]
        hungryIndexedSpecies = [(2, big), (1, aCarnivore), (4, smallerVeg), (0, smallerFatTissue)]

        player = Player(1)

        sorted1 = player.sortSpecies(ourAlreadySortedIndexedSpecies)
        sorted2 = player.sortSpecies(outOfOrderIndexedSpecies)
        sorted3 = player.sortSpecies(outOfOrderIndexedSpecies, removeFed=True)

        self.assertEquals(sorted1, ourSortedIndexedSpecies)
        self.assertEquals(sorted2, secondSortedIndexedSpecies)
        self.assertEquals(sorted3, hungryIndexedSpecies)

    def testGetFatTissueSpecies(self):
        big = Species(5, 1, 6, [TraitCard(FAT_TISSUE), TraitCard(CARNIVORE)], 0)
        aCarnivore = Species(1, 2, 4, [TraitCard(CARNIVORE)])
        fedVeg = Species(3, 4, 3)
        smallerVeg = Species(1, 4, 2)
        smallerFatTissue = Species(0, 4, 2, [TraitCard(FAT_TISSUE)])  # 'needier' than big

        list_of_species = [(0, big), (1, smallerFatTissue), (2, aCarnivore), (3, fedVeg), (4, smallerVeg)]
        player = Player(1)

        choice1 = player.getFatTissueSpecies(list_of_species, 3)
        choice2 = player.getFatTissueSpecies([(0, fedVeg)], 3)

        self.assertEquals(choice1[0], 1)
        self.assertEquals(choice1[1], 3)
        self.assertFalse(choice2)

    def testGetVegetarian(self):
        big = Species(5, 1, 6, [TraitCard(FAT_TISSUE), TraitCard(CARNIVORE)], 0)
        aCarnivore = Species(1, 2, 4, [TraitCard(CARNIVORE)])
        fedVeg = Species(3, 4, 3)  # full
        smallerVeg = Species(1, 4, 2)  # hungry
        smallerFatTissue = Species(0, 4, 2, [TraitCard(FAT_TISSUE)])

        list_of_species = [(0, big), (1, aCarnivore), (2, fedVeg), (3, smallerVeg), (4, smallerFatTissue)]
        player = Player(1)

        list_of_full = [(0, big), (1, aCarnivore), (2, fedVeg)]

        vegetarian = player.getVegetarian(list_of_species)
        with self.assertRaises(Exception):
            player.getVegetarian(list_of_full)

        self.assertEquals(vegetarian, 3)

    def testHasHungryVegetarian(self):
        big = Species(5, 1, 6, [TraitCard(FAT_TISSUE), TraitCard(CARNIVORE)], 0)
        aCarnivore = Species(1, 2, 4, [TraitCard(CARNIVORE)])
        fedVeg = Species(3, 4, 3)  # full
        smallerVeg = Species(1, 4, 2)  # hungry
        smallerFatTissue = Species(0, 4, 2, [TraitCard(FAT_TISSUE)])

        player = Player(1)

        list_of_species = [(0, big), (1, aCarnivore), (2, fedVeg), (3, smallerVeg), (4, smallerFatTissue)]
        list_of_full = [(0, big), (1, aCarnivore), (2, fedVeg)]

        self.assertFalse(player.hasHungryVegetarian(list_of_full))
        self.assertTrue(player.hasHungryVegetarian(list_of_species))

    def test_get_carnivores(self):
        big = Species(5, 1, 6, [TraitCard(FAT_TISSUE), TraitCard(CARNIVORE)], 0)
        aCarnivore = Species(1, 2, 4, [TraitCard(CARNIVORE)])
        fedVeg = Species(3, 4, 3)  # full
        smallerVeg = Species(1, 4, 2)  # hungry
        smallerFatTissue = Species(0, 4, 2, [TraitCard(FAT_TISSUE)])

        list_of_species = [(0, big), (1, aCarnivore), (2, fedVeg), (3, smallerVeg), (4, aCarnivore)]
        carnivore_list = [(0, big), (1, aCarnivore), (4, aCarnivore)]
        empty_list = []
        veg_list = [(2, fedVeg), (3, smallerVeg), (4, smallerFatTissue)]
        player = Player(1)

        self.assertEquals(player.get_carnivores(list_of_species), carnivore_list)
        self.assertEquals(player.get_carnivores(empty_list), [])
        self.assertEquals(player.get_carnivores(veg_list), [])

    def testGetCarnivoreAttack(self):
        species1 = Species(3, 4, 3, [TraitCard(CARNIVORE)])
        species2 = Species(0, 2, 1, [TraitCard(CARNIVORE)])
        species2a = Species(1, 5, 1, [TraitCard(CARNIVORE), TraitCard(CLIMBING)])

        species3 = Species(1, 2, 6, [])  # smaller
        species4 = Species(4, 4, 6, [])  # larger

        species5 = Species(1, 1, 1, [])
        species6 = Species(4, 6, 6, [TraitCard(CLIMBING)])

        species3a = Species(1, 2, 6, [TraitCard(CLIMBING)])  # smaller
        species4a = Species(4, 4, 6, [TraitCard(CLIMBING)])  # larger

        species5a = Species(1, 1, 1, [TraitCard(CLIMBING)])
        species6a = Species(4, 6, 6, [TraitCard(CLIMBING)])

        player2 = PlayerState(2, 2, [], [])
        player3 = PlayerState(3, 2, [species3, species4], [])
        player3a = PlayerState(3, 2, [species3a, species4a], [])
        player4 = PlayerState(4, 2, [species5, species6])
        player4a = PlayerState(4, 2, [species5a, species6a], [])

        players_list_of_species = [(0, species1), (1, species2)]
        second_list_of_att = [(0, species1), (1, species2), (2, species2a)]
        player = Player(1)

        self.assertEquals(player.getCarnivoreAttack(players_list_of_species, [player2, player3, player4]), [0, 1, 1])
        self.assertEquals(player.getCarnivoreAttack(second_list_of_att, [player3a, player4a]), [2, 1, 1])
        self.assertEqual(player.getCarnivoreAttack(players_list_of_species, [player2]), False)

    def test_is_larger_attack_option(self):
        species1 = Species(3, 4, 3, [TraitCard(CARNIVORE)])
        species2 = Species(0, 2, 1, [TraitCard(CARNIVORE)])
        species3 = Species(1, 2, 6, [])  # smaller
        species4 = Species(4, 4, 6, [])  # larger
        species5 = Species(1, 1, 1, [])
        species6 = Species(4, 6, 6, [TraitCard(CLIMBING)])
        species4a = Species(4, 4, 6, [TraitCard(CLIMBING)])  # larger

        player3 = PlayerState(3, 2, [species3, species4], [])
        player4 = PlayerState(4, 2, [species5, species6])

        player = Player(1)

        self.assertFalse(player.is_larger_attack_option(player3, 0, species1, species4a))
        self.assertEquals(player.is_larger_attack_option(player3, 1, species1, species3), (1, species4))
        self.assertFalse(player.is_larger_attack_option(player4, 1, species1, species2))


    def testFeedNext(self):
        big = Species(5, 1, 6, [TraitCard(FAT_TISSUE), TraitCard(CARNIVORE)], 0)
        aCarnivore = Species(1, 2, 4, [TraitCard(CARNIVORE)])
        smallerVeg = Species(1, 4, 2)  # hungry
        smallerFatTissue = Species(0, 4, 2, [TraitCard(FAT_TISSUE)])

        player_basic = PlayerState(1, 0, [], [])
        player2 = PlayerState(2, 0, [aCarnivore, smallerVeg], [])
        player3 = PlayerState(3, 0, [aCarnivore], [])
        player4 = PlayerState(3, 0, [big, smallerFatTissue], [])

        player = Player(1)

        with self.assertRaises(Exception):
            player.feedNext(player_basic, 4, [])

        self.assertEquals(player.feedNext(player2, 4, [player_basic.species, player3.species]).to_json(),
                            VegFeedAction(1).to_json())
        self.assertEquals(player.feedNext(player3, 4, [player_basic.species]).to_json(),
                          NoFeedAction().to_json())
        self.assertEquals(player.feedNext(player3, 4, [player_basic.species, player2.species]).to_json(),
                          CarnFeedAction(0, 1, 0).to_json())
        self.assertEquals(player.feedNext(player3, 4, [player3.species, player2.species]).to_json(),
                          CarnFeedAction(0, 0, 0).to_json())
        self.assertEquals(player.feedNext(player4, 4, [player3.species, player2.species]).to_json(),
                          FatStoreAction(1, 4).to_json())

    def test_pair_species_with_index(self):
        species1 = Species(1, 1, 1)
        species2 = Species(2, 2, 2)
        species3 = Species(3, 3, 3)
        species4 = Species(4, 4, 4)

        species_list = [species1, species2, species3, species4]
        expected_list = [(0, species1), (1, species2), (2, species3), (3, species4)]

        player = Player(1)

        self.assertEquals(player.pair_species_with_index(species_list), expected_list)

    def test_store_current_player_state(self):
        ps = PlayerState(1, 1, [], [])
        player = Player(1)

        player.storeCurrentPlayerState(ps)

        self.assertEquals(player.playerState, ps)

    def test_find_card_in_trait_list(self):
        traits = [TraitCard(AMBUSH), TraitCard(AMBUSH, 1), TraitCard(CARNIVORE), TraitCard(CARNIVORE, 1)]
        player = Player(1)
        self.assertEquals(player.find_card_in_trait_list(TraitCard(AMBUSH, 1), traits), 1)


if __name__ == "__main__":
    unittest.main()
