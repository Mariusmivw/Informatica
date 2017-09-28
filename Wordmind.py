import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(anchor="nw")
        self.create_widgets(chars=5)

    def create_widgets(self, chars=8, rows=5, boxsize=75, boxspacing=0.5):
        # self.hi_there = tk.Button(self)
        # self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")

        # self.guess = tk.Entry(self)
        # self.guess.pack(side="top")

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

        self.guess = []
        self.text = []
        for i in range(chars):
            for u in range(rows):
                self.canvas.create_rectangle(0+(boxsize+boxspacing)*i, 0+(boxsize+boxspacing)*u, boxsize+(boxsize+boxspacing)*i, boxsize+(boxsize+boxspacing)*u, fill="#1768F5", outline="#0A3175")
            self.text.append(self.canvas.create_text(((boxsize+boxspacing)*i+boxsize/2, boxsize/2), text="", font=("", boxsize-20), fill="#FFFFFF"))

        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                      command=root.destroy)
        # self.quit.pack(side="bottom")


    def make_guess(self):
        print("You guessed:", "".join(self.guess))

    def key(self, event):
        # print(event.keysym)
        if len(event.keysym) == 1:
            self.guess.append(event.keysym.upper())
            self.canvas.itemconfig(self.text[len(self.guess)-1], text=self.guess[len(self.guess)-1])
        elif event.keysym == "BackSpace":
            self.guess = self.guess[:-1]
            self.canvas.itemconfig(self.text[len(self.guess)], text="")
        elif event.keysym == "Return":
            self.make_guess()

root = tk.Tk()
app = Application(master=root)
app.bind_all("<KeyPress>", app.key)
app.mainloop()
