#!/usr/bin/env python2.7

class BoardTrade:

    def __init__(self, trait_card_index, traits_for_species):
        """
        Initialze a BoardTrade object with the given values
        :param trait_card_index: Nat - Index of the trait_card in playerState to exchange for new species
        :param traits_for_species: listOf(Nat) - Optional trait indices to exchange for traits on new species
        :return: BoardTrait object with populated values
        """
        self.trait_card_index = trait_card_index
        self.traits_for_species = traits_for_species

    def __eq__(self, that):
        """
        Determines if 'that' object is a BoardTrade and is equal to this BoardTrade
        :param other: the Object to compare with this BoardTrade
        :return: Boolean - True if equal, False otherwise
        """
        return isinstance(that, BoardTrade) \
               and self.trait_card_index == that.trait_card_index \
               and self.traits_for_species == that.traits_for_species

    def board_trade(self, playerState):
        """
        Effect: Remove any trait_cards at self.trait_card_index or in self.traits_for_species, adding a new species with
        optional traits from the exchanged self.traits_for_species
        :param playerState:
        :return: Void
        """
        trait_cards = [playerState.trait_cards[i] for i in self.traits_for_species]
        playerState.add_species_with_traits(trait_cards)

    @staticmethod
    def parse_board_trade(json_bt):
        """
        Parse a json representation of a board trade into a BoardTrade object
        :param json_bt: listOf(Nat) of length 1, 2, 3, or 4
        :return: BoardTrade object with species_index of json_bt[0], and remaining indices as traits-for_species
        """
        if BoardTrade.is_valid_board_trade(json_bt):
            return BoardTrade(json_bt[0], json_bt[1:])
        else:
            raise Exception("Invalid board trade json representation")

    @staticmethod
    def is_valid_board_trade(json_bt):
        """
        is the json_bt a valid representation?
        :param json_bt: json board trade representation
        :return: True if is valid
        """
        if isinstance(json_bt, list) and 1 <= len(json_bt) <= 4:
            for item in json_bt:
                if not (not isinstance(item, bool) and isinstance(item, int) and item >= 0):
                    return False
            return True
        return False

    def to_json(self):
        """
        Returns a json interpretation of a board trade object
        :return: JSON list - [Nat, Nat]
        """
        return [self.trait_card_index] + self.traits_for_species

