#!/usr/bin/env python2.7

class CarnFeedAction:

    def __init__(self, att_species_index, def_player_index, def_species_index):
        """
        CarnFeedAction will have species index in PlayerState to attack, as well as defending player and species indices
        :param att_species_index: Nat - Index of attacking species
        :param def_player_index: Nat - Index of defending playerState
        :param def_species_index: Nat - Index of species in defending playerState to attack
        :return: CarnFeedAction with the populated attributes
        """
        self.att_species_index = att_species_index
        self.def_player_index = def_player_index + 1
        self.def_species_index = def_species_index

    def feed(self, dealer):
        """
        Effect: Add food to carnivore at self.att_species_index using the attack indices in this CarnFeedAction
        :param dealer: The dealer of the Evolution game
        :return: Void
        """
        dealer.feed_result_carnivore(self.att_species_index, self.def_player_index, self.def_species_index)

    def to_json(self):
        """
        Returns a json representation of the carnFeedAction
        @:return: [Nat, Nat, Nat] - indicates a carnivore attack [CarnivoreIndex, DefendingPlayerIndex, DefendingSpeciesIndex]
        """
        return [self.att_species_index, self.def_player_index - 1, self.def_species_index]