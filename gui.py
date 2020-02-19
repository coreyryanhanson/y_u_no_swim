from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from activity import Activity

class ActivityDialogue(Activity):
    def __init__(self, master):
        self.activity = None
        self.overwrite = BooleanVar()
        self.length_unit = StringVar()
        self.master = master
        master.title("Y U no swim")

        self.loader = ttk.Frame(self.master)
        self.load_button = ttk.Button(self.loader, text = "Load File", command = self._open_dialogue)

        self.parameters = ttk.Frame(self.master)

        self.lap_entry_frame = ttk.Frame(self.parameters)
        self.length_unit_selector = ttk.Combobox(self.lap_entry_frame, width = 5, textvariable = self.length_unit)
        self.length_unit_selector.config(values = ("m"))
        self.length_unit_selector.set("m")
        self.distance_text_box = ttk.Entry(self.lap_entry_frame, width = 10)
        self.lap_entry_button = ttk.Button(self.lap_entry_frame, text="Enter", state='disabled', command=self._lap_entry)


        self.saver = ttk.Frame(self.master)
        self.save_button = ttk.Button(self.saver, text="Save File", state='disabled', command=self._save_dialogue)
        self.overwrite_check = ttk.Checkbutton(self.saver, text = "overwrite", state='disabled', variable = self.overwrite)


        self.loader.pack()
        self.load_button.pack()

        self.parameters.pack()
        self.length_unit_selector.pack()
        self.lap_entry_frame.pack()
        self.distance_text_box.pack(side = LEFT)
        self.length_unit_selector.pack(side=LEFT)
        self.lap_entry_button.pack(side=RIGHT)


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
        messagebox.showinfo(title = arg, message = self.error_msg[arg])

    def _open_dialogue(self):
        filepath = filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))
        self.load_tcx(filepath)
        if self.activity:
            self.save_button.config(state='normal')
            self.overwrite_check.config(state='normal')
            self.lap_entry_button.config(state='normal')
        else:
            self.save_button.config(state='disabled')
            self.overwrite_check.config(state='disabled')
            self.lap_entry_button.config(state='disabled')

    def _save_dialogue(self):
        filepath = filedialog.asksaveasfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))
        self.to_xml(filepath, overwrite=self.overwrite.get())

    def _lap_entry(self):
        pool_length = self.distance_text_box.get()
        self.set_pool_length(pool_length)



root = Tk()
# filneame =  filedialog.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("tcx files","*.tcx"),("all files","*.*")))



tcx = ActivityDialogue(root)
root.mainloop()

print(type(tcx.activity))
# print(tcx.to_xml())
# tcx.to_xml("test", overwrite=True)
print(tcx.total_laps)
