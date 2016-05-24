#!/usr/bin/env python2.7

import unittest
from growBody import GrowBody
from growPopulation import GrowPopulation
from replaceTrait import ReplaceTrait
from boardTrade import BoardTrade
from playerAction import PlayerAction
from dealer import Dealer

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'feeding'))
from playerState import PlayerState
from species import Species
from traitCard import TraitCard
from constants import *


class ActionTests(unittest.TestCase):

    def setUp(self):
        self.valid_grow_body = ["body", 1, 0]
        self.valid_grow_body2 = ["body", 5, 1]
        self.valid_grow_body3 = ["body", 3, 3]
        self.valid_grow_body4 = ["body", 1, 1]
        self.valid_grow_body5 = ["body", 0, 2]

        self.invalid_grow_body1 = [-1, 2, 9]
        self.invalid_grow_body2 = ["body", 2, "a"]
        self.invalid_grow_body3 = ["body", 2, -1]
        self.invalid_grow_body4 = ["body", 2]
        self.invalid_grow_body5 = ["body", 0, False]

        self.valid_grow_population = ["population", 1, 0]
        self.valid_grow_population2 = ["population", 4, 2]
        self.valid_grow_population3 = ["population", 3, 1]

        self.invalid_grow_population1 = [-1, 2, 9]
        self.invalid_grow_population2 = ["population", 2, "a"]
        self.invalid_grow_population3 = ["population", 2, -1]
        self.invalid_grow_population4 = ["population", 2]
        self.invalid_grow_population5 = ["population", 0, False]

        self.valid_proxy_grow_body = [1, 1]
        self.invalid_proxy_grow_body1 = [2, -9]
        self.valid_proxy_grow_population = [1, 0]
        self.invalid_proxy_grow_population1 = [-1, 2, 9]

        self.valid_replace1 = [1, 4, 2]
        self.valid_replace2 = [0, 2, 3]
        self.valid_replace3 = [2, 1, 9]
        self.valid_replace4 = [3, 2, 10]
        self.valid_replace5 = [2, 1, 0]

        self.invalid_replace1 = ["1", 1, 1]
        self.invalid_replace2 = [False, 1, 1]
        self.invalid_replace3 = [1, 1]
        self.invalid_replace4 = []
        self.invalid_replace5 = "abc"
        self.invalid_replace6 = [-1, 1, 1]

        self.valid_btrade1 = [1, 1, 1]
        self.valid_btrade2 = [0, 0, 0]
        self.valid_btrade3 = [1, 1]
        self.valid_btrade4 = [1, 1, 2, 1]
        self.valid_btrade5 = [0]
        self.valid_btrade6 = [5, 6, 7]
        self.valid_btrade7 = [8]
        self.valid_btrade8 = [0, 1, 2, 3]

        self.invalid_btrade1 = ["1", 1, 1]
        self.invalid_btrade2 = [False, 1, 1]
        self.invalid_btrade3 = []
        self.invalid_btrade4 = "abc"
        self.invalid_btrade5 = [-1, 1, 1]
        self.invalid_btrade6 = [-1, 1]
        self.invalid_btrade7 = [False, 1]
        self.invalid_btrade8 = [4, 1, 2, 1, 2]

        self.valid_action1 = [0, [], [], [], []]
        self.valid_action2 = [1, [self.valid_grow_population, self.valid_grow_population2, self.valid_grow_population3], [], [], []]
        self.valid_action3 = [2, [self.valid_grow_population], [self.valid_grow_body4], [], []]
        self.valid_action4 = [3, [self.valid_grow_population2], [self.valid_grow_body, self.valid_grow_body2, self.valid_grow_body3],
                         [self.valid_btrade1, self.valid_btrade2], []]
        self.valid_action5 = [4, [self.valid_grow_population], [self.valid_grow_body4, self.valid_grow_body5, self.valid_grow_body3],
                         [self.valid_btrade6, self.valid_btrade7], [self.valid_replace3, self.valid_replace4]]

        self.valid_proxy_action3 = [2, [self.valid_proxy_grow_population], [self.valid_proxy_grow_body], [], []]


        self.invalid_action1 = [-1, [], [], [], []]
        self.invalid_action2 = [False, [self.valid_grow_population, self.valid_grow_population2,
                                        self.invalid_grow_population3], [], [], []]
        self.invalid_action3 = [2, [self.invalid_grow_population2], [self.valid_grow_body], []]
        self.invalid_action4 = [3, [self.valid_grow_population2],
                           [self.valid_grow_body, self.valid_grow_body2, self.valid_grow_body3],
                           [self.valid_btrade1, self.valid_btrade2], [], []]
        self.invalid_action5 = [4]

        self.valid_step4 = [self.valid_action5, self.valid_action1, self.valid_action2]

        self.valid_replace_list = [self.valid_replace1, self.valid_replace2]
        self.invalid_replace_list = [self.invalid_replace1, self.invalid_replace2, self.invalid_replace3,
                                    self.invalid_replace4, self.invalid_replace5,
                                    self.invalid_replace6]

        self.invalid_list = [self.invalid_btrade1, self.invalid_btrade2, self.invalid_btrade3, self.invalid_btrade4,
                             self.invalid_btrade5, self.invalid_btrade6, self.invalid_btrade7, self.invalid_btrade8]
        self.valid_list = [self.valid_btrade1, self.valid_btrade2, self.valid_btrade3,
                           self.valid_btrade4, self.valid_btrade5]

        self.trait1 = TraitCard(CARNIVORE)
        self.trait2 = TraitCard(SCAVENGER)
        self.trait3 = TraitCard(LONG_NECK)
        self.trait4 = TraitCard(HERDING)
        self.trait5 = TraitCard(FERTILE)
        self.trait6 = TraitCard(HORNS)

        self.species1 = Species(3, 4, 5)
        self.species1a = Species(3, 4, 5)
        self.species2 = Species(4, 5, 6)
        self.species2a = Species(4, 5, 6)
        self.species3 = Species(2, 2, 2, [self.trait1, self.trait3])
        self.species4 = Species(1, 2, 3, [self.trait2, self.trait4, self.trait6])

        self.player1 = PlayerState(1, 2, [self.species1, self.species2], [self.trait1])
        self.player2 = PlayerState(2, 2, [self.species1, self.species2], [self.trait1, self.trait2, self.trait3,
                                                                          self.trait1])
        self.player3 = PlayerState(3, 3, [self.species1a, self.species2a, self.species3, self.species4],
                                   [self.trait1, self.trait2, self.trait3, self.trait4, self.trait5, self.trait6,
                                    self.trait1, self.trait2, self.trait3, self.trait4, self.trait5, self.trait6])

        self.dealer1 = Dealer([self.player1], 4, [self.trait1, self.trait2, self.trait1])
        self.dealer2 = Dealer([self.player2], 4, [self.trait1, self.trait2])
        self.dealer3 = Dealer([self.player1, self.player3], 5, [self.trait1, self.trait3, self.trait5])

    def tearDown(self):
        del self.valid_grow_body
        del self.valid_grow_body2
        del self.valid_grow_body3
        del self.valid_grow_body4
        del self.valid_grow_body5

        del self.invalid_grow_body1
        del self.invalid_grow_body2
        del self.invalid_grow_body3
        del self.invalid_grow_body4
        del self.invalid_grow_body5

        del self.valid_grow_population
        del self.valid_grow_population2
        del self.valid_grow_population3

        del self.invalid_grow_population1
        del self.invalid_grow_population2
        del self.invalid_grow_population3
        del self.invalid_grow_population4
        del self.invalid_grow_population5

        del self.valid_proxy_grow_body
        del self.invalid_proxy_grow_body1
        del self.valid_proxy_grow_population
        del self.invalid_proxy_grow_population1

        del self.valid_replace1
        del self.valid_replace2
        del self.valid_replace3
        del self.valid_replace4
        del self.valid_replace5

        del self.invalid_replace1
        del self.invalid_replace2
        del self.invalid_replace3
        del self.invalid_replace4
        del self.invalid_replace5
        del self.invalid_replace6

        del self.valid_btrade1
        del self.valid_btrade2
        del self.valid_btrade3
        del self.valid_btrade4
        del self.valid_btrade5
        del self.valid_btrade6
        del self.valid_btrade7
        del self.valid_btrade8

        del self.invalid_btrade1
        del self.invalid_btrade2
        del self.invalid_btrade3
        del self.invalid_btrade4
        del self.invalid_btrade5
        del self.invalid_btrade6
        del self.invalid_btrade7
        del self.invalid_btrade8

        del self.valid_action1
        del self.valid_action2
        del self.valid_action3
        del self.valid_action4
        del self.valid_action5

        del self.valid_proxy_action3

        del self.invalid_action1
        del self.invalid_action2
        del self.invalid_action3
        del self.invalid_action4
        del self.invalid_action5

        del self.valid_replace_list
        del self.invalid_replace_list

        del self.invalid_list
        del self.valid_list

        del self.trait1
        del self.trait2
        del self.trait3
        del self.trait4
        del self.trait5
        del self.trait6

        del self.species1
        del self.species1a
        del self.species2
        del self.species2a
        del self.species3
        del self.species4

        del self.player1
        del self.player2
        del self.player3

        del self.dealer1
        del self.dealer2
        del self.dealer3


    def test_parse_step4(self):
        step4 = Dealer.parse_step4(self.valid_step4)

        self.assertEquals(step4[0].food_card_index, 4)
        self.assertEquals(len(step4[0].gp_list), 1)
        self.assertEquals(len(step4[0].gb_list), 3)
        self.assertEquals(len(step4[0].bt_list), 2)
        self.assertEquals(len(step4[0].rt_list), 2)
        self.assertEquals(step4[1].food_card_index, 0)
        self.assertEquals(len(step4[1].gp_list), 0)
        self.assertEquals(len(step4[1].gb_list), 0)
        self.assertEquals(len(step4[1].bt_list), 0)
        self.assertEquals(len(step4[1].rt_list), 0)
        self.assertEquals(step4[2].food_card_index, 1)
        self.assertEquals(len(step4[2].gp_list), 3)
        self.assertEquals(len(step4[2].gb_list), 0)
        self.assertEquals(len(step4[2].bt_list), 0)
        self.assertEquals(len(step4[2].rt_list), 0)


    def test_is_valid_action(self):

        self.assertTrue(PlayerAction.is_valid_action(self.valid_action1))
        self.assertTrue(PlayerAction.is_valid_action(self.valid_action2))
        self.assertTrue(PlayerAction.is_valid_action(self.valid_action3))
        self.assertTrue(PlayerAction.is_valid_action(self.valid_action4))
        self.assertTrue(PlayerAction.is_valid_action(self.valid_action5))

        self.assertFalse(PlayerAction.is_valid_action(self.invalid_action1))
        self.assertFalse(PlayerAction.is_valid_action(self.invalid_action2))
        self.assertFalse(PlayerAction.is_valid_action(self.invalid_action3))
        self.assertFalse(PlayerAction.is_valid_action(self.invalid_action4))
        self.assertFalse(PlayerAction.is_valid_action(self.invalid_action5))

    def test_valid_grow_body(self):
        self.assertTrue(GrowBody.is_valid_body_grow(self.valid_grow_body))
        self.assertFalse(GrowBody.is_valid_body_grow(self.invalid_grow_body1))
        self.assertFalse(GrowBody.is_valid_body_grow(self.invalid_grow_body2))
        self.assertFalse(GrowBody.is_valid_body_grow(self.invalid_grow_body3))
        self.assertFalse(GrowBody.is_valid_body_grow(self.invalid_grow_body4))
        self.assertFalse(GrowBody.is_valid_body_grow(self.invalid_grow_body5))

    def test_valid_proxy_grow_body(self):
        self.assertTrue(GrowBody.is_valid_proxy_grow(self.valid_proxy_grow_body))
        self.assertFalse(GrowBody.is_valid_proxy_grow(self.invalid_proxy_grow_body1))

    def test_valid_grow_population(self):
        self.assertTrue(GrowPopulation.is_valid_pop_grow(self.valid_grow_population))
        self.assertFalse(GrowPopulation.is_valid_pop_grow(self.invalid_grow_population1))
        self.assertFalse(GrowPopulation.is_valid_pop_grow(self.invalid_grow_population2))
        self.assertFalse(GrowPopulation.is_valid_pop_grow(self.invalid_grow_population3))
        self.assertFalse(GrowPopulation.is_valid_pop_grow(self.invalid_grow_population4))
        self.assertFalse(GrowPopulation.is_valid_pop_grow(self.invalid_grow_population5))

    def test_valid_proxy_grow_population(self):
        self.assertTrue(GrowPopulation.is_valid_proxy_grow(self.valid_proxy_grow_population))
        self.assertFalse(GrowPopulation.is_valid_proxy_grow(self.invalid_proxy_grow_population1))

    def test_parse_grow_body(self):
        body_growing = GrowBody.parse_grow_body(self.valid_grow_body)

        self.assertEquals(body_growing.__class__, GrowBody)
        self.assertFalse(body_growing.__class__ == GrowPopulation)

        self.assertEquals(body_growing.species_index, 1)
        self.assertEquals(body_growing.card_trade_index, 0)

        with self.assertRaises(Exception):
            GrowBody.parse_grow_body(self.invalid_grow_body1)

    def test_parse_proxy_grow_body(self):
        body_growing = GrowBody.parse_proxy_grow_body(self.valid_proxy_grow_body)

        self.assertEquals(body_growing.__class__, GrowBody)
        self.assertFalse(body_growing.__class__ == GrowPopulation)

        self.assertEquals(body_growing.species_index, 1)
        self.assertEquals(body_growing.card_trade_index, 1)

        with self.assertRaises(Exception):
            GrowBody.parse_proxy_grow_body(self.invalid_proxy_grow_body1)

    def test_population_to_json(self):
        gp = GrowPopulation(2, 3)
        self.assertEquals(gp.to_json(), ["population", 2, 3])

    def test_population_to_json_proxy(self):
        gp = GrowPopulation(2, 3)
        self.assertEquals(gp.to_json_proxy(), [2, 3])

    def test_parse_grow_population(self):
        population_growing = GrowPopulation.parse_grow_population(self.valid_grow_population)

        self.assertEquals(population_growing.__class__, GrowPopulation)
        self.assertFalse(population_growing.__class__ == GrowBody)

        self.assertEquals(population_growing.species_index, 1)
        self.assertEquals(population_growing.card_trade_index, 0)

        with self.assertRaises(Exception):
            GrowPopulation.parse_grow_population(self.invalid_grow_population3)

    def test_parse_proxy_grow_population(self):
        population_growing = GrowPopulation.parse_proxy_grow_population(self.valid_proxy_grow_population)

        self.assertEquals(population_growing.__class__, GrowPopulation)
        self.assertFalse(population_growing.__class__ == GrowBody)

        self.assertEquals(population_growing.species_index, 1)
        self.assertEquals(population_growing.card_trade_index, 0)

        with self.assertRaises(Exception):
            GrowPopulation.parse_proxy_grow_population(self.invalid_proxy_grow_population1)

    def test_body_to_json(self):
        gb = GrowBody(2, 3)
        self.assertEquals(gb.to_json(), ["body", 2, 3])

    def test_body_to_json_proxy(self):
        gb = GrowBody(2, 3)
        self.assertEquals(gb.to_json_proxy(), [2, 3])

    def test_is_valid_replaceTrait(self):
        for valid in self.valid_replace_list:
            try:
                self.assertTrue(ReplaceTrait.is_valid_replace(valid))
            except AssertionError:
                raise AssertionError("Failed: Expected True (but got False) for " + str(valid))

        for invalid in self.invalid_replace_list:
            try:
                self.assertFalse(ReplaceTrait.is_valid_replace(invalid))
            except AssertionError:
                raise AssertionError("Failed: Expected False (but got True) for " + str(invalid))

    def test_is_valid_boardTrade(self):
        for valid in self.valid_list:
            try:
                self.assertTrue(BoardTrade.is_valid_board_trade(valid))
            except AssertionError:
                raise AssertionError("Failed: Expected True (but got False) for " + str(valid))

        for invalid in self.invalid_list:
            try:
                self.assertFalse(BoardTrade.is_valid_board_trade(invalid))
            except AssertionError:
                raise AssertionError("Failed: Expected False (but got True) for " + str(invalid))

    def test_parse_board_trade(self):
        bt = BoardTrade.parse_board_trade(self.valid_btrade1)
        bt2 = BoardTrade.parse_board_trade(self.valid_btrade2)

        self.assertEquals(bt.trait_card_index, 1)
        self.assertEquals(bt.traits_for_species, [1, 1])

        self.assertEquals(bt2.trait_card_index, 0)
        self.assertEquals(bt2.traits_for_species, [0, 0])

        with self.assertRaises(Exception):
            BoardTrade.parse_board_trade(self.invalid_btrade1)

    def test_board_to_json(self):
        bt = BoardTrade(0, [3, 2])
        self.assertEquals(bt.to_json(), [0, 3, 2])

    def test_parse_replace_trait(self):
        rt = ReplaceTrait.parse_replace_trait(self.valid_replace1)

        self.assertEquals(rt.species_index, 1)
        self.assertEquals(rt.trait_to_remove, 4)
        self.assertEquals(rt.trait_to_add, 2)

        with self.assertRaises(Exception):
            ReplaceTrait.parse_replace_trait(self.invalid_replace1)

        with self.assertRaises(Exception):
            ReplaceTrait.parse_replace_trait(self.invalid_replace2)

    def test_replace_to_json(self):
        rt = ReplaceTrait(0, 3, 2)
        self.assertEquals(rt.to_json(), [0, 3, 2])

    def test_action_to_json(self):
        pa = PlayerAction(1, [GrowPopulation(2, 3)], [GrowBody(1, 2), GrowBody(0, 1)], [BoardTrade(3, [1, 2, 3])],
                                                                                       [ReplaceTrait(1, 2, 3)])
        self.assertEquals(pa.to_json_action_4(), [1, [["population", 2, 3]], [["body", 1, 2], ["body", 0, 1]],
                                                  [[3, 1, 2, 3]], [[1, 2, 3]]])

    def test_to_proxy_json_action_4(self):
        pa = PlayerAction(1, [GrowPopulation(2, 3)], [GrowBody(1, 2), GrowBody(0, 1)], [BoardTrade(3, [1, 2, 3])],
                          [ReplaceTrait(1, 2, 3)])
        self.assertEquals(pa.to_proxy_json_action_4(), [1, [[2, 3]], [[1, 2], [0, 1]],
                                                  [[3, 1, 2, 3]], [[1, 2, 3]]])

    def test_grow_population(self):
        gp = GrowPopulation.parse_grow_population(self.valid_grow_population)

        self.assertEquals(self.player1.trait_cards, [self.trait1])
        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.species2.body, 5)
        self.assertEquals(self.species2.population, 6)
        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species1.body, 4)
        self.assertEquals(self.species1.population, 5)
        self.assertEquals(self.dealer1.hand, [self.trait1, self.trait2, self.trait1])

        gp.grow_population(self.player1)

        self.assertEquals(self.player1.trait_cards, [self.trait1])
        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.species2.body, 5)
        self.assertEquals(self.species2.population, 7)
        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species1.body, 4)
        self.assertEquals(self.species1.population, 5)
        self.assertEquals(self.dealer1.hand, [self.trait1, self.trait2, self.trait1])

    def test_grow_body(self):
        gb = GrowBody.parse_grow_body(self.valid_grow_body)

        self.assertEquals(self.player1.trait_cards, [self.trait1])
        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.species2.body, 5)
        self.assertEquals(self.species2.population, 6)
        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species1.body, 4)
        self.assertEquals(self.species1.population, 5)
        self.assertEquals(self.dealer1.hand, [self.trait1, self.trait2, self.trait1])

        gb.grow_body(self.player1)

        self.assertEquals(self.player1.trait_cards, [self.trait1])
        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.species2.body, 6)
        self.assertEquals(self.species2.population, 6)
        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species1.body, 4)
        self.assertEquals(self.species1.population, 5)
        self.assertEquals(self.dealer1.hand, [self.trait1, self.trait2, self.trait1])

    def test_board_trade_simple(self):
        bt = BoardTrade.parse_board_trade(self.valid_btrade5)

        self.assertEquals(self.player2.species, [self.species1, self.species2])
        bt.board_trade(self.player2)
        self.assertEquals(self.player2.species, [self.species1, self.species2, Species(0, 0, 1)])

    def test_board_trade_complex(self):
        bt = BoardTrade.parse_board_trade(self.valid_btrade8)

        new_species = Species(0, 0, 1, [self.trait2, self.trait3, self.trait1])
        self.assertEquals(self.player2.trait_cards, [self.trait1, self.trait2, self.trait3, self.trait1])
        self.assertEquals(self.player2.species, [self.species1, self.species2])
        bt.board_trade(self.player2)
        self.assertEquals(self.player2.trait_cards, [self.trait1, self.trait2, self.trait3, self.trait1])
        self.assertEquals(self.player2.species, [self.species1, self.species2, new_species])

    def test_replace_trait(self):
        rt = ReplaceTrait.parse_replace_trait(self.valid_replace5)

        trait_list = [self.trait1, self.trait1]
        new_species = Species(self.species3.food, self.species3.body, self.species3.population, trait_list)
        unchanged_species = Species(self.species1.food, self.species1.body, self.species1.population)
        self.assertEquals(self.species3.trait_cards, [self.trait1, self.trait3])

        rt.replace_trait(self.player3)

        self.assertEquals(self.species3, new_species)
        self.assertEquals(self.species1, unchanged_species)

    def test_perform_all_actions(self):
        # will grow body at species index 1, remove card 0, then grow population at species index 1, remove card 0
        playerAction = PlayerAction.parse_player_action(self.valid_action3)

        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species1.body, 4)
        self.assertEquals(self.species1.population, 5)

        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.species2.body, 5)
        self.assertEquals(self.species2.population, 6)

        self.assertEquals(self.player2.trait_cards, [self.trait1, self.trait2, self.trait3, self.trait1])

        self.assertEquals(self.dealer2.hand, [self.trait1, self.trait2])

        playerAction.perform_all_actions(self.player2)

        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species1.body, 4)
        self.assertEquals(self.species1.population, 5)

        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.species2.body, 6)
        self.assertEquals(self.species2.population, 7)

        self.assertEquals(self.player2.trait_cards, [self.trait1])
        self.assertTrue(isinstance(self.player2.trait_cards, list))

        self.assertEquals(self.dealer2.hand, [self.trait1, self.trait2])

    def test_perform_all_actions_2(self):
        playerAction = PlayerAction.parse_player_action(self.valid_action5)

        self.valid_replace3 = [2, 1, 9]
        self.valid_replace4 = [3, 2, 10]

        new_species_1a = Species(3, 5, 5)
        new_species_2a = Species(4, 6, 7)
        new_species_3 = Species(2, 2, 2, [self.trait1, self.trait4])
        new_species_4 = Species(1, 3, 3, [self.trait2, self.trait4, self.trait5])
        added_species_1 = Species(0, 0, 1, [self.trait1, self.trait2])
        added_species_2 = Species(0, 0, 1)

        new_player_3_hand = [self.trait6]
        new_dealer_hand = [self.trait1, self.trait3, self.trait5]

        self.assertEquals(self.player1.id, 1)
        self.assertEquals(self.player1.foodbag, 2)
        self.assertEquals(self.player1.species, [self.species1, self.species2])
        self.assertEquals(self.player1.trait_cards, [self.trait1])

        self.assertEquals(self.player3.id, 3)
        self.assertEquals(self.player3.foodbag, 3)
        self.assertEquals(self.player3.species, [self.species1a, self.species2a, self.species3, self.species4])
        self.assertEquals(self.player3.trait_cards, [self.trait1, self.trait2, self.trait3, self.trait4, self.trait5,
                                                     self.trait6, self.trait1, self.trait2, self.trait3, self.trait4,
                                                     self.trait5, self.trait6])

        self.assertEquals(self.dealer3.playerStates, [self.player1, self.player3])
        self.assertEquals(self.dealer3.wateringHole, 5)
        self.assertEquals(self.dealer3.hand, [self.trait1, self.trait3, self.trait5])

        playerAction.perform_all_actions(self.player3)

        self.assertEquals(self.player1.id, 1)
        self.assertEquals(self.player1.foodbag, 2)
        self.assertEquals(self.player1.species, [self.species1, self.species2])
        self.assertEquals(self.player1.trait_cards, [self.trait1])

        self.assertEquals(self.player3.id, 3)
        self.assertEquals(self.player3.foodbag, 3)
        self.assertEquals(len(self.player3.species), 6)
        self.assertEquals(self.player3.species[0], new_species_1a)
        self.assertEquals(self.player3.species[1], new_species_2a)
        self.assertEquals(self.player3.species[2], new_species_3)
        self.assertEquals(self.player3.species[3], new_species_4)
        self.assertEquals(self.player3.species[4], added_species_1)
        self.assertEquals(self.player3.species[5], added_species_2)

        self.assertEquals(len(self.player3.trait_cards), 1)
        self.assertEquals(self.player3.trait_cards, new_player_3_hand)

        self.assertEquals(self.dealer3.playerStates, [self.player1, self.player3])
        self.assertEquals(self.dealer3.wateringHole, 5)
        self.assertEquals(self.dealer3.hand, new_dealer_hand)
        # self.assertEquals(self.dealer3.face_down_cards, [self.trait5])

    def test_perform_all_actions_proxy(self):
        # will grow body at species index 1, remove card 0, then grow population at species index 1, remove card 0
        playerAction = PlayerAction.parse_proxy_player_action(self.valid_proxy_action3)

        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species1.body, 4)
        self.assertEquals(self.species1.population, 5)

        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.species2.body, 5)
        self.assertEquals(self.species2.population, 6)

        self.assertEquals(self.player2.trait_cards, [self.trait1, self.trait2, self.trait3, self.trait1])

        self.assertEquals(self.dealer2.hand, [self.trait1, self.trait2])

        playerAction.perform_all_actions(self.player2)

        self.assertEquals(self.species1.food, 3)
        self.assertEquals(self.species1.body, 4)
        self.assertEquals(self.species1.population, 5)

        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.species2.body, 6)
        self.assertEquals(self.species2.population, 7)

        self.assertEquals(self.player2.trait_cards, [self.trait1])
        self.assertTrue(isinstance(self.player2.trait_cards, list))

        self.assertEquals(self.dealer2.hand, [self.trait1, self.trait2])


    def test_add_index(self):
        playerAction = PlayerAction.parse_player_action(self.valid_action3)
        # Initially populated with first nat in playerAction json-in
        self.assertEquals(playerAction.player_card_trade_indices, [2])

        playerAction.add_index(3)

        self.assertEquals(playerAction.player_card_trade_indices, [2, 3])

        playerAction.add_index(4)

        self.assertEquals(playerAction.player_card_trade_indices, [2, 3, 4])

        with self.assertRaises(Exception):
            playerAction.add_index(4)


if __name__ == "__main__":
    unittest.main()