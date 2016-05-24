#!/usr/bin/env python2.7

from constants import *


class TraitCard:

    def __init__(self, name, food=0):
        """
        Creates a new trait card with the given name, and a food value
        :param name: String - the name of the trait
        :param food: Integer (optional) - the food value for the card. Default to 0
        :return: TraitCard with populated name and food values
        """
        self.name = name
        self.food = food

    def __eq__(self, that):
        """
        This is the equals method that determines if the inputted 'that' object is equal to this TraitCard
        :param that: Any (object)
        :return: Boolean (true if equal, false otherwise)
        """
        if isinstance(that, TraitCard):
            return self.name == that.name and self.food == that.food
        else:
            return False

    @staticmethod
    def from_json(json_card):
        """
        Creates a TraitCard from an inputted json representation of a traitCard.
        :param json_card: [Nat, String] - the food value and the name of the new card
        :return: TraitCard - the trait card object created
        """
        if len(json_card) == 2:
            foodValue = json_card[0]
            trait = json_card[1]
            if isinstance(foodValue, int) and TraitCard.is_valid_food(json_card) and trait in TRAIT_TYPES:
                return TraitCard(trait, foodValue)
            else:
                raise Exception("Invalid JSON Trait Card")
        else:
            raise Exception("Invalid JSON Trait Card")

    def to_json(self):
        """
        Creates a json representation of this TraitCard
        :return: [Nat, String] - the food value and name of the trait in a json list
        """
        return [self.food, self.name]

    @staticmethod
    def is_valid_food(json_card):
        """
        Does this trait card have a valid food value?
        :return: True if food value is in correct range
        """
        return (json_card[1] == CARNIVORE and CARNIVORE_LOWER_BOUND <= json_card[0] <= CARNIVORE_UPPER_BOUND) or \
               (TRAIT_LOWER_BOUND <= json_card[0] <= TRAIT_UPPER_BOUND)
