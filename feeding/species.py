#!/usr/bin/env python2.7

from constants import *
from traitCard import TraitCard

class Species:

    def __init__(self, food=0, body=0, population=1, trait_cards=None, fatFood=0):
        """
        Creates a new species with the food, body, population, trait_cards, and fatFood
        :param food: Nat - the number of food tokens for this species
        :param body: Nat - the body size of this species
        :param population: Nat - the population size of this species
        :param trait_cards: List of TraitCards (see traitCard.py) for this species
        :param fatFood: Nat - the fat food on this species (for use with fat-tissue trait)
        :return: Species with the populated attributes
        """
        self.food = food
        self.body = body
        self.population = population
        self.trait_cards = trait_cards or []
        self.fatFood = fatFood

    def __eq__(self, that):
        """
        This is the equals method that determines if the inputted 'that' object is equal to this Species
        :param that: Any (object)
        :return: Boolean (true if equal, false otherwise)
        """
        if isinstance(that, Species):
            return self.food == that.food and self.body == that.body and self.population == that.population and \
                    self.trait_cards == that.trait_cards and self.fatFood == that.fatFood
        else:
            return False

    def isHungry(self):
        """
        Determines if this species is hungry (food < population)
        :return: True if species is hungry, False otherwise
        """
        return self.food < self.population

    def getFatRoom(self):
        """
        Finds the difference between body size and fatFood value. Assumes this species has fat-tissue trait
        :return: The number of fat food tokens available for storage
        """
        return self.body - self.fatFood

    def hasTrait(self, trait_type):
        """
        Determines if this species contains the given trait card type
        :param trait_type: String - the trait card type to look for
        :return: Boolean - True if the trait is contained in this species
        """
        for trait_card in self.trait_cards:
            if trait_card.name == trait_type:
                return True
        return False

    def isLarger(self, other_species):
        """
        Determines if this species is larger than other_species based on body, population, and food in that order.
        :param other_species: One of: Species or False
        :return: Boolean - True if this species is larger than the other_species
        """
        if not other_species:
            return True

        if self.population == other_species.population and self.food == other_species.food:
            return self.body > other_species.body
        elif self.population == other_species.population:
            return self.food > other_species.food
        else:
            return self.population > other_species.population

    def toJsonArray(self):
        """
        Creates a JSON representation of this species
        :return: JSON Species: [["food",Nat],
                             ["body",Nat],
                             ["population",Nat],
                             ["traits",LOT]]
                or JSON Species+: [["food",Nat],
                                 ["body",Nat],
                                 ["population",Nat],
                                 ["traits",LOT]
                                 ["fat-food" ,Nat]]
        """
        result = [["food", self.food],
                  ["body", self.body],
                  ["population", self.population],
                  ["traits", [trait.name for trait in self.trait_cards]]]

        if self.fatFood > 0:
            result.append(["fat-food", self.fatFood])

        return result

    @staticmethod
    def jsonToSituation(situation):
        """
        Converts the given Situation (JSON) into a Python Tuple of (Species, Species, OptSpecies, OptSpecies)
        :param situation: [json_species, json_species, json_opt_species, json_opt_species]
        :return: Tuple (Species, Species, Species or False, Species or False)
        """
        defend = Species.convertSpecies(situation[0])
        attack = Species.convertSpecies(situation[1])

        if not attack or not defend:
            quit()

        lNeighbor = Species.convertSpecies(situation[2]) or False
        rNeighbor = Species.convertSpecies(situation[3]) or False

        return defend, attack, lNeighbor, rNeighbor

    @staticmethod
    def convertSpecies(jsonSpecies):
        """
        Create Species out of json representation of species
        JSONSpecies = [["food",Nat],
                    ["body",Nat],
                   ["population",Nat],
                    ["traits",LOT],
              OPT: ["fat-food",Nat]]
        :param jsonSpecies: the Species in JSON
        :return: OptSpecies - Species or False
        """
        try:
            if jsonSpecies[0][0] == FOOD_LABEL and jsonSpecies[1][0] == BODY_LABEL and \
                    jsonSpecies[2][0] == POPULATION_LABEL and jsonSpecies[3][0] == TRAITS_LABEL:
                food = jsonSpecies[0][1]
                body = jsonSpecies[1][1]
                population = jsonSpecies[2][1]
                traits = []
                fatFood = 0
                hasFatTissue = False
                for trait in jsonSpecies[3][1]:
                    hasFatTissue = hasFatTissue or trait == FAT_TISSUE
                    traits.append(TraitCard(trait))
                if len(jsonSpecies) == 5 and hasFatTissue and jsonSpecies[4][0] == FAT_FOOD_LABEL:
                    fatFood = jsonSpecies[4][1]
                return Species(food, body, population, traits, fatFood)
            else:
                return False
        except:
            return False

    @staticmethod
    def isAttackable(defend, attack, lNeighbor, rNeighbor):
        """
        Determines if the given defender species is attackable by the attacker,
        while taking into consideration the rules provided by the traits on the
        left and right neighbors
        :param defend: Species - the defender
        :param attack: Species - the attacker
        :param lNeighbor: Species or False - left neighbor
        :param rNeighbor: Species or False - right neighbor
        :return: Boolean - True if the defender is attackable by the attacker, False otherwise
        """
        if not attack.hasTrait(CARNIVORE):
            return False

        canDefBurrowing = defend.hasTrait(BURROWING) and defend.food == defend.population
        canDefClimbing = defend.hasTrait(CLIMBING) and not attack.hasTrait(CLIMBING)
        canDefSymbiosis = defend.hasTrait(SYMBIOSIS) and (rNeighbor and rNeighbor.body > defend.body)
        canLeftDefAmbush = not attack.hasTrait(AMBUSH) and lNeighbor and lNeighbor.hasTrait(WARNING_CALL)
        canRightDefAmbush = not attack.hasTrait(AMBUSH) and rNeighbor and rNeighbor.hasTrait(WARNING_CALL)
        canDefHardShell = defend.hasTrait(HARD_SHELL) and Species.canDefendHardShell(attack, defend)
        canDefHerding = defend.hasTrait(HERDING) and Species.canDefendHerding(attack, defend)
        defendable = [canDefBurrowing, canDefClimbing, canLeftDefAmbush, canRightDefAmbush, canDefSymbiosis,
                                    canDefHardShell, canDefHerding]

        return not any(defendables for defendables in defendable)

    @staticmethod
    def canDefendHardShell(attacker, defender):
        """
        Is this hard-shell defender able to be attacked by attacker?
        :param attacker: Species - The attacking species
        :param defend: Species - Defending species with hard-shell trait
        :return: True if defender can be attacked
        """
        attackBody = attacker.body
        if attacker.hasTrait(PACK_HUNTING):
            attackBody += attacker.population
        return attackBody - defender.body < 4

    @staticmethod
    def canDefendHerding(attacker, defender):
        """
        Is this herding defender able to be attacked by attacker?
        :param attacker: Species - The attacking species
        :param defend: Species - Defending species with herding trait
        :return: True if defender can be attacked
        """
        attackPopulation = attacker.population
        if defender.hasTrait(HORNS):
            attackPopulation -= 1
        return attackPopulation - defender.population <= 0

    def feed(self, num_food=1):
        """
        Effect: Adds num_food food tokens to this species food
        :param num_food: Nat - Number of food tokens to give. Default to 1
        :return Void
        """
        if self.food + num_food > self.population:
            raise Exception("Cannot feed this many tokens to this species")

        self.food += num_food

    def store_fat(self, fat_tokens):
        """
        Effect: Adds the given number of fat_tokens to this species' fat food
        :param fat_tokens: Number of food tokens to store
        :return: Void
        """
        if self.fatFood + fat_tokens > self.body or fat_tokens == 0 or not self.hasTrait(FAT_TISSUE):
            raise Exception("Cannot store this many fat food tokens on this species")

        self.fatFood += fat_tokens

    def decrease_population(self, attack_points=1):
        """
        Effect: Decreases this species' population by attack_points
        :param attack_points: Number of animals killed in this species. default to 1
        :return: Void
        """
        self.population -= attack_points
        self.food = min(self.population, self.food)

    def increase_population(self):
        """
        Effect: Increases this species' population by 1 if possible
        :return: Void
        """
        if self.population < 7:
            self.population += 1

    def increase_body(self):
        """
        Effect: Increases this species' body size by 1 if possible
        :return: Void
        """
        if self.body < 7:
            self.body += 1

    def transfer_fat_food(self):
        """
        Effect: Transfers as much fat-food to food on this species as possible
        :return: Void
        """
        food_to_add = min(self.population - self.food, self.fatFood)
        self.food += food_to_add
        self.fatFood -= food_to_add