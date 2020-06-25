import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from activity import Activity

class ActivityDialogue(Activity):
    def __init__(self, master):
        self.print_xml = False
        self.activity = None
        self.filepath = None
        self.lap_distance = None
        self.overwrite = BooleanVar()
        self.length_unit = StringVar()
        self.master = master
        master.title("Y U no swim")

        self.pathstr = StringVar()
        self.pathlabel = ttk.Label(self.master, textvariable= self.pathstr)
        self.load_button = ttk.Button(self.master, text = "Load File", command = self._open_dialogue)

        self.parameters = ttk.Frame(self.master)

        self.length_unit_selector = ttk.Combobox(self.parameters, width = 5, textvariable = self.length_unit)
        self.length_unit_selector.config(values = ("m"))
        self.length_unit_selector.set("m")
        self.distance_text_box = ttk.Entry(self.parameters, width = 10)
        self.lap_entry_button = ttk.Button(self.master, text="Enter", state='disabled', command=self._lap_entry)


        self.save_button = ttk.Button(self.master, text="Save File", state='disabled', command=self._save_dialogue)
        self.overwrite_check = ttk.Checkbutton(self.master, text = "overwrite", state='disabled', variable = self.overwrite)


        self.master.grid()
        self.pathlabel.grid(row=0, column=0, padx=10)
        self.load_button.grid(row=0, column=1)

        self.parameters.grid(row=1, column=0)
        self.distance_text_box.grid(row=0, column=1)
        self.length_unit_selector.grid(row=0, column=0)
        self.lap_entry_button.grid(row=1, column=1)


        self.overwrite_check.grid(row=2, column=0, padx=10)
        self.save_button.grid(row=2, column=1)

        style = ttk.Style()
        print(style.theme_names())
        print(style.theme_use())
        style.theme_use("default")

    #Redirects the error output to the GUI
    def _errors(self, arg, required_extension=None):
        super()._errors(arg, required_extension)
        messagebox.showinfo(title = arg, message = self.error_msg[arg])

    def _open_dialogue(self):
        filepath = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))
        if filepath:
            self.load_tcx(filepath)
            self.overwrite_check.config(state='normal')
            self.lap_entry_button.config(state='normal')
            self.pathstr.set(os.path.basename(self.filepath))

    def _save_dialogue(self):
        filepath = filedialog.asksaveasfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))
        if filepath:
            self.to_xml(filepath, overwrite=self.overwrite.get())

    def _lap_entry(self):
        pool_length = self.distance_text_box.get()
        self.set_pool_length(pool_length)
        if self.lap_distance:
            self.save_button.config(state='normal')



root = Tk()
# filneame =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))



tcx = ActivityDialogue(root)
root.mainloop()

print(type(tcx.activity))
# print(tcx.to_xml())
# tcx.to_xml("test", overwrite=True)
print(tcx.total_laps)
