import os
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import Listbox

from tkinter import filedialog
import ttkbootstrap as tk
from ttkbootstrap.constants import *
import cv2
from tkinter import Scale


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
        self.rotate_flip_button = None  # Add this line
        # Browse button
        self.browse_button = tk.Button(self.master, text="Browse Folder", command=self.browse_directory)
        self.browse_dcm_button = tk.Button(self.master, text="Browse File", command=self.browse_dcm_file)
        # Labels for HN (Hospital Number) and Accession
        self.hn_label = tk.Label(self.master, text="Hospital Number:")

        self.hn_entry = tk.Entry(self.master, textvariable=self.hospital_number, width=20)
        self.hn_entry.bind("<Return>", self.load_dicom_from_directory)

        # Load button
        self.load_button = tk.Button(self.master, text="Load DICOM", command=self.load_dicom_image)

        # Label for displaying error messages
        self.error_label = tk.Label(self.master, text="")
        


        
        #pack the widget
        self.error_label.pack(side=tk.BOTTOM,anchor='n', padx=5,pady=50,expand=True)
        self.browse_button.pack(side=tk.LEFT,anchor='nw', padx=5,expand=True)
        self.browse_dcm_button.pack(side=tk.LEFT,anchor='nw', padx=5,expand=True)
        self.hn_label.pack(side=tk.LEFT,anchor='nw', padx=5,expand=True)
        self.hn_entry.pack(side=tk.LEFT,anchor='nw', padx=5,expand=True)
        self.load_button.pack(side=tk.LEFT,anchor='nw', padx=5,expand=True)
        



    
    def browse_directory(self):
        # Open a file dialog to select a directory
        selected_directory = filedialog.askdirectory()

        # Update the Entry widget with the selected directory path
        self.hospital_number.set(os.path.basename(selected_directory))

        # Load DICOM files from the selected directory
        self.file_paths = [os.path.join(selected_directory, file) for file in os.listdir(selected_directory) if file.endswith('.dcm')]

        if self.file_paths:
            self.current_index = 0
            self.update_entry()
            self.create_image_window()
        else:
            self.error_label.config(text=f"No DICOM files found in directory: {selected_directory}")
    def browse_dcm_file(self):
        # Open a file dialog to select a .dcm file
        selected_file = filedialog.askopenfilename(filetypes=[("DICOM files", "*.dcm")])

        if selected_file:
            # Update the Entry widget with the selected file path
            self.hospital_number.set(selected_file)

            # Load the selected DICOM file
            self.file_paths = [selected_file]
            self.current_index = 0
            self.update_entry()
            self.create_image_window()
        else:
            self.error_label.config(text="No DICOM file selected.")

    def load_dicom_from_directory(self, event):
        # Event handler for pressing Enter in the HN Entry box
        self.load_dicom_image()

    def load_dicom_image(self):
        # Automatically locate the corresponding folder and load the first DICOM image
        hn = self.hospital_number.get()
        if hn:
            directory_path = os.path.abspath(f"C:/Users/Admin/Desktop/TG/Test/img/{hn}")
            
            self.hospital_number.set(os.path.basename(directory_path))
            self.file_paths = [os.path.join(directory_path, file) for file in os.listdir(directory_path) if file.endswith('.dcm')]
            if self.file_paths:
                self.current_index = 0
                self.update_entry()
                self.create_image_window()
            else:
                self.error_label.config(text=f"No DICOM files found in directory: {directory_path}")
        else:
            self.error_label.config(text="Please enter an HN (Hospital Number).")
    def load_dicom_image_internal(self, ax, canvas):
        if self.file_paths:
            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(self.file_paths[self.current_index])

                # Display the image using matplotlib
                ax.clear()
                ax.imshow(dicom_data.pixel_array, cmap=plt.cm.gray)
                ax.axis('off')  # Hide the axes
                canvas.draw()

                # Set Accession number from the DICOM file
                accession_number = dicom_data.get("AccessionNumber", "N/A")
                self.accession_number.set(accession_number)

                # Clear error message
                self.error_label.config(text="")
            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")

    def show_next(self, ax, canvas):
        if self.file_paths and self.current_index < len(self.file_paths) - 1:
            self.current_index += 1
            self.update_entry()
            self.load_dicom_image_internal(ax, canvas)

    def show_previous(self, ax, canvas):
        if self.file_paths and self.current_index > 0:
            self.current_index -= 1
            self.update_entry()
            self.load_dicom_image_internal(ax, canvas)

    def update_entry(self):
        # Update the Entry widgets with the current Accession and HN
        

        self.hn_entry.delete(0, tk.END)
        self.hn_entry.insert(tk.END, self.hospital_number.get())

    def create_image_window(self):
        # Create a new window to display the DICOM image with next, previous, zoom in, and zoom out buttons
        image_window = tk.Toplevel(self.master)
        image_window.title("DICOM Image Viewer")
        image_window.geometry("1600x900")
        image_window.state("zoomed")
       
        self.fig, ax = plt.subplots(figsize=(7, 7))
        self.fig.patch.set_facecolor('none')  # Set the facecolor of the figure to be transparent

        canvas = FigureCanvasTkAgg(self.fig, master=image_window)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.config(highlightthickness=0) 
        
        # Load the DICOM image in the new window    
        self.load_dicom_image_internal(ax, canvas)
        # Create a Frame to contain widgets on the left side
        left_frame = tk.Frame(image_window)

        # Listbox to display DICOM series
        series_listbox = Listbox(left_frame, selectbackground='lightgray', selectmode=tk.SINGLE, height=10, width=30)

        # Load DICOM series into the Listbox
        self.load_dicom_series(series_listbox)

        # Bind the ListboxSelect event to a callback function
        series_listbox.bind("<<ListboxSelect>>", lambda event: self.load_selected_series(series_listbox.get(tk.ACTIVE)))

        

        # Variables for dragging
        self._drag_data = {"x": 0, "y": 0, "item": None}
        
     

        # Connect the mouse click and release events to the drawing function
        self.cid_press = None
        self.cid_release = None
        # Listbox to display DICOM tags
        tags_listbox = Listbox(image_window, selectbackground='lightgray', selectmode=tk.SINGLE, height=10, width=30)
        
        # Load DICOM tags into the Listbox
        self.load_dicom_tags(tags_listbox)

        # Function to update Listbox when a new image is displayed
        def update_tags_listbox(ax, canvas):
            tags_listbox.delete(0, tk.END)  # Clear existing items
            self.load_dicom_tags(tags_listbox)  # Load DICOM tags for the current image

        # Bind the update function to the canvas redraw event
        canvas.mpl_connect('draw_event', lambda event: update_tags_listbox(ax, canvas))

        # Connect the mouse click and release events to the drawing function
        self.cid_press = None
        self.cid_release = None
        # Create a frame to display DICOM information
        info_frame = tk.Frame(image_window)
        


        #place widjet
        left_frame.pack(side=tk.LEFT,anchor='w', padx=10, pady=10, fill=tk.BOTH, expand=True)
        series_listbox.pack(side=tk.LEFT,anchor='w', pady=10,fill=tk.Y, expand=True)
        self.canvas_widget.pack(side=tk.BOTTOM, expand=True, padx=5, pady=5,anchor="sw",fill=tk.X)
        
        
        tags_listbox.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        info_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
      
   
   



    def load_dicom_tags(self, listbox):
        # Load specific DICOM tags into the provided Listbox
        if self.file_paths:
            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(self.file_paths[self.current_index])

                # Specify the tags to include
                tags_to_include = ["PatientName", "PatientID", "Modality", "StudyTime"]

                # Add specified DICOM tags to the Listbox
                for tag in tags_to_include:
                    if tag in dicom_data:
                        listbox.insert(tk.END, f"{tag}: {dicom_data[tag].value}")

            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")
    def load_dicom_series(self, listbox):
        # Load DICOM series into the provided Listbox
        if self.file_paths:
            try:
                # Get unique series descriptions from the DICOM files
                series_descriptions = set()
                for file_path in self.file_paths:
                    dicom_data = pydicom.dcmread(file_path)
                    series_description = dicom_data.get("SeriesDescription", "N/A")
                    series_descriptions.add(series_description)

                # Add unique series descriptions to the Listbox
                for series_description in series_descriptions:
                    listbox.insert(tk.END, series_description)

            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")

    def load_selected_series(self, selected_series):
     # Load and display the selected DICOM series
        if self.file_paths and selected_series:
            try:
                # Update the hospital number variable
                self.hospital_number.set(selected_series)

                # Filter file paths based on whether the selected series is part of the SeriesDescription
                matching_series = [series for series in self.file_paths if selected_series.lower() in pydicom.dcmread(series).get("SeriesDescription", "").lower()]

                if matching_series:
                    # Update the entire file paths list with the file paths of the selected series
                    self.file_paths = matching_series
                    self.current_index = 0

                    # Update the displayed image in the existing image window
                    self.load_dicom_image_internal(self.fig.axes[0], self.canvas_widget)

                    # Clear error message
                    self.error_label.config(text="")
                else:
                    # Display an error message if no matching series is found
                    self.error_label.config(text=f"No matching DICOM series found: {selected_series}")
            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")



    
#main
if __name__ == "__main__":
    root = tk.Window(themename="yeti")
    root.geometry("670x200")
    viewer = DICOMViewer(root)
    root.mainloop()
