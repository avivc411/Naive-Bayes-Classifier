from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from DataProcessor import *
from Classifier import *
import os.path


def build():
    structure = filename+"/Structure.txt"
    train = filename+"/train.csv"
    test = filename+"/test.csv"
    try:
        processor=data_processor(structure, train, int(bins_num.get()), test)
        global data
        data = processor.process_data()
        messagebox.showinfo("Naive Bayes Classifier", "Building classifier using train-set is done!")
    except Exception as e:
        messagebox.showinfo("Naive Bayes Classifier", str(e))


def classify():
    global data
    classifier = Classifier(test=data[3], structure=data[0],
                            train=data[1], meta_data=data[2], bins=bins_num)
    output = open(filename+"/output.txt", "a")
    i=1
    for classification in classifier.classify():
        output.write(str(i)+" "+str(classification)+"\n")
        i+=1
    output.close()
    messagebox.showinfo("Naive Bayes Classifier", "Classification is done!")
    root.destroy()
    sys.exit(0)


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
    global folder_path, filename
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    validation=validate_all_files()
    if not validation[0]:
        folder_path.set("")
        messagebox.showinfo("Naive Bayes Classifier", validation[1])
    return None


def input_check(*args):
    bins = bins_input.get()
    if bins and filename!="":
        try:
            value=int(bins)
            if value>0:
                build_button.config(state='normal')
        except:
            return
    else:
        build_button.config(state='disabled')


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
bins_num = StringVar(root)
bins_num.trace("w", input_check)
bins_lbl = Label(master=root, text="Discretization Bins")
bins_lbl.grid(row=2, column=1)
bins_input = Entry(root, textvariable=bins_num)
bins_input.grid(row=2, column=2)

# build button
build_button = Button(text="Build", command=build)
build_button.grid(row=4, column=2)
build_button.config(state='disabled')

# classify button
classify_button = Button(text="Classify", command=classify)
classify_button.grid(row=5, column=2)

root.mainloop()
