#!/usr/bin/env python2.7

import unittest
from species import *
from traitCard import *
from constants import *

HW_5_TEST_PATH = "homework_5_tests/"


class SpeciesTests(unittest.TestCase):

    def testIsHungry(self):
        hungrySpecies = Species(4, 6, 5)
        self.assertTrue(hungrySpecies.isHungry())
        fullSpecies = Species(4, 6, 4)
        self.assertFalse(fullSpecies.isHungry())

    def testGetFatRoom(self):
        hungrySpecies = Species(4, 6, 5, [FAT_TISSUE])
        self.assertEquals(hungrySpecies.getFatRoom(), 6)
        someRoomSpecies = Species(4, 6, 4, [FAT_TISSUE], 3)
        self.assertEquals(someRoomSpecies.getFatRoom(), 3)
        noRoomSpecies = Species(4, 6, 4, [FAT_TISSUE], 6)
        self.assertEquals(noRoomSpecies.getFatRoom(), 0)

    def testHasTrait(self):
        species1 = Species(4, 6, 5, [])
        trait1 = TraitCard(FAT_TISSUE, 0)
        self.assertFalse(species1.hasTrait(CARNIVORE))
        species2 = Species(4, 6, 5, [trait1])
        self.assertFalse(species2.hasTrait(CARNIVORE))
        self.assertTrue(species2.hasTrait(FAT_TISSUE))

    def testIsLarger(self):
        species1 = Species(4, 6, 5, [])
        equalSpecies = Species(4, 6, 5, [])
        largerBodySpecies = Species(4, 7, 5, [])
        smallerBodySpecies = Species(4, 5, 5, [])
        largerPopulationSpecies = Species(4, 6, 6, [])
        smallerPopulationSpecies = Species(4, 6, 4, [])
        largerFoodSpecies = Species(5, 6, 5, [])
        smallerFoodSpecies = Species(3, 6, 5, [])

        self.assertFalse(species1.isLarger(equalSpecies))
        self.assertTrue(species1.isLarger(smallerBodySpecies))
        self.assertTrue(species1.isLarger(smallerFoodSpecies))
        self.assertTrue(species1.isLarger(smallerPopulationSpecies))
        self.assertFalse(species1.isLarger(largerBodySpecies))
        self.assertFalse(species1.isLarger(largerFoodSpecies))
        self.assertFalse(species1.isLarger(largerPopulationSpecies))

    def testToJsonArray(self):
        species_plus = [[FOOD_LABEL, 3],
                        [BODY_LABEL, 4],
                        [POPULATION_LABEL, 5],
                        [TRAITS_LABEL, [FAT_TISSUE]],
                        [FAT_FOOD_LABEL, 3]]
        species = Species(3, 4, 5, [TraitCard(FAT_TISSUE, 2)], 3)
        self.assertEquals(species.toJsonArray(), species_plus)
        species_no_fat_json = [[FOOD_LABEL, 3],
                            [BODY_LABEL, 4],
                            [POPULATION_LABEL, 5],
                            [TRAITS_LABEL, [CARNIVORE]]]
        species_no_fat = Species(3, 4, 5, [TraitCard(CARNIVORE, 2)])
        self.assertEquals(species_no_fat.toJsonArray(), species_no_fat_json)

    def testJsonToSituation(self):
        species_plus = [[FOOD_LABEL, 3],
                        [BODY_LABEL, 4],
                        [POPULATION_LABEL, 5],
                        [TRAITS_LABEL, [FAT_TISSUE]],
                        [FAT_FOOD_LABEL, 3]]
        species = Species(3, 4, 5, [TraitCard(FAT_TISSUE, 2)], 3)
        species_no_fat_json = [[FOOD_LABEL, 3],
                            [BODY_LABEL, 4],
                            [POPULATION_LABEL, 5],
                            [TRAITS_LABEL, [CARNIVORE]]]
        species_no_fat = Species(3, 4, 5, [TraitCard(CARNIVORE, 2)])
        json_situation = [species_plus, species_no_fat_json, species_plus, False]
        created_situation = Species.jsonToSituation(json_situation)

        species_1 = created_situation[0]
        self.assertEquals(species_1.body, species.body)
        self.assertEquals(species_1.food, species.food)
        self.assertEquals(species_1.population, species.population)
        self.assertEquals(species_1.trait_cards[0].name, species.trait_cards[0].name)

        self.assertEquals(created_situation[3], False)

        species_2 = created_situation[1]
        self.assertEquals(species_2.body, species_no_fat.body)
        self.assertEquals(species_2.food, species_no_fat.food)
        self.assertEquals(species_2.population, species_no_fat.population)
        self.assertEquals(species_2.trait_cards[0].name, species_no_fat.trait_cards[0].name)

        species_3 = created_situation[2]
        self.assertEquals(species_3.body, species.body)
        self.assertEquals(species_3.food, species.food)
        self.assertEquals(species_3.population, species.population)
        self.assertEquals(species_3.trait_cards[0].name, species.trait_cards[0].name)


    def testConvertSpecies(self):
        goodJson = [[FOOD_LABEL, 3],
                    [BODY_LABEL, 4],
                    [POPULATION_LABEL, 5],
                    [TRAITS_LABEL, [CARNIVORE]]]
        badJson = [[FOOD_LABEL, 3],
                   ["nonsense", 4],
                   [POPULATION_LABEL, 4],
                   [TRAITS_LABEL, [CARNIVORE]]]

        self.assertFalse(Species.convertSpecies(badJson))
        self.assertFalse(Species.convertSpecies(False))
        self.assertEqual(Species.convertSpecies(goodJson).body, 4)
        self.assertEqual(Species.convertSpecies(goodJson).food, 3)
        self.assertEqual(Species.convertSpecies(goodJson).population, 5)
        self.assertEqual(Species.convertSpecies(goodJson).trait_cards[0], TraitCard(CARNIVORE))

    def testIsAttackable(self):
        att_species_1 = Species(1, 2, 3, [TraitCard(CARNIVORE), TraitCard(AMBUSH)])
        att_species_2 = Species(2, 3, 4)
        climbing_attacker = Species(2, 5, 4, [TraitCard(CLIMBING), TraitCard(CARNIVORE)])
        pack_hunt_attacker = Species(1, 1, 6, [TraitCard(CARNIVORE), TraitCard(PACK_HUNTING)])

        def_species_1 = Species(1, 2, 3)

        self.assertFalse(Species.isAttackable(def_species_1, att_species_2, False, False))

        burrow_species_1 = Species(4, 3, 4, [TraitCard(BURROWING)])
        burrow_species_2 = Species(3, 3, 4, [TraitCard(BURROWING)])

        self.assertFalse(Species.isAttackable(burrow_species_1, att_species_1, False, False))
        self.assertTrue(Species.isAttackable(burrow_species_2, att_species_1, False, False))

        climbing_species_1 = Species(3, 3, 3, [TraitCard(CLIMBING)])

        self.assertFalse(Species.isAttackable(climbing_species_1, att_species_1, False, False))
        self.assertTrue(Species.isAttackable(climbing_species_1, climbing_attacker, False, False))

        symbiosis_species_1 = Species(1, 1, 3, [TraitCard(SYMBIOSIS)])

        self.assertFalse(Species.isAttackable(symbiosis_species_1, att_species_1, False, def_species_1))
        self.assertTrue(Species.isAttackable(symbiosis_species_1, att_species_1, def_species_1, False))

        warning_call_species = Species(3, 3, 3, [TraitCard(WARNING_CALL)])

        self.assertFalse(Species.isAttackable(def_species_1, climbing_attacker, warning_call_species, False))
        self.assertFalse(Species.isAttackable(def_species_1, climbing_attacker, False, warning_call_species))
        self.assertTrue(Species.isAttackable(def_species_1, att_species_1, warning_call_species, warning_call_species))

        hard_shell_species = Species(3, 1, 3, [TraitCard(HARD_SHELL)])

        self.assertFalse(Species.isAttackable(hard_shell_species, att_species_1, False, False))
        self.assertTrue(Species.isAttackable(hard_shell_species, climbing_attacker, False, False))
        self.assertTrue(Species.isAttackable(hard_shell_species, pack_hunt_attacker, False, False))

        herding_species = Species(2, 2, 2, [TraitCard(HERDING)])
        herding_horns = Species(2, 2, 3, [TraitCard(HORNS), TraitCard(HERDING)])

        self.assertTrue(Species.isAttackable(herding_species, att_species_1, False, False))
        self.assertTrue(Species.isAttackable(herding_species, climbing_attacker, False, False))
        self.assertFalse(Species.isAttackable(herding_horns, climbing_attacker, False, False))

    def test_can_defend_hard_shell(self):
        att_species_1 = Species(1, 2, 3, [TraitCard(CARNIVORE), TraitCard(AMBUSH)])
        climbing_attacker = Species(2, 5, 4, [TraitCard(CLIMBING), TraitCard(CARNIVORE)])
        pack_hunt_attacker = Species(1, 1, 6, [TraitCard(CARNIVORE), TraitCard(PACK_HUNTING)])

        hard_shell_species = Species(3, 1, 3, [TraitCard(HARD_SHELL)])

        self.assertTrue(Species.canDefendHardShell(att_species_1, hard_shell_species))
        self.assertFalse(Species.canDefendHardShell(climbing_attacker, hard_shell_species))
        self.assertFalse(Species.canDefendHardShell(pack_hunt_attacker, hard_shell_species))

    def test_can_defend_herding(self):
        att_species_1 = Species(1, 2, 4, [TraitCard(CARNIVORE), TraitCard(AMBUSH)])
        att_species_2 = Species(1, 2, 5, [TraitCard(CARNIVORE), TraitCard(AMBUSH)])

        herding_species = Species(2, 2, 2, [TraitCard(HERDING)])
        herding_horns = Species(2, 2, 3, [TraitCard(HORNS), TraitCard(HERDING)])

        self.assertFalse(Species.canDefendHerding(att_species_1, herding_species))
        self.assertTrue(Species.canDefendHerding(att_species_1, herding_horns))
        self.assertFalse(Species.canDefendHerding(att_species_2, herding_horns))

    def test_feed(self):
        species = Species(1, 2, 3)

        self.assertEquals(species.food, 1)
        self.assertEquals(species.body, 2)
        self.assertEquals(species.population, 3)

        species.feed(2)

        self.assertEquals(species.food, 3)
        self.assertEquals(species.body, 2)
        self.assertEquals(species.population, 3)

        with self.assertRaises(Exception):
            species.feed()

    def test_store_fat(self):
        species = Species(1, 2, 3, [TraitCard(FAT_TISSUE)], 0)

        self.assertEquals(species.food, 1)
        self.assertEquals(species.body, 2)
        self.assertEquals(species.population, 3)
        self.assertEquals(species.fatFood, 0)

        species.store_fat(2)

        self.assertEquals(species.food, 1)
        self.assertEquals(species.body, 2)
        self.assertEquals(species.population, 3)
        self.assertEquals(species.fatFood, 2)

        with self.assertRaises(Exception):
            species.store_fat(1)

    def test_decrease_population(self):
        species = Species(3, 3, 3)

        self.assertEquals(species.food, 3)
        self.assertEquals(species.body, 3)
        self.assertEquals(species.population, 3)

        species.decrease_population(2)

        self.assertEquals(species.food, 1)
        self.assertEquals(species.body, 3)
        self.assertEquals(species.population, 1)

    def test_increase_population(self):
        species = Species(3, 3, 3)
        max_pop_species = Species(3, 4, 7)

        self.assertEquals(species.food, 3)
        self.assertEquals(species.body, 3)
        self.assertEquals(species.population, 3)

        species.increase_population()

        self.assertEquals(species.food, 3)
        self.assertEquals(species.body, 3)
        self.assertEquals(species.population, 4)

        self.assertEquals(max_pop_species.food, 3)
        self.assertEquals(max_pop_species.body, 4)
        self.assertEquals(max_pop_species.population, 7)

        max_pop_species.increase_population()

        self.assertEquals(max_pop_species.food, 3)
        self.assertEquals(max_pop_species.body, 4)
        self.assertEquals(max_pop_species.population, 7)

    def test_increase_body(self):
        species = Species(3, 3, 3)
        max_body_species = Species(3, 7, 6)

        self.assertEquals(species.food, 3)
        self.assertEquals(species.body, 3)
        self.assertEquals(species.population, 3)

        species.increase_body()

        self.assertEquals(species.food, 3)
        self.assertEquals(species.body, 4)
        self.assertEquals(species.population, 3)

        self.assertEquals(max_body_species.food, 3)
        self.assertEquals(max_body_species.body, 7)
        self.assertEquals(max_body_species.population, 6)

        max_body_species.increase_body()

        self.assertEquals(max_body_species.food, 3)
        self.assertEquals(max_body_species.body, 7)
        self.assertEquals(max_body_species.population, 6)

    def test_transfer_fat_food(self):
        fat1 = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 3)
        empty_fat = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        fat2 = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 6)
        new_fat1 = Species(5, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        new_empty_fat = Species(2, 5, 7, [TraitCard(FAT_TISSUE)], 0)
        new_fat2 = Species(7, 5, 7, [TraitCard(FAT_TISSUE)], 1)

        fat1.transfer_fat_food()
        empty_fat.transfer_fat_food()
        fat2.transfer_fat_food()

        self.assertEquals(fat1, new_fat1)
        self.assertEquals(empty_fat, new_empty_fat)
        self.assertEquals(fat2, new_fat2)


if __name__ == "__main__":
    unittest.main()
