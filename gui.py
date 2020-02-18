from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from activity import Activity

class ActivityDialogue(Activity):
    def __init__(self, master):
        self.activity = None
        self.overwrite = BooleanVar()
        self.master = master
        master.title("Y U no swim")

        self.loader = ttk.Frame(self.master)
        self.load_button = ttk.Button(self.loader, text = "Load File", command = self._open_dialogue)

        self.parameters = ttk.Frame(self.master)

        self.saver = ttk.Frame(self.master)
        self.save_button = ttk.Button(self.saver, text="Save File", state='disabled', command=self._save_dialogue)
        self.overwrite_check = ttk.Checkbutton(self.saver, text = "overwrite", state='disabled', variable = self.overwrite)

        self.loader.pack()
        self.load_button.pack()

        self.saver.pack()
        self.save_button.pack()
        self.overwrite_check.pack()

        style = ttk.Style()
        print(style.theme_names())
        print(style.theme_use())
        style.theme_use("default")

    #Redirects the error output to the GUI
    def _errors(self, arg, required_extension=None):
        super()._errors(arg, required_extension)

    def _open_dialogue(self):
        filepath = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))
        self.load_tcx(filepath)
        if self.activity:
            self.save_button.config(state='normal')
            self.overwrite_check.config(state='normal')
        else:
            self.save_button.config(state='disabled')
            self.overwrite_check.config(state='disabled')

    def _save_dialogue(self):
        filepath = filedialog.asksaveasfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))
        self.to_xml(filepath, overwrite=self.overwrite.get())


root = Tk()
# filneame =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))



tcx = ActivityDialogue(root)
root.mainloop()

print(type(tcx.activity))
# print(tcx.to_xml())
# tcx.to_xml("test", overwrite=True)