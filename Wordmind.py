import math
import time
import random
import tkinter as tk
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_data(self, data): # Redifining the handle_data function
        if ("".join(data.split()) != "" and "".join(data.split()).startswith("Letter") == False):
            words.append(data) # add the words to the word list

hp = MyHTMLParser()
words = []
wordfiles = ["5Letters.html", "6Letters.html"]

for i in range(len(wordfiles)):
    with open(wordfiles[i]) as file:        # getting the contents of '6Letters.html'
        hp.feed(file.read())                # feeding it to the HTML-parser so it can do its thing

with open("additionalWords.txt") as file:   #adding words from the additionalWords list
    addedWords = file.read().upper().split()
    for i in range(len(addedWords)):
        words.append(addedWords[i-1])

secretword = words[random.randint(0,len(words)-1)].upper()
# secretword = "zelden".upper()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="nw")
        self.create_widgets(chars=len(secretword))
        self.stay = []
        self.canvas.itemconfig(self.text[0], text=secretword[0], fill="#AFAFAF")
        self.canvas.itemconfig(self.correct[0], state="normal")

    def create_widgets(self, chars=6, rows=5, boxsize=75, boxspacing=1):
        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")

        # self.guess = tk.Entry(self)
        # self.guess.pack(side="top")
        self.chars      = chars
        self.rows       = rows
        self.boxsize    = boxsize
        self.boxspacing = boxspacing

        self.canvas = tk.Canvas(self, width=chars*(boxsize+boxspacing)-boxspacing, height=rows*(boxsize+boxspacing)-boxspacing)
        self.canvas.pack(side="top") # ^^^^making a canvas with at the right size^^

        self.enter = tk.Button(self) # making a guess button, if you don't like pressing Enter
        self.enter["text"] = "Make my guess!"
        self.enter["command"] = self.make_guess
        self.enter.pack(side="left")

        self.again = tk.Button(self) # making a restart button, if you don't feel like solving your currnt word
        self.again["text"] = "Restart"
        self.again["command"] = self.restart
        self.again.pack(side="left")



        # self.text = tk.Label(self)
        # self.text.pack()

        # self.canvas.create_line(0, 0, 200, 100)
        # self.canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
        self.initialize_line(chars=chars, rows=rows, boxsize=boxsize, boxspacing=boxspacing)

    def initialize_line(self, chars=6, rows=5, boxsize=75, boxspacing=1, line=0):
        self.text    = []
        self.guess   = []
        self.circle  = []
        self.correct = []
        self.lines = line + 1
        for i in range(chars):
            if (line==0):
                for u in range(rows):
                    self.startTime = time.time() # setting the startTime so I can measure how long it took to guess the word
                    self.canvas.create_rectangle((boxsize+boxspacing)*i, (boxsize+boxspacing)*u, boxsize+(boxsize+boxspacing)*i, boxsize+(boxsize+boxspacing)*u, fill="#1768F5", outline="#0A3175")
            self.circle.append(self.canvas.create_oval((boxsize+boxspacing)*i, line*(boxsize+boxspacing), boxsize+(boxsize+boxspacing)*i, boxsize+line*(boxsize+boxspacing), fill="#EEEE11", outline="#DCCE52", state="hidden"))
            self.correct.append(self.canvas.create_rectangle((boxsize+boxspacing)*i, line*(boxsize+boxspacing), boxsize+(boxsize+boxspacing)*i, boxsize+line*(boxsize+boxspacing), fill="#FF0000", outline="#7C0000", state="hidden"))
            self.text.append(self.canvas.create_text(((boxsize+boxspacing)*i+boxsize/2, boxsize/2+line*(boxsize+boxspacing)), text="", font=("", boxsize-20), fill="#FFFFFF"))
            # [80-83] >> creating the proper backgrounds for the text, and the text itself

        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                      command=root.destroy)
        # self.quit.pack(side="bottom")

    def restart(self):
        self.canvas.delete("all") # clearing the canvas
        secretword = words[random.randint(0,len(words)-1)].upper() # selecting a new secret word
        self.initialize_line()
        self.stay = [0] # there are no chars that should stay yet, except the first letter
        self.canvas.itemconfig(self.text[0], text=secretword[0], fill="#AFAFAF") # setting the first letter
        self.canvas.itemconfig(self.correct[0], state="normal") # making the background red

    def make_guess(self): # go to the next function first to know what this is about (line 133)
        print("You guessed: " + "".join(self.guess)) # info on what the guessed word was in the console
        secretwordTemp = list(secretword) # just the same, but this one can be alterd without consequences
        guess = self.guess # so works this one

        for i in range(len(self.guess)):
            if (self.guess[i] == secretword[i]): # the letter is in the correct position
                self.canvas.itemconfig(self.correct[i], state="normal") # making the background red
                secretwordTemp[i] = "~" # making note that the this letter has been guessed, for when a letter is typed in multiple times (like in: 'tree')
                self.stay.append(i) # this letter should stay next round

        for i in range(len(self.guess)):
            if (self.guess[i] in secretwordTemp): # the letter is somewhere in the word
                self.canvas.itemconfig(self.circle[i], state="normal") # making the yellow circle appear (behind the red square)
                secretwordTemp[secretwordTemp.index(self.guess[i])] = "~" # making note that the this letter has been guessed, for when a letter is typed in multiple times (like in: 'tree')

        self.initialize_line(chars=self.chars, rows=self.rows, boxsize=self.boxsize, boxspacing=self.boxspacing, line=self.lines)
        for i in range(len(self.stay)): # making the letter that were correct show and have the red background in the next round
            self.canvas.itemconfig(self.text[self.stay[i]], text=secretword[self.stay[i]], fill="#AFAFAF")
            self.canvas.itemconfig(self.correct[self.stay[i]], state="normal")

        if (guess == list(secretword)): # the word has been guessed
            print("You found it!!!")
            print("It took you " + str(math.floor((time.time() - self.startTime)*10)/10) + "s") # info to the console about how long it took to guess
            self.canvas.itemconfig(self.text[-1], text="s")
            for i in range(len(str(math.floor((time.time() - self.startTime)*10)/10))):
                self.canvas.itemconfig(self.text[-i-2], text=list(str(math.floor((time.time() - self.startTime)*10)/10))[-i-1])
            for i in range(5-len(str(math.floor((time.time() - self.startTime)*10)/10))):
                self.canvas.itemconfig(self.text[i], text="")
            # [122-126] >> making the time appear correctly in the GUI

            self.popup = Popup(tk.Tk())
            self.popup.bind_all("<KeyPress>", self.popup.key)
            self.popup.mainloop()

    def key(self, event): # this runs whenever a key is pressed
        # print(event.keysym)
        if (len(event.keysym) == 1): # the key pressed was probably a letter (could be a number, but that's your own stupidity)
            self.guess.append(event.keysym.upper())
            self.canvas.itemconfig(self.text[len(self.guess)-1], text=self.guess[len(self.guess)-1], fill="#FFFFFF")
            # ^^^^making the letter white, because it could have been gray from beeing right in a guess before and not yet typed in
            if (len(self.guess)-1 in self.stay and self.guess[len(self.guess)-1] != secretword[len(self.guess)-1]): # the letter typed is not the displayed, (correct), letter
                self.canvas.itemconfig(self.correct[len(self.guess)-1], state="hidden") # making the background not red anymore because it's now wrong

        elif (event.keysym == "BackSpace"):
            self.guess = self.guess[:-1] # remove the last guessed letter from the list
            self.canvas.itemconfig(self.text[len(self.guess)], text="") # removing that letter from the screen
            if (len(self.guess) in self.stay): # you already know the letter that should be there
                self.canvas.itemconfig(self.text[len(self.guess)], text=secretword[len(self.guess)], fill="#AFAFAF") # making the letter that should be there appear and gray
                self.canvas.itemconfig(self.correct[len(self.guess)], state="normal") # making the background red again

        elif (event.keysym == "Return"):
            if (len(self.guess) == len(secretword)): # the typed in word is the correct length
                self.make_guess() # now you can go back to that function (line 98)

class Popup(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="nw")
        self.label = tk.Label(self)
        self.label["text"] = "Do you want to play again? (Y/N)"
        self.label.pack() # made a piece of text appear with the text above
        self.input = tk.Entry(self)
        self.input.pack() # created an input
        self.input.focus_force() # focussing on that input

    def key(self, event):
        if (event.keysym == "Return"):          # if Enter is pressed
            val = self.input.get().upper()      # get the users input
            self._root().destroy()              # exit this popup window
            if (val == "Y" or val == "YES"):    # vcalidate the input
                app.restart()                   # guess a new word
            else:                               # the user didn't want to play again
                root._root().destroy()          # exit the program

root = tk.Tk()
app = Application(master=root)
app.bind_all("<KeyPress>", app.key) # actually making the key function run every time a key is pressed
app.mainloop()
