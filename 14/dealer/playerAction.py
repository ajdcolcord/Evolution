#!/usr/bin/env python2.7


from growBody import GrowBody
from growPopulation import GrowPopulation
from boardTrade import BoardTrade
from replaceTrait import ReplaceTrait


class PlayerAction:

    def __init__(self, food_card_index, gp_list, gb_list, bt_list, rt_list):
        """
        Initialize a PlayerAction with the given values
        :param player_index: Nat - index of current acting playerstate
        :param gp_list: listOf(GrowPopulation) - list of grow population actions
        :param gb_list: listOf(GrowBody) - list of grow body actions
        :param bt_list: listOf(BoardTrade) - list of board trade actions
        :param rt_list: listOf(ReplaceTrait) - list of trait replace actions
        :return: PlayerAction with populated attributes
        """
        self.food_card_index = food_card_index
        self.gp_list = gp_list
        self.gb_list = gb_list
        self.bt_list = bt_list
        self.rt_list = rt_list
        self.player_card_trade_indices = [self.food_card_index]

    def __eq__(self, that):
        """
        Return True if 'that' object is a PlayerAction with the same values as this
        :param that: The object to compare
        :return: True if this equals that
        """
        return isinstance(that, PlayerAction) and self.food_card_index == that.food_card_index and \
               self.gp_list == that.gp_list and self.gb_list == that.gb_list and self.bt_list == that.bt_list and \
               self.rt_list == that.rt_list

    def perform_all_actions(self, playerState):
        """
        Effect: Modify dealer's hand, as well as playerStates' foodbag, species chosen to alter, and trait_cards
        :param playerState: The playerState to perform the actions of this PlayerAction on
        :return: Void
        """
        for bt in self.bt_list:
            self.add_index(bt.trait_card_index)
            [self.add_index(i) for i in bt.traits_for_species]
            bt.board_trade(playerState)

        for gp in self.gp_list:
            self.add_index(gp.card_trade_index)
            gp.grow_population(playerState)

        for gb in self.gb_list:
            self.add_index(gb.card_trade_index)
            gb.grow_body(playerState)

        for rt in self.rt_list:
            self.add_index(rt.trait_to_add)
            rt.replace_trait(playerState)

        playerState.remove_trait_cards_at_indices(self.player_card_trade_indices)

    def add_index(self, index):
        """
        Effect: Adds the given index to self.player_card_trade_indices, making sure nothing is added twice
        :param index: Nat - Index to add to self.player_card_trade_indices
        :return: Void
        """
        if index not in self.player_card_trade_indices:
            self.player_card_trade_indices.append(index)
        else:
            raise Exception("Player tried to use one card for multiple actions")


    @staticmethod
    def parse_player_action(json_action):
        """
        parse a given Action4 into a PlayerAction object
        Action4 is [Natural, [GP, ...], [GB, ...], [BT, ...], [RT, ...]]
        A GP is ["population",Natural, Natural]
        A GB is ["body",Natural, Natural]
        A BT is listOf(Natural) of length 1, 2, 3, or 4
        An RT is [Natural, Natural, Natural]
        :param json_action: json representation of a player action
        :return: PlayerAction object populated with values from json_action
        """
        if PlayerAction.is_valid_action(json_action):
            gp_list = [GrowPopulation.parse_grow_population(gp) for gp in json_action[1]]
            gb_list = [GrowBody.parse_grow_body(gb) for gb in json_action[2]]
            bt_list = [BoardTrade.parse_board_trade(bt) for bt in json_action[3]]
            rt_list = [ReplaceTrait.parse_replace_trait(rt) for rt in json_action[4]]
            return PlayerAction(json_action[0], gp_list, gb_list, bt_list, rt_list)
        else:
            raise Exception("Invalid player action json representation")

    @staticmethod
    def parse_proxy_player_action(json_action):
        """
        parse a given Action4 into a PlayerAction object. NOTE: This parse does not include 'population' and 'body' tags
        Action4 is [Natural, [GP, ...], [GB, ...], [BT, ...], [RT, ...]]
        A GP is [Natural, Natural]
        A GB is [Natural, Natural]
        A BT is listOf(Natural) of length 1, 2, 3, or 4
        An RT is [Natural, Natural, Natural]
        :param json_action: json representation of a player action
        :return: PlayerAction object populated with values from json_action
        """
        if PlayerAction.is_valid_action(json_action):
            gp_list = [GrowPopulation.parse_proxy_grow_population(gp) for gp in json_action[1]]
            gb_list = [GrowBody.parse_proxy_grow_body(gb) for gb in json_action[2]]
            bt_list = [BoardTrade.parse_board_trade(bt) for bt in json_action[3]]
            rt_list = [ReplaceTrait.parse_replace_trait(rt) for rt in json_action[4]]
            return PlayerAction(json_action[0], gp_list, gb_list, bt_list, rt_list)
        else:
            raise Exception("Invalid player action json representation")

    @staticmethod
    def is_valid_action(json_action):
        """
        json_action is valid if it is a list of length 5, containing a Nat, and 4 lists
        :param json_action: json_representation of a player action
        :return: True if json_action is valid
        """
        return isinstance(json_action, list) and len(json_action) == 5 and \
               not isinstance(json_action[0], bool) and isinstance(json_action[0], int) and json_action[0] >= 0 and \
                isinstance(json_action[1], list) and isinstance(json_action[2], list) and \
                isinstance(json_action[3], list) and isinstance(json_action[4], list)

    def to_json_action_4(self):
        """
        Parses this player action into an 'action4' json interpretation
        :return: Action4 - json list:
             [Nat,                              - represents index of traitCard to trade for food
             [['population', Nat, Nat], ...],  - represents index of species to grow population using index of traitcard to trade
             [['body', Nat, Nat], ...],        - represents index of species to grow body using index of traitcard to trade
             [[Nat, (optional Nat), (optionalNat), (optionalNat)], ...], - for a board trade action, size of list can be 1, 2, 3, or 4
             [[Nat, Nat, Nat], ...]            - represents index of species to trade the index of it's trait with the given index of the trait in player's hand
             ]
        """
        return [self.food_card_index,
                [gp.to_json() for gp in self.gp_list],
                [gb.to_json() for gb in self.gb_list],
                [bt.to_json() for bt in self.bt_list],
                [rt.to_json() for rt in self.rt_list]]

    def to_proxy_json_action_4(self):
        """
        Parses this player action into an 'action4' json interpretation.
        NOTE: This parsing does not include the 'population' and 'body' tags
        :return: Action4 - json list:
             [Nat,                              - represents index of traitCard to trade for food
             [[Nat, Nat], ...],  - represents index of species to grow population using index of traitcard to trade
             [[Nat, Nat], ...],        - represents index of species to grow body using index of traitcard to trade
             [[Nat, (optional Nat), (optionalNat), (optionalNat)], ...], - for a board trade action, size of list can be 1, 2, 3, or 4
             [[Nat, Nat, Nat], ...]            - represents index of species to trade the index of it's trait with the given index of the trait in player's hand
             ]
        """
        return [self.food_card_index,
                [gp.to_json_proxy() for gp in self.gp_list],
                [gb.to_json_proxy() for gb in self.gb_list],
                [bt.to_json() for bt in self.bt_list],
                [rt.to_json() for rt in self.rt_list]]

