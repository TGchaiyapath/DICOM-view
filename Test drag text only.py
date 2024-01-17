import tkinter as tk
from tkinter import filedialog
import os

class YourApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.hospital_number = tk.StringVar()
        self.file_paths = []
        self.current_index = 0

        self.error_label = tk.Label(self, text="")
        self.error_label.pack()

        browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        browse_button.pack()

        undo_button = tk.Button(self, text="Undo", command=self.undo_action)
        undo_button.pack()

    def browse_file(self):
        selected_file = filedialog.askopenfilename(filetypes=[("DICOM files", "*.dcm;*.DCM")])

        if selected_file:
            self.hospital_number.set(selected_file)
            self.file_paths = [selected_file]
            self.current_index = 0
            self.update_entry()
            self.create_image_window()
        else:
            self.error_label.config(text="No DICOM file selected.")

    def undo_action(self):
        # Implement your undo logic here
        # For example, reset the current index to the previous index
        if self.current_index > 0:
            self.current_index -= 1
            self.update_entry()

    def update_entry(self):
        # Implement your entry update logic here
        pass

    def create_image_window(self):
        # Implement your image window creation logic here
        pass

if __name__ == "__main__":
    app = YourApp()
    app.mainloop()
