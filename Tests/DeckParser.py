
import Tkinter
import tkFileDialog
import Pydeck
from Tkinter import *


class deckParse(Tkinter.Tk):
    def sort_dupes(self, cardList):
        counts = {}
        for i in cardList:
            try:
                counts[i] += 1
            except KeyError:
                counts[i] = 1
        return ["%sx %s" % (v, i)
                for i, v in counts.items()]
        # if v > 1 else "%s" % i -- Use me if you want 1x excluded

    def parse_deck(self, deck_file, cardDB_file):
        Pydeck.loadDatabase(cardDB_file)  # WHOOO MODULES
        mainDeck = Pydeck.Deck("main", 40)
        sideDeck = Pydeck.Deck("side", 15)
        extraDeck = Pydeck.Deck("extra", 15)
        parsePhase = 0
        outBuffer = []
        with open(deck_file) as infile:
            for line in infile:
                if line.rstrip() == "#main":
                    parsePhase = 1
                elif line.rstrip() == "#extra":
                    parsePhase = 2
                elif line.rstrip() == "!side":
                    parsePhase = 3
                elif "#" in line.rstrip():
                    outBuffer.append(line.rstrip().replace("#", ""))
                else:
                    if parsePhase == 1:
                        mainDeck.add(Pydeck.Card(int(line.rstrip())))
                    elif parsePhase == 2:
                        extraDeck.add(Pydeck.Card(int(line.rstrip())))
                    elif parsePhase == 3:
                        sideDeck.add(Pydeck.Card(int(line.rstrip())))
                    else:
                        print("Invalid card ID" + line)

            #Begin output
            #Output deck name
            outBuffer.append("##%s deck" % deck_file.split("/")[len(deck_file.split("/")) - 1].replace(".ydk", ""))
            #Output main deck and count
            outBuffer.append("##Main Deck (%s cards) :" % len(mainDeck))
            strMain = []
            for c in mainDeck:
                strMain.append(c.name)
            for card in self.sort_dupes(strMain):
                outBuffer.append("* %s" % card)

            #Output extra deck and count
            outBuffer.append("##Extra Deck (%s cards) :" % len(extraDeck))
            strExtra = []
            for c in extraDeck:
                strExtra.append(c.name)
            for card in self.sort_dupes(strExtra):
                outBuffer.append("* %s" % card)

            #Output side deck and count
            outBuffer.append("##Side Deck (%s cards) :" % len(sideDeck))
            strSide = []
            for c in sideDeck:
                strSide.append(c.name)
            for card in self.sort_dupes(strSide):
                outBuffer.append("* %s" % card)

            #Final output to textbox
            self.parseResultsTextbox.config(state=NORMAL)
            for line in outBuffer:
                self.parseResultsTextbox.insert(END, line + "  \r\n")
            self.parseResultsTextbox.config(state=DISABLED)

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        #Deck browser button & info label
        deck_info_label = Tkinter.Label(self, text="YDK Deck File", anchor="w", fg="black")
        deck_info_label.grid(column=0, row=0, sticky="W")

        deck_browse_button = Tkinter.Button(self, text="Browse", command=self.on_deck_browse_button_click, anchor="w")
        deck_browse_button.grid(column=1, row=0, sticky="W")

        self.deck_file_label_text = Tkinter.StringVar()
        deck_fileLabel = Tkinter.Label(self, textvariable=self.deck_file_label_text,
                                       anchor="w", fg="black", bg="white", width=50)
        deck_fileLabel.grid(column=2, row=0)

        #Card Database button & info label
        cardDB_info_label = Tkinter.Label(self, text="CardDB File", anchor="w", fg="black")
        cardDB_info_label.grid(column=0, row=1, sticky="W")

        cardDB_browse_button = Tkinter.Button(self, text="Browse",
                                              command=self.on_cardDB_browse_button_click, anchor="w")
        cardDB_browse_button.grid(column=1, row=1, sticky="W")

        self.cardDB_file_label_text = Tkinter.StringVar()
        cardDB_fileLabel = Tkinter.Label(self, textvariable=self.cardDB_file_label_text,
                                         anchor="w", fg="black", bg="white", width=50)
        cardDB_fileLabel.grid(column=2, row=1)

        #Final parse button!
        parseButton = Tkinter.Button(self, text="Parse!", command=self.on_parse_button_click)
        parseButton.grid(column=0, row=2, columnspan=3, sticky="WE")

        #Copy button
        copyButton = Tkinter.Button(self, text="Copy", command=self.on_copy_button_click)
        copyButton.grid(column=0, row=4, columnspan=3, sticky="WE")

        #Results textfield!
        self.parseResultsTextbox = Text(self, background='white', width=50)
        self.parseResultsTextbox.grid(column=0, row=3, columnspan=3)
        self.parseResultsTextbox.config(state=DISABLED)

        # General stuff
        self.grid_columnconfigure(0, weight=1)
        self.resizable(False, False)

    def on_parse_button_click(self):
        self.parse_deck(self.deck_file, self.cardDB_file)

    def on_deck_browse_button_click(self):
        self.deck_file = tkFileDialog.askopenfile(parent=self.parent, mode='rb', title='Locate your .ydk deck file').name
        self.deck_file_label_text.set(self.deck_file)

    def on_cardDB_browse_button_click(self):
        self.cardDB_file = tkFileDialog.askopenfile(parent=self.parent, mode='rb', title='Locate the YGOPRO .CDB file').name
        self.cardDB_file_label_text.set(self.cardDB_file)

    def on_copy_button_click(self):
        self.clipboard_clear()
        self.clipboard_append(self.parseResultsTextbox.get(1.0, END))


if __name__ == "__main__":
    app = deckParse(None)
    app.title("DeckParser v1.0 - Powered by Pydeck")
    app.mainloop()