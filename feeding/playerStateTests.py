#!/usr/bin/env python2.7

import unittest, sys, os
from playerState import PlayerState
from player import Player
from traitCard import TraitCard
from species import Species
from constants import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dealer'))
from playerAction import PlayerAction
from growPopulation import GrowPopulation
from replaceTrait import ReplaceTrait
from boardTrade import BoardTrade
from vegFeedAction import VegFeedAction
from fatStoreAction import FatStoreAction
from carnFeedAction import CarnFeedAction

class PlayerStateTests(unittest.TestCase):

    def testToJsonArray(self):
        speciesarr = [["food", 1],
                        ["body", 1],
                        ["population", 1],
                        ["traits", ["carnivore"]]]
        species2arr = [["food", 2],
                    ["body", 2],
                    ["population", 2],
                    ["traits", ["warning-call"]]]

        onePlayerarr = [["id", 1],
                        ["species", [speciesarr, species2arr]],
                        ["bag", 0]]

        playerArr2 = [["id", 1],
                        ["species", [speciesarr, species2arr]],
                        ["bag", 0],
                        ["cards", [[3, CARNIVORE]]]]

        species1 = Species(1, 1, 1, [TraitCard(CARNIVORE)])
        species2 = Species(2, 2, 2, [TraitCard(WARNING_CALL)])

        ps = PlayerState(1, 0, [species1, species2], [])
        ps2 = PlayerState(1, 0, [species1, species2], [TraitCard(CARNIVORE, 3)])

        self.assertEquals(ps.toJsonArray(), onePlayerarr)
        self.assertEquals(ps2.toJsonArray(), playerArr2)

    def testConvertPlayerState(self):
        species1 = [["food", 3],
                    ["body", 4],
                    ["population", 5],
                    ["traits", ["carnivore"]]]
        species2 = [["food", 1],
                    ["body", 3],
                    ["population", 4],
                    ["traits", ["warning-call"]]]

        onePlayer = [["id", 1],
                    ["species", [species1, species2]],
                    ["bag", 0]]


        ps1 = PlayerState()
        ps2 = PlayerState()
        ps1.trait_cards.append(TraitCard("carnivore"))
        ps1.foodbag = 4
        self.assertEquals(ps2.foodbag, 0)
        self.assertEquals(len(ps2.trait_cards), 0)
        ps = PlayerState.convertPlayerState(onePlayer)
        self.assertEqual(ps.id, onePlayer[0][1])
        self.assertEqual(ps.foodbag, onePlayer[2][1])
        self.assertEqual(ps.trait_cards, [])

    def test_to_json_state(self):
        ps = PlayerState(1, 2, [Species(1, 2, 3), Species(1, 1, 1, [TraitCard(CLIMBING)])],
                         [TraitCard(CARNIVORE, 2), TraitCard(AMBUSH, 3)])
        json_ps = [2,
                   [[["food", 1], ["body", 2], ["population", 3], ["traits", []]],
                       [["food", 1], ["body", 1], ["population", 1], ["traits", ["climbing"]]]],
                   [[2, "carnivore"], [3, "ambush"]]]
        self.assertEquals(ps.to_json_state(), json_ps)

    def test_from_json_state(self):
        ps = PlayerState(0, 2, [Species(1, 2, 3, []), Species(1, 1, 1, [TraitCard(CLIMBING)])],
                         [TraitCard(CARNIVORE, 2), TraitCard(AMBUSH, 3)])
        json_ps = [2,
                   [[["food", 1], ["body", 2], ["population", 3], ["traits", []]],
                       [["food", 1], ["body", 1], ["population", 1], ["traits", ["climbing"]]]],
                   [[2, "carnivore"], [3, "ambush"]]]
        self.assertEquals(PlayerState.from_json_state(json_ps), ps)

    def test_from_json_gamestate(self):
        ps = PlayerState(0, 2, [Species(1, 2, 3, []), Species(1, 1, 1, [TraitCard(CLIMBING)])],
                         [TraitCard(CARNIVORE, 2), TraitCard(AMBUSH, 3)])
        species_list = [[Species(1, 2, 3, []), Species(2, 2, 2, [TraitCard(CLIMBING)])], [Species(1, 2, 3, [])]]
        json_state = [
                        2,
                        [[["food", 1], ["body", 2], ["population", 3], ["traits", []]],
                         [["food", 1], ["body", 1], ["population", 1], ["traits", ["climbing"]]]],
                        [[2, "carnivore"], [3, "ambush"]],
                        3,
                        [[[["food", 1], ["body", 2], ["population", 3], ["traits", []]],
                         [["food", 2], ["body", 2], ["population", 2], ["traits", ["climbing"]]]],
                         [[["food", 1], ["body", 2], ["population", 3], ["traits", []]]]]
                    ]
        self.assertEquals(PlayerState.from_json_gamestate(json_state), [ps, 3, species_list])


    def test_new(self):
        ex_player = Player(3)
        ps = PlayerState.new(1, ex_player)

        self.assertEquals(ps.player_reference, ex_player)
        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.foodbag, 0)
        self.assertEquals(ps.trait_cards, [])
        self.assertEquals(ps.species, [])

    def test_start(self):
        ps = PlayerState.new(1, Player(1))
        ps.start(0, Species(1, 1, 1), [TraitCard(SCAVENGER)])

        self.assertEquals(ps, PlayerState(1, 0, [Species(1, 1, 1)], [TraitCard(SCAVENGER)]))

        ps.start(0, False, [TraitCard(CARNIVORE)])

        self.assertEquals(ps, PlayerState(1, 0, [Species(1, 1, 1)], [TraitCard(SCAVENGER), TraitCard(CARNIVORE)]))

    def test_step4i(self):
        playerAction = PlayerAction(0, [GrowPopulation(0, 1)], [], [], [ReplaceTrait(0, 0, 2)])
        traits = [TraitCard(HERDING), TraitCard(CARNIVORE), TraitCard(CLIMBING)]
        player1 = Player(1)
        ps = PlayerState(1, 0, [Species(1, 2, 1, [TraitCard(HERDING)])], traits, player1)

        self.assertEquals(ps.foodbag, 0)
        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.species, [Species(1, 2, 1, [TraitCard(HERDING)])])
        self.assertEquals(ps.trait_cards, traits)
        ps.step4i(playerAction)

        self.assertEquals(ps.foodbag, 0)
        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.trait_cards, [])
        self.assertEquals(ps.species, [Species(1, 2, 2, [TraitCard(CLIMBING)])])

    def test_choose(self):
        traits = [TraitCard(HERDING), TraitCard(CARNIVORE), TraitCard(CLIMBING), TraitCard(SCAVENGER)]
        player1 = Player(1)
        ps1 = PlayerState(1, 0, [Species(1, 2, 1, [TraitCard(HERDING)])], traits, player1)
        ps2 = PlayerState(2, 0, [])
        ps3 = PlayerState(3, 0, [])

        player1.start(ps1, 0)
        self.assertEquals(ps1.choose([ps2, ps1, ps3]), PlayerAction(1, [GrowPopulation(1, 3)], [],
                                                                    [BoardTrade(2, [0])], []))

    def test_feedNext(self):
        wh = 2
        species1 = Species(1, 1, 3, [TraitCard(SCAVENGER)])
        species2 = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        fat_species = Species(2, 4, 3, [TraitCard(FAT_TISSUE)], 0)
        species3 = Species(1, 3, 5, [TraitCard(FORAGING), TraitCard(SCAVENGER)])

        trait1 = TraitCard(SCAVENGER)
        trait2 = TraitCard(CARNIVORE)
        trait3 = TraitCard(BURROWING)

        player1 = Player(1)
        player2 = Player(2)
        player3 = Player(3)

        ps1 = PlayerState(1, 0, [species1, species2, species3], [trait1], player1)
        ps2 = PlayerState(2, 0, [fat_species, species2], [trait1, trait2], player2)
        ps3 = PlayerState(3, 0, [species2], [trait3, trait1], player3)

        self.assertEquals(ps1.feedNext(wh, [ps1, ps2, ps3]).to_json(), VegFeedAction(2).to_json())
        self.assertEquals(ps2.feedNext(wh, [ps2, ps1, ps3]).to_json(), FatStoreAction(0, 2).to_json())
        self.assertEquals(ps3.feedNext(wh, [ps3, ps2, ps1]).to_json(), CarnFeedAction(0, 1, 2).to_json())

    def testGetLeftNeighbor(self):
        species1 = Species(1, 1, 1)
        species2 = Species(2, 2, 2)
        species3 = Species(3, 3, 3)
        ps = PlayerState(1, 0, [species1, species2, species3])
        self.assertFalse(ps.getLeftNeighbor(0))
        self.assertEquals(ps.getLeftNeighbor(1), species1)

    def testGetRightNeighbor(self):
        species1 = Species(1, 1, 1)
        species2 = Species(2, 2, 2)
        species3 = Species(3, 3, 3)
        ps = PlayerState(1, 0, [species1, species2, species3])
        self.assertFalse(ps.getRightNeighbor(2))
        self.assertEquals(ps.getRightNeighbor(1), species3)

    def test_get_neighbors(self):
        big = Species(5, 1, 6, [TraitCard(FAT_TISSUE), TraitCard(CARNIVORE)], 0)
        aCarnivore = Species(1, 2, 4, [TraitCard(CARNIVORE)])
        fedVeg = Species(3, 4, 3)  # full
        smallerVeg = Species(1, 4, 2)  # hungry
        smallerFatTissue = Species(0, 4, 2, [TraitCard(FAT_TISSUE)])
        list_of_species = [big, aCarnivore, fedVeg, smallerFatTissue, smallerVeg, aCarnivore]

        playerstate = PlayerState(1, 2, list_of_species, [])

        self.assertEquals(playerstate.get_neighbors(0), (False, aCarnivore))
        self.assertEquals(playerstate.get_neighbors(2), (aCarnivore, smallerFatTissue))
        self.assertEquals(playerstate.get_neighbors(5), (smallerVeg, False))

    def test_get_species_at(self):
        species1 = Species(1, 1, 1)
        species2 = Species(2, 2, 2)
        species3 = Species(3, 3, 3)
        ps = PlayerState(1, 0, [species1, species2, species3])
        self.assertEquals(ps.get_species_at(0), species1)
        self.assertEquals(ps.get_species_at(1), species2)
        self.assertEquals(ps.get_species_at(2), species3)

    def test_remove_extinct(self):
        species1 = Species(1, 1, 1)
        species2 = Species(2, 2, 0)
        species3 = Species(3, 3, 3)
        ps = PlayerState(1, 0, [species1, species2, species3])

        self.assertEquals(ps.species, [species1, species2, species3])

        self.assertFalse(ps.remove_extinct(0), species1)
        self.assertTrue(ps.remove_extinct(1), species2)
        self.assertFalse(ps.remove_extinct(1), species3)

        self.assertEquals(ps.species, [species1, species3])

    def test_can_feed_veg(self):
        species1 = Species(1, 1, 1)
        species2 = Species(2, 2, 0)
        species3 = Species(3, 3, 3, [TraitCard(CARNIVORE)])
        ps = PlayerState(1, 0, [species1, species2, species3])

        self.assertTrue(ps.can_feed_veg(1))
        self.assertFalse(ps.can_feed_veg(2))

    def test_feed_species_with_trait(self):
        species1 = Species(1, 1, 3, [TraitCard(SCAVENGER)])
        species2 = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        species3 = Species(3, 3, 5, [TraitCard(CARNIVORE), TraitCard(SCAVENGER)])
        ps = PlayerState(1, 0, [species1, species2, species3])

        self.assertEquals(species1.food, 1)
        self.assertEquals(species2.food, 2)
        self.assertEquals(species3.food, 3)

        ps.feed_species_with_trait(SCAVENGER, 4)

        self.assertEquals(species1.food, 2)
        self.assertEquals(species2.food, 2)
        self.assertEquals(species3.food, 4)

        ps.feed_species_with_trait(CARNIVORE, 1)

        self.assertEquals(species1.food, 2)
        self.assertEquals(species2.food, 3)
        self.assertEquals(species3.food, 4)

    def test_add_fertile_populations(self):
        fertile = Species(1, 1, 3, [TraitCard(FERTILE)])
        carnivore = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        fertile_scav = Species(3, 3, 7, [TraitCard(FERTILE), TraitCard(SCAVENGER)])
        new_fertile = Species(1, 1, 4, [TraitCard(FERTILE)])
        new_carnivore = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        new_fertile_scav = Species(3, 3, 7, [TraitCard(FERTILE), TraitCard(SCAVENGER)])
        ps = PlayerState(1, 0, [fertile, carnivore, fertile_scav])

        ps.add_fertile_populations()
        self.assertEquals(fertile, new_fertile)
        self.assertEquals(carnivore, new_carnivore)
        self.assertEquals(fertile_scav, new_fertile_scav)

    def test_transfer_fat_food(self):
        fat1 = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 3)
        empty_fat = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        fat2 = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 6)
        non_fat = Species(2, 3, 4)

        new_fat1 = Species(5, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        new_empty_fat = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        new_fat2 = Species(7, 5, 7, [TraitCard(FAT_TISSUE)], 1)
        new_non_fat = Species(2, 3, 4)

        player1 = PlayerState(2, 2, [fat1, non_fat, empty_fat, fat2])

        player1.transfer_fat_food()

        self.assertEquals(fat1, new_fat1)
        self.assertEquals(non_fat, new_non_fat)
        self.assertEquals(fat2, new_fat2)
        self.assertEquals(empty_fat, new_empty_fat)

    def test_cooperation_feed(self):
        species1 = Species(3, 4, 5, [TraitCard(COOPERATION)])
        species2 = Species(3, 3, 6, [TraitCard(COOPERATION)])
        species3 = Species(0, 3, 3)
        species4 = Species(0, 1, 2)
        speciesList1 = [species1, species2, species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player1.watering_hole = 4

        self.assertEquals(player1.watering_hole, 4)
        self.assertEquals(species1.food, 3)
        self.assertEquals(species2.food, 3)
        self.assertEquals(species3.food, 0)
        self.assertEquals(species4.food, 0)

        player1.cooperationFeed(0)

        self.assertEquals(player1.watering_hole, 2)
        self.assertEquals(species1.food, 3)
        self.assertEquals(species2.food, 4)
        self.assertEquals(species3.food, 1)
        self.assertEquals(species4.food, 0)

    def test_feed_from_watering_hole(self):
        species1 = Species(1, 1, 3, [TraitCard(SCAVENGER)])
        species2 = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        species3 = Species(1, 3, 5, [TraitCard(FORAGING), TraitCard(SCAVENGER)])
        ps = PlayerState(1, 0, [species1, species2, species3])

        self.assertEquals(species1.food, 1)
        self.assertEquals(species2.food, 2)
        self.assertEquals(species3.food, 1)

        ps.feedFromWateringHole(1, 4)

        self.assertEquals(species1.food, 1)
        self.assertEquals(species2.food, 3)
        self.assertEquals(species3.food, 1)
        self.assertEquals(ps.watering_hole, 3)

        ps.feedFromWateringHole(2, 3)

        self.assertEquals(species1.food, 1)
        self.assertEquals(species2.food, 3)
        self.assertEquals(species3.food, 3)
        self.assertEquals(ps.watering_hole, 1)

        ps.feedFromWateringHole(2, 1)

        self.assertEquals(species1.food, 1)
        self.assertEquals(species2.food, 3)
        self.assertEquals(species3.food, 4)
        self.assertEquals(ps.watering_hole, 0)

        ps.feedFromWateringHole(2, 0)

        self.assertEquals(species1.food, 1)
        self.assertEquals(species2.food, 3)
        self.assertEquals(species3.food, 4)
        self.assertEquals(ps.watering_hole, 0)

    def test_remove_card(self):
        species1 = Species(1, 1, 3, [TraitCard(SCAVENGER)])
        species2 = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        species3 = Species(1, 3, 5, [TraitCard(FORAGING), TraitCard(SCAVENGER)])

        trait1 = TraitCard(SCAVENGER)

        ps = PlayerState(1, 0, [species1, species2, species3], [trait1])

        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.foodbag, 0)
        self.assertEquals(ps.species, [species1, species2, species3])
        self.assertEquals(ps.trait_cards, [trait1])

        removed_card = ps.remove_card(0)

        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.foodbag, 0)
        self.assertEquals(ps.species, [species1, species2, species3])
        self.assertEquals(ps.trait_cards, [])
        self.assertEquals(removed_card, trait1)

    def test_add_species_with_traits(self):
        species1 = Species(1, 1, 3, [TraitCard(SCAVENGER)])
        species2 = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        species3 = Species(1, 3, 5, [TraitCard(FORAGING), TraitCard(SCAVENGER)])

        trait1 = TraitCard(SCAVENGER)
        trait2 = TraitCard(CARNIVORE)
        trait3 = TraitCard(BURROWING)

        ps = PlayerState(1, 0, [species1, species2, species3], [trait1])

        self.assertEquals(ps.species, [species1, species2, species3])
        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.foodbag, 0)

        ps.add_species_with_traits([trait2, trait3])

        self.assertEquals(ps.species[:3], [species1, species2, species3])
        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.foodbag, 0)
        self.assertEquals(ps.species[3].food, 0)
        self.assertEquals(ps.species[3].body, 0)
        self.assertEquals(ps.species[3].population, 1)
        self.assertEquals(ps.species[3].trait_cards, [trait2, trait3])

    def test_remove_trait_cards_at_indices(self):
        species1 = Species(1, 1, 3, [TraitCard(SCAVENGER)])
        species2 = Species(2, 2, 3, [TraitCard(CARNIVORE)])

        scavenger = TraitCard(SCAVENGER)
        carnivore = TraitCard(CARNIVORE)
        long_neck = TraitCard(LONG_NECK)
        burrowing = TraitCard(BURROWING)
        fertile = TraitCard(FERTILE)
        climbing = TraitCard(CLIMBING)


        ps = PlayerState(1, 0, [species1, species2], [scavenger, carnivore, long_neck, burrowing, fertile, climbing])

        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.foodbag, 0)
        self.assertEquals(len(ps.species), 2)
        self.assertEquals(ps.species, [species1, species2])
        self.assertEquals(len(ps.trait_cards), 6)
        self.assertEquals(ps.trait_cards, [scavenger, carnivore, long_neck, burrowing, fertile, climbing])

        ps.remove_trait_cards_at_indices([0, 3, 5])

        self.assertEquals(ps.id, 1)
        self.assertEquals(ps.foodbag, 0)
        self.assertEquals(len(ps.species), 2)
        self.assertEquals(ps.species[0].trait_cards[0].name, SCAVENGER)
        self.assertEquals(ps.species[1].trait_cards[0].name, CARNIVORE)
        self.assertEquals(len(ps.trait_cards), 3)
        self.assertEquals(ps.trait_cards[0], carnivore)
        self.assertEquals(ps.trait_cards[1], long_neck)
        self.assertEquals(ps.trait_cards[2], fertile)

    def test_calculate_score(self):
        species1 = Species(1, 1, 3, [TraitCard(SCAVENGER)])
        species2 = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        species3 = Species(1, 3, 5, [TraitCard(FORAGING), TraitCard(SCAVENGER)])

        trait1 = TraitCard(SCAVENGER)

        ps = PlayerState(1, 8, [species1, species2, species3], [trait1])

        self.assertEquals(ps.calculate_score(), 23)

    def test_end_player_turn(self):
        species1 = Species(1, 1, 3, [TraitCard(SCAVENGER)])
        species2 = Species(2, 2, 3, [TraitCard(CARNIVORE)])
        species3 = Species(0, 3, 5, [TraitCard(FORAGING), TraitCard(SCAVENGER)])

        trait1 = TraitCard(SCAVENGER)

        ps = PlayerState(1, 8, [species1, species2, species3], [trait1])

        num_extinct = ps.end_player_turn()
        self.assertEquals(num_extinct, 1)
        self.assertEquals(ps.species, [species1, species2])
        self.assertEquals(ps.foodbag, 11)
        self.assertEquals(ps.trait_cards, [trait1])
        self.assertEquals(species1, Species(0, 1, 1, [TraitCard(SCAVENGER)]))
        self.assertEquals(species2, Species(0, 2, 2, [TraitCard(CARNIVORE)]))



    def test_parse_feeding(self):
        species_list = [[["food", 0],
                       ["body",2],
                       ["population", 3],
                       ["traits",[]],
                       ["fat-food" , 0]]]
        player1 = [["id", 1],["species", species_list], ["bag", 0]]

        json_in = [player1, 3, [player1, player1]]

        species = Species(0, 2, 3, [], 0)
        ps = PlayerState(1, 2, [species])

        first_player = PlayerState.parse_feeding(json_in)[0]
        watering_hole = PlayerState.parse_feeding(json_in)[1]
        other_players = PlayerState.parse_feeding(json_in)[2]

        self.assertEquals(first_player.species[0].food, ps.species[0].food)
        self.assertEquals(first_player.species[0].body, ps.species[0].body)
        self.assertEquals(first_player.species[0].population, ps.species[0].population)
        self.assertEquals(first_player.species[0].trait_cards, ps.species[0].trait_cards)
        self.assertEquals(first_player.species[0].fatFood, ps.species[0].fatFood)

        self.assertEquals(watering_hole, 3)

        self.assertEquals(len(other_players[0]), 1)


if __name__ == "__main__":
    unittest.main()
