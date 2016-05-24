#!/usr/bin/env python2.7
import copy
from species import Species
from traitCard import TraitCard
from constants import *
import numpy


class PlayerState:

    def __init__(self, id=0, bag=0, speciesList=None, trait_cards=None, player_reference=None, info=""):
        """
        Creates a new PlayerState with the given player attributes
        :param id: Nat - the id for the player state (default 0)
        :param bag: Nat - the food contained in the bag (default 0)
        :param speciesList: List of Species (see species.py) (default None)
        :param trait_cards: List of TraitCards (see traitCard.py) (default None)
        :param player_reference: An external player reference that implements external player API for strategy
        :return: PlayerState with populated attributes
        """
        self.id = id
        self.foodbag = bag
        self.species = speciesList or []
        self.trait_cards = trait_cards or []
        self.watering_hole = 0
        self.player_reference = player_reference
        self.info = info

    def __eq__(self, that):
        """
        This is the equals method that determines if the inputted 'that' object is equal to this PlayerState
        :param that: Any (object)
        :return: Boolean (true if equal, false otherwise)
        """
        if isinstance(that, PlayerState):
            return self.id == that.id and self.foodbag == that.foodbag and self.species == that.species and \
                   self.trait_cards == that.trait_cards
        else:
            return False

    @staticmethod
    def new(id, player):
        """
        Create a PlayerState object, giving this PlayerState a reference to an external Player
        :param id: An integer >= 1, and <= 8, to identify which player this is
        :param player: Player that has implemented the external player API
        :return: PlayerState with populated values and player references
        """
        return PlayerState(id, player_reference=player, info=player.info)

    def start(self, watering_hole, opt_new_species, trait_cards):
        """
        Effect: Gives information to external players to start the round with
        :param watering_hole: Nat- Number of tokens in the watering hole
        :param opt_new_species: Species or False - Optional species with population=1
        :param trait_cards: listOf(TraitCard) - Appropriate cards to give an external player
        :return: Void
        """
        if opt_new_species:
            self.species.append(opt_new_species)
        self.trait_cards.extend(trait_cards)
        self.player_reference.start(copy.deepcopy(self), watering_hole)

    def choose(self, playerStates):
        """
        Call external player's choose function giving preceding players, and players to go after this player
        :param playerStates: - the list of PlayerStates in the entire game
        :return: A PlayerAction that represents a player's choice:
        """
        for i in range(len(playerStates)):
            player = playerStates[i]
            if player.id == self.id:
                prev_species = [copy.deepcopy(ps.species) for ps in playerStates[:i]]
                later_species = [copy.deepcopy(ps.species) for ps in playerStates[i+1:]]
                return self.player_reference.choose(prev_species, later_species)

    def step4i(self, player_action):
        """
        Effect: Trades in cards for new species, cards on species, and/or growth of population/body
        :param player_action: PlayerAction - contains desired actions to perform (see playerAction.py)
        :return: Void
        """
        player_action.perform_all_actions(self)

    def feedNext(self, wateringHole, playerStates):
        """
        Calls the external player reference's feed function and returns results of that call
        :param wateringHole: Nat - The current number of food tokens in the watering hole
        :param playerStates: listOf(PlayerState) - All playerstates in turn order beginning from ccurrent PlayerState
        :return: FeedAction - the desired feeding action of the player (see feedAction.py)
        """
        otherPlayers = [copy.deepcopy(ps.species) for ps in playerStates[1:]]
        return self.player_reference.feedNext(copy.deepcopy(self), wateringHole, otherPlayers)

    def getLeftNeighbor(self, index):
        """
        Get the species to the left of the species at index
        :param index: Nat - index of currentSpecies. 0 <= index < len(ps.species)
        :return: Species or False - Species to left of player if present
        """
        return index > 0 and self.species[index-1]

    def getRightNeighbor(self, index):
        """
        Get the species to the right of the species at index
        :param index: Nat - index of currentSpecies. 0 <= index < len(ps.species)
        :return: Species or False - Species to right of player if present
        """
        return index + 1 < len(self.species) and self.species[index+1]

    def get_species_at(self, index):
        """
        Get the species at the given index
        :param index: Nat - index to get species at
        :return: Species - Species at given index
        """
        return self.species[index]

    def get_neighbors(self, index):
        """
        Returns the left and right neighbor Species of the index in this playerState
        :param index: Nat - the index of the species to find the neighbors of
        :return: Tuple(Species, Species) - the neighbors in reference to index
        """
        return self.getLeftNeighbor(index), self.getRightNeighbor(index)

    def remove_extinct(self, species_index):
        """
        Remove a species from this playerState if extinct, returning True if removed
        Effect: removes species at species_index if that species population is 0
        :param species_index: Nat - index of species to check
        :return True if a species was removed
        """
        species = self.species[species_index]
        if species.population <= 0:
            self.species.pop(species_index)
            return True
        return False

    def can_feed_veg(self, speciesIndex):
        """
        Are we allowed to feed the species at speciesIndex as a vegetarian?
        :param speciesIndex: The index we are attempting to feed
        :return: True if we can feed the species at speciesIndex (i.e., not a carnivore)
        """
        if self.species[speciesIndex].hasTrait(CARNIVORE):
            return False
        return True

    def feed_species_with_trait(self, trait, num_tokens_available):
        """
        Effect: Adds food all of this player's species that have the given trait, subtracts food from self.watering_hole
        :param trait: String - trait that decides if this species gets feed
        :param num_tokens_available: Nat - total number of food tokens available to this player
        :return: Void
        """
        self.watering_hole = num_tokens_available
        for specIndex in range(len(self.species)):
            if num_tokens_available <= 0:
                break

            species_board = self.get_species_at(specIndex)
            if species_board.hasTrait(trait) and species_board.isHungry():
                self.feedFromWateringHole(specIndex, num_tokens_available)
                num_tokens_available = self.watering_hole

    def add_fertile_populations(self):
        """
        Effect: All species with fertile in the player's species increase population by 1 if possible
        :return: Void
        """
        [species.increase_population() for species in self.species if species.hasTrait(FERTILE)]

    def transfer_fat_food(self):
        """
        Effect: All species with fat-tissue trait will have their fat_food transferred to their food
        :return: Void
        """
        [species.transfer_fat_food() for species in self.species if species.hasTrait(FAT_TISSUE)]

    def cooperationFeed(self, speciesIndex):
        """
        Effect: Species to the right of given species adds food from wateringHole if this species has cooperation trait.
        :param: speciesIndex: index of current feeding species
        :return: Void
        """
        rightNeighbor = self.getRightNeighbor(speciesIndex)
        if rightNeighbor and rightNeighbor.isHungry():
            self.feedFromWateringHole(speciesIndex + 1, self.watering_hole)

    def feedFromWateringHole(self, speciesIndex, watering_hole):
        """
        Effect: Takes food from the wateringHole, adding value to species' food.
        :param: playerIndex: Index of the player to feed
        :param watering_hole: Number of food tokens available in watering_hole
        :return: Void
        """
        foodToEat = min(watering_hole, 1)
        food_ate = 0
        feeding_species = self.species[speciesIndex]
        self.watering_hole = watering_hole

        if feeding_species.hasTrait(FORAGING):
            foodToEat = min(self.watering_hole, 2)

        for i in range(foodToEat):
            if feeding_species.isHungry():
                feeding_species.feed()
                self.watering_hole -= 1
                food_ate += 1

        for i in range(food_ate):
            if feeding_species.hasTrait(COOPERATION):
                self.cooperationFeed(speciesIndex)

    def remove_card(self, card_index):
        """
        Effect: Removes this player's card in self.trait_cards at the given card_index (return that card)
        :param card_index: Nat - Index of TraitCard to remove
        :return: TraitCard - Card that was removed from self.trait_cards
        """
        if card_index < len(self.trait_cards):
            return self.trait_cards.pop(card_index)

    def add_species_with_traits(self, trait_list):
        """
        Effect: Add a species with food=0, body=0, population=1, and given traits in trait_list to this playerState
        :param trait_list: listOf(TraitCard) - the TraitCards to add to the new Species
        :return: Void
        """
        self.species.append(Species(0, 0, 1, trait_list))

    def remove_trait_cards_at_indices(self, list_of_indices):
        """
        Effect: Removes every species in this playerState at each index in list_of_indices
        :param list_of_indices: listOf(Nat) - List of indices corresponding to species in self.species
        :return: Void
        """
        self.trait_cards = numpy.delete(self.trait_cards, list_of_indices).tolist()

    def calculate_score(self):
        """
        Calculate this player's score based on foodbag, species populations, and number of species traits
        :return: Nat - The player's score
        """
        score = self.foodbag
        for species in self.species:
            score += species.population + len(species.trait_cards)
        return score

    def print_results(self, rank):
        """
        Print this players results at the end of the game, including rank, player info string, score, and ID
        :param rank: The player's rank at the end of the game. From 1 to numPlayers
        :return: Void
        """
        print str(rank) + " player id: " + str(self.id) + " | player info: " + str(self.info) + \
              " | score: " + str(self.calculate_score())

    def end_player_turn(self):
        """
        Effect: 1) Reduce population size of each species to the number of food tokens on its species board,
                2) Removes newly extinct species (from reducing the population size), adding to num_extinct
                3) Move all food tokens from all species boards to food bags
        :return: Nat - The Number of species that went extinct (to be used by dealer)
        """
        num_extinct = 0
        i = len(self.species) - 1
        while i >= 0:
            species = self.species[i]
            species.population = species.food
            if self.remove_extinct(i):
                num_extinct += 1
            else:
                self.foodbag += species.food
                species.food = 0
            i -= 1
        return num_extinct

    def exit_game(self):
        """
        Effect: Exits the game for this external playerstate
        :return: Void
        """
        self.player_reference.exit_game()

    @staticmethod
    def parse_feeding(json_feeding):
        """
        Create a (playerState, Nat, listOf(PlayerState)) tuple from json_feeding
            - json_feeding is [Player, Nat+, LOP]
                - Player is [["id", Nat+],["species", LOS], ["bag", Nat]]
                - LOP is [Player, ..., Player]
                - LOS is [Species, ..., Species]
                - Species is [["food",Nat],
                              ["body",Nat],
                              ["population",Nat+],
                              ["traits",LOT]
                     (Opional)["fat-food" ,Nat]]
        :param json_feeding:
        :return: PlayerState, Nat, listOf(PlayerState)
        """
        curState = PlayerState.convertPlayerState(json_feeding[0])
        wateringHole = int(json_feeding[1])
        otherPlayers = []
        for player in json_feeding[2]:
            if player:
                otherPlayers.append(PlayerState.convertPlayerState(player).species)

        return curState, wateringHole, otherPlayers

    def toJsonArray(self):
        """
        Creates a json representation of this PlayerState
        :return: JSON list representing this PlayerState
        """
        species = [animal.toJsonArray() for animal in self.species]

        if self.trait_cards:
            traits = [trait_card.to_json() for trait_card in self.trait_cards]

            return [[ID_LABEL, self.id],
                    [SPECIES_LABEL, species],
                    [BAG_LABEL, self.foodbag],
                    [CARDS_LABEL, traits]]
        else:
            return [[ID_LABEL, self.id],
                    [SPECIES_LABEL, species],
                    [BAG_LABEL, self.foodbag]]

    def to_json_state(self):
        """
        Creates a json representation of this PlayerState
        :return: JSON list representing this PlayerState
            - [Natural,[Species+, ..., Species+], Cards]
        """
        species = [animal.toJsonArray() for animal in self.species]
        traits = [trait_card.to_json() for trait_card in self.trait_cards]
        return [self.foodbag, species, traits]

    @staticmethod
    def from_json_state(json_state):
        """
        Takes in a json 'state' of a Player, converting it into a new PlayerState object
        :param json_state: JSON List -  [Natural, [Species+, ..., Species+], Cards]
        :return: PlayerState - the new PlayerState object created from the json representation
        """
        food_bag = json_state[0]
        species_list = [Species.convertSpecies(species) for species in json_state[1]]
        trait_cards = [TraitCard.from_json(trait) for trait in json_state[2]]
        return PlayerState(bag=food_bag, speciesList=species_list, trait_cards=trait_cards)

    @staticmethod
    def from_json_gamestate(json_state):
        """
        Takes in a json game state, converting it into a list that contains the PlayerState, WateringHole, and other species
        :param json_state: JSON List - [Natural, [Species+, ..., Species+], Cards, Natural+, LOB]
        :return: [PlayerState, Nat, List of Species]
        """
        ps = PlayerState.from_json_state(json_state[:3])
        watering_hole = json_state[3]
        all_species = []
        for species_list in json_state[4]:
            all_species.append([Species.convertSpecies(species) for species in species_list])
        return [ps, watering_hole, all_species]


    @staticmethod
    def convertPlayerState(state):
        """
        Creates a PlayerState from from the given JSON representation
        :param state: JSON list - represents the playerState
        :return: PlayerState - with attributes contained in 'state'
        """
        playerTraitCards = []

        if state[0][0] == ID_LABEL and state[1][0] == SPECIES_LABEL and state[2][0] == BAG_LABEL:
            id = state[0][1]
            speciesList = [Species.convertSpecies(species) for species in state[1][1]]
            bag = state[2][1]
            if len(state) == 4 and state[3][0] == CARDS_LABEL:
                playerTraitCards = [TraitCard.from_json(card) for card in state[3][1]]
            if id < 1 or bag < 0:
                raise Exception("Bad JSON PlayerState Data")

            return PlayerState(id, bag, speciesList, playerTraitCards)

        else:
            raise Exception("Bad JSON PlayerState input")