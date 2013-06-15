import sqlite3
import random

def loadDatabase(cardDB):
    """Connects to the passed card database

    @type cardDB: string
    @param cardDB: The path to the .cdb file being connected to
    @return: Nothing
    """
    global lookup
    conn = sqlite3.connect(cardDB)
    lookup = conn.cursor()


def getText(cardID, dataType):
    """
    @type cardID: int
    @type dataType: string
    @param cardID: The number of the card being looked up
    @param dataType: The column to look up
    @rtype: string
    @return: A string from the TEXTS column of the joined database
    """
    global lookup
    lookup.execute('SELECT ' + dataType + ' FROM texts WHERE id = ' + str(cardID))
    return lookup.fetchone()[0]


def getData(cardID, dataType):
    """
    @type cardID: int
    @type dataType: string
    @param cardID: The number of the card being looked up
    @param dataType: The column to look up
    @rtype: string
    @return: A string from the DATAS column of the joined database
    """
    global lookup
    lookup.execute('SELECT ' + dataType + ' FROM datas WHERE id = ' + str(cardID))
    return lookup.fetchone()[0]


def getCardsFromName(cardName):
    """Finds a list cards with the given string in their title
    @rtype: int
    @return: A list of possible card IDs
    """
    global lookup
    lookup.execute('SELECT id FROM texts WHERE name LIKE "' + cardName + '"')
    l = lookup.fetchone()
    if l:
        return l[0]
    else:
        return ""


class Card:
    def __init__(self, c):

        """Initializes a new Card.
        @type cid: int
        @param cid: The number/name of the card being created
        """
        if int(c):
            self.cardID = c
        else:
            self.cardID = getCardsFromName(c)[0]

        self.name = getText(self.cardID, 'name')
        self.description = getText(self.cardID, 'desc')
        self.attack = getData(self.cardID, 'atk')
        self.defense = getData(self.cardID, 'def')
        self.level = getData(self.cardID, 'level')
        self.typeNum = getData(self.cardID, 'type')
        self.typeString = self.getTypeStringFromID(self.typeNum)
        self.attribute = self.getAttributeFromID(getData(self.cardID, 'attribute'))

    def getTypeStringFromID(self, cardType):
        """
        @rtype: string
        @return: The type of the Card as a human-readable string
        """
        return {
            2:       'Spell Card',
            4:       'Trap Card',
            17:      'Monster',
            33:      'Effect Monster',
            65:      'Fusion Monster',
            97:      'Fusion / Effect Monster',
            129:     'Ritual Monster',
            130:     'Ritual Spell',
            161:     'Ritual / Effect Monster',
            545:     'Spirit Monster',
            1057:    'Union Monster',
            2081:    'Gemini Monster',
            4113:    'Tuner / Normal Monster',
            4129:    'Tuner / Effect Monster',
            8193:    'Synchro Monster',
            8225:    'Synchro / Effect Monster',
            12321:   'Synchro / Tuner / Effect Monster',
            16401:   'Token',
            65538:   'Quick-Play Spell Card',
            131074:  'Continuous Spell Card',
            131076:  'Continuous Trap Card',
            262146:  'Equip Spell Card',
            524290:  'Field Spell Card',
            1048580: 'Counter Trap Card',
            2097185: 'Flip Effect Monster',
            4194337: 'Toon Monster',
            8388609: 'Xyz Monster',
            8388641: 'Xyz / Effect Monster',
        }.get(cardType, cardType)

    def getAttributeFromID(self, ID):
        """
        @rtype: string
        @return: The attribute of the Card
        """
        cardType = ID
        return {
            1:  'Earth',
            2:  'Water',
            4:  'Fire',
            8:  'Wind',
            16: 'Light',
            32: 'Dark',
            64: 'Divine'
        }.get(cardType, cardType)


class Deck:
    # Make Iterable
    def __iter__(self):
        return self.cardList.__iter__()

    def __len__(self):
        return len(self.cardList)

    def __contains__(self, v):
        return v in self.cardList

    def __getitem__(self, v):
        return self.cardList[v]

    def __init__(self, decktype, limit):
        """Creates a new Deck
        @type decktype: string
        @type limit: int
        @param decktype: Identifies deck. If type is "extra", only allows Xyz, Synchro, and Fusion monsters.
        @param limit: How many Cards are allowed in the Deck. 0 for unlimited.
        """
        self.cardList = []
        self.decktype = decktype
        self.limit = limit
        if self.limit == 0:
            self.limit = 999999

    def add(self, card):
        """Adds a Card to the Deck
        @type card: Card
        @param card: the Card to add
        @rtype: bool
        @return Whether the Card was added successfully
        """
        if self.decktype == "extra":
            s = card.typeString
            if ("Xyz" in s or "Synchro" in s or "Fusion" in s) and len(self.cardList) <= self.limit:
                self.cardList.append(card)
                return True
            else:
                return False
        else:  # Normal Deck
            if len(self) <= self.limit:
                self.cardList.append(card)
                return True
            else:
                return False
    def shuffle(self):
        """Shuffles the cards in the Deck"""
        random.shuffle(self.cardList)