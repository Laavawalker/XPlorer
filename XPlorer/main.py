from tkinter import *
from tkinter import simpledialog, messagebox, font
import shutil
import os
import ctypes
import pathlib
import pickle
from turtle import bgcolor
import tkinter as tk
import pystray
from PIL import Image, ImageTk
import threading
import requests
from io import BytesIO
import PIL
import time
import random
from pystray import MenuItem as item
import sys
# import win32gui
# import win32con

version1 = "Pre-alpha 3"
version2 = "0.3.241021"
version3 = "Pre-alpha 3 (0.3.241021)"
# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)



def minimize_window():
    root.withdraw()
    threading.Thread(target=show_system_tray_icon, daemon=True).start()

def restore_window(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

def create_simple_icon(color, size=(64, 64)):
    image = Image.new('RGB', size, color=color)
    return image

def show_system_tray_icon():
    global icon
    
    try:
        # Create a simple colored icon
        icon_image = create_simple_icon("yellow")  # You can change "blue" to any color you prefer
        
        # Create the menu
        menu = pystray.Menu(item('Restore', restore_window))
        
        # Create and run the icon
        icon_title = "XPlorer v" + version2
        icon = pystray.Icon('name', icon_image, menu=menu, title=icon_title)
        icon.run()
    except Exception as e:
        print(f"Error creating system tray icon: {e}")
    
    return



def close_window():
    global icon
    if icon:
        icon.stop()
    root.destroy()

class CustomTitleBar(Frame):
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.master = master
        self.pack(fill="x")

        self.close_button = Button(self, text="╳", command=close_window, bg="#333333", fg="#ffffff", bd=0)
        self.close_button.pack(side="right", padx=5)

        self.minimize_button = Button(self, text="−",  command=minimize_window, bg="#333333", fg="#ffffff", bd=0)
        self.minimize_button.pack(side="right", padx=5)

        self.title_text = "XPlorer " + version3
        self.title_label = tk.Label(self, text=self.title_text, font=("Segoe UI", 11), bg="#333333", fg="#ffffff")
        self.title_label.pack(side="left", padx=5)

        def change_x_button_color(event):
            # global close_button
            self.close_button.config(fg="#ffffff", bg="#e80000")

        def reset_x_button_color(event=None):
            # global close_button
            self.close_button.config(fg="#ffffff", bg="#333333")

        def change_min_button_color(event):
            # global minimize_button
            self.minimize_button.config(fg="#ffffff", bg="#07abf7")

        def reset_min_button_color(event=None):
            # global minimize_button
            self.minimize_button.config(fg="#ffffff", bg="#333333")

        self.close_button.bind("<Enter>", change_x_button_color)
        self.close_button.bind("<Leave>", reset_x_button_color)
        self.close_button.bind("<ButtonRelease-1>", reset_x_button_color)

        self.minimize_button.bind("<Enter>", change_min_button_color)
        self.minimize_button.bind("<Leave>", reset_min_button_color)
        self.minimize_button.bind("<ButtonRelease-1>", reset_min_button_color)


root = Tk()
# set a title for our file explorer main window
root.title('XPlorer')
# root.iconbitmap("./icon.ico")
root.geometry("900x500")
root.configure(bg="#222222")
root.overrideredirect(True)

custom_font = font.Font(root, family="Neonclipper", size=12)
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
    about_ver_text = "Version " + version3 + " | 11/2024"
    # top.iconbitmap("icon.ico")
    top.config(bg="#333333")
    Label(top, text='About', fg="#ffffff", bg= "#333333", font="Segoe-UI 24").grid()
    Label(top, text='The icon was generated in Google ImageFX!', fg="#ffffff", bg= "#333333").grid()
    Label(top, text='Other icons from Google Fonts.', fg="#ffffff", bg= "#333333").grid()
    Label(top, text='By Galaxica', fg="#ffffff", bg= "#333333").grid()
    Label(top, text=about_ver_text, fg="#ffffff", bg= "#333333").grid()

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

def mhelp():
    global top
    top = Toplevel(root)
    top.geometry("400x700")
    top.resizable(False, False)
    top.title("Help")
    top.columnconfigure(0, weight=1)
    # top.iconbitmap("icon.ico")
    top.config(bg="#333333")
    Label(top, text='Help', fg="#ffffff", bg= "#333333", font="Segoe-UI 24", wraplength=300).grid()
    Label(top, text="List of commands", fg="#ffffff", bg="#333333", font="Segoe-UI 16", wraplength=300).grid()
    Label(top, text="new - opens a popup to make a new file or folder", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="about - opens a popup about the app", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="exit - closes the app", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="newpatch - opens the What's new? window", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="home - redirects to homescreen, which is a welcome screen", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="settings or options - comming soon | there's a huge problem with this, so I've disabled this. And if enabled there aren't any settings", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="help - (you read infos from this window now :) opens a window that contains some infos you'd probably ask about", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="More", fg="#ffffff", bg="#333333", font="Segoe-UI 16", wraplength=300).grid()
    Label(top, text="If you minimize the main window, you shall see a yellow square in your tray. Right-click it, then select restore, and you restore the window. I don't know how it works on Linux or Mac.", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="If you're in the homescreen and clicking back gives you a blank screen, you should provide a valid path in the input.", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="When you launch this app, the homescreen will pop-up, just click back and nothing shouldn't stay on your way to return to a normal work of a file manager :)", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()
    Label(top, text="Contact", fg="#ffffff", bg="#333333", font="Segoe-UI 16", wraplength=300).grid()
    Label(top, text="If you encounter any promlem that is not written about here, then fell free to ask me on Discord: gl.laavawalker", fg="#ffffff", bg="#333333", font="Segoe-UI 11", wraplength=300).grid()


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

def change_back_btn_color(event):
    back_button.config(fg="#eeeeee", bg="#4cb72c")

def reset_back_btn_color(event=None):
    back_button.config(fg="#ffffff", bg="#444444")



# def change_back_btn_settings_color(event):
  #  back_button_settings.config(fg="#eeeeee", bg="#4cb72c")

# def reset_back_btn_settings_color(event=None):
  #  back_button_settings.config(fg="#ffffff", bg="#444444")


# Keyboard shortcut for going up
root.bind("<Alt-Up>", goBack)




class CustomMenuBar(Frame):
    global file_button
    global edit_button
    global help_button
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

        def change_file_button_color(event):
            self.file_button.config(fg="#eeeeee", bg="#4cb72c")

        def reset_file_button_color(event=None):
            self.file_button.config(fg="#ffffff", bg="#333333")

        def change_edit_button_color(event):
            self.edit_button.config(fg="#eeeeee", bg="#4cb72c")

        def reset_edit_button_color(event=None):
            self.edit_button.config(fg="#ffffff", bg="#333333")

        def change_help_button_color(event):
            self.help_button.config(fg="#eeeeee", bg="#4cb72c")

        def reset_help_button_color(event=None):
            self.help_button.config(fg="#ffffff", bg="#333333")

        self.file_button.bind("<Enter>", change_file_button_color)
        self.file_button.bind("<Leave>", reset_file_button_color)
        self.file_button.bind("<ButtonRelease-1>", reset_file_button_color)

        self.edit_button.bind("<Enter>", change_edit_button_color)
        self.edit_button.bind("<Leave>", reset_edit_button_color)
        self.edit_button.bind("<ButtonRelease-1>", reset_edit_button_color)

        self.help_button.bind("<Enter>", change_help_button_color)
        self.help_button.bind("<Leave>", reset_help_button_color)
        self.help_button.bind("<ButtonRelease-1>", reset_help_button_color)

    def file_menu(self):
        # Create a popup menu for File
        menu = Menu(self.master, tearoff=0, bd=0, relief=FLAT, background="#333333", foreground="#ffffff",
                    activebackground="#4cb72c", activeforeground="#ffffff")
        self.add_menu_item(menu, "New", open_popup)
        menu.add_separator()
        self.add_menu_item(menu, "Exit", self.master.destroy)
        menu.tk_popup(self.file_button.winfo_rootx(), self.file_button.winfo_rooty() + self.file_button.winfo_height())

    def edit_menu(self):
        # Create a popup menu for Edit
        menu = Menu(self.master, tearoff=0, bd=0, relief=FLAT, background="#333333", foreground="#ffffff",
                    activebackground="#4cb72c", activeforeground="#ffffff")
        self.add_menu_item(menu, "Copy", copy_selected)
        self.add_menu_item(menu, "Paste", paste_copied)
        self.add_menu_item(menu, "Delete", delete_selected)
        menu.tk_popup(self.edit_button.winfo_rootx(), self.edit_button.winfo_rooty() + self.edit_button.winfo_height())

    def help_menu(self):
        # Create a popup menu for Help
        menu = Menu(self.master, tearoff=0, bd=0, relief=FLAT, background="#333333", foreground="#ffffff",
                    activebackground="#4cb72c", activeforeground="#ffffff")
        self.add_menu_item(menu, "About", about)
        self.add_menu_item(menu, "What's new?", new_patch)
        self.add_menu_item(menu, "More help", mhelp)
        menu.tk_popup(self.help_button.winfo_rootx(), self.help_button.winfo_rooty() + self.help_button.winfo_height())

    def add_menu_item(self, menu, label, command):
        menu.add_command(label=label, command=command)
        index = menu.index(label)
        menu.entryconfig(index, background="#333333", foreground="#ffffff")
        menu.bind("<Enter>", lambda event, idx=index: self.on_menu_item_hover(event, menu, idx))
        menu.bind("<Leave>", lambda event, idx=index: self.on_menu_item_leave(event, menu, idx))

    def on_menu_item_hover(self, event, menu, index):
        menu.entryconfig(index, background="#4cb72c", foreground="#ffffff")

    def on_menu_item_leave(self, event, menu, index):
        menu.entryconfig(index, background="#333333", foreground="#ffffff")

    



def custom_command(event=None):
    command = commandbar.get()
    if command.startswith("cd "):
        new_path = command[3:]
        if os.path.exists(new_path):
            currentPath.set(new_path)
        else:
            messagebox.showerror("Error", "Path not found")
            print("custom_command: Error Path not found")
    elif command == "new":
        open_popup()
    elif command == "newpatch":
        new_patch()
    elif command == "about":
        about()
    elif command == "exit":
        root.destroy()
        close_window()
    elif command == "home":
        change_listbox_to_homescreen()
    elif command == "settings":
        print('Attempt to get to settings section by the "settings" command')
        messagebox.showinfo("Settings", "Settings are not available yet")
    elif command == "options":
        print('Attempt to get to settings section by the "options" command')
        messagebox.showinfo("Settings", "Settings are not available yet")
    elif command == "help":
        mhelp()
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

version_text_text = "Version " + version3 + ". This app is still under development and can be unstable. Developer still makes huge and small changes, and he is not responsible to what happens at your place. The project is public, but do not distribute."
version_text = Label(root, text=version_text_text, fg="#555555", bg="#222222", width=35, height=7, wraplength=200)
version_text.place(relx=1.0, rely=1.0, anchor='se', x=10, y=0)

# text_widget_settings = Text(root, width=50, height=10)
# text_widget_settings.place(relx=0.5, rely=0.5, anchor=CENTER)

def change_listbox_to_homescreen(event=None):
        global back_button
        list.delete(0, END)
        list.pack_forget()
        text_widget.place(relx=0.5, rely=0.5, anchor=CENTER)

        text_widget.delete(1.0, END)
        text_widget.insert(END, "Welcome back to XPlorer!", "large_font")
        text_widget.insert(END, "\nWhat's up, what would you like to do today?", "small_font")

        text_widget.tag_config("large_font", font=("Segoe UI Bold", 24), justify=CENTER)
        text_widget.tag_config("small_font", font=("Segoe UI", 12), justify=CENTER)

        text_widget.config(state=DISABLED, bg="#222222", bd=0, fg="#ffffff")

        text_widget.bind("<Button-1>", lambda e: "break")
        text_widget.bind("<B1-Motion>", lambda e: "break")

        back_button = Button(root, text="Back", command=show_listbox, bg="#333333", fg="#ffffff", border="0", width=15, font=("Segoe UI Bold", 14))
        back_button.place(relx=0.5, rely=0.7, anchor=CENTER)

        back_button.bind("<Enter>", change_back_btn_color)

        back_button.bind("<Leave>", reset_back_btn_color)
        back_button.bind("<ButtonRelease-1>", reset_back_btn_color)


# def change_listbox_to_settings(event=None):
#         global back_button_settings
#         list.delete(0, END)
#         list.pack_forget()
#         text_widget_settings.place(relx=0.5, rely=0.5, anchor=CENTER)
# 
#         text_widget_settings.delete(1.0, END)
#         text_widget_settings.insert(END, "Settings (coming soon)", "large_font")
# 
#         text_widget_settings.tag_config("large_font", font=("Segoe UI Bold", 24), justify=CENTER)
#         text_widget_settings.tag_config("small_font", font=("Segoe UI", 12), justify=CENTER)
# 
#         text_widget_settings.config(state=DISABLED, bg="#222222", bd=0, fg="#ffffff")
# 
#         text_widget_settings.bind("<Button-1>", lambda e: "break")
#         text_widget_settings.bind("<B1-Motion>", lambda e: "break")
# 
#         back_button_settings = Button(root, text="Back", command=show_listbox, bg="#333333", fg="#ffffff", border="0", width=15, font=("Segoe UI Bold", 14))
#         back_button_settings.place(relx=0.5, rely=0.7, anchor=CENTER)
# 
#         back_button_settings.bind("<Enter>", change_back_btn_settings_color)
# 
#         back_button_settings.bind("<Leave>", reset_back_btn_settings_color)
#         back_button_settings.bind("<ButtonRelease-1>", reset_back_btn_settings_color)

def show_listbox():
    global back_button
    # global back_button_settings
    text_widget.place_forget()
    back_button.place_forget()
    # text_widget_settings.place_forget()
    # back_button_settings.place_forget()
    list.pack(fill=BOTH, expand=True)
    pathChange()



# Call the function so the list displays
# pathChange('')
# run the main program
change_listbox_to_homescreen()


root.mainloop()

# hidden window run
# hidden_window.mainloop()