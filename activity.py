#!/usr/bin/env python3

import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom



class Activity(object):
    def __init__(self, filepath):
        self.activity = None
        self.load_tcx(filepath)

    #Function containing the outputs in the event of given errors (to be overridden if using GUI).
    def _errors(self, arg, required_extension=None):
        msg = {"filepath_str": "Error-filepath is not a string.",
               "wrong_filepath": "Error file does not exist. Make sure to specify the correct path.",
               "missing_path": "Error path does not exist. Make sure to specify the correct path.",
               "no_extension":"Error file has no extension.",
               "wrong_extension": f"Error file extension must be {required_extension}",
               "need_overwrite": "Error, the file exists and you haven't given permission to overwrite it. Choose another filename.",
               "missing_activity": "Error, activity does not exist."}
        print(msg[arg])

    #Verifies that filepath is a string
    def _try_filepath_string(self, filepath):
        if type(filepath) == str:
            self.filepath = filepath
            return filepath
        else:
            self._errors("filepath_str")
            return False

    #Seperates the filename and file extension
    def _file_extension_extract(self, filepath):
        filepath = self._try_filepath_string(filepath)
        if filepath:
            try:
                filename, file_extension = os.path.splitext(filepath)
            except:
                self._errors("no_extension")
                return None, None
            finally:
                return filename, file_extension
        else:
            return None, None

    #Checks to see if file exists and that it matches the correct file extension before loading it.
    def _load_file(self, filepath, required_extension):
        filename, file_extension = self._file_extension_extract(filepath)
        if file_extension != required_extension:
            self._errors("wrong_extension", required_extension)
            return
        elif not os.path.exists(filepath):
            self._errors("wrong_filepath")
            return
        else:
            return ET.parse(filepath)

    def _save_file(self, filepath, output):
        path, file = os.path.split(filepath)
        if path and file:
            tmp, new_file = f"{path}/.{file}_temp", f"{path}/{file}"
        else:
            tmp, new_file = f".{file}_temp", file
        with open(tmp, "w") as f:
            output.writexml(f, indent="\t", addindent="\t", newl="\n")
        os.replace(tmp, new_file)

    def _export_to_file(self, filepath=None, overwrite=False):
        if filepath == None:
            filepath = self.filepath
        else:
            filepath = self._try_filepath_string(filepath)
        if filepath == False:
            return
        else:
            path, file = os.path.split(filepath)
            file_exists = os.path.exists(filepath)
            path_exists = os.path.exists(path)
        if path and not path_exists:
            self._errors("missing_path")
            return
        elif overwrite == False and file_exists:
            self._errors("need_overwrite")
            return
        else:
            self._save_file(filepath, self.output)

    #Registers the xml namespaces if they exist
    def _register_namespaces(self):
        namespaces = [node for _, node in ET.iterparse(self.filepath, events=['start-ns'])]
        for namespace in namespaces:
            ET.register_namespace(namespace[0], namespace[1])

    def _get_laps(self):
        return list(self.activity.findall("lap"))

    #Standardizes and parses the text with minidom for cleaner output.
    def _mini_parse(self):
        raw_string = ET.tostring(self.activity, 'utf-8').decode().replace("\n","").replace("\t","")
        self.output = minidom.parseString(raw_string)

    #Loads tcx data into an attribute if file can be loaded.
    def load_tcx(self, filepath):
        tree = self._load_file(filepath, ".tcx")
        if not tree:
            return
        else:
            self._register_namespaces()
            self.tree = tree
            self.activity = self.tree.getroot()


    def to_xml(self, filepath=None, print_xml=True, overwrite=False):
        if self.activity == None:
            self._errors("missing_activity")
            return
        else:
            self._mini_parse()
            print(self.output.toprettyxml(indent="\t"))
            self._export_to_file(filepath, overwrite=overwrite)


