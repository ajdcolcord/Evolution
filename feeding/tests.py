#!/usr/bin/env python2.7

import unittest
import json
import glob
from player import Player
from playerState import PlayerState
from species import Species
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dealer'))
from dealer import Dealer

ATTACK_TEST_PATH = "attack_tests/"
HW_5_TEST_PATH = "homework_5_tests/"
HW_6_TEST_PATH = "homework_6_tests/"
HW_7_TEST_PATH = "homework_7_tests/"
HW_8_TEST_PATH = "homework_8_tests/"
HW_10_TEST_PATH = "homework_10_tests/"
HW_11_TEST_PATH = "homework_11_tests/"
HW_12_TEST_PATH = "homework_12_tests/"
FEED_TEST_PATH = "feed_tests/"


class Tests(unittest.TestCase):

    def testSpeciesIsAttackable(self):
        os.chdir(HW_5_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        os.chdir("..")
        # Loop through the files in homework_5_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(HW_5_TEST_PATH + inFiles[i], 'r') as input:
                    with open(HW_5_TEST_PATH + outFiles[i], 'r') as output:
                        print "HW-5 - " + str(inFileName)
                        input = json.load(input)
                        output = json.load(output)
                        defend, attack, lNeighbor, rNeighbor = Species.jsonToSituation(input)
                        self.assertEqual(Species.isAttackable(defend, attack, lNeighbor, rNeighbor), output)
        os.chdir("..")

    def testFeed(self):
        os.chdir(HW_6_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        # Loop through the files in homework_6_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(inFiles[i], 'r') as input:
                    with open(outFiles[i], 'r') as output:
                        print "HW-6 - " + str(inFileName)
                        try:
                            output = json.load(output)
                        except:
                            output = -1
                        finally:
                            input = json.load(input)
                            ps = PlayerState.convertPlayerState(input[0])
                            wateringHole = int(input[1])
                            otherPlayers = []
                            for player in input[2]:
                                if player:
                                    otherPlayers.append(PlayerState.convertPlayerState(player).species)
                            player = Player(ps.id)
                            if output != -1:
                                self.assertEqual(player.feedNext(ps, wateringHole, otherPlayers).to_json(), output)
                            else:
                                with self.assertRaises(Exception):
                                    player.feedNext(ps, wateringHole, otherPlayers)
        os.chdir("..")


    def testAgainstHW7TestFest(self):
        os.chdir(HW_7_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        # Loop through the files in homework_7_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(inFiles[i], 'r') as input:
                    with open(outFiles[i], 'r') as output:
                        print "HW-7 - " + str(inFileName)
                        # if os.stat(outFiles[i]).st_size > 0:
                        try:
                            output = json.load(output)
                        except:
                            output = -1
                        finally:
                            input = json.load(input)
                            ps = PlayerState.convertPlayerState(input[0])
                            wateringHole = int(input[1])
                            otherPlayers = []
                            for player in input[2]:
                                if player:
                                    otherPlayers.append(PlayerState.convertPlayerState(player).species)
                            player = Player(ps.id)
                            if output != -1:
                                self.assertEqual(player.feedNext(ps, wateringHole, otherPlayers).to_json(), output)
                            else:
                                with self.assertRaises(Exception):
                                    player.feedNext(ps, wateringHole, otherPlayers)
        os.chdir("..")

    def testAgainstHW8Fest(self):
        os.chdir(HW_8_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        # Loop through the files in homework_8_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(inFiles[i], 'r') as input:
                    with open(outFiles[i], 'r') as output:
                        print "HW-8 - " + str(inFileName)
                        if os.stat(outFiles[i]).st_size > 0:
                            output = json.load(output)
                        else:
                            output = -1
                        input = json.load(input)
                        dealer = Dealer.create_dealer_from_configuration(input)
                        dealer.feed1()
                        json_dealer = dealer.create_json_from_dealer()
                        self.assertEquals(json.dumps(json_dealer), json.dumps(output))
        os.chdir("..")

    def testAgainstHW10Fest(self):
        os.chdir(HW_10_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        # Loop through the files in homework_8_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                with open(inFiles[i], 'r') as input:
                    with open(outFiles[i], 'r') as output:
                        print "HW-10 - " + str(inFileName)
                        if os.stat(outFiles[i]).st_size > 0:
                            output = json.load(output)
                        else:
                            output = -1
                        input = json.load(input)
                        dealer = Dealer.create_dealer_from_configuration(input)
                        dealer.feed1()
                        json_dealer = dealer.create_json_from_dealer()
                        self.assertEquals(json.dumps(json_dealer), json.dumps(output))

        os.chdir("..")

    def testAgainstHW11xstep4(self):
        os.chdir(HW_11_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        # Loop through the files in homework_8_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:
                if inFileName not in ["0067-2657-1", "0067-2657-2", "0067-2657-3"]:
                    with open(inFiles[i], 'r') as input:
                        with open(outFiles[i], 'r') as output:
                            print "HW-11 xstep4 - " + str(inFileName)
                            if os.stat(outFiles[i]).st_size > 0:
                                output = json.load(output)
                            else:
                                output = -1

                            step4_input = json.load(input)

                            dealer = Dealer.create_dealer_from_configuration(step4_input[0])
                            step4_actions = Dealer.parse_step4(step4_input[1])
                            dealer.step4(step4_actions)
                            dealer.playerStates = dealer.originalPlayerOrder
                            json_dealer = dealer.create_json_from_dealer()

                            self.assertEquals(json.dumps(json_dealer), json.dumps(output))

        os.chdir("..")

    def testAgainstHW12xstep4(self):
        os.chdir(HW_12_TEST_PATH)
        inFiles = glob.glob("*-in.json")
        outFiles = glob.glob("*-out.json")
        # Loop through the files in homework_8_tests directory and make sure inputs match expected outputs
        for i in range(len(inFiles)):
            inFileName = inFiles[i].replace("-in.json", "")
            outFileName = outFiles[i].replace("-out.json", "")
            # Make sure that these are the same corresponding test files
            self.assertEquals(inFileName, outFileName)
            if inFileName == outFileName:

                with open(inFiles[i], 'r') as input:
                    with open(outFiles[i], 'r') as output:
                        print "HW-12 xsilly - " + str(inFileName)
                        if os.stat(outFiles[i]).st_size > 0:
                            output = json.load(output)
                        else:
                            output = -1


                        json_choice = json.load(input)
                        player = Player.new(1)
                        choice = Player.parse_choice(json_choice)
                        player.start(choice[0], 0)
                        action = player.choose(choice[1], choice[2]).to_json_action_4()

                        self.assertEquals(json.dumps(action), json.dumps(output))

        os.chdir("..")


if __name__ == "__main__":
    unittest.main()
