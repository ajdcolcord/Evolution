#!/usr/bin/env python2.7


class VegFeedAction:

    def __init__(self, veg_index):
        """
        Initialize this VegFeedAction with the index of the species a player wishes to feed
        :param veg_index: Nat - Index of Veg in PlayerState
        :return: VegFeedAction with the given veg_index
        """
        self.veg_index = veg_index

    def feed(self, dealer):
        """
        Effect: Add food to this VegFeedAction's veg species at self.veg_index
        :param dealer: The dealer for the Evolution game
        :return: Void
        """
        dealer.feed_result_vegetarian(self.veg_index)

    def to_json(self):
        """
        Returns a json representation of the vegFeedAction
        @:return: Nat - indicates the hungry vegetarian to feed
        """
        return self.veg_index