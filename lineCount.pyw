import os
import customtkinter as ctk
import json
from pathlib import Path

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

with open(os.path.join(Path(__file__).parent.absolute(), "extensions.json"), "r") as file:
    extensions = sorted(json.load(file))

class customCheckboxFrame(ctk.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master, fg_color="transparent")
        self.checkboxes = []
        self.filetypes = values

        for i, filetype in enumerate(values):
            checkbox = ctk.CTkCheckBox(self, text=f".{filetype}")
            checkbox.grid(row=i//2, column=i%2, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text")[1:])
        return checked_checkboxes
    

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.project_directory = None

        self.title("Project line counter")
        self.geometry("800x550")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nws")
        self.button_set_project_directory = ctk.CTkButton(self.output_frame, text="Change project directory", command=self.set_project_directory)
        self.button_set_project_directory.grid(row=0, column=0, padx=10, pady=10, sticky="esw")
        self.project_path_label = ctk.CTkLabel(self.output_frame, text="Current project: ")
        self.project_path_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.line_count_label = ctk.CTkLabel(self.output_frame, text="Line count: ")
        self.line_count_label.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")

        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nes")
        self.checkbox_frame = customCheckboxFrame(self.selection_frame, values=extensions)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nes")
        self.button_count_project_lines = ctk.CTkButton(self.selection_frame, text="Count project lines", command=self.count_project)
        self.button_count_project_lines.grid(row=1, column=0, padx=10, pady=10, sticky="esw")

        

    def get_allowed_extensions(self) -> list[str]:
        return self.checkbox_frame.get()
        ...

    def set_project_directory(self):
        path = ctk.filedialog.askdirectory()
        if not path == "":
            self.project_directory = path
            print(self.project_directory)
            self.project_path_label.configure(text=f"Current project: {self.project_directory}")

    def count_project(self):
        if self.project_directory in [None, ""]:
            return 0
        allowed_extensions = self.checkbox_frame.get()
        print(f"Extensions: {allowed_extensions}")
        total_lines = self.count_directory(self.project_directory, self.get_allowed_extensions())

        print(f"Line count: {total_lines}")
        self.line_count_label.configure(text=f"Line count: {total_lines}")

    def count_directory(self, path: str, allowed_extensions: list[str]) -> int:
        directory_total = 0
        for file in os.listdir(path=path):
            if file.startswith("."):
                continue
            if os.path.isfile(os.path.join(path, file)):
                if file.split(".")[-1] not in allowed_extensions:
                    continue
                directory_total += self.getFileLineCount(os.path.join(path, file))
            elif os.path.isdir(os.path.join(path, file)):
                directory_total += self.count_directory(os.path.join(path, file), allowed_extensions)
        return directory_total


    def getFileLineCount(self, filepath: str) -> int:
        try:
            with open(filepath, "rb") as f:
                return sum(1 for line in f if len(line.strip()) > 0)
        except OSError:
            return 0



app = App()
app.mainloop()