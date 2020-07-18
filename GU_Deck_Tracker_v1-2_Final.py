#Please don't edit the import statements, thanks!
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import getpass
userName = getpass.getuser()
import os



#Note: You might need to change the paths depending on how your files are setup.
logFileName = "C:\\Users\\" + userName + "\\AppData\\LocalLow\\FuelGames\\Gods Unchained - Version 0.22.1.3365(2020.5.8) - Built at 12_53_44\\output_log_simple.txt"
tempFileName = os.getcwd() + "\\test.txt"
deckFileName = os.getcwd() + "\\deck.txt"
iconLocation = "C:\\Users\\" + userName + "\\Desktop\\Gods Unchained Deck Tracker v1-1\\JMoney_Icon.ico"

#You can change these too, if needed:


#This is how big the font size is to start (keep between 6 and 50 probably)
defaultFontSize = 14

#This is how transparent the window is when you launch the program (1 is full visibility, 0 is completely transparent)
alphaLevel = 1

#Defaults the program to night mode or not (put "True" no quotes instead of "False" to launch in night mode)
nightMode=False










#Don't edit below this line unless you know what you're doing. (Or do, I don't care. It just might not work right afterwards.)


cardsInDeck = 30
version = "v1.2"
update = False

def updateTempFile():
    global cardsInDeck
    drawnCardList = {}
    logFile = open(logFileName, "r")
    tempFile = open(tempFileName, "w")
    deckFile = open(deckFileName, "r")
    tempFile.write("\n")
    
    cardsInDeck = 30
    
    for line in logFile:
        if "Deck to Hand" in line:
            cardsInDeck  = cardsInDeck - 1
            splitStr = line.split("EffectSolver.MoveCard - ")
            secondStr = splitStr[-1]
            splitStr = secondStr.split(" moved from Deck to Hand")
            cardName = splitStr[0]
            if (cardName in drawnCardList.keys()):
                drawnCardList[cardName] = drawnCardList[cardName] + 1
            else :
                drawnCardList[cardName] = 1



    
        

            
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



  
    for drawnCard in sortedDrawnCardList:
        found=False
        for deckCard in sortedDeckCardList:
            
            if (drawnCard[0] == deckCard[0]):
               deckCard[1] = int(deckCard[1]) - int(drawnCard[1])
               found=True
               break

    sortedDrawnCardList = sorted(sortedDrawnCardList)

    tempFile.write("Cards Remaining in Deck: " + str(cardsInDeck) + "\n\n")

    for deckCard in sortedDeckCardList:
        if (int(deckCard[1]) > 0):
            if (deckCard[2] == True):
                tempFile.write("**")
            
            tempFile.write(str(deckCard[0]) + " (" + str(deckCard[1]) + ") [" + str(round(100*float(deckCard[1])/cardsInDeck,1)) + "%]\n")
    tempFile.write("\n--Extra Cards Drawn--\n\n")
    for deckCard in sortedDeckCardList:
        if (int(deckCard[1]) < 0):
            tempFile.write("**" + str(deckCard[0]) + "** (" + str(-1*deckCard[1]) + ")\n")
    
    logFile.close()
    tempFile.close()



    
