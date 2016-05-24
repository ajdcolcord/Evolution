import sys, os
from Tkinter import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'gui'))
from playerDisplay import PlayerDisplay
from dealerDisplay import DealerDisplay

def displayDealer(configuration):
        """
        Creates a Tk display for the Dealer, and returns it
        (does not run the main loop)
        :param: dealer - Dealer object to display
        :return: Tk object
        """
        root = Tk()
        root.title("Dealer")
        app = DealerDisplay(configuration, master=root)
        return app

def displayPlayer(playerState):
        """
        Creates a Tk display for the Player (with the given playerState)
        and returns it (does not run the main loop)
        :param playerState the playerState information of this player to display
        :return: Tk object
        """
        root = Tk()
        root.title("Player: " + str(playerState[0][1]))
        app = PlayerDisplay(playerState, master=root)
        return app

def runBothWindows(dealer):
    """
    Creates TK objects by calling the displayDealer method and the displayPlayer method (on the first playerState of
    the given dealer), and runs the main loop
    :param dealer: the dealer that contains the information to be displayed
    :return: Void
    """
    displayDealer(dealer)
    displayPlayer(dealer[0][0]).mainloop()
