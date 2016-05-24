from Tkinter import *
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'feeding'))
from constants import *

class PlayerDisplay(Frame):

    def __init__(self, playerState, master=None):
        """
        Create a scene of this Dealer configuration in an Evolution Game
        :param playerState: The current PlayerState to display
        :param master:
        :return: a DealerDisplay object to be used by the Dealer for rendering
        """
        self.frame = Frame.__init__(self, master)

        self.canvas = Canvas(master, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)

        Frame.__init__(self, self.canvas)

        self.create_scroll_bars(master)

        self.createPlayerStateDisplay(playerState, self)

    def create_scroll_bars(self, master):
        """
        Create vertical and horizontal scrollbar on the master frame
        :param master: The frame to place the scrollbars on
        :return Void
        """
        self.vbar = Scrollbar(master, orient=VERTICAL, command=self.canvas.yview)
        self.hbar = Scrollbar(master, orient=HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.vbar.set)
        self.canvas.configure(xscrollcommand=self.hbar.set)

        self.vbar.pack(side=RIGHT, fill=Y)
        self.hbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas.create_window((0, 0), window=self)
        self.bind("<Configure>", self.OnFrameConfigure)

    def OnFrameConfigure(self, event):
        """
        Function to add scrollregion to canvas. Needed for scrollbar
        :param event: Event needed to bind a scrollbar
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def createPlayerStateDisplay(self, playerState, master):
        """
        Effect: Formats a playerState representation on the master frame
        :param playerState: The playerState to display
        :param master: The parent widget to display on
        """
        playerFrame = Frame(master, bg="grey", bd=5, highlightbackground='black')
        playerFrame.grid(row=1)

        playerText = "Player #" + str(playerState[0][1]) + "    Food Bag: " + str(playerState[2][1])

        idLabel = Label(playerFrame, text=playerText, bg=playerFrame["bg"])
        idLabel.grid(row=0)

        if len(playerState[1][1]) > 0:
            self.createSpeciesListDisplay(playerState[1][1], playerFrame)

        if len(playerState) == 4:
            self.createTraitCardListDisplay(playerState[3][1], playerFrame, False)

    def createSpeciesDisplay(self, species, rowIndex, master):
        """
        Effect: Formats a species representation on the master frame at row rowIndex in a grid
        :param species: Species to display
        :param rowIndex: current row to display species in
        :param master: Widget to display on
        """
        speciesFrame = Frame(master, background='orange', bd=3)
        speciesFrame.grid(row=rowIndex)

        speciesText = "Food: " + str(species[0][1]) + " Body: " + str(species[1][1]) + " Population: " + str(species[2][1])
        speciesLabel = Label(speciesFrame, text=speciesText)
        speciesLabel.grid(row=0)

        self.createTraitCardListDisplay(species[3][1], speciesFrame, True)

        if len(species) == 5 and species[4][1] != 0:
            fatFoodLabel = Label(speciesFrame, text="Fat Food: " + str(species[4][1]))
            fatFoodLabel.grid(row=2)


    def createSpeciesListDisplay(self, speciesList, master):
        """
        Effect: Formats a listOf(species) representation on the master frame
        :param speciesList: List of Species to display
        :param master: Widget to display on
        """
        allSpeciesFrame = Frame(master, background='red', bd=3)
        allSpeciesFrame.grid(row=2)

        speciesLabel = Label(allSpeciesFrame, text="Species...", bg=allSpeciesFrame["bg"])
        speciesLabel.grid(row=0)

        for i in range(len(speciesList)):
            speciesListFrame = Frame(allSpeciesFrame)
            speciesListFrame.grid(row=i+1)
            species = speciesList[i]
            self.createSpeciesDisplay(species, i, speciesListFrame)

    def createTraitCardDisplay(self, traitCard, rowIndex, master, speciesListFlag=False):
        """
        Effect: Formats a TraitCard representation on the master frame at rowIndex on master's grid
        :param traitCard: the trait card to display
        :param rowIndex: the current row to display TraitCard
        :param master: Widget to place this display on
        :param speciesListFlag: True if the traits displayed are on a Species
        """
        traitFrame = Frame(master, background='red', bd=1)
        traitFrame.grid(row=rowIndex)

        if not speciesListFlag:
            traitText = "Trait: " + str(traitCard[1]) + " | Food Value: " + str(traitCard[0])
        else:
            traitText = "Trait: " + str(traitCard)

        traitLabel = Label(traitFrame, text=traitText)
        traitLabel.grid(row=0)


    def createTraitCardListDisplay(self, traitList, master, speciesListFlag=False):
        """
        Effect: Formats a listOf(TraitCard) representation on the master frame
        :param traitList: List of TraitCards to display
        :param master: Widget to display on
        :param speciesListFlag: True if the traits to display are on a species
        """
        allTraitFrame = Frame(master, background='lightblue', bd=3)
        allTraitFrame.grid()

        if not speciesListFlag:
            handLabel = Label(allTraitFrame, text="Hand...", bg=allTraitFrame["bg"])
            handLabel.grid(row=0)

        for i in range(len(traitList)):
            traitListFrame = Frame(allTraitFrame)
            traitListFrame.grid(row=i+1)
            trait = traitList[i]
            self.createTraitCardDisplay(trait, i, traitListFrame, speciesListFlag)
