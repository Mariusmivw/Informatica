import random
import tkinter as tk
from html.parser import HTMLParser

words = []
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        if ("".join(data.split()) != "" and "".join(data.split()).startswith("Letter") == False):
            words.append(data)

hp = MyHTMLParser()
with open("6Letters.html") as file:
    hp.feed(file.read())


# note: make sure a 2nd guess is possible


secretword = words[random.randint(0,len(words)-1)].upper()
# secretword = "hallo".upper()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="nw")
        self.create_widgets(chars=len(secretword), rows=10)

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

        self.enter = tk.Button(self)
        self.enter["text"] = "Make my guess!"
        self.enter["command"] = self.make_guess
        self.enter.pack(side="bottom")

        self.canvas = tk.Canvas(self, width=chars*(boxsize+boxspacing)-boxspacing, height=rows*(boxsize+boxspacing)-boxspacing)
        self.canvas.pack(side="top")

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
                    self.canvas.create_rectangle((boxsize+boxspacing)*i, (boxsize+boxspacing)*u, boxsize+(boxsize+boxspacing)*i, boxsize+(boxsize+boxspacing)*u, fill="#1768F5", outline="#0A3175")
            self.circle.append(self.canvas.create_oval((boxsize+boxspacing)*i, line*(boxsize+boxspacing), boxsize+(boxsize+boxspacing)*i, boxsize+line*(boxsize+boxspacing), fill="#EEEE11", outline="#DCCE52", state="hidden"))
            self.correct.append(self.canvas.create_rectangle((boxsize+boxspacing)*i, line*(boxsize+boxspacing), boxsize+(boxsize+boxspacing)*i, boxsize+line*(boxsize+boxspacing), fill="#FF0000", outline="#7C0000", state="hidden"))
            self.text.append(self.canvas.create_text(((boxsize+boxspacing)*i+boxsize/2, boxsize/2+line*(boxsize+boxspacing)), text="", font=("", boxsize-20), fill="#FFFFFF"))

        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                      command=root.destroy)
        # self.quit.pack(side="bottom")


    def make_guess(self):
        print("You guessed:", "".join(self.guess))
        secretwordTemp = list(secretword)
        for i in range(len(self.guess)):
            if (self.guess[i] == secretword[i]):
                self.canvas.itemconfig(self.correct[i], state="normal")
                secretwordTemp[secretwordTemp.index(self.guess[i])] = "~"
                if (self.guess == list(secretword)):
                    correct = True
        for i in range(len(self.guess)):
            if (self.guess[i] in secretwordTemp):
                self.canvas.itemconfig(self.circle[i], state="normal")
                secretwordTemp[secretwordTemp.index(self.guess[i])] = "~"
        self.initialize_line(chars=self.chars, rows=self.rows, boxsize=self.boxsize, boxspacing=self.boxspacing, line=self.lines)

    def key(self, event):
        # print(event.keysym)
        if (len(event.keysym) == 1):
            self.guess.append(event.keysym.upper())
            self.canvas.itemconfig(self.text[len(self.guess)-1], text=self.guess[len(self.guess)-1])
        elif (event.keysym == "BackSpace"):
            self.guess = self.guess[:-1]
            self.canvas.itemconfig(self.text[len(self.guess)], text="")
        elif (event.keysym == "Return"):
            self.make_guess()

root = tk.Tk()
app = Application(master=root)
app.bind_all("<KeyPress>", app.key)
app.mainloop()
