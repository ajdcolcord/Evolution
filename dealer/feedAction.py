#!/usr/bin/env python2.7

from abc import ABCMeta, abstractmethod
from noFeedAction import NoFeedAction
from vegFeedAction import VegFeedAction
from fatStoreAction import FatStoreAction
from carnFeedAction import CarnFeedAction

class FeedAction:

    __metaclass__ = ABCMeta

    @abstractmethod
    def feed(self, dealer):
        """
        Should be implemented by each subclass to feed a species. If it is not, raise an Error
        :param dealer: The dealer of the Evolution game
        """
        raise NotImplementedError()

    @staticmethod
    def parse_food_action(foodAction):
        """
        Given a JSON foodAction, delegate to a subclass depending on foodAction value
        :param: foodAction is one of:
                    - False - indicates no species desired to be fed
                    - Nat - indicates the hungry vegetarian to feed
                    - [Nat, Nat] - indicates a fat-tissue species and desired number of food to store
                    - [Nat, Nat, Nat] - indicates a carnivore attack
                                    [CarnivoreIndex, DefendingPlayerIndex, DefendingSpeciesIndex]
        :return: FeedAction - The necessary type of FeedAction to instantiate
        """
        if isinstance(foodAction, bool):
            if foodAction:
                raise Exception("True is not a valid foodAction")
            else:
                return NoFeedAction()

        elif isinstance(foodAction, int):
            return VegFeedAction(foodAction)

        elif isinstance(foodAction, list) and len(foodAction) == 2:
            return FatStoreAction(foodAction[0], foodAction[1])

        elif isinstance(foodAction, list) and len(foodAction) == 3:
            return CarnFeedAction(foodAction[0], foodAction[1], foodAction[2])
        else:
            raise Exception("Invalid feed action")

    @abstractmethod
    def to_json(self):
        """
        Returns a json representation of the feedAction - to be implemented by subclasses
        - False - indicates no species desired to be fed
        - Nat - indicates the hungry vegetarian to feed
        - [Nat, Nat] - indicates a fat - tissue species and desired number of food to store
        - [Nat, Nat, Nat] - indicates a carnivore attack [CarnivoreIndex, DefendingPlayerIndex, DefendingSpeciesIndex]
        """
        raise NotImplementedError()


FeedAction.register(NoFeedAction)
FeedAction.register(VegFeedAction)
FeedAction.register(FatStoreAction)
FeedAction.register(CarnFeedAction)