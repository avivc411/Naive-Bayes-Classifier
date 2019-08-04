from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from DataProcessor import *
import pandas
import os.path


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Assignment IV")

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:")

        vcmd = master.register(self.validate)  # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)

        self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

        self.add_button.grid(row=2, column=0)
        self.subtract_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2, sticky=W+E)

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        else:  # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0, END)


def build():
    structure = filename+"/Structure.txt"
    train = filename+"/train.csv"
    test = filename+"/test.csv"
    processor=data_processor(structure, train, test)

def classify():
    print("classifying")


def validate_all_files():
    if not os.path.isdir(filename):
        return False, "The Chosen File Is Not A Folder"
    elif not os.path.isfile(filename+"/Structure.txt"):
        return False, "Structure.txt Doesn't Exists"
    elif not os.path.isfile(filename+"/train.csv"):
        return False, "train.csv Doesn't Exists"
    elif not os.path.isfile(filename+"/test.csv"):
        return False, "test.csv Doesn't Exists"
    else:
        return True, None


def browse_button():
    # Allow user to select a directory and store it in global var called folder_path
    global folder_path, filename
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    validation=validate_all_files()
    if not validation[0]:
        folder_path.set("")
        messagebox.showinfo("Error", validation[1])
    return None


def input_check(*args):
    bins = disc_input.get()
    if bins and filename!="":
        try:
            value=int(bins)
            if value>0:
                build_button.config(state='normal')
        except:
            return
    else:
        build_button.config(state='disabled')


print "Not Graduate,Graduate".split(",")

root = Tk()
root.geometry("500x400+400+300")

filename = ""
folder_path = StringVar()
# browse
browse_lbl = Label(master=root, text="Directory Path")
browse_lbl.grid(row=1, column=1)
input_path = Entry(root, textvariable=folder_path)
input_path.grid(row=1, column=2)
browse_button = Button(text="Browse", command=browse_button)
browse_button.grid(row=1, column=5)

# Discretization
var = StringVar(root)
var.trace("w", input_check)
disc_lbl = Label(master=root, text="Discretization Bins")
disc_lbl.grid(row=2, column=1)
disc_input = Entry(root, textvariable=var)
disc_input.grid(row=2, column=2)

# build button
build_button = Button(text="Build", command=build)
build_button.grid(row=4, column=2)
build_button.config(state='disabled')

# classify button
classify_button = Button(text="Classify", command=classify)
classify_button.grid(row=5, column=2)

root.mainloop()
