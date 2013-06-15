import Pydeck
import sys

if len(sys.argv) > 1:
    Pydeck.loadDatabase('Resources/cards.cdb')
    if not sys.argv[1] == "":
        #cardID = Pydeck.getCardsFromName(sys.argv[1])
        c = Pydeck.Card(sys.argv[1])
        print(c.name)

        if "Monster" in c.typeString:
            print("Level %s" % c.level + " " + c.attribute + " " + c.typeString)
            print("Atk: %s" % c.attack)
            print("Def: %s" % c.defense)
        else:
            print(c.typeString)
        print(c.description)
    else:
        print("No card with that name exists!")
else:
    print("Bad input! Use like this: 'CardID.py <card name>'")