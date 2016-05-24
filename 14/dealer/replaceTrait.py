#!/usr/bin/env python2.7

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'feeding'))
from constants import *


class ReplaceTrait:

    def __init__(self, species_index, trait_to_remove, trait_to_add):
        """
        Initialize a ReplaceTrait object with given values
        :param species_index: Nat - Index of Species to replace traits of
        :param trait_to_remove: Nat - Index of trait of species to remove
        :param trait_to_add: Nat - Index of traitcard of player to add
        :return: ReplaceTrait - ReplaceTrait action object with populated values
        """
        self.species_index = species_index
        self.trait_to_remove = trait_to_remove
        self.trait_to_add = trait_to_add

    def __eq__(self, that):
        """
        Determines if 'that' object is a ReplaceTrait and is equal to this ReplaceTrait
        :param other: the Object to compare with this ReplaceTrait
        :return: Boolean - True if equal, False otherwise
        """
        return isinstance(that, ReplaceTrait) \
               and self.species_index == that.species_index \
               and self.trait_to_remove == that.trait_to_remove \
               and self.trait_to_add == that.trait_to_add

    def replace_trait(self, playerState):
        """
        Effect: self.trait_to_remove is replaced with self.trait_to_add within species at self.species_index in playerState
        :param playerState: The playerState containing species to trade traits of
        :return: Void
        """
        current_species = playerState.species[self.species_index]
        trait_card_to_remove = current_species.trait_cards[self.trait_to_remove]
        if trait_card_to_remove.name == FAT_TISSUE:
            current_species.fatFood = 0
        current_species.trait_cards[self.trait_to_remove] = playerState.trait_cards[self.trait_to_add]

    @staticmethod
    def parse_replace_trait(json_replace):
        """
        Parse a json representation of a trait replacement into a ReplaceTrait object
        :param json_replace: [Nat, Nat, Nat]
        :return: ReplaceTrait - A ReplaceTrait object
        """
        if ReplaceTrait.is_valid_replace(json_replace):
            return ReplaceTrait(json_replace[0], json_replace[1], json_replace[2])
        else:
            raise Exception("Invalid trait replacement json represention")

    @staticmethod
    def is_valid_replace(json_replace):
        """
        is the json a valid representation?
        :param json_replace: json replacement representation
        :return: True if is valid
        """
        if isinstance(json_replace, list) and len(json_replace) == 3:
            for item in json_replace:
                if not (not isinstance(item, bool) and isinstance(item, int) and item >= 0):
                    return False
            return True
        return False

    def to_json(self):
        """
        Returns a json interpretation of a grow population object
        :return: JSON list - [Nat, Nat]
        """
        return [self.species_index, self.trait_to_remove, self.trait_to_add]