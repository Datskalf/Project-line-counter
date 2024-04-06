import os
from pathlib import Path
import customtkinter as ctk

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class customCheckboxFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_c = ctk.CTkCheckBox(self, text=".c")
        self.checkbox_c.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_txt = ctk.CTkCheckBox(self, text=".txt")
        self.checkbox_txt.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")

        self.checkbox_h = ctk.CTkCheckBox(self, text=".h")
        self.checkbox_h.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_md = ctk.CTkCheckBox(self, text=".md")
        self.checkbox_md.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")

        self.checkbox_py = ctk.CTkCheckBox(self, text=".py")
        self.checkbox_py.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_java = ctk.CTkCheckBox(self, text=".java")
        self.checkbox_java.grid(row=2, column=1, padx=10, pady=(10, 0), sticky="w")

        self.checkbox_cpp = ctk.CTkCheckBox(self, text=".cpp")
        self.checkbox_cpp.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_cs = ctk.CTkCheckBox(self, text=".cs")
        self.checkbox_cs.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")
        

    def get(self):
        checked_checkboxes = []

        if self.checkbox_c.get() == 1:
            checked_checkboxes.append("c")
        if self.checkbox_txt.get() == 1:
            checked_checkboxes.append("txt")

        if self.checkbox_h.get() == 1:
            checked_checkboxes.append("h")
        if self.checkbox_md.get() == 1:
            checked_checkboxes.append("md")

        if self.checkbox_py.get() == 1:
            checked_checkboxes.append("py")
        if self.checkbox_java.get() == 1:
            checked_checkboxes.append("java")

        if self.checkbox_cpp.get() == 1:
            checked_checkboxes.append("cpp")
        if self.checkbox_cs.get() == 1:
            checked_checkboxes.append("cs")
        
        return checked_checkboxes
    

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.project_directory = None

        self.title("Project line counter")
        self.geometry("600x450")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkbox_frame = customCheckboxFrame(self)
        self.checkbox_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nes")

        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nws")

        self.project_path_label = ctk.CTkLabel(self.output_frame, text="Current project: ")
        self.project_path_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.line_count_label = ctk.CTkLabel(self.output_frame, text="Line count: ")
        self.line_count_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        self.button_set_project_directory = ctk.CTkButton(self, text="Project directory", command=self.set_project_directory)
        self.button_set_project_directory.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.button_count_project_lines = ctk.CTkButton(self, text="Count project lines", command=self.count_project)
        self.button_count_project_lines.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        



    def set_project_directory(self):
        path = ctk.filedialog.askdirectory()
        if not path == "":
            self.project_directory = path
            print(self.project_directory)
            self.project_path_label.configure(text=self.project_directory)

    def count_project(self):
        if self.project_directory in [None, ""]:
            return 0
        allowed_extensions = self.checkbox_frame.get()
        print(f"Extensions: {allowed_extensions}")
        os.chdir(self.project_directory)
        total_lines = 0
        for file in os.listdir():
            if not os.path.isfile(file):
                continue
            if file.split(".")[-1] not in allowed_extensions:
                continue
            total_lines += self.getFileLineCount(file)
        
        print(f"Line count: {total_lines}")
        self.line_count_label.configure(text=f"Line count: {total_lines}")

    def getFileLineCount(self, filepath: str) -> int:
        try:
            with open(filepath, "rb") as f:
                return sum(1 for line in f if len(line.strip()) > 0)
        except OSError:
            return 0



app = App()
app.mainloop()