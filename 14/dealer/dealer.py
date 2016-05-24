#!/usr/bin/env python2.7

import sys, os
import copy
from playerAction import PlayerAction
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'feeding'))
from player import Player
from playerState import PlayerState
from constants import *
from species import Species
from traitCard import TraitCard


class Dealer:

    def __init__(self, playerStates, wateringHole, hand):
        """
        Initializes a new Dealer object based on the input values for playerstates, wateringhole, and speciesCards.
        :param playerStates: List of PlayerStates - the PlayerStates involved in the game
        :param wateringHole: Nat - the value of the watering hole
        :param hand: List of TraitCard - this dealer's hand
        :return: Dealer - the new initialized dealer object
        """
        self.playerStates = playerStates
        self.originalPlayerOrder = copy.copy(self.playerStates)
        self.wateringHole = wateringHole
        self.hand = hand
        self.fullPlayerIds = []

    def __eq__(self, that):
        """
        This is the equals method that determines if the inputted 'that' object is equal to this Dealer
        :param that: Any (object)
        :return: Boolean (true if equal, false otherwise)
        """
        if isinstance(that, Dealer):
            return self.playerStates == that.playerStates and self.wateringHole == that.wateringHole and \
                    self.hand == that.hand
        else:
            return False

    @staticmethod
    def new(players):
        """
        Create a new Dealer with the given list of player references
        :param players: List of external Player references
        :return: Dealer object with the starting default values for each playerState, wateringHole, hand
        """
        playerStates = []

        for i in range(len(players)):
            playerStates.append(PlayerState.new(i + 1, players[i]))

        hand = Dealer.create_hand()
        return Dealer(playerStates, 0, hand)

    @staticmethod
    def create_hand():
        """
        Creates a deck for a dealer: 122 cards->17 carnivore (values -8 to 8), 7 of each other trait (values -3 to 3)
        :return: listOf(TraitCard) - The deck to be used by a dealer of the Evolution game
        """
        deck = []
        for i in range(CARNIVORE_LOWER_BOUND, CARNIVORE_UPPER_BOUND + 1):
            deck.append(TraitCard(CARNIVORE, i))
        for trait in TRAIT_TYPES[1:]:
            for i in range(TRAIT_LOWER_BOUND, TRAIT_UPPER_BOUND + 1):
                deck.append(TraitCard(trait, i))
        sorted_deck = sorted(deck, key=lambda x: (x.name, x.food))
        return sorted_deck

    def runGame(self):
        """
        Runs an entire game of Evolution from start to finish
        Effect: All values will be mutated according to how each player interacts with each
               other and the dealer until the game is over
        :return: Void
        """
        while not self.is_game_over():
            self.turn()
            self.cycle_players()
        self.print_results()

    def turn(self):
        """
        Runs one full turn in the Evolution game
        Effect: All values will be mutated according to how each player interacts with each other and the dealer.
        :return: Void
        """
        self.step1()
        player_actions = self.get_player_choices()
        self.step4(player_actions)
        self.end_turn()

    def cycle_players(self):
        """
        Effect: Cycles the players for the next turn, shifting the first player to the end.
        :return: Void
        """
        self.playerStates = copy.copy(self.originalPlayerOrder)
        self.playerStates.append(self.playerStates.pop(0))
        self.originalPlayerOrder = copy.copy(self.playerStates)

    def is_game_over(self):
        """
        Checks if the Evolution game is over by deciding if this dealer has enough cards to deal to each player
        :return: Boolean - True if the game over
        """
        num_cards_needed = 0
        for player in self.playerStates:
            if len(player.species):
                num_cards_needed += CARDS_PER_TURN + len(player.species)
            else:
                num_cards_needed += CARDS_PER_TURN + 1

        return num_cards_needed > len(self.hand)

    def step1(self):
        """
        Effect: Calls the start function for each player in self.playerStates, and takes trait_cards from dealer's hand
        :return: Void
        """
        for ps in self.playerStates:
            num_existing_species = len(ps.species)
            new_species = num_existing_species == 0 and Species(0, 0, 1)
            num_cards_to_give = num_existing_species + CARDS_PER_TURN
            if new_species:
                num_cards_to_give += 1
            trait_list = self.hand[:num_cards_to_give]
            self.hand = self.hand[num_cards_to_give:]
            ps.start(self.wateringHole, new_species, trait_list)

    def get_player_choices(self):
        """
        Call each playerState's choose function, return a list of actions that each player has chosen
        Effect: If a Player sends in data that is invalid, they will be removed from the game
        :return: Step4 - The player's action choices, to be parsed into a listOf(PlayerAction)
        """
        result = []
        player_indices_to_remove = []
        for i in range(len(self.playerStates)):
            ps = self.playerStates[i]
            try:
                result.append(ps.choose(self.playerStates))
            except:
                player_indices_to_remove.append(i)

        self.remove_players_at_indices(player_indices_to_remove)
        return result

    def add_silly_players(self):
        """
        Creates the list of 'silly-strategy' players using the player states of this Dealer (Testing Purposes)
        Effect: self.players is populated with Player objects
        :return: Void
        """
        players = [Player(state.id) for state in self.playerStates]
        for i in range(len(players)):
            self.playerStates[i].player_reference = players[i]
            self.playerStates[i].info = str(self.playerStates[i].id)

    def step4(self, player_actions):
        """
        Perform all actions in player_actions, with each action corresponding to a player in self.playerStates
        Effect: players in self.playerStates are mutated, self.hand may add cards, may add to self.face_down_cards
        :param player_actions: listOf(PlayerAction) - Actions taken by each player (length = len(self.playerStates))
        :return: Void
        """
        cheater_indices = []
        for i in range(len(player_actions)):
            try:
                card_on_wateringHole = self.playerStates[i].trait_cards[player_actions[i].food_card_index]
                self.wateringHole = max(0, card_on_wateringHole.food + self.wateringHole)
                self.playerStates[i].step4i(player_actions[i])
            except:
                cheater_indices.append(i)

        self.remove_players_at_indices(cheater_indices)
        self.add_fertile_populations()
        self.feed_all_species_with_trait(LONG_NECK)
        self.transfer_fat_food()
        self.feeding()

    def end_turn(self):
        """
        Effect: Modifies each playerState to adjust species populations and food, foodbags, and extinct species
                Deals NUM_CARDS_FOR_EXTINCTION to a player for each species that went extinct
        :return: Void
        """
        for ps in self.playerStates:
            num_extinct = ps.end_player_turn()
            self.deal_x_cards(ps, num_extinct * NUM_CARDS_FOR_EXTINCTION)
        self.fullPlayerIds = []

    def feeding(self):
        """
        Call feed1 on each playerState until no players can feed any more, or wateringHole is empty
        Effect: self.wateringHole, self.playerState, self.fullPlayerIds, self.hand all change depending on each feed1
        :return: Void
        """
        while self.wateringHole > 0 and len(self.fullPlayerIds) < len(self.playerStates):
            if self.playerStates[0].id not in self.fullPlayerIds:
                self.feed1()
            self.playerStates.append(self.playerStates.pop(0))

    def feed1(self):
        """
        Runs one step in the feeding process, autofeeding for the player if possible, else query their feed function.
        Effect: Modifies:  - self.playerStates (for all playerStates involved in the feeding process)
                           - self.wateringHole (each time a food token is consumed)
                           - self.hand (each time a species goes extinct)
                           - self.fullPlayerIds (each time a player cannot feed or chooses not to feed)
        :return: Void (modify state of this dealer)
        """
        if self.wateringHole > 0:
            if not self.auto_feed():
                self.request_feed()

    def request_feed(self):
        """
        Delegates to further feeding functions depending on if the foodAction is veg feed, fat feed, or carnivore feed.
        Effect: modifies the entire state of this Dealer. See feed1 function Effect. Removes any cheating players
        :return: Void
        """
        player = self.playerStates[0]
        try:
            player_choice = player.feedNext(self.wateringHole, self.playerStates)
            player_choice.feed(self)
        except:
            self.remove_cheater(0)

    def feed_result_vegetarian(self, speciesIndex):
        """
        Effect: The first in self.playerStates species at speciesIndex gets fed and induces any autofeeding necessary
        :param speciesIndex: Nat - the index of the species in the player to feed
        :return: Void - modifies the players species and the watering hole
        """
        if self.playerStates[0].can_feed_veg(speciesIndex):
            self.feedFromWateringHole(0, speciesIndex)
        else:
            raise Exception("Bad Veg Feed")

    def feed_result_fat_food(self, speciesIndex, requestedFatFood):
        """
        Effect: Stores as much requestedFatFood as possible on the first playerStates species at speciesIndex,
                Takes this stored food from wateringHole
        :param speciesIndex: Nat - the index of the species in the player to feed
        :param requestedFatFood: Nat - the player's desired number of food to store in fat-food
        :return: Void
        """
        current_species = self.playerStates[0].get_species_at(speciesIndex)
        requestedFatFood = min(self.wateringHole, requestedFatFood, current_species.getFatRoom())

        current_species.store_fat(requestedFatFood)
        self.wateringHole -= requestedFatFood

    def feed_result_carnivore(self, attSpecIndex, defPlayerIndex, defSpecIndex):
        """
        Effect: Attacking species will get food, decrease population if attacking horns.
                Defending species of defPlayerIndex will reduce in population if attack succeeds
                Food is taken from the wateringHole for successful attacks
                Extinction will cause extinct species owners to get cards, which are removed from this dealers hand
        :param attSpecIndex: Nat - the index of the carnivore species in the player that is attacking
        :param defPlayerIndex: Nat - the index of the player to attack
        :param defSpecIndex: Nat - the index of the species in the defending player to attack
        :return: Void
        """
        attPlayerState = self.playerStates[0]
        attSpecies = attPlayerState.get_species_at(attSpecIndex)

        defPlayerState = self.playerStates[defPlayerIndex]
        defSpecies = defPlayerState.get_species_at(defSpecIndex)

        leftSpecies = defPlayerState.getLeftNeighbor(defSpecIndex)
        rightSpecies = defPlayerState.getRightNeighbor(defSpecIndex)

        if Species.isAttackable(defSpecies, attSpecies, leftSpecies, rightSpecies):
            self.execute_attack(attSpecies, defSpecies, attPlayerState, defPlayerState, attSpecIndex, defSpecIndex)
        else:
            raise Exception("Bad Attack")


    def execute_attack(self, attSpecies, defSpecies, attPlayerState, defPlayerState, attSpecIndex, defSpecIndex):
        """
        Executes an attack on an attackable species (assumes attackable). Checks and removes any extinct species.
        Effect: Populations decrease according to attack, Scavenger species add food, hand is modified if cards dealt
        :param attSpecies: Species - the attacking species
        :param defSpecies: Species - the defending species
        :param attPlayerState: PlayerState - the attacking playerstate
        :param defPlayerState: PlayerState - the defending playerstate
        :param attSpecIndex: Nat - the index of the attacking Species
        :param defSpecIndex: Nat - the index of the defending Species
        :return: Void - modifies various pieces to Species contained in PlayerStates
        """
        defSpecies.decrease_population()
        if defSpecies.hasTrait(HORNS):
            attSpecies.decrease_population()

        if defPlayerState.remove_extinct(defSpecIndex):
            self.deal_x_cards(defPlayerState, NUM_CARDS_FOR_EXTINCTION)

        if attPlayerState.remove_extinct(attSpecIndex):
            self.deal_x_cards(attPlayerState, NUM_CARDS_FOR_EXTINCTION)
        elif attSpecies.isHungry():
            self.feedFromWateringHole(0, attSpecIndex)
            self.feed_all_species_with_trait(SCAVENGER)

    def feed_all_species_with_trait(self, trait):
        """
        Effect: All species with given trait are fed if possible, wateringHole gets decreased for each feeding.
        :param: trait: String - the given trait to feed
        :return: Void
        """
        for state in self.playerStates:
            state.feed_species_with_trait(trait, self.wateringHole)
            self.wateringHole = state.watering_hole

    def add_fertile_populations(self):
        """
        Effect: All species with the fertile trait's populations increase by 1 if possible
        :return: Void
        """
        [state.add_fertile_populations() for state in self.playerStates]

    def transfer_fat_food(self):
        """
        Effect: All species with the fat-tissue trait will have fat food transferred to food
        :return: Void
        """
        [state.transfer_fat_food() for state in self.playerStates]

    def feedFromWateringHole(self, playerIndex, speciesIndex):
        """
        Effect: Takes food from the wateringHole, adding value to species' food.
        :param: playerIndex: Index of the player to feed
        :param speciesIndex: Index of the species to feed
        :return: Void
        """
        self.playerStates[playerIndex].feedFromWateringHole(speciesIndex, self.wateringHole)
        self.wateringHole = self.playerStates[playerIndex].watering_hole

    def auto_feed(self):
        """
        Autofeeds the first player if it possesses only one hungry vegetarian and no options for fat food storage
        Effect: Modifies: - the first playerstate (if auto-feed occurs)
                          - self.wateringhole (if autofed)
                          - self.fullPlayerIds (if no hungry species found on the playerState)
        :return: Boolean: True if this dealer makes a decision for the player, False if need to query the player still
        """
        first_player = self.playerStates[0]

        hungry_index_list, fat_tissue_indexes = self.get_hungry_and_fat_tissue_lists()
        if len(fat_tissue_indexes) and len(hungry_index_list):
            return False

        if len(hungry_index_list) == 0 and len(fat_tissue_indexes) == 0:
            self.fullPlayerIds.append(first_player.id)
            return True

        if len(fat_tissue_indexes) == 1:
            return False

        if len(hungry_index_list) == 1:
            return self.auto_feed_one_hungry(hungry_index_list[0])

        return False

    def auto_feed_one_hungry(self, hungry_index):
        """
        Effect: Autofeeds a hungry species at given index only if it is a vegetarian
        :param hungry_index: Nat - index of species in first playerState
        :return: Boolean - True if the species was autofed by this dealer
        """
        first_player = self.playerStates[0]
        current_species = first_player.get_species_at(hungry_index)

        if not current_species.hasTrait(CARNIVORE):
            self.feed_result_vegetarian(hungry_index)
            return True

        return False

    def get_hungry_and_fat_tissue_lists(self):
        """
        Gets the hungry and fat tissue index lists of species from the first playerstate in this dealer's playerstates.
        :return: Tuple(Listof Nat, Listof Nat)
        """
        hungry_index_list = []
        fat_tissue_index_list = []
        first_player = self.playerStates[0]

        for i in range(len(first_player.species)):
            current_species = first_player.get_species_at(i)

            if current_species.isHungry():
                hungry_index_list.append(i)

            if current_species.hasTrait(FAT_TISSUE) and current_species.getFatRoom() > 0:
                fat_tissue_index_list.append(i)

        return hungry_index_list, fat_tissue_index_list

    def deal_x_cards(self, playerState, x):
        """
        Effect: Adds up to x number of cards to the playerState at the given index, removing cards from this dealer's hand
        :param PlayerState: The playerState to deal cards to
        :param x: Nat - The number of cards to deal
        :return: Void
        """
        cards_to_deal = min(x, len(self.hand))

        new_traits = []
        for i in range(cards_to_deal):
            new_traits.append(self.hand.pop(0))
        playerState.trait_cards = new_traits + playerState.trait_cards

    def print_results(self):
        """
        Print the results of the game to standard out, printing each player's id and food score in decreasing order
        :return: Void
        """
        results = sorted(self.playerStates, key=lambda x: x.calculate_score(), reverse=True)
        for i in range(len(results)):
            results[i].print_results(i+1)

    def remove_cheater(self, cheater_index):
        """
        Effect: Remove a playerState at cheater_index of self.playerStates that tries to cheat, or gives bad input
        :param cheater_index: The index of the cheating player in self.playerStates
        :return: Void
        """
        if self.playerStates[cheater_index].id in self.fullPlayerIds:
            self.fullPlayerIds.remove(self.playerStates[cheater_index].id)

        self.remove_id_from_original_player_order(self.playerStates[cheater_index].id)
        self.playerStates[cheater_index].exit_game()
        self.playerStates.pop(cheater_index)

        if len(self.playerStates) == 0:
            sys.exit(0)

    def remove_players_at_indices(self, indices):
        """
        Effect: Removes all players from playerStates, orginalPlayerOrder, fullPlayerIDs in the index of playerStates
        :param indices: listOf(Nat) - Each Nat corresponds to and index in playerStates to remove
        :return: Void
        """
        i = len(self.playerStates) - 1
        while i >= 0:
            if i in indices:
                self.remove_cheater(i)
            i -= 1

    def remove_id_from_original_player_order(self, id):
        """
        Effect: Removes player with given id from given players list
        :param id: Nat - id to search and remove
        :return: Void
        """
        for i in range(len(self.originalPlayerOrder)):
            if self.originalPlayerOrder[i].id == id:
                self.originalPlayerOrder.pop(i)
                break

    @staticmethod
    def create_dealer_from_configuration(json_configuration):
        """
        Takes in a configuration from stdin as a JSON object
        :param json_configuration: the JSON configuration
        :return: Dealer - the dealer created from the configuration
        """
        try:
            list_of_player_states = []
            for player_state in json_configuration[0]:
                ps = PlayerState.convertPlayerState(player_state)
                ps.player_reference = Player(ps.id)
                list_of_player_states.append(ps)

            wh = json_configuration[1]

            if isinstance(wh, int) and not isinstance(wh, bool) and wh >= 0:
                watering_hole = json_configuration[1]
                hand = Dealer.get_hand(json_configuration[2])

                return Dealer(list_of_player_states, watering_hole, hand)
            else:
                raise Exception("Invalid JSON Watering Hole")
        except:
            raise Exception("Ill formed json configuration")

    def create_json_from_dealer(self):
        """
        Creates a JSON representation of a Dealer Configuration

        Rendering Your classes should render objects as follows:
            - a Species+ with a 0-valued "fat-food" field renders as a plain Species;
            - a Player+ with a []-valued "cards" field renders as a plain Player;

        :param dealer: Dealer - the dealer object
        :return: JSON configuration of a Dealer ([ListOfPlayers, Natural, ListOfSpeciesCards])
        """
        list_of_players = []
        wateringhole = self.wateringHole
        list_of_species_cards = []

        for player_state in self.playerStates:
            list_of_players.append(player_state.toJsonArray())

        for species_card in self.hand:
            list_of_species_cards.append([species_card.food, species_card.name])

        return [list_of_players, wateringhole, list_of_species_cards]

    @staticmethod
    def get_hand(json_trait_cards):
        """
        Parse a json trait hand into a list of TraitCards
        :param json_trait_cards: JSON list of [traitValue, traitName]
        :return: listOf(TraitCard) - The Dealer's hand from configuration
        """
        list_of_species_cards = []
        found_traits = {}
        for trait_card in json_trait_cards:
            if len(trait_card) == 2:
                list_of_species_cards.append(TraitCard.from_json(trait_card))
                if trait_card[1] in found_traits:
                    found_traits[trait_card[1]] += 1
                else:
                    found_traits[trait_card[1]] = 1

        Dealer.validate_hand(found_traits)

        return list_of_species_cards

    @staticmethod
    def validate_hand(traits_dict):
        """
        Raise an exception if there are too many cards of a specific trait in the hand
        :param traits_dict: a dictionary of form: {TraitName: numTrait}
        """
        for trait in traits_dict:
            if trait == CARNIVORE:
                if traits_dict[trait] > MAX_CARNIVORE_TRAITS:
                    raise Exception("Too many Carnivores")
            else:
                if traits_dict[trait] > MAX_OTHER_TRAITS:
                    raise Exception("Too many " + str(trait) + "s")

    @staticmethod
    def parse_step4(json_step4):
        """
        Parse a json step4 configuration, delegating each item of the given list to PlayerAction.parse_player_action
        :param json_step4: listOf(Action4) where Action4 is defined in PlayerAction.parse_player_action
        :return: listOf(PlayerAction)
        """
        if not isinstance(json_step4, list):
            sys.exit(0)
        return [PlayerAction.parse_player_action(action4) for action4 in json_step4]
