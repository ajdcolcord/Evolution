#!/usr/bin/env python2.7

class FatStoreAction:

    def __init__(self, fat_species_index, storage_num):
        """
        Initialize FatStoreAction with the index of the species to store food on, and the num_food to store.
        :param fat_species_index: Nat - Index of species in PlayerState
        :param storage_num: Nat - Number of food to store on fat tissue species
        :return: FatStoreAction with populated fields
        """
        self.fat_species_index = fat_species_index
        self.storage_num = storage_num

    def feed(self, dealer):
        """
        Effect: Add fat food to species at self.fat_species_index
        :param dealer: The dealer of the Evolution game
        return: Void
        """
        dealer.feed_result_fat_food(self.fat_species_index, self.storage_num)

    def to_json(self):
        """
        Returns a json representation of the fatStoreAction
        @:return: [Nat, Nat] - indicates a fat - tissue species and desired number of food to store
        """
        return [self.fat_species_index, self.storage_num]