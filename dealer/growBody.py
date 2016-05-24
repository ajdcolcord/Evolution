#!/usr/bin/env python2.7


class GrowBody:

    def __init__(self, species_index, card_trade_index):
        """
        Initialize GrowBody action with given values
        :param species_index: Indicates the species to grow the body of
        :param card_trade_index: Indicates the card to trade in for this action
        :return: GrowBody - A GrowBody action containing the populated values
        """
        self.species_index = species_index
        self.card_trade_index = card_trade_index

    def __eq__(self, that):
        """
        Return True if 'that' is a GrowBody and this GrowBody has the same value as that GrowBody
        :param that: Object to compare
        :return: True if this equals that
        """
        return isinstance(that, GrowBody) and self.species_index == that.species_index and \
               self.card_trade_index == that.card_trade_index

    def grow_body(self, playerState):
        """
        Effect: Remove card from playerState, add to dealer's hand, add 1 to species body at species_index in playerState
        :param playerState: PlayerState - The player trading a card for body growth
        :return: Void
        """
        playerState.species[self.species_index].increase_body()

    @staticmethod
    def parse_grow_body(json_grow):
        """
        Parse this body grow action from json to a GrowBody
        :param json_grow: json representation of grow body action
        :return: GrowBody
        """
        if GrowBody.is_valid_body_grow(json_grow):
            return GrowBody(json_grow[1], json_grow[2])
        else:

            raise Exception("Invalid json body grow action")

    @staticmethod
    def parse_proxy_grow_body(json_grow):
        """
        Parse this body grow action from json to a GrowBody
        :param json_grow: json representation of grow body action
        :return: GrowBody
        """
        if GrowBody.is_valid_proxy_grow(json_grow):
            return GrowBody(json_grow[0], json_grow[1])
        else:
            raise Exception("Invalid json body grow action")

    @staticmethod
    def is_valid_body_grow(json_grow):
        """
        Is json_grow a valid json representation of a species growth?
        :param json_grow: the json grow representation
        :return: True if json_grow is valid
        """
        return isinstance(json_grow, list) and len(json_grow) == 3 and json_grow[0] == "body" and\
               not isinstance(json_grow[1], bool) and isinstance(json_grow[1], int) and json_grow[1] >= 0 and\
               not isinstance(json_grow[2], bool) and isinstance(json_grow[2], int) and json_grow[2] >= 0

    @staticmethod
    def is_valid_proxy_grow(json_grow):
        """
        Is json_grow a valid json representation of a species growth?
        :param json_grow: the json grow representation
        :return: True if json_grow is valid
        """
        return isinstance(json_grow, list) and len(json_grow) == 2 and\
               not isinstance(json_grow[0], bool) and isinstance(json_grow[0], int) and json_grow[0] >= 0 and\
               not isinstance(json_grow[1], bool) and isinstance(json_grow[1], int) and json_grow[1] >= 0

    def to_json(self):
        """
        Returns a json interpretation of a grow body object
        :return: JSON list - ["body", Nat, Nat]
        """
        return ["body", self.species_index, self.card_trade_index]

    def to_json_proxy(self):
        """
        Returns a json interpretation of a grow body object - used in new proxy specifications
        :return: JSON list - [Nat, Nat]
        """
        return [self.species_index, self.card_trade_index]