import tkinter as tk
from tkinter import ttk, filedialog
import pydicom

class DicomEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("DICOM Tag Editor")

        self.file_path_label = ttk.Label(master, text="DICOM File:")
        self.file_path_label.grid(row=0, column=0, padx=10, pady=10)

        self.file_path_entry = ttk.Entry(master, state="readonly")
        self.file_path_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

        self.browse_button = ttk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=3, padx=10, pady=10)

        self.tag_label = ttk.Label(master, text="DICOM Tag (e.g., PatientName):")
        self.tag_label.grid(row=1, column=0, padx=10, pady=10)

        self.tag_entry = ttk.Entry(master)
        self.tag_entry.grid(row=1, column=1, padx=10, pady=10)

        self.value_label = ttk.Label(master, text="New Value:")
        self.value_label.grid(row=1, column=2, padx=10, pady=10)

        self.value_entry = ttk.Entry(master)
        self.value_entry.grid(row=1, column=3, padx=10, pady=10)

        self.edit_button = ttk.Button(master, text="Edit Tag", command=self.edit_dicom_tag)
        self.edit_button.grid(row=2, column=0, columnspan=4, pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("DICOM Files", "*.dcm")])
        if file_path:
            self.file_path_entry.configure(state="normal")
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, file_path)
            self.file_path_entry.configure(state="readonly")

    def edit_dicom_tag(self):
        file_path = self.file_path_entry.get()
        tag = self.tag_entry.get()
        value = self.value_entry.get()

        if file_path and tag and value:
            try:
                dicom_data = pydicom.dcmread(file_path)
                dicom_data[tag].value = value
                dicom_data.save_as(file_path)
                tk.messagebox.showinfo("Success", "DICOM Tag Edited Successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            tk.messagebox.showerror("Error", "Please provide DICOM file path, tag, and new value.")

if __name__ == "__main__":
    root = tk.Tk()
    editor = DicomEditor(root)
    root.mainloop()
