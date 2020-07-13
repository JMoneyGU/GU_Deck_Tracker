#Please don't edit the import statements, thanks!
import tkinter as tk
import tkinter.font as tkFont



#Note: you need to change <USER> to your user. You also might need to change the paths depending on how your files are setup.
logFileName = "C:\\Users\\<USER>\\AppData\\LocalLow\\FuelGames\\Gods Unchained - Version 0.22.1.3365(2020.5.8) - Built at 12_53_44\\output_log_simple.txt"
tempFileName = "C:\\Users\\<USER>\\Desktop\\Gods Unchained Deck Tracker v1-0\\test.txt"
deckFileName = "C:\\Users\\<USER>\\Desktop\\Gods Unchained Deck Tracker v1-0\\deck.txt"

#You can change this too, if needed
defaultFontSize = 20



#Don't edit below this line unless you know what you're doing. (Or do, I don't care. It just might not work right afterwards.)




update = False

def updateTempFile():
    drawnCardList = {}
    logFile = open(logFileName, "r")
    tempFile = open(tempFileName, "w")
    deckFile = open(deckFileName, "r")
    tempFile.write("\n")
    addedCardDict = {}
    
    for line in logFile:
        if "Deck to Hand" in line:
                
            splitStr = line.split("EffectSolver.MoveCard - ")
            secondStr = splitStr[-1]
            splitStr = secondStr.split(" moved from Deck to Hand")
            cardName = splitStr[0]
            if (cardName in drawnCardList.keys()):
                drawnCardList[cardName] = drawnCardList[cardName] + 1
            else :
                drawnCardList[cardName] = 1
        elif "Completed data pack received from server, with TargetData ID instance of: TargetData:(targetType:'Card', playerID:'0'," in line:
            addedCard = line.split("targetName:'")[1].split("',")[0]
            if (addedCard in addedCardDict.keys()) :
                addedCardDict[addedCard] = addedCardDict[addedCard] + 1
            else :
                addedCardDict[addedCard] = 1

    
        

            
    sortedDrawnCardList = sorted(drawnCardList.items())
    sortedDeckCardList = []
    deckCardDict = {}
    for line in deckFile:
        addArr = []
        splitArr = line.split("::")
        addArr.append(splitArr[0])
        addArr.append(splitArr[1].split("\n")[0])
        addArr.append(0)
        sortedDeckCardList.append(addArr)
        deckCardDict[splitArr[0]] = splitArr[1]


    cardsToAdd = []
    for key in addedCardDict.keys():
        added=False
        for card in sortedDeckCardList:
            if (key == card[0]):
                card[1] = int(card[1]) + int(addedCardDict[key])
                card[2] = True
                added=True
                break
        if (added==False):
            newCard = []
            newCard.append(key)
            newCard.append(addedCardDict[key])
            newCard.append(True)
            cardsToAdd.append(newCard)

    count = 0
    for card in cardsToAdd:
        count += 1
        sortedDeckCardList.append(card)

    for drawnCard in sortedDrawnCardList:
        found=False
        for deckCard in sortedDeckCardList:
            
            if (drawnCard[0] == deckCard[0]):
                deckCard[1] = int(deckCard[1]) - int(drawnCard[1])
                found=True
                break
        #at this point we have a card that we did not find in our deck
        if (found == False):
            newCard = []
            newCard.append(drawnCard[0])
            newCard.append(-1*drawnCard[1])
            sortedDeckCardList.append(newCard)

    sortedDrawnCardList = sorted(sortedDrawnCardList)

    for deckCard in sortedDeckCardList:
        if (int(deckCard[1]) > 0):
            if (deckCard[2] == True):
                tempFile.write("**")
            tempFile.write(str(deckCard[0]) + " (" + str(deckCard[1]) + ")\n")
        elif (int(deckCard[1]) < 0):
            tempFile.write("[[" + str(deckCard[0]) + "]] (" + str(deckCard[1]) + ")\n")
    
    logFile.close()
    tempFile.close()



    
class Application(tk.Frame):
    def __init__(self):
        self.win = tk.Tk()
        self.fontStyle = tkFont.Font(family="Times", size=defaultFontSize)
        self.headerLabel = tk.Label(self.win, text="Cards Remaining in Deck:", font=self.fontStyle)
        self.headerLabel.pack(side="top")
        self.win.title("GU Deck Tracker a1.0 - Created by JMoney")
        self.win.geometry("400x800")
        self.win.wm_attributes("-topmost", 1)
        self.labelText = tk.StringVar()
        self.labelText.set("Default text")
        self.label = tk.Label(self.win, textvariable=self.labelText, font=self.fontStyle)
        self.label.place(x=5, y=50)

        self.increaseButton = tk.Button(self.win, text="Increase Font Size", command=self.increase_font_size)
        self.decreaseButton = tk.Button(self.win, text="Decrease Font Size", command=self.decrease_font_size)
        self.createDeckButton = tk.Button(self.win, text="Create New Deck based on Previous Game (must be AI)", command=self.create_deck)
        self.loadDeckButton = tk.Button(self.win, text="Load Deck", command=self.load_deck)
        self.decreaseButton.pack(side="bottom")
        self.increaseButton.pack(side="bottom")
        self.createDeckButton.pack(side="bottom")
        self.loadDeckButton.pack(side="bottom")
                
        self.update_label()
        self.win.mainloop()

    def update_label(self):
        if (update == False):
            self.labelText.set("Warning: Deck not loaded.")
            return
        updateTempFile()
        tempFile = open(tempFileName, "r")
        self.labelText.set(tempFile.read())
        tempFile.close
        self.label.after(1000, self.update_label)

    def increase_font_size(self):
        fontsize = self.fontStyle['size']
        self.fontStyle.configure(size=fontsize+2)

    def decrease_font_size(self):
        fontsize = self.fontStyle['size']
        self.fontStyle.configure(size=fontsize-2)

    def load_deck(self):
        global update
        update=True
        self.update_label()

    def create_deck(self):
        global update
        update=False
        cardNum = 100
        cardList = {}

        logFile = open(logFileName, "r")
        checkString = ":" + str(cardNum) + ","
        for line in logFile:
            if checkString in line:
                cardName = line.split(checkString)[0].split("RuntimeCard: ")[1]
                if (cardName in cardList.keys()):
                    cardList[cardName] = cardList[cardName] + 1
                else:
                    cardList[cardName] = 1
                cardNum = cardNum + 1
                checkString = ":" + str(cardNum) + ","
                if (cardNum == 130):
                    break
        if (cardNum < 130):
            print("Error on deck creation")
            return

        cardFile = open(deckFileName, "w")

        sortedCardList = sorted(cardList.items())
        for card in sortedCardList:
            cardFile.write(str(card[0]) + "::" + str(card[1])+"\n")

        cardFile.close()
        logFile.close()
        update=True
        self.update_label()
        

app = Application()
