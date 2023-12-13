import os
import tkinter as tk
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import Listbox, Menu


class DICOMViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("DICOM Image Viewer")

        self.file_paths = []  # List to store DICOM file paths
        self.current_index = 0  # Index of the currently displayed DICOM file
        self.accession_number = tk.StringVar()  # Variable to store Accession number
        self.hospital_number = tk.StringVar()  # Variable to store Hospital Number
        self.is_flipped_horizontal = False  # Variable to track the horizontal flip state
        self.is_flipped_vertical = False 
        self.rotation_angle = 0  # Variable to track the rotation angle

        # Labels for HN (Hospital Number) and Accession
        self.hn_label = tk.Label(self.master, text="HN (Hospital Number):")
        self.hn_label.pack(pady=5)

        self.hn_entry = tk.Entry(self.master, textvariable=self.hospital_number, width=20)
        self.hn_entry.pack(pady=5)
        #self.hn_entry.bind("<Return>", self.load_dicom_from_directory)
       

        self.accession_label = tk.Label(self.master, text="Accession:")
        self.accession_label.pack(pady=5)

        self.accession_entry = tk.Entry(self.master, textvariable=self.accession_number, width=20)
        self.accession_entry.pack(pady=5)

        # Load button
        #self.load_button = tk.Button(self.master, text="Load DICOM", command=self.load_dicom_image)
        self.load_button = tk.Button(self.master, text="Load DICOM")
        self.load_button.pack(side=tk.RIGHT, pady=10)

        # Label for displaying error messages
        self.error_label = tk.Label(self.master, text="", fg="red")
        self.error_label.pack(pady=5)




# MAIN window
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    viewer = DICOMViewer(root)
    root.mainloop()
