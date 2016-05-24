#!/usr/bin/env python2.7

from species import Species
from playerState import PlayerState
from constants import *
import sys, os
import copy
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dealer'))
from playerAction import PlayerAction
from growBody import GrowBody
from growPopulation import GrowPopulation
from boardTrade import BoardTrade
from replaceTrait import ReplaceTrait
from feedAction import FeedAction


class Player:

    def __init__(self, id_in=1):
        """
        Creates a new player with the given ID number
        :param id_in: Nat+ (greater than 0)
        :return: Player with given ID
        """
        self.playerId = id_in
        self.playerState = PlayerState(1)
        self.info = str(id_in)

    def __eq__(self, that):
        """
        This is the equals method that determines if the inputted 'that' object is equal to this Player
        :param that: Any (object)
        :return: Boolean (true if equal, false otherwise)
        """
        if isinstance(that, Player):
            return self.playerId == that.playerId
        else:
            return False

    @staticmethod
    def new(id):
        """
        Given an id, create and return a player object
        :param id: Nat - Player's id
        :return: Player with given id
        """
        return Player(id)

    def start(self, playerState, watering_hole):
        """
        Effect: Takes in this player's current playerState to be stored in self.playerState
        :param playerState: PlayerState - Current state of this player
        :param watering_hole: Nat - the state of the watering hole of the dealer
        :return: Void
        """
        self.storeCurrentPlayerState(playerState)

    def choose(self, prev_species, later_species):
        """
        Chooses card actions, first by trading the first card to wateringHole, then next two cards for a new speices w/
        trait, then any remaining cards go to population, then body, then replace the trait of the new species.
        Effect: modifies this player's knowledge of it's playerState's trait cards
        :param prev_species: The species who's players that have turns before this player
        :param later_species: The species who's players that have turns after this player
        :return: PlayerAction - chosen by the player for trading cards
        """
        traits = self.playerState.trait_cards
        actions = []

        for i in range(len(traits)):
            actions.append(self.find_card_in_trait_list(traits[i], self.unsorted))

        new_species_index = len(self.playerState.species)
        resultAction = PlayerAction(actions[0], [], [], [BoardTrade(actions[1], [actions[2]])], [])
        self.playerState.trait_cards = self.playerState.trait_cards[3:]

        if len(actions) > 3:
            resultAction.gp_list = [GrowPopulation(new_species_index, actions[3])]
            self.playerState.trait_cards.pop(0)
        if len(actions) > 4:
            resultAction.gb_list = [GrowBody(new_species_index, actions[4])]
            self.playerState.trait_cards.pop(0)
        if len(actions) > 5:
            resultAction.rt_list = [ReplaceTrait(new_species_index, 0, actions[5])]
            self.playerState.trait_cards.pop(0)

        return resultAction

    def sortSpecies(self, list_of_species, removeFed=False):
        """
        Sorts a list of species from largest to smallest based on population, then food, then body
        :param list_of_species: the list of Tuples(Nat, Species) to sort. Nat is the preserved index of Species.
        :param removeFed: (optional). If True, does not return 'full' (not hungry) species in the list
        :return: List of Tuples (Nat (original index), Species)
        """
        unsorted_list = []
        if removeFed:
            for i, s in list_of_species:
                if s.isHungry() or (s.body > s.fatFood and s.hasTrait(FAT_TISSUE)):
                    unsorted_list.append((i, s))
        else:
            unsorted_list = list_of_species
        sorted_list = sorted(unsorted_list, key=lambda x: (x[1].population, x[1].food, x[1].body), reverse=True)

        return sorted_list

    def getFatTissueSpecies(self, species_list, wateringHole):
        """
        Finds the largest 'needy' fat-tissue species in the species_list. Returns False if there are none.
        :param species_list: List of Tuple (Nat (original species index), Species) - Species are in decreasing order
        :param wateringHole: Nat - the value in the watering hole
        :return: [Nat (Index of the Neediest Species) , Nat (Need)] or False
        """
        fatTissueSpecies = False
        speciesIndex = -1
        largestNeed = 0

        for i, animal in species_list:
            if animal.hasTrait(FAT_TISSUE) and animal.body > animal.fatFood:
                thisNeed = animal.getFatRoom()
                if thisNeed > largestNeed:
                    fatTissueSpecies = True
                    speciesIndex = i
                    largestNeed = thisNeed

        currentNeed = min(wateringHole, largestNeed)

        return fatTissueSpecies and [speciesIndex, currentNeed]

    def getVegetarian(self, species):
        """
        Retrieves the first hungry vegetarian species from a sorted (largest to smallest) species list
        :param species: ListOf(Tuple(Nat (index of the Species), Species))
        :return: Nat - the Index of the Species
        """
        for index, animal in species:
            if not animal.hasTrait(CARNIVORE) and animal.isHungry():
                return index

        raise Exception("This function should not be called if there are no hungry vegetarians")

    def hasHungryVegetarian(self, species_list):
        """
        Is there a hungry vegetarian in this species_list?
        :param species: ListOf(Tuple(Nat (index of the Species), Species))
        :return: True if there is a hungry veg in this species_list
        """
        for index, animal in species_list:
            if not animal.hasTrait(CARNIVORE) and animal.isHungry():
                return True

        return False

    def getCarnivoreAttack(self, species_list, otherPlayers):
        """
        Finds indexes of largest carnivore to attack, player to attack, largest species to attack (of player to attack)
        :param species_list: ListOf(Tuple(Nat (index of species), Species)) species of this player
        :param otherPlayers: List of PlayerStates
        :return: [Index of Attacking Species, Index of Defending Player, Index of Defending Species] or False
        """
        max_def_spec = False
        for attacking_spec_index, animal in self.get_carnivores(species_list):

            for def_play_index in range(len(otherPlayers)):
                defender = otherPlayers[def_play_index]
                for def_spec_index in range(len(defender.species)):

                    larger_attack_option = self.is_larger_attack_option(defender, def_spec_index, animal, max_def_spec)
                    if larger_attack_option:

                        preyIndex, max_def_spec = larger_attack_option
                        defPlayerIndex = def_play_index
                        carnIndex = attacking_spec_index

            if max_def_spec:
                return [carnIndex, defPlayerIndex, preyIndex]

        return False

    def get_carnivores(self, species_tup_list):
        """
        Returns a list of Tuples containing only carnivore Species
        :param species_tup_list: List of Tuple (Nat, Species) - the list of Indices with the Species
        :return: List of Tuple(Nat, Species) - Only Carnivore species from the input, with their original indices
        """
        return [spec_tup for spec_tup in species_tup_list if spec_tup[1].hasTrait(CARNIVORE)]

    def is_larger_attack_option(self, defend_player, def_spec_index, attacker, largest_def_species):
        """
        Checks if the attacker -> def_species_index is a larger attack option than attacker -> largest_def_species
        :param defend_player: PlayerState - the defending playerState containing the defending species to compare
        :param def_spec_index: Nat - the index of the species to compare against largest_def_species
        :param attacker: Species - the attacking species
        :param largest_def_species: Species - the current largest defending species to compare against
        :return: One of: - Tuple(Nat, Species) - the new larger option found
                         - False (if not a larger option)
        """
        lNeighbor, rNeighbor = defend_player.get_neighbors(def_spec_index)

        def_species = defend_player.species[def_spec_index]

        if Species.isAttackable(def_species, attacker, lNeighbor, rNeighbor) and def_species.isLarger(largest_def_species):
            return def_spec_index, defend_player.species[def_spec_index]
        return False

    def feedNext(self, curState, wateringHole, otherPlayers):
        """
        Takes in a PlayerState, wateringHole, and a list of other player states, and
        this player decides which species in it's playerState to feed, based on if
        it has fatTissue, an attacking carnivore, or a hungry vegetarian.
        :param curState: PlayerState - the current player's PlayerState
        :param wateringHole: Nat - number of food in the wateringhole (> 0)
        :param otherPlayers: List of PlayerState - The other players in the game
        :return: FeedAction - the feeding choices of the player
        """
        result = False
        otherPlayers = [PlayerState(speciesList=species) for species in otherPlayers]
        speciesWithIndices = self.pair_species_with_index(curState.species)
        self.storeCurrentPlayerState(curState)

        species = self.sortSpecies(speciesWithIndices, removeFed=True)  # sorted by largeness
        if not species:
            raise Exception("This player has no hungry species")

        elif self.getFatTissueSpecies(species, wateringHole):
            result = self.getFatTissueSpecies(species, wateringHole)

        elif self.hasHungryVegetarian(species):
            result = self.getVegetarian(species)

        elif self.getCarnivoreAttack(species, otherPlayers):
            result = self.getCarnivoreAttack(species, otherPlayers)

        return FeedAction.parse_food_action(result)

    def pair_species_with_index(self, species_list):
        """
        Creates a tuple for each element of species_list, pairing it's index in the list with the species
        :param species_list: listOf(Species) - The species list to given indices to
        :return: listOf((Nat, Species)) - Tuples of form: (index, species)
        """
        return [(i, species_list[i]) for i in range(len(species_list))]

    def storeCurrentPlayerState(self, playerState):
        """
        Effect: This player's playerState field is now the given playerState
        Call this to store the current playerState whenever it is handed to us by the dealer
        :param playerState: a PlayerState to store
        """
        self.playerState = playerState
        self.unsorted = copy.deepcopy(self.playerState.trait_cards)
        self.playerState.trait_cards = sorted(self.playerState.trait_cards, key=lambda x: (x.name, x.food))

    def find_card_in_trait_list(self, card, cards):
        """
        Find and return the index of a card in cards. card must be in cards for this function to work
        :param card: A TraitCards to find
        :param cards: A listOf(TraitCard) to search through
        :return: The index of card in cards
        """
        for i in range(len(cards)):
            if card == cards[i]:
                return i

    def exit_game(self):
        """
        Used for testing purposes, as a substitute for when an external player should get removed
        :return:
        """
        return

    @staticmethod
    def parse_choice(choice):
        """
        Parse a choice into a [PlayerState, listOf(Species), listOf(Species]
        :param choice: json list representing [playerstate, listof species, listof species]
        :return: [PlayerState, listOf(Species), listOf(Species)]
        """
        ps = PlayerState.convertPlayerState(choice[0])
        prev_species = [Species.convertSpecies(species) for species in [prev for prev in choice[1]]]
        later_species = [Species.convertSpecies(species) for species in [late for late in choice[2]]]

        return [ps, prev_species, later_species]

    @staticmethod
    def parse_cj_dj(json_cj_dj):
        """
        Parse a json cj_dj into a [listOf(listOf(Species)), listOf(listOf(Species))]
        :param json_cj_dj: json list representing [listof species, listof species]
                        - First list of species is each specieslist of all players acting before this player
                        - Second list of species is each specieslist of all players who's turns come after this player
        :return: (listOf(Species), listOf(Species))
        """
        prev_species, later_species = [], []
        for prev in json_cj_dj[0]:
            prev_species.append([Species.convertSpecies(species) for species in prev])
        for later in json_cj_dj[1]:
            later_species.append([Species.convertSpecies(species) for species in later])
        return prev_species, later_species
