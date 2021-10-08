from tkinter import *
from tkinter import font 
from tkinter import ttk 

class App:
    def __init__(self):

            # chat window which is currently hidden
            self.Window = Tk()
            self.Window.withdraw()
            # login window
            self.login = Toplevel()
            # set the title
            self.login.title("Login")
            self.login.resizable(width = False,
                                 height = False)
            self.login.configure(width = 400,
                                 height = 300)
            # create a Label
            self.pls = Label(self.login,
                           text = "Please login to continue",
                           justify = CENTER,
                           font = "Helvetica 14 bold")
            self.pls.place(relheight = 0.15,
                           relx = 0.2,
                           rely = 0.07)
            # create a Label
            self.labelName = Label(self.login,
                                   text = "Name: ",
                                   font = "Helvetica 12")
            self.labelName.place(relheight = 0.2,
                                 relx = 0.1,
                                 rely = 0.2)
            # create a entry box for
            # tyoing the message
            self.entryName = Entry(self.login,
                                 font = "Helvetica 14")
            self.entryName.place(relwidth = 0.4,
                                 relheight = 0.12,
                                 relx = 0.35,
                                 rely = 0.2)
            # set the focus of the curser
            self.entryName.focus()
            # create a Continue Button
            # along with action
            self.go = Button(self.login,
                             text = "CONTINUE",
                             font = "Helvetica 14 bold",
                             command = lambda: self.goAhead(self.entryName.get()))
            self.go.place(relx=0.4,
                          rely=0.55)

            self.Window.mainloop()

    def goAhead(self, name):
        print(name)
        self.login.destroy()


app = App()