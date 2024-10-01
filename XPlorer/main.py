from tkinter import *
from tkinter import simpledialog, messagebox, font
import shutil
import os
import ctypes
import pathlib
import pickle
from turtle import bgcolor
import tkinter as tk
# import win32gui
# import win32con

# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# hidden window
# hidden_window = Tk()
# hidden_window.withdraw()
# hidden_window.overrideredirect(False)

class CustomTitleBar(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.master = master
        self.pack(fill="x")

        self.close_button = Button(self, text="X", command=self.master.destroy, bg="#333333", fg="#ffffff", bd=0)
        self.close_button.pack(side="right", padx=5)

        self.minimize_button = Button(self, text="-", command=self.master.iconify, bg="#333333", fg="#ffffff", bd=0)
        self.minimize_button.pack(side="right", padx=5)

        self.title_label = tk.Label(self, text="XPlorer", font=("Segoe UI", 12), bg="#333333", fg="#ffffff")
        self.title_label.pack(side="left", padx=5)

root = Tk()
# set a title for our file explorer main window
root.title('XPlorer')
# root.iconbitmap("./icon.ico")
root.geometry("900x500")
root.configure(bg="#222222")
root.overrideredirect(True)

custom_title_bar = CustomTitleBar(root, bg="#333333")
custom_title_bar.pack(fill="x")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

def drag_window(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def drag_window_motion(event):
    global last_x, last_y
    x = root.winfo_x() + event.x - last_x
    y = root.winfo_y() + event.y - last_y
    last_x, last_y = event.x, event.y
    root.geometry("+%s+%s" % (x, y))

custom_title_bar.bind("<Button-1>", drag_window)
custom_title_bar.bind("<B1-Motion>", drag_window_motion)

def pathChange(*event):
    # Get all Files and Folders from the given Directory
    directory = os.listdir(currentPath.get())
    # Clearing the list
    list.delete(0, END)
    # Inserting the files and directories into the list
    for file in directory:
        list.insert(0, file)

def changePathByClick(event=None):
    # Get clicked item.
    picked = list.get(list.curselection()[0])
    # get the complete path by joining the current path with the picked item
    path = os.path.join(currentPath.get(), picked)
    # Check if item is file, then open it
    if os.path.isfile(path):
        print('Opening: '+path)
        os.startfile(path)
    # Set new path, will trigger pathChange function.
    else:
        currentPath.set(path)

def goBack(event=None):
    # get the new path
    newPath = pathlib.Path(currentPath.get()).parent
    # set it to currentPath
    currentPath.set(newPath)
    # simple message
    print('Going Back')
    # change button format
    upbtn.config(bg="#444444")

def open_popup():
    global top
    top = Toplevel(root, bg="#444444")
    top.geometry("250x250")
    top.resizable(False, False)
    top.title("Add a file or a folder")
    top.columnconfigure(0, weight=1)
    top.iconbitmap("icon.ico")
    Label(top, text='Enter File or Folder name', bg="#444444", fg="#ffffff", font=("Segoe UI", 16)).grid()
    Entry(top, textvariable=newFileName, bg="#333333", fg="#ffffff", bd=0, insertbackground="#ffffff", selectbackground="#4cb72c").grid(column=0, pady=10, sticky='NSEW')
    create_button = Button(top, text="Create", command=newFileOrFolder, bg="#333333", fg="#ffffff", bd=0)
    create_button.grid(padx=25, pady=50, sticky='NSEW')
    create_button.bind("<Enter>", lambda event: create_button.config(bg="#4cb72c", fg="#ffffff"))
    create_button.bind("<Leave>", lambda event: create_button.config(bg="#333333", fg="#ffffff"))

def newFileOrFolder():
    # check if it is a file name or a folder
    if len(newFileName.get().split('.')) != 1:
        open(os.path.join(currentPath.get(), newFileName.get()), 'w').close()
    else:
        os.mkdir(os.path.join(currentPath.get(), newFileName.get()))
    # destroy the top
    top.destroy()
    pathChange()

def rename_selected():
    selected_item = list.get(list.curselection())
    if selected_item:
        new_name = simpledialog.askstring("Rename", "Enter new name for " + selected_item, parent=root)
        if new_name:
            old_path = os.path.join(currentPath.get(), selected_item)
            new_path = os.path.join(currentPath.get(), new_name)
            os.rename(old_path, new_path)
            pathChange()

def delete_selected():
    selected_item = list.get(list.curselection())
    if selected_item:
        if messagebox.askokcancel("Delete", "Are you sure you want to delete " + selected_item + "?", parent=root):
            path = os.path.join(currentPath.get(), selected_item)
            if os.path.isfile(path):
                os.remove(path)
            else:
                os.rmdir(path)
            pathChange()

def copy_selected():
    global copied_item
    copied_item = list.get(list.curselection())

def paste_copied():
    if copied_item:
        src = os.path.join(currentPath.get(), copied_item)
        dst = os.path.join(currentPath.get(), os.path.basename(src))
        if os.path.isfile(src):
            shutil.copy(src, dst)
        else:
            shutil.copytree(src, dst)
        pathChange()

def about():
    global top
    top = Toplevel(root)
    top.geometry("300x275")
    top.resizable(False, False)
    top.title("About XPlorer")
    top.columnconfigure(0, weight=1)
    # top.iconbitmap("icon.ico")
    top.config(bg="#333333")
    Label(top, text='About', fg="#ffffff", bg= "#333333", font="Segoe-UI 24").grid()
    Label(top, text='The icon was generated in Google ImageFX!', fg="#ffffff", bg= "#333333").grid()
    Label(top, text='Other icons from Google Fonts.', fg="#ffffff", bg= "#333333").grid()
    Label(top, text='By Galaxica', fg="#ffffff", bg= "#333333").grid()
    Label(top, text='Version 0.11 | 07/2024', fg="#ffffff", bg= "#333333").grid()

def new_patch():
    global top
    top = Toplevel(root)
    top.geometry('350x350')
    top.title("What's new?")
    top.resizable(False, False)
    top.columnconfigure(0, weight=1)
    top.columnconfigure(1, weight=1)
    # top.iconbitmap("icon.ico")
    top.config(bg="#333333")
    green_box = Frame(top, bg="#4cb72c", width=125, height=125)
    green_box.grid(row=1, column=0, pady=15, padx=15, sticky="NW")
    Label(green_box, text='New in version 0.1! ')
    blue_box = Frame(top, bg="#1a9bdd", width=125, height=125)
    blue_box.grid(row=2, column=0, pady=15, padx=15, sticky="NW")

    orange_box = Frame(top, bg="#dd4b39", width=150, height=280)
    orange_box.grid(row=1, column=1, rowspan=2, pady=15, padx=15)







top = ''

# String variables
newFileName = StringVar(root, "File.dot", 'new_name')
currentPath = StringVar(
    root,
    name='currentPath',
    value='C:/'
)
# Bind changes in this variable to the pathChange function
currentPath.trace('w', pathChange)


def change_up_button_color(event):
    upbtn.config(fg="#eeeeee", bg="#4cb72c")

def reset_up_button_color(event=None):
    upbtn.config(fg="#ffffff", bg="#444444")




# Keyboard shortcut for going up
root.bind("<Alt-Up>", goBack)




class CustomMenuBar(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.master = master
        self.pack(fill="x")

        # Create menu buttons
        self.file_button = Button(self, text="File", command=self.file_menu, bg="#333333", fg="#ffffff", bd=0)
        self.file_button.pack(side="left", padx=5)

        self.edit_button = Button(self, text="Edit", command=self.edit_menu, bg="#333333", fg="#ffffff", bd=0)
        self.edit_button.pack(side="left", padx=5)

        self.help_button = Button(self, text="Help", command=self.help_menu, bg="#333333", fg="#ffffff", bd=0)
        self.help_button.pack(side="left", padx=5)

    def file_menu(self):
        # Create a popup menu for File
        menu = Menu(self.master, tearoff=0)
        menu.add_command(label="Save", command=open_popup)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.master.destroy)
        menu.tk_popup(self.file_button.winfo_x(), self.file_button.winfo_y() + self.file_button.winfo_height())

    def edit_menu(self):
        # Create a popup menu for Edit
        menu = Menu(self.master, tearoff=0)
        menu.add_command(label="Copy", command=copy_selected)
        menu.add_command(label="Paste", command=paste_copied)
        menu.tk_popup(self.edit_button.winfo_x(), self.edit_button.winfo_y() + self.edit_button.winfo_height())

    def help_menu(self):
        # Create a popup menu for Help
        menu = Menu(self.master, tearoff=0)
        menu.add_command(label="About", command=about)
        menu.add_command(label="What's new?", command=new_patch)
        menu.tk_popup(self.help_button.winfo_x(), self.help_button.winfo_y() + self.help_button.winfo_height())


def custom_command(event=None):
    command = commandbar.get()
    if command.startswith("cd "):
        new_path = command[3:]
        if os.path.exists(new_path):
            currentPath.set(new_path)
        else:
            messagebox.showerror("Error", "Path not found")
            print("custom_command: Error Path not found")
    elif command == "mkdir":
        open_popup()
    elif command == "newpatch":
        new_patch()
    elif command == "about":
        about()
    elif command == "exit":
        root.destroy()
    elif command == "home":
        change_listbox_to_homescreen()
    else:
        messagebox.showerror("Error", "Invalid command")
        print("custom_command: Error Unknown command")
    command.delete(0, END)
    pass
cmb = CustomMenuBar(root)
cmb.pack(fill="x")
cmb.config(bg="#333333")

top_frame = Frame(root, bg="#222222")
top_frame.pack(fill="x")

upbtn = Button(top_frame, text='Folder Up', command=goBack, bg="#333333", fg="#ffffff", border="0")
upbtn.pack(side=LEFT, padx=5)

commandbar = Entry(top_frame, textvariable=currentPath, bg="#444444", fg="#ffffff", border=0, insertbackground="#ffffff", selectbackground="#4cb72c")
commandbar.pack(side=LEFT, fill='x', padx=5, pady=7, expand=True)
commandbar.bind("<Return>", custom_command)

upbtn.bind("<Enter>", change_up_button_color)

upbtn.bind("<Leave>", reset_up_button_color)
upbtn.bind("<ButtonRelease-1>", reset_up_button_color)
# List of files and folder
list = Listbox(root, bg="#222222", fg="#ffffff", selectbackground="#444444", bd=0, highlightthickness=0, highlightbackground="#333333")
list.pack(fill='x', padx=10, pady=10)
# List Accelerators
list.bind('<Double-1>', changePathByClick)
list.bind('<Return>', changePathByClick)

text_widget = Text(root, width=50, height=10)
text_widget.place(relx=0.5, rely=0.5, anchor=CENTER)

def change_listbox_to_homescreen(event=None):
        global back_button
        list.delete(0, END)
        list.pack_forget()
        text_widget.place(relx=0.5, rely=0.5, anchor=CENTER)

        text_widget.delete(1.0, END)
        text_widget.insert(END, "Welcome back to XPlorer!", "large_font")
        text_widget.insert(END, "\nWhat's up, what would you like to do today?", "small_font")

        text_widget.tag_config("large_font", font=("Segoe UI", 24), justify=CENTER)
        text_widget.tag_config("small_font", font=("Segoe UI", 12), justify=CENTER)

        text_widget.config(state=DISABLED)

        back_button = Button(root, text="Back", command=show_listbox)
        back_button.place(relx=0.5, rely=0.7, anchor=CENTER)

def show_listbox():
    global back_button
    text_widget.place_forget()
    back_button.place_forget()
    list.pack(fill=BOTH, expand=True)
    pathChange()

# Call the function so the list displays
pathChange('')
# run the main program
root.mainloop()

# hidden window run
# hidden_window.mainloop()