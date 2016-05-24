README

dealerDisplay.py - Contains methods necessary for rendering a Dealer configuration
playerDisplay.py - Contains methods necessary for rendering a Player configuration
run.py - Contains a wrapper that runs both displays, given a Dealer

To run run.py (to display both windows), run './xgui < [inputFile].json' from the
parent directory.

To understand the code in dealerDisplay.py, first understand the Dealer configuration
to be displayed. Functions use the Tkinter library to display different components of
the configuration in a grid-like structure. The file playerDisplay.py simply creates
different display components for a single Player's current PlayerState, using similar
functionality as dealerDisplay.py.
