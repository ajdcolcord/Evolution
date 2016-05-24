#!/usr/bin/env python2.7


from playerAction import PlayerAction
import json
import select
import sys, os
import datetime
from feedAction import FeedAction
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'feeding'))
from constants import *


class ProxyPlayer:

    def __init__(self, sock, info=None):
        """
        Initializes a new ProxyPlayer with the given socket connection
        :param sock: the socket connection for this new ProxyPlayer
        """
        self.sock = sock
        self.info = info

    @staticmethod
    def new(sock, info=None):
        """
        Given an id, create and return a player object
        :param sock - the socket connection used to send requests/receive responses from the remote player
        :return: ProxyPlayer with the given socket connection
        """
        return ProxyPlayer(sock, info)

    def start(self, playerState, watering_hole):
        """
        Calls the start method to the player through the socket connection, sending over it's State
        :param playerState: the PlayerState handed by the dealer containing the reference to the remote player
        :return: Void
        """
        state = [watering_hole] + playerState.to_json_state()
        self.sock.send(json.dumps(state))

    def choose(self, prev_species, later_species):
        """
        Calls the choose method to the player through the socket connection, sending over the list of players before
        it, and the list of players after it. If the player takes too long to respond, raise exception.
        @:param: prev_species - List of [List of Species]
        @:param: later_species - List of [List of Species]
        @:return: PlayerAction - the player's choice parsed into a PlayerAction object for the Dealer
        """
        json_prev_species, json_later_species = [], []
        for species_list in prev_species:
            json_prev_species.append([species.toJsonArray() for species in species_list])
        for species_list in later_species:
            json_later_species.append([species.toJsonArray() for species in species_list])

        cj_dj = [json_prev_species, json_later_species]
        self.sock.send(json.dumps(cj_dj))

        request_time = datetime.datetime.now()
        while True:
            ready, i, x = select.select([self.sock], [], [], 0.1)
            if ready:
                result = self.sock.recv(MESSAGE_SIZE)
                return PlayerAction.parse_proxy_player_action(json.loads(result))

            if (datetime.datetime.now() - request_time).seconds > TIMEOUT:
                raise Exception("Player Timed Out")

    def feedNext(self, playerState, wateringHole, otherPlayers):
        """
        Sends over -- [Natural, [Species+, ..., Species+], Cards, Natural+, LOB]
        :param playerState:
        :param wateringHole:
        :param otherPlayers:
        :return:
        """
        newOtherPlayers = []
        for species_list in otherPlayers:
            newOtherPlayers.append([species.toJsonArray() for species in species_list])
        state = playerState.to_json_state() + [wateringHole] + [newOtherPlayers]
        self.sock.send(json.dumps(state))

        request_time = datetime.datetime.now()
        while True:
            ready, i, x = select.select([self.sock], [], [], 0.1)
            if ready:
                result = self.sock.recv(MESSAGE_SIZE)
                return FeedAction.parse_food_action(json.loads(result))

            if (datetime.datetime.now() - request_time).seconds > TIMEOUT:
                raise Exception("Player Timed Out")

    def exit_game(self):
        """
        Effect: Closes this socket, ending the game for the external player
        :return: Void
        """
        self.sock.close()