class Application(tk.Frame):
    global alphaLevel

    def __init__(self):
	
        self.win = tk.Tk()
       

        try:
            self.win.iconbitmap(self, default=iconLocation)
        except tk.TclError:
            print("Oops, no icon!")

    
        self.daymodeStyle = ttk.Style()
        self.daymodeStyle.configure("daymode", foreground="black", background="white")
        
        
        self.win.attributes('-alpha', alphaLevel)
        self.fontStyle = tkFont.Font(family="Times", size=defaultFontSize)
       
        self.win.title("GU Deck Tracker " + version + " - Created by JMoney")
        self.win.geometry("300x700")
        self.win.wm_attributes("-topmost", 1)
        self.labelText = tk.StringVar()
        self.labelText.set("Default text")
        self.label = ttk.Label(self.win, textvariable=self.labelText, font=self.fontStyle)
        self.label.pack(side="top")

        self.increaseButton = tk.Button(self.win, text="Increase Font Size", command=self.increase_font_size)
        self.decreaseButton = tk.Button(self.win, text="Decrease Font Size", command=self.decrease_font_size)
        self.createDeckButton = tk.Button(self.win, text="Create Deck (AI Only)", command=self.create_deck)
        self.loadDeckButton = tk.Button(self.win, text="Load Deck", command=self.load_deck)
        self.increaseVisButton = tk.Button(self.win, text="More Transparent", command=self.decrease_visibility)
        self.decreaseVisButton = tk.Button(self.win, text="Less Transparent", command=self.increase_visibility)
        self.changeNightButton = tk.Button(self.win, text="Nightmode On/Off", command=self.change_nightmode)



      
        self.changeNightButton.pack(side="bottom", fill=tk.X)
        self.loadDeckButton.pack(side="bottom", fill=tk.X)
        self.createDeckButton.pack(side="bottom", fill=tk.X)
        self.decreaseVisButton.pack(side="bottom", fill=tk.X)
        self.increaseVisButton.pack(side="bottom", fill=tk.X)
        self.decreaseButton.pack(side="bottom", fill=tk.X)
        self.increaseButton.pack(side="bottom", fill=tk.X)
        self.update_nightmode()
        self.update_label()
        self.win.mainloop()
            
        
               

    def update_nightmode(self):
        global nightMode
        if (nightMode == True):

            self.win.configure(bg='black')

            
            labelStyleNight = ttk.Style()
            labelStyleNight.configure("Night.TLabel", foreground="white", background="black")

           
            self.label.configure(style="Night.TLabel")
            self.changeNightButton.configure(fg="white", bg="black")
            self.loadDeckButton.configure(fg="white", bg="black")
            self.createDeckButton.configure(fg="white", bg="black")
            self.decreaseVisButton.configure(fg="white", bg="black")
            self.increaseVisButton.configure(fg="white", bg="black")
            self.decreaseButton.configure(fg="white", bg="black")
            self.increaseButton.configure(fg="white", bg="black")

            
        else:
            
            self.win.configure(bg='white')

            labelStyleNight = ttk.Style()
            labelStyleNight.configure("Day.TLabel", foreground="black", background="white")

           
            self.label.configure(style="Day.TLabel")
            self.changeNightButton.configure(fg="black", bg="white")
            self.loadDeckButton.configure(fg="black", bg="white")
            self.createDeckButton.configure(fg="black", bg="white")
            self.decreaseVisButton.configure(fg="black", bg="white")
            self.increaseVisButton.configure(fg="black", bg="white")
            self.decreaseButton.configure(fg="black", bg="white")
            self.increaseButton.configure(fg="black", bg="white")




    def update_label(self):
        if (update == False):
            self.labelText.set("Warning: Deck not loaded.")
            self.label.after(1000, self.update_label)
            return
        updateTempFile()
        tempFile = open(tempFileName, "r")
        self.labelText.set(tempFile.read())
        tempFile.close
        self.label.after(1000, self.update_label)
        

    def increase_font_size(self):
        fontsize = self.fontStyle['size']
        if (fontsize < 50):
            self.fontStyle.configure(size=fontsize+2)

    def decrease_font_size(self):
        fontsize = self.fontStyle['size']
        if (fontsize > 6):
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

    def increase_visibility(self):
        global alphaLevel
        if (alphaLevel < 1):
            alphaLevel += .1
            self.win.attributes("-alpha", alphaLevel)

    def decrease_visibility(self):
        global alphaLevel
        if (alphaLevel > .15):
            alphaLevel -= .1
            self.win.attributes("-alpha", alphaLevel)

    def change_nightmode(self):
        global nightMode
        
        if (nightMode == True):
            nightMode = False
            self.update_nightmode()
        else:
            nightMode = True
            self.update_nightmode()
        

app = Application()
