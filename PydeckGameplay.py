import Pydeck

class Player:
    class Hand:
        def __iter__(self):
            return self.cardList.__iter__()

        def __len__(self):
            return len(self.cardList)

        def __contains__(self, v):
            return v in self.cardList

        def __getitem__(self, v):
            return self.cardList[v]

        def __init__(self):
            """Creates a new Hand
            """
            self.cardList = []

    def __init__(self, deck, sideDeck, extraDeck):
        self.deck = deck
        self.sideDeck = sideDeck
        self.extraDeck = extraDeck
        self.hand = self.Hand()
        self.drawAmount = 1
    def drawCard(self):
        self.hand.append(self.deck.pop())
