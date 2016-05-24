README

API Methods
The API methods for the Dealer class are contained in dealer/dealer.py
The API methods for the Internal Player representations are contained in feeding/playerState.py
The API methods for the External Player representations are contained in feeding/player.py


main - The main program to run a full Evolution game
client - Starts up an external player proxy connecting to the main server
compile - returns an exit code of 0 (can't pre-compile python)
configuration_parsing.py - Contains code that parses json to dealer
configuration_parsing_tests.py - Contains unit tests for configuration_parsing.
test_xattack.py - a suite of unit tests for xattack
test_xfeed.py - a suite of unit tests for xfeed
xattack - executable for the dealer to access species.isAttackable
xfeed - executable for the dealer to access player.feed
xgui - executable used to open dealer and player display windows from json input.
xstep - executable for the dealer to access dealer.feed1
xstep4 - executable used for running the step4 method in dealer.py
rest.txt - Contains a wishlist of remaining Player methods
xgui_tests - directory for the xgui example displays
xstep_tests - directory for the xstep test harness input/output files
xstep4_tests - directory for the xstep4 test harness input/output files
xsilly_tests - directory for the xsilly test harness input/output files
api/ - the directory containing protocol designs for the Evolution game (see api.txt)
remote/ - the directory containing protocol designs for the Evolution game with a remote player (see remote.txt)
__init__.py - necessary for this to be considered a package

To run a game from the server side:
    run main, run './main [n]', where n is the number of players you wish to join (between 3 and 8)
    The host and port for this server default to '0.0.0.0' and 5999 respectively (see constants.py)

To join a game from the client side:
    run './client [HOST] [PORT]', where HOST and PORT correspond to the server you wish to join

To run xfeed, run ./xfeed < input-json > out
To run xattack, run ./xattack < input-json > out
To run xstep, run ./xstep < input-json > out
To run xstep4, run ./xstep4 < input-json > out
To run xsilly, run ./xsilly < input-json > out
To run xgui, run ./xgui < input-json

main will create a Dealer, and hand it external players connected through TCP, and call dealer.runGame()
All timing constraints and host and port information for the networked game is contained in constants.py

To understand xfeed and xattack, you may wish to read the code it calls. 
Follow the README in /feeding to understand that code, then read the 
programs themselves.

To understand xstep, you may wish to read the code contained dealer/dealer.py.

To understand xstep4, you may wish to read the code contained in dealer/dealer.py.

To understand xsilly, you may wish to read the code contained in feeding/player.py.

To understand xgui, you may wish to read the code and README contained in
the /gui directory.

