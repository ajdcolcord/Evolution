#!/usr/bin/env python2.7

import unittest
import sys, os
import copy
from playerAction import PlayerAction
from growPopulation import GrowPopulation
from growBody import GrowBody
from boardTrade import BoardTrade
from replaceTrait import ReplaceTrait
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'feeding'))
from playerState import PlayerState
from player import Player
from species import Species
from dealer import Dealer
from traitCard import TraitCard
from constants import *

class DealerTests(unittest.TestCase):

    def setUp(self):
        self.trait1 = TraitCard(CARNIVORE)
        self.trait2 = TraitCard(SCAVENGER)
        self.long_neck0 = TraitCard(LONG_NECK, 0)
        self.horns0 = TraitCard(HORNS, 0)
        self.fertile0 = TraitCard(FERTILE, 0)
        self.fat_tissue0 = TraitCard(FAT_TISSUE, 0)
        self.scav0 = TraitCard(SCAVENGER, 0)
        self.forage0 = TraitCard(FORAGING, 0)
        self.carn2 = TraitCard(CARNIVORE, 2)
        self.horns1 = TraitCard(HORNS, 1)
        self.scav_neg_1 = TraitCard(SCAVENGER, -1)
        self.scav3 = TraitCard(SCAVENGER, 3)
        self.forage1 = TraitCard(FORAGING, 1)
        self.carn0 = TraitCard(CARNIVORE, 0)
        self.warning0 = TraitCard(WARNING_CALL, 0)

        self.p1_hand = [self.long_neck0, self.horns0, self.fertile0, self.fat_tissue0, self.scav0, self.forage0]
        self.p2_hand = [self.carn2, self.horns0, self.fertile0, self.horns1, self.scav_neg_1, self.forage0]
        self.p3_hand = [self.carn0, self.horns0, self.warning0, self.horns0, self.scav3, self.forage1]

        self.coop = Species(2, 5, 6, [TraitCard(COOPERATION)])
        self.forage_coop = Species(2, 5, 3, [TraitCard(FORAGING), TraitCard(COOPERATION)])
        self.coop2 = Species(2, 5, 3, [TraitCard(COOPERATION)])
        self.fat_long_neck = Species(2, 5, 4, [TraitCard(FAT_TISSUE), TraitCard(LONG_NECK)], 4)
        self.fertile_long_neck = Species(2, 1, 6, [TraitCard(FERTILE), TraitCard(LONG_NECK)])

        self.player1 = PlayerState(1, 0, [self.coop, self.forage_coop, self.coop2], self.p1_hand)
        self.player2 = PlayerState(2, 0, [self.fat_long_neck], self.p2_hand)
        self.player3 = PlayerState(3, 0, [self.fertile_long_neck], self.p3_hand)

        self.dealer = Dealer([self.player1, self.player2, self.player3], 3, [self.trait1, self.trait2])
        self.dealer.add_silly_players()

        self.bt = BoardTrade(4, [0, 2, 3])
        self.rt = ReplaceTrait(2, 0, 5)
        self.gb = GrowBody(0, 0)
        self.gp = GrowPopulation(0, 1)
        self.bt2 = BoardTrade(1, [2])
        self.bt3 = BoardTrade(3, [4, 5])

        self.p1_actions = PlayerAction(1, [], [], [self.bt], [self.rt])
        self.p2_actions = PlayerAction(4, [self.gp], [self.gb], [], [])
        self.p3_actions = PlayerAction(0, [], [], [self.bt2, self.bt3], [])

        self.valid_actions = [self.p1_actions, self.p2_actions, self.p3_actions]

    def tearDown(self):
        del self.trait1
        del self.trait2
        del self.long_neck0
        del self.horns0
        del self.fertile0
        del self.fat_tissue0
        del self.scav0
        del self.forage0
        del self.carn2
        del self.horns1
        del self.scav_neg_1
        del self.scav3
        del self.forage1
        del self.carn0
        del self.warning0

        del self.p1_hand
        del self.p2_hand
        del self.p3_hand

        del self.coop
        del self.forage_coop
        del self.coop2
        del self.fat_long_neck
        del self.fertile_long_neck

        del self.player1
        del self.player2
        del self.player3

        del self.dealer

        del self.bt
        del self.rt
        del self.gb
        del self.gp
        del self.bt2
        del self.bt3

        del self.p1_actions
        del self.p2_actions
        del self.p3_actions

        del self.valid_actions

    def test_new(self):
        players = [Player(i) for i in range(1, 5)]

        dealer = Dealer.new(players)

        self.assertEquals(len(dealer.hand), 122)
        self.assertEquals(dealer.wateringHole, 0)
        self.assertEquals(len(dealer.playerStates), 4)

    def test_create_hand(self):
        hand = Dealer.create_hand()

        self.assertEquals(hand[0], TraitCard(AMBUSH, -3))
        self.assertEquals(hand[121], TraitCard(WARNING_CALL, 3))
        self.assertEquals(len(hand), 122)

        ambushes = 0
        for trait in hand:
            if trait.name == AMBUSH:
                ambushes += 1
        self.assertEquals(ambushes, 7)

        carnivores = 0
        for trait in hand:
            if trait.name == CARNIVORE:
                carnivores += 1
        self.assertEquals(carnivores, 17)

        warnings = 0
        for trait in hand:
            if trait.name == WARNING_CALL:
                warnings += 1
        self.assertEquals(warnings, 7)

        longs = 0
        for trait in hand:
            if trait.name == LONG_NECK:
                longs += 1
        self.assertEquals(longs, 7)

    def test_run_game(self):
        dealer = Dealer.new([Player(1), Player(2)])
        dealer.hand = []
        expected_dealer1 = copy.deepcopy(dealer)

        dealer.runGame()

        self.assertEquals(dealer, expected_dealer1)

        dealer.hand = [TraitCard(AMBUSH, -1), TraitCard(AMBUSH), TraitCard(AMBUSH, 1), TraitCard(BURROWING),
                       TraitCard(BURROWING, 3), TraitCard(CARNIVORE, -1), TraitCard(CLIMBING), TraitCard(CLIMBING, 2),
                       TraitCard(CLIMBING, 3), TraitCard(WARNING_CALL)]

        expected_player1_species = [Species(0, 0, 2, [TraitCard(AMBUSH, 1)])]
        expected_player2_species = [Species(0, 0, 1, [TraitCard(CLIMBING)])]
        expected_player1 = PlayerState(1, 2, expected_player1_species,
                                       [], Player(1))
        expected_player2 = PlayerState(2, 1, expected_player2_species,
                                       [TraitCard(CLIMBING, 3), TraitCard(WARNING_CALL)], Player(2))
        self.assertEquals(dealer.wateringHole, 0)
        dealer.runGame()
        self.assertEquals(dealer.playerStates[0].trait_cards, [TraitCard(CLIMBING, 3), TraitCard(WARNING_CALL)])
        self.assertEquals(dealer.playerStates[1].trait_cards, [])

        self.assertEquals(dealer.hand, [])
        self.assertEquals(dealer.playerStates[1].species[0].trait_cards, expected_player1_species[0].trait_cards)
        self.assertEquals(dealer.playerStates[0].species[0], expected_player2_species[0])
        self.assertEquals(dealer.wateringHole, 0)
        self.assertEquals(dealer.playerStates[1].foodbag, 2)
        self.assertEquals(dealer.playerStates[0].foodbag, 1)

        self.assertEquals(dealer.playerStates[1].species, expected_player1.species)
        self.assertEquals(dealer.playerStates[0].species, expected_player2.species)
        self.assertEquals(dealer.playerStates[1].trait_cards, expected_player1.trait_cards)
        self.assertEquals(dealer.playerStates[0].trait_cards, expected_player2.trait_cards)

        self.assertEquals(dealer.playerStates[1], expected_player1)

        self.assertEquals(dealer.playerStates, [expected_player2, expected_player1])

        exp_dealer2 = Dealer([expected_player2, expected_player1], 0, [])
        self.assertEquals(dealer, exp_dealer2)

        dealer3 = Dealer.new([Player(1), Player(1), Player(1), Player(1), Player(1), Player(1), Player(1), Player(1)])
        dealer3.runGame()
        dealer4 = Dealer.new([Player(1), Player(1), Player(1), Player(1)])
        dealer4.runGame()

    def test_cycle_players(self):
        dealer = Dealer.new([Player(1), Player(2), Player(3), Player(4), Player(5), Player(6), Player(7), Player(8)])
        dealer.cycle_players()
        self.assertEquals(dealer.playerStates[0].id, 2)
        self.assertEquals(dealer.playerStates[1].id, 3)
        self.assertEquals(dealer.playerStates[2].id, 4)
        self.assertEquals(dealer.playerStates[3].id, 5)
        self.assertEquals(dealer.playerStates[4].id, 6)
        self.assertEquals(dealer.playerStates[5].id, 7)
        self.assertEquals(dealer.playerStates[6].id, 8)
        self.assertEquals(dealer.playerStates[7].id, 1)


    def test_turn(self):
        dealer = Dealer.new([Player(1), Player(2), Player(3)])
        result_dealer = copy.deepcopy(dealer)
        result_dealer.hand = result_dealer.hand[24:]
        result_dealer.playerStates[0] = PlayerState(1, 0, [], [TraitCard(BURROWING, 2), TraitCard(BURROWING, 3),
                                                               TraitCard(CARNIVORE, -8), TraitCard(CARNIVORE, -7)])
        result_dealer.playerStates[1] = PlayerState(2, 0, [], [TraitCard(CARNIVORE, -6), TraitCard(CARNIVORE, -5),
                                                               TraitCard(CARNIVORE, -4), TraitCard(CARNIVORE, -3)])
        result_dealer.playerStates[2] = PlayerState(3, 0, [], [TraitCard(CARNIVORE, -2), TraitCard(CARNIVORE, -1),
                                                               TraitCard(CARNIVORE, 0), TraitCard(CARNIVORE, 1)])
        dealer.turn()
        self.assertEquals(dealer, result_dealer)

    def test_is_game_over(self):
        traits = [TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(WARNING_CALL), TraitCard(LONG_NECK),
                  TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(WARNING_CALL), TraitCard(LONG_NECK)]
        enough_traits = [TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(WARNING_CALL), TraitCard(LONG_NECK),
                         TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(WARNING_CALL), TraitCard(LONG_NECK),
                         TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(FERTILE), TraitCard(FERTILE, 3)]

        dealer = Dealer.new([Player(1), Player(2), Player(3)])

        dealer.hand = traits
        self.assertTrue(dealer.is_game_over())

        dealer.hand = enough_traits
        self.assertFalse(dealer.is_game_over())

    def test_step1(self):
        species1 = Species(3, 4, 5)
        species2 = Species(3, 3, 3)
        speciesList1 = [species1, species2]
        dealer_hand = [TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(WARNING_CALL), TraitCard(LONG_NECK),
                         TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(WARNING_CALL), TraitCard(LONG_NECK),
                         TraitCard(CARNIVORE), TraitCard(AMBUSH)]

        play_strat1 = Player(1)
        play_strat2 = Player(2)
        player1 = PlayerState(1, 0, [], [], play_strat1)
        player2 = PlayerState(2, 2, speciesList1, [], play_strat2)

        expected_player1 = copy.deepcopy(player1)
        expected_player1.species.append(Species(0, 0, 1))
        expected_player1.trait_cards = [TraitCard(AMBUSH), TraitCard(CARNIVORE),
                                        TraitCard(LONG_NECK), TraitCard(WARNING_CALL)]
        expected_player2 = copy.deepcopy(player2)
        expected_player2.trait_cards = [TraitCard(AMBUSH), TraitCard(CARNIVORE), TraitCard(CARNIVORE),
                                        TraitCard(LONG_NECK), TraitCard(WARNING_CALL)]

        dealer = Dealer([player1, player2], 4, dealer_hand)
        dealer.step1()

        self.assertEquals(player1.player_reference.playerState, expected_player1)
        self.assertEquals(player2.player_reference.playerState, expected_player2)
        self.assertEquals(dealer.hand, [TraitCard(AMBUSH)])

    def test_get_player_choices(self):
        species1 = Species(3, 4, 5)
        species2 = Species(3, 3, 3)
        speciesList1 = [species1, species2]
        traits = [TraitCard(AMBUSH, -2), TraitCard(CARNIVORE, -2), TraitCard(LONG_NECK, -2), TraitCard(WARNING_CALL, -2)]
        traits2 = [TraitCard(AMBUSH, -1), TraitCard(AMBUSH, 0), TraitCard(AMBUSH, 1), TraitCard(CARNIVORE, -1),
                   TraitCard(CARNIVORE), TraitCard(CARNIVORE, 1), TraitCard(LONG_NECK), TraitCard(LONG_NECK, 1),
                         TraitCard(WARNING_CALL), TraitCard(WARNING_CALL, 1)]

        play_strat1 = Player(1)
        play_strat2 = Player(2)
        player1 = PlayerState(1, 0, [], [], play_strat1)
        player2 = PlayerState(2, 2, speciesList1, traits, play_strat2)

        dealer = Dealer([player1, player2], 4, traits2)
        dealer.step1()
        play_act1 = PlayerAction(0, [GrowPopulation(1, 3)], [], [BoardTrade(1, [2])], [])
        play_act2 = PlayerAction(0, [GrowPopulation(2, 5)], [GrowBody(2, 2)], [BoardTrade(1, [4])],
                                    [ReplaceTrait(2, 0, 6)])

        choices = dealer.get_player_choices()
        self.assertEquals(choices, [play_act1, play_act2])

    def test_add_silly_players(self):
        species1 = Species(3, 4, 5)
        species2 = Species(3, 3, 3)
        species3 = Species(1, 2, 3)
        species4 = Species(1, 2, 3)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 4, [])
        dealer.add_silly_players()

        self.assertEquals(dealer.playerStates[0].player_reference.playerId, 1)
        self.assertEquals(dealer.playerStates[1].player_reference.playerId, 2)

    def test_step4(self):
        new_p1_hand = []
        new_p2_hand = [self.fertile0, self.horns1, self.forage0]
        new_p3_hand = []

        new_coop = Species(2, 5, 6, [TraitCard(COOPERATION)])
        new_forage_coop = Species(2, 5, 3, [TraitCard(FORAGING), TraitCard(COOPERATION)])
        new_coop2 = Species(2, 5, 3, [TraitCard(FORAGING)])
        added_spec = Species(1, 0, 2, [TraitCard(LONG_NECK), TraitCard(FERTILE), TraitCard(FAT_TISSUE)])
        new_fat_long_neck = Species(5, 6, 5, [TraitCard(FAT_TISSUE), TraitCard(LONG_NECK)], 2)
        new_fertile_long_neck = Species(2, 1, 7, [TraitCard(FERTILE), TraitCard(LONG_NECK)])
        added_warning = Species(0, 0, 1, [TraitCard(WARNING_CALL)])
        added_scav_forage = Species(0, 0, 1, [TraitCard(SCAVENGER, 3), TraitCard(FORAGING, 1)])

        new_player1 = PlayerState(1, 0, [new_coop, new_forage_coop, new_coop2, added_spec], new_p1_hand)
        new_player2 = PlayerState(2, 0, [new_fat_long_neck], new_p2_hand)
        new_player3 = PlayerState(3, 0, [new_fertile_long_neck, added_warning, added_scav_forage], new_p3_hand)

        new_dealer = Dealer([new_player1, new_player2, new_player3], 0, [self.trait1, self.trait2])

        self.dealer.step4(self.valid_actions)

        self.assertEquals(self.dealer, new_dealer)

    def test_end_turn(self):
        species1 = Species(3, 4, 5, [TraitCard(CARNIVORE)])
        species2 = Species(3, 3, 3)
        species3 = Species(0, 2, 3)
        species4 = Species(1, 2, 3)
        species5 = Species(0, 3, 3)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species4, species5]

        dealer_hand = [TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(WARNING_CALL)]

        player1 = PlayerState(1, 0, speciesList1, [], Player(1))
        player2 = PlayerState(2, 2, speciesList2, [], Player(2))

        new_player1 = copy.deepcopy(player1)
        new_player1.species = [Species(0, 4, 3, [TraitCard(CARNIVORE)]), Species(0, 3, 3)]
        new_player1.foodbag = 6
        new_player2 = copy.deepcopy(player2)
        new_player2.species = [Species(0, 2, 1)]
        new_player2.trait_cards = [TraitCard(CARNIVORE), TraitCard(AMBUSH), TraitCard(WARNING_CALL)]
        new_player2.foodbag = 3

        dealer = Dealer([player1, player2], 4, dealer_hand)
        new_dealer = copy.deepcopy(dealer)
        new_dealer.playerStates = [new_player1, new_player2]
        new_dealer.hand = []

        dealer.end_turn()

        self.assertEquals(dealer, new_dealer)

    def feeding(self):
        unchanged_dealer = copy.deepcopy(self.dealer)
        self.dealer.fullPlayerIds = [1, 2, 3]
        self.dealer.feeding()

        self.assertEquals(self.dealer, unchanged_dealer)

        self.dealer.fullPlayerIds = []
        self.dealer.wateringHole = 0
        unchanged_dealer.wateringHole = 0
        self.dealer.feeding()

        self.assertEquals(self.dealer, unchanged_dealer)

        self.dealer.fullPlayerIds = [1]
        self.dealer.wateringHole = 2
        self.dealer.feeding()

        new_fat_long_neck = Species(2, 5, 4, [TraitCard(FAT_TISSUE), TraitCard(LONG_NECK)], 5)
        new_fertile_long_neck = Species(3, 1, 6, [TraitCard(FERTILE), TraitCard(LONG_NECK)])
        changed_dealer = copy.deepcopy(self.dealer)
        changed_dealer.wateringHole = 0
        changed_dealer.playerStates[1].species[0] = new_fat_long_neck
        changed_dealer.playerStates[2].species[0] = new_fertile_long_neck

        self.assertEquals(self.dealer, changed_dealer)

    def testVegFeed1(self):
        species1 = Species(3, 4, 5)
        species2 = Species(3, 3, 3)
        species3 = Species(1, 2, 3)
        species4 = Species(1, 2, 3)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 4, [])
        self.assertEquals(dealer.playerStates[0].species[0].food, 3)
        dealer.feed1()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.wateringHole, 3)
        self.assertEquals(dealer.playerStates[0].id, 2)
        self.assertEquals(dealer.playerStates[1].species[0].food, 4)

    def testFatFoodFeed1(self):
        species1 = Species(3, 4, 5, [TraitCard(FAT_TISSUE)], 1)
        species2 = Species(3, 3, 3)
        species3 = Species(1, 4, 3, [TraitCard(FAT_TISSUE)], 0)
        species4 = Species(1, 2, 3)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 5, [])
        dealer.add_silly_players()
        self.assertEquals(dealer.wateringHole, 5)
        dealer.request_feed()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.wateringHole, 2)
        self.assertEquals(dealer.playerStates[1].species[0].fatFood, 4)
        dealer.request_feed()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.wateringHole, 0)
        self.assertEquals(dealer.playerStates[1].species[0].fatFood, 2)

    def testCarnivoreFeed1(self):
        species1 = Species(3, 4, 5, [TraitCard(CARNIVORE)], 1)
        species2 = Species(3, 3, 3)
        species3 = Species(1, 5, 4)
        species4 = Species(1, 2, 6)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 5, [])
        dealer.add_silly_players()
        self.assertEquals(dealer.wateringHole, 5)

        self.assertEquals(dealer.playerStates[0].species[0].food, 3)
        self.assertEquals(dealer.playerStates[1].species[1].population, 6)

        dealer.feed1()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.wateringHole, 4)
        self.assertEquals(dealer.playerStates[1].species[0].food, 4)
        self.assertEquals(dealer.playerStates[0].species[1].population, 5)

    def testCarnivoreFeed1_withHorns(self):
        species1 = Species(2, 4, 3, [TraitCard(CARNIVORE)])
        species2 = Species(0, 2, 1, [TraitCard(CARNIVORE)])

        species4 = Species(1, 2, 6, [TraitCard(HORNS)])
        speciesList1 = [species1, species2]
        speciesList2 = [species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 5, [])
        dealer.add_silly_players()
        self.assertEquals(dealer.wateringHole, 5)

        self.assertEquals(dealer.playerStates[0].species[0].food, 2) # carnivore
        self.assertEquals(dealer.playerStates[1].species[0].population, 6) # horns

        dealer.feed1() #carnivore attacks horns
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.wateringHole, 5)
        self.assertEquals(dealer.playerStates[1].species[0].food, 2) # carnivore
        self.assertEquals(dealer.playerStates[1].species[0].population, 2) # carnivore
        self.assertEquals(dealer.playerStates[0].species[0].population, 5) # horns

        dealer.feed1() #horns feeds
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.wateringHole, 4)
        self.assertEquals(dealer.playerStates[1].species[0].food, 2) # horns
        self.assertEquals(dealer.playerStates[1].species[0].population, 5) # horns
        self.assertEquals(dealer.playerStates[0].species[0].food, 2) # carnivore
        self.assertEquals(dealer.playerStates[0].species[0].population, 2) # carnivore

        self.assertEquals(len(dealer.playerStates[0].species), 2)
        dealer.feed1()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        # carnivore 2 went extinct
        self.assertEquals(len(dealer.playerStates[0].species), 1)

        self.assertEquals(dealer.wateringHole, 4)
        self.assertEquals(dealer.playerStates[1].species[0].population, 2) # carnivore
        self.assertEquals(dealer.playerStates[0].species[0].population, 4) # horns

    def test_feed_result_vegetarian(self):
        species1 = Species(3, 4, 5)
        species2 = Species(3, 3, 3)
        species3 = Species(1, 2, 3)
        species4 = Species(1, 2, 3)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 4, [])
        self.assertEquals(dealer.playerStates[0].species[0].food, 3)
        dealer.feed_result_vegetarian(0)
        self.assertEquals(dealer.wateringHole, 3)
        self.assertEquals(dealer.playerStates[1].id, 2)
        self.assertEquals(dealer.playerStates[0].species[0].food, 4)

    def test_feed_result_fat_food(self):
        species1 = Species(3, 4, 5, [TraitCard(FAT_TISSUE)], 1)
        species2 = Species(3, 3, 3)
        species3 = Species(1, 4, 3, [TraitCard(FAT_TISSUE)], 0)
        species4 = Species(1, 2, 3)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 5, [])
        dealer.add_silly_players()
        self.assertEquals(dealer.wateringHole, 5)
        dealer.feed_result_fat_food(0, 4)
        self.assertEquals(dealer.wateringHole, 2)
        self.assertEquals(dealer.playerStates[0].species[0].fatFood, 4)

        # Requesting too much fat food, catch this exception in feeding cycle and throw player out
        with self.assertRaises(Exception):
            dealer.feed_result_fat_food(1, 2)

        self.assertEquals(dealer.wateringHole, 2)
        self.assertEquals(dealer.playerStates[0].species[1].fatFood, 0)

    def testfeed_result_carnivore(self):
        species1 = Species(1, 4, 2, [TraitCard(CARNIVORE)], 1)
        species4 = Species(1, 2, 6, [TraitCard(HORNS)])
        speciesList1 = [species1]
        speciesList2 = [species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 5, [])
        self.assertEquals(dealer.wateringHole, 5)

        self.assertEquals(dealer.playerStates[0].species[0].food, 1) # carnivore
        self.assertEquals(dealer.playerStates[1].species[0].population, 6) # horns

        dealer.feed_result_carnivore(0, 1, 0) #carnivore attacks horns
        self.assertEquals(dealer.wateringHole, 5)
        self.assertEquals(dealer.playerStates[0].species[0].food, 1) # carnivore
        self.assertEquals(dealer.playerStates[0].species[0].population, 1) # carnivore
        self.assertEquals(dealer.playerStates[1].species[0].population, 5) # horns

        dealer.feed_result_carnivore(0, 1, 0) #carnivore attacks horns
        self.assertEquals(dealer.wateringHole, 5)
        self.assertEquals(len(dealer.playerStates[0].species), 0)
        self.assertEquals(len(dealer.playerStates[1].species), 1)
        self.assertTrue(dealer.playerStates[1].species[0].hasTrait(HORNS))

    def test_execute_attack(self):
        carnivore1 = Species(1, 4, 3, [TraitCard(CARNIVORE)], 1)
        horns1 = Species(1, 2, 6, [TraitCard(HORNS)])
        carnivore2 = Species(1, 4, 1, [TraitCard(CARNIVORE)], 1)
        horns2 = Species(1, 2, 1, [TraitCard(HORNS)])

        player1carn = PlayerState(1, 0, [carnivore1], [])
        player2horn = PlayerState(2, 2, [horns1], [])
        player3carn = PlayerState(3, 3, [carnivore2])
        player4horn = PlayerState(4, 4, [horns2])

        traits = [TraitCard(CARNIVORE), TraitCard(SCAVENGER), TraitCard(LONG_NECK)]

        dealer = Dealer([player1carn, player2horn], 5, traits)
        self.assertEquals(dealer.wateringHole, 5)

        self.assertEquals(dealer.playerStates[0].species[0].food, 1) # carnivore
        self.assertEquals(dealer.playerStates[1].species[0].population, 6) # horns
        self.assertEquals(dealer.hand, traits)

        dealer.execute_attack(carnivore1, horns1, player1carn, player2horn, 0, 0) #carnivore attacks horns
        self.assertEquals(dealer.wateringHole, 4)
        self.assertEquals(carnivore1.food, 2) # carnivore
        self.assertEquals(carnivore1.population, 2) # carnivore
        self.assertEquals(horns1.population, 5) # horns
        self.assertEquals(carnivore2.food, 1) # carnivore
        self.assertEquals(horns2.population, 1) # horns


        # tests below show species going extinct
        dealer2 = Dealer([player3carn, player4horn], 5, traits)
        self.assertEquals(dealer2.hand, traits)

        self.assertEquals(dealer2.wateringHole, 5)
        self.assertEquals(len(player3carn.species), 1)
        self.assertEquals(len(player4horn.species), 1)
        self.assertEquals(dealer2.hand, [TraitCard(CARNIVORE), TraitCard(SCAVENGER), TraitCard(LONG_NECK)])
        self.assertEquals(player4horn.trait_cards, [])
        self.assertEquals(player3carn.trait_cards, [])

        dealer2.execute_attack(carnivore2, horns2, player3carn, player4horn, 0, 0) #both die

        self.assertEquals(dealer2.wateringHole, 5)
        self.assertEquals(len(player3carn.species), 0)
        self.assertEquals(len(player4horn.species), 0)
        self.assertEquals(dealer2.hand, [])
        self.assertEquals(player4horn.trait_cards, [TraitCard(CARNIVORE), TraitCard(SCAVENGER)])
        self.assertEquals(player3carn.trait_cards, [TraitCard(LONG_NECK)])

    def testFeedAllSpeciesWithTrait(self):
        # Species(food, body, population, traits, fatfood)
        species1 = Species(3, 4, 5, [TraitCard(SCAVENGER)]) # will feed
        species2 = Species(3, 3, 3, [TraitCard(SCAVENGER)]) # won't feed
        species3 = Species(1, 5, 4, [TraitCard(SCAVENGER), TraitCard(FORAGING)]) # will feed
        species4 = Species(1, 2, 6, [TraitCard(SCAVENGER)]) # can't feed (watering hole empty)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 3, [])

        self.assertEquals(species1.food, 3)
        self.assertEquals(species2.food, 3)
        self.assertEquals(species3.food, 1)
        self.assertEquals(species4.food, 1)
        self.assertEquals(dealer.wateringHole, 3)

        dealer.feed_all_species_with_trait(SCAVENGER)
        self.assertEquals(species1.food, 4)
        self.assertEquals(species2.food, 3)
        self.assertEquals(species3.food, 3)
        self.assertEquals(species4.food, 1)
        self.assertEquals(dealer.wateringHole, 0)

    def test_add_fertile_populations(self):
        # Species(food, body, population, traits, fatfood)
        fertile1 = Species(3, 4, 5, [TraitCard(FERTILE)]) # will feed
        scavenger = Species(3, 3, 3, [TraitCard(SCAVENGER)]) # won't feed
        fertile2 = Species(1, 5, 4, [TraitCard(FERTILE), TraitCard(FORAGING)]) # will feed
        fertile3 = Species(1, 2, 7, [TraitCard(FERTILE)]) # can't feed (watering hole empty)
        speciesList1 = [fertile1, scavenger]
        speciesList2 = [fertile2, fertile3]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 3, [])

        dealer.add_fertile_populations()

        self.assertEquals(fertile1, Species(3, 4, 6, [TraitCard(FERTILE)]))
        self.assertEquals(scavenger, Species(3, 3, 3, [TraitCard(SCAVENGER)]))
        self.assertEquals(fertile2, Species(1, 5, 5, [TraitCard(FERTILE), TraitCard(FORAGING)]))
        self.assertEquals(fertile3, Species(1, 2, 7, [TraitCard(FERTILE)]))

    def test_transfer_fat_food(self):
        fat1 = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 3)
        empty_fat = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        fat2 = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 6)
        non_fat = Species(2, 3, 4)
        non_fat2 = Species(1, 1, 4, [TraitCard(CARNIVORE), TraitCard(FERTILE)])

        new_fat1 = Species(5, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        new_empty_fat = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        new_fat2 = Species(7, 5, 7, [TraitCard(FAT_TISSUE)], 1)
        new_non_fat = Species(2, 3, 4)
        new_non_fat2 = Species(1, 1, 4, [TraitCard(CARNIVORE), TraitCard(FERTILE)])

        player1 = PlayerState(1, 2, [fat1, non_fat, empty_fat])
        player2 = PlayerState(2, 5, [fat2])
        player3 = PlayerState(3, 4, [non_fat2])
        new_player1 = PlayerState(1, 2, [new_fat1, new_non_fat, new_empty_fat])
        new_player2 = PlayerState(2, 5, [new_fat2])
        new_player3 = PlayerState(3, 4, [new_non_fat2])

        dealer = Dealer([player1, player2, player3], 100, [])
        dealer.transfer_fat_food()
        new_dealer = Dealer([new_player1, new_player2, new_player3], 100, [])

        self.assertEquals(player1, new_player1)
        self.assertEquals(player2, new_player2)
        self.assertEquals(player3, new_player3)
        self.assertEquals(dealer, new_dealer)

    def testForagingFeed(self):
        # Species(food, body, population, traits, fatfood)
        species1 = Species(3, 4, 5, [TraitCard(FORAGING)])
        species2 = Species(3, 3, 5, [TraitCard(FORAGING)])
        species3 = Species(3, 5, 4, [TraitCard(FORAGING)])
        speciesList1 = [species1, species2]
        speciesList2 = [species3]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 4, [])
        dealer.add_silly_players()
        self.assertEquals(dealer.wateringHole, 4)
        dealer.feed1()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.wateringHole, 2)
        self.assertEquals(dealer.playerStates[1].species[0].food, 5)

        dealer.feed1()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.wateringHole, 1)
        self.assertEquals(dealer.playerStates[1].species[0].food, 4)

        dealer.feed1()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(dealer.playerStates[1].species[1].food, 4)

    def testFeedFromWateringHole(self):
        # Species(food, body, population, traits, fatfood)
        species1 = Species(5, 4, 5, [TraitCard(FORAGING)])
        species2 = Species(3, 3, 5, [TraitCard(FORAGING)])
        species3 = Species(3, 5, 4, [TraitCard(FORAGING)])
        species4 = Species(3, 5, 5, [TraitCard(FORAGING)])
        speciesList1 = [species1, species2, species3, species4]

        player1 = PlayerState(1, 0, speciesList1, [])

        dealer = Dealer([player1], 4, [])

        dealer.feedFromWateringHole(0, 0)

        self.assertEquals(dealer.playerStates[0].species[0].food, 5)
        self.assertEquals(dealer.wateringHole, 4)

        dealer.feedFromWateringHole(0, 1)

        self.assertEquals(dealer.playerStates[0].species[1].food, 5)
        self.assertEquals(dealer.wateringHole, 2)

        dealer.feedFromWateringHole(0, 2)

        self.assertEquals(dealer.playerStates[0].species[2].food, 4)
        self.assertEquals(dealer.wateringHole, 1)

        dealer.feedFromWateringHole(0, 3)

        self.assertEquals(dealer.playerStates[0].species[3].food, 4)
        self.assertEquals(dealer.wateringHole, 0)

    def testDoneFeeding(self):
        species1 = Species(5, 4, 5)
        species2 = Species(3, 3, 3)
        species3 = Species(4, 5, 4)
        speciesList1 = [species1, species2]
        speciesList2 = [species3]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])

        dealer = Dealer([player1, player2], 4, [])

        dealer.feed1()
        dealer.playerStates.append(dealer.playerStates.pop(0))
        self.assertEquals(len(dealer.fullPlayerIds), 1)
        self.assertEquals(dealer.fullPlayerIds[0], 1)

    def testAutoFeed(self):
        species1 = Species(5, 4, 5)
        species2 = Species(3, 3, 3)
        species3 = Species(3, 5, 4)
        species3a = Species(1, 5, 4)
        species4 = Species(4, 3, 4, [TraitCard("fat-tissue", 0)], 3)
        species5 = Species(4, 3 ,4, [TraitCard("fat-tissue", 0)], 1)
        carn1 = Species(3, 2, 4, [TraitCard("carnivore")])
        carn2 = Species(4, 2, 5, [TraitCard("carnivore"), TraitCard("climbing")])
        attackable = Species(3, 3, 5)
        speciesList1 = [species1, species2]
        speciesList2 = [species3, species3a]
        carnList1 = [carn1]
        carnList2 = [carn2, attackable]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, speciesList2, [])
        player3 = PlayerState(3, 3, [species4, species5], [])
        player4 = PlayerState(4, 4, [species3], [])
        player5 = PlayerState(5, 5, carnList1)
        player6 = PlayerState(6, 5, carnList2)

        dealer1 = Dealer([player1, player2], 4, [])
        dealer2 = Dealer([player2], 4, [])
        dealer3 = Dealer([player3], 3, [])
        dealer4 = Dealer([player4], 3, [])
        dealer5 = Dealer([player5, player6], 6, [])

        unchanged_player1 = copy.deepcopy(player1)
        unchanged_player2 = copy.deepcopy(player2)
        self.assertTrue(dealer1.auto_feed())
        self.assertEquals(dealer1.fullPlayerIds, [1])
        self.assertEquals(unchanged_player1, player1)
        self.assertEquals(unchanged_player2, player2)

        unchanged_species4 = copy.deepcopy(species4)
        self.assertFalse(dealer3.auto_feed())
        self.assertEquals(species5.fatFood, 1)
        self.assertEquals(unchanged_species4, species4)

        self.assertFalse(dealer2.auto_feed())
        self.assertEquals(species3.food, 3)
        self.assertEquals(species3a.food, 1)

        self.assertTrue(dealer4.auto_feed())
        self.assertEquals(species3.food, 4)

        # no autofeeding on carnivores
        self.assertEquals(carn1.food, 3)
        unchanged_carn2 = copy.deepcopy(carn2)
        self.assertFalse(dealer5.auto_feed())
        self.assertEquals(carn1.food, 3)
        self.assertEquals(unchanged_carn2, carn2)
        self.assertEquals(attackable.population, 5)

    def test_auto_feed_one_hungry(self):
        carn1 = Species(3, 2, 4, [TraitCard("carnivore")])
        full_fat = Species(4, 3, 4, [TraitCard("fat-tissue", 0)], 3)
        veg1 = Species(5, 4, 5)
        veg2 = Species(3, 3, 4)

        player1 = PlayerState(1, 3, [full_fat, carn1])
        attackable_player1 = PlayerState(2, 3, [veg1])
        attackable_player2 = PlayerState(3, 4, [veg2])

        dealer1 = Dealer([player1, attackable_player1], 3, [])
        dealer2 = Dealer([player1], 3, [])
        dealer3 = Dealer([player1, attackable_player1, attackable_player2], 5, [])
        dealer4 = Dealer([attackable_player2], 4, [])

        unchanged_full_fat = copy.deepcopy(full_fat)
        self.assertEquals(carn1.food, 3)
        self.assertEquals(carn1.population, 4)
        self.assertEquals(carn1.body, 2)
        self.assertEquals(veg1.food, 5)
        self.assertEquals(veg1.population, 5)
        self.assertEquals(veg1.body, 4)

        # contains player who has carnivore, no autofeed
        self.assertFalse(dealer1.auto_feed_one_hungry(1))

        self.assertEquals(unchanged_full_fat, full_fat)
        self.assertEquals(carn1.food, 3)
        self.assertEquals(carn1.population, 4)
        self.assertEquals(carn1.body, 2)
        self.assertEquals(veg1.food, 5)
        self.assertEquals(veg1.population, 5)
        self.assertEquals(veg1.body, 4)

        unchanged_dealer2 = copy.deepcopy(dealer2)
        self.assertFalse(dealer2.auto_feed_one_hungry(1))
        self.assertEquals(unchanged_dealer2, dealer2)

        unchanged_dealer3 = copy.deepcopy(dealer3)
        self.assertFalse(dealer3.auto_feed_one_hungry(1))
        self.assertEquals(unchanged_dealer3, dealer3)

        changed_veg = copy.deepcopy(veg2)
        changed_veg.food += 1
        self.assertTrue(dealer4.auto_feed_one_hungry(0))
        self.assertEquals(changed_veg, veg2)

    def test_get_hungry_and_fat_tissue_lists(self):
        species1 = Species(5, 4, 5)
        species2 = Species(3, 3, 3)
        species3 = Species(3, 5, 4)
        species4 = Species(3, 3, 4, [TraitCard("fat-tissue", 0)], 3)
        species5 = Species(3, 3 ,4, [TraitCard("fat-tissue", 0)], 1)
        speciesList1 = [species1, species2, species3, species4, species5]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, [species1, species1, species2])

        dealer1 = Dealer([player1], 4, [])
        dealer2 = Dealer([player2], 3, [])

        self.assertEquals(dealer1.get_hungry_and_fat_tissue_lists(), ([2, 3, 4], [4]))
        self.assertEquals(dealer2.get_hungry_and_fat_tissue_lists(), ([], []))

    def test_deal_x_cards(self):
        species1 = Species(5, 4, 5)
        species2 = Species(3, 3, 3)
        species3 = Species(3, 5, 4)
        species4 = Species(3, 3, 4, [TraitCard("fat-tissue", 0)], 3)
        species5 = Species(3, 3 ,4, [TraitCard("fat-tissue", 0)], 1)
        speciesList1 = [species1, species2, species3, species4, species5]

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 2, [species1, species1, species2])

        dealer1 = Dealer([player1], 4, [TraitCard(CARNIVORE), TraitCard(SCAVENGER), TraitCard(LONG_NECK)])

        self.assertEquals(len(dealer1.hand), 3)

        dealer1.deal_x_cards(player1, 2)

        self.assertEquals(len(dealer1.hand), 1)
        self.assertEquals(player1.trait_cards, [TraitCard(CARNIVORE), TraitCard(SCAVENGER)])
        self.assertEquals(len(player2.trait_cards), 0)
        self.assertEquals(dealer1.hand, [TraitCard(LONG_NECK)])

        dealer1.deal_x_cards(player2, 2)

        self.assertEquals(len(dealer1.hand), 0)
        self.assertEquals(player2.trait_cards, [TraitCard(LONG_NECK)])
        self.assertEquals(len(player1.trait_cards), 2)
        self.assertEquals(dealer1.hand, [])

    def test_remove_cheater(self):
        player1 = PlayerState(1, 0, [])
        player2 = PlayerState(2, 2, [])

        dealer1 = Dealer([player1, player2], 4, [TraitCard(CARNIVORE), TraitCard(SCAVENGER), TraitCard(LONG_NECK)])
        new_dealer1 = Dealer([player1], 4, [TraitCard(CARNIVORE), TraitCard(SCAVENGER), TraitCard(LONG_NECK)])
        dealer1.fullPlayerIds = [1, 2]
        dealer1.add_silly_players()

        self.assertEquals(dealer1.fullPlayerIds, [1, 2])
        dealer1.remove_cheater(1)

        self.assertEquals(dealer1, new_dealer1)
        self.assertEquals(dealer1.fullPlayerIds, [1])

    def test_remove_players_at_indices(self):
        player1 = PlayerState(1, 0, [])
        player2 = PlayerState(2, 2, [])
        player3 = PlayerState(3, 1, [])

        dealer1 = Dealer([player1, player2, player3], 4, [TraitCard(CARNIVORE), TraitCard(SCAVENGER), TraitCard(LONG_NECK)])
        new_dealer1 = Dealer([player2], 4, [TraitCard(CARNIVORE), TraitCard(SCAVENGER), TraitCard(LONG_NECK)])
        dealer1.fullPlayerIds = [1, 2, 3]
        dealer1.add_silly_players()
        self.assertEquals(len(dealer1.originalPlayerOrder), 3)
        self.assertEquals(dealer1.fullPlayerIds, [1, 2, 3])

        dealer1.remove_players_at_indices([0, 2])

        self.assertEquals(dealer1, new_dealer1)
        self.assertEquals(dealer1.fullPlayerIds, [2])
        self.assertEquals(len(dealer1.originalPlayerOrder), 1)

    def test_remove_id_from_original_player_order(self):
        player1 = PlayerState(1, 0, [])
        player2 = PlayerState(2, 2, [])
        player3 = PlayerState(1, 1, [])

        dealer1 = Dealer([player1, player2, player3], 4, [TraitCard(CARNIVORE), TraitCard(SCAVENGER), TraitCard(LONG_NECK)])
        dealer1.add_silly_players()
        dealer1.fullPlayerIds = [1, 2, 3]

        dealer1.remove_id_from_original_player_order(1)

        self.assertEquals(dealer1.originalPlayerOrder, [player2, player3])
        self.assertEquals(dealer1.fullPlayerIds, [1, 2, 3])



    # JSON Configuration
    input1 = [
          [
            [["id", 1], ["species", []], ["bag", 0]],
            [["id", 2], ["species", []], ["bag", 0]],
            [["id", 3], ["species", [[["food", 6],
                                       ["body", 5],
                                       ["population", 6],
                                       ["traits", ["fat-tissue"]]]]],
              ["bag", 0]]
          ],
          2,
          [
            [4, "carnivore"],
            [3, "scavenger"]
          ]
        ]

    def testCreateDealerFromJson(self):

        dealer = Dealer.create_dealer_from_configuration(self.input1)
        self.assertEquals(len(dealer.playerStates[0].species), 0)
        self.assertEquals(len(dealer.playerStates[1].species), 0)
        self.assertEquals(len(dealer.playerStates[2].species), 1)
        self.assertEquals(dealer.playerStates[2].species[0].food, 6)
        self.assertEquals(dealer.playerStates[2].species[0].trait_cards[0].name, "fat-tissue")

    def testCreateJsonFromDealer(self):

        species1 = Species(6, 5, 6, [TraitCard("fat-tissue")])
        speciesList1 = []
        speciesList2 = []
        speciesList3 = [species1]

        trait1 = TraitCard("carnivore", 4)
        trait2 = TraitCard("scavenger", 3)

        player1 = PlayerState(1, 0, speciesList1, [])
        player2 = PlayerState(2, 0, speciesList2, [])
        player3 = PlayerState(3, 0, speciesList3, [])

        dealer = Dealer([player1, player2, player3], 2, [trait1, trait2])

        json_dealer = dealer.create_json_from_dealer()

        self.assertEquals(json_dealer, self.input1)

    def test_get_hand(self):
        json_hand = [[4, "carnivore"], [3, "scavenger"], [3, "long-neck"], [3, "scavenger"]]
        traits = [TraitCard(CARNIVORE, 4), TraitCard(SCAVENGER, 3), TraitCard(LONG_NECK, 3), TraitCard(SCAVENGER, 3)]

        self.assertEquals(Dealer.get_hand(json_hand), traits)

    def test_validate_hand(self):
        veg_dict = {"scavenger": MAX_OTHER_TRAITS + 1}
        with self.assertRaises(Exception):
            Dealer.validate_hand(veg_dict)

        carn_dict = {"carnivore": MAX_CARNIVORE_TRAITS + 1}
        with self.assertRaises(Exception):
            Dealer.validate_hand(carn_dict)

        Dealer.validate_hand({"carnivore": 4, "scavenger": 5})

    # ************** Dealer.parse_step4 tests are in PlayerActionTests ********************

if __name__ == "__main__":
    unittest.main()