#!/usr/bin/env python2.7

class NoFeedAction:

    def feed(self, dealer):
        """
        Effect: add first playerstate in dealer.playerstates id to the dealer's list of non-hungry players
        :param dealer: The dealer of the Evolution game
        :return: Void
        """
        dealer.fullPlayerIds.append(dealer.playerStates[0].id)

    def to_json(self):
        """
        Returns a json representation of the noFeedAction
        @:return: False - indicates no species desired to be fed
        """
        return False