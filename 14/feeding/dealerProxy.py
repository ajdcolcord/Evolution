#!/usr/bin/env python2.7

import socket, select
from constants import *
from player import Player
from playerState import PlayerState
import json
import sys


class ProxyDealer:

    def __init__(self, host, port):
        """
        Initialize a Socket with the host and port, and create a Player to use as a strategy for Evolution
        :param host: String - IP address of the host
        :param port: Nat - Port number to connect to
        :return: ProxyDealer
        """
        self.player = Player()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((host, port))
            self.sock.send(json.dumps("player"))
        except:
            print "FAILED TO CONNECT TO HOST"

    def run(self):
        """
        Contains logic for which functions should be called when we receive messages from the Evolution game
        Effect: Runs a whole game of Evolution using our Player as a strategy
        :return: Void
        """
        while True:
            ready, i, x = select.select([self.sock], [], [], .1)
            if ready:
                msg = self.sock.recv(MESSAGE_SIZE)
                if msg == '':
                    sys.exit()
                messages = ProxyDealer.parse_incoming_messages(msg)
                for received in messages:
                    self.receive_one_message(received)

    @staticmethod
    def parse_incoming_messages(msg):
        """
        Parses incoming messages, separating them out if two are received at the same time
        :param msg: The incoming message received from the internal state of an Evolution game
        :return: listOf(Message) - Message is a json loaded object from the dealer
        """
        decoder = json.JSONDecoder()
        messages = []
        if msg != json.dumps(OK):
            message, offset = decoder.raw_decode(msg)
            messages.append(message)
            if offset != len(msg):
                message2, offset2 = decoder.raw_decode(msg[offset:])
                messages.append(message2)
        return messages

    def receive_one_message(self, received):
        """
        Effect: Receive one message given order, a dictionary containing information about where we are at in the game
        :param received: JSON value of incoming message
        :return: Void
        """
        if len(received) == START_MSG_LENGTH:
            self.start(received)
        elif len(received) == CHOOSE_MSG_LENGTH:
            self.choose(received)
        elif len(received) == FEED_MSG_LENGTH:
            self.feedNext(received)

    def start(self, msg):
        """
        Effect: Parses the json message and call start on the Player
        :param msg: JSON playerState message
        :return: Void
        """
        watering_hole = msg[0]
        ps = PlayerState.from_json_state(msg[1:])
        self.player.start(ps, watering_hole)

    def choose(self, msg):
        """
        Effect: Parses the json message and calls choose on the Player. Sends json result of choice
        :param msg: JSON list of [list of species before player, list of species after player]
        :return: Void
        """
        choice = Player.parse_cj_dj(msg)
        action4 = self.player.choose(choice[0], choice[1])
        json_action4 = json.dumps(action4.to_proxy_json_action_4())
        self.sock.send(json_action4)

    def feedNext(self, msg):
        """
        Effect: Parses the json message and calls feed on the Player. Sends json result of feed
        :param msg: JSON state of the game.
        :return: Void
        """
        feed_info = PlayerState.from_json_gamestate(msg)
        food_action = self.player.feedNext(feed_info[0], feed_info[1], feed_info[2])
        json_feeding = json.dumps(food_action.to_json())
        self.sock.send(json_feeding)



