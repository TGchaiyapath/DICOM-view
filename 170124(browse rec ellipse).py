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

#today We add the browse .dcm file button in code line 31,50,76-90
#draw ellipse button in code line 283,348,572-608
#draw rectangle button in code line 284,347,611-646

#there is some issue in the freehand drawing of 187-194,
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

        # Button to toggle drag functionality
        self.toggle_drag_button = tk.Button(image_window, text="Toggle Drag", command=self.toggle_drag)
        
        # Button to toggle freehand drawing functionality
        self.freehand_button = tk.Button(image_window, text="Freehand Draw", command=self.activate_freehand_drawing)

        # Variable for tracking whether freehand drawing is enabled
        self.freehand_enabled = False

        # Variables for freehand drawing
        self.freehand_points = []
        self.cid_motion = None
        
        # Next and Previous buttons in the new window
        next_button = tk.Button(image_window, text="Next", command=lambda: self.show_next(ax, canvas))
        
        image_window.bind("<Right>", lambda event: self.show_next(ax, canvas))
        prev_button = tk.Button(image_window, text="Previous", command=lambda: self.show_previous(ax, canvas))
        
        image_window.bind("<Left>", lambda event: self.show_previous(ax, canvas))

        # Load a zoom in icon image with a relative path
        zoom_in_icon_path = os.path.relpath("icon/zoom-in.png")  # Adjust the folder structure as needed
        icon_ZM = tk.PhotoImage(file=zoom_in_icon_path)
        self.zoom_in_icon = icon_ZM.subsample(27, 27)

        # Zoom in button with icon
        zoom_in_button = tk.Button(image_window, command=lambda: self.zoom_in(ax, canvas), image=self.zoom_in_icon)
        
        image_window.bind("<Key-z>", lambda event: self.zoom_in(ax, canvas))

        # Load a zoom out icon image with a relative path
        zoom_out_icon_path = os.path.relpath("icon/magnifying-glass.png")  # Adjust the folder structure as needed
        icon_ZO = tk.PhotoImage(file=zoom_out_icon_path)
        self.zoom_out_icon = icon_ZO.subsample(27, 27)

        # Zoom out button
        zoom_out_button = tk.Button(image_window, command=lambda: self.zoom_out(ax, canvas), image=self.zoom_out_icon)
        image_window.bind("<Key-x>", lambda event: self.zoom_out(ax, canvas))

        # Load a straight icon image with a relative path
        straight_icon_path = os.path.relpath("icon/shape.png")  # Adjust the folder structure as needed
        icon_ST = tk.PhotoImage(file=straight_icon_path)
        self.straight_icon = icon_ST.subsample(27, 27)

        # Add drawing tool button in the new window
        straight_line_button = tk.Button(image_window, command=lambda: self.activate_straight_line(ax, canvas), image=self.straight_icon)
        

        # Load a dashed icon image with a relative path
        dashed_icon_path = os.path.relpath("icon/dashed line.png")  # Adjust the folder structure as needed
        icon_D = tk.PhotoImage(file=dashed_icon_path)
        self.dashed_icon = icon_D.subsample(27, 27)

        # Dash line button
        dashed_line_button = tk.Button(image_window, command=lambda: self.activate_dashed_line(ax, canvas), image=self.dashed_icon)
        

        # Load an arrow icon image with a relative path
        arrow_icon_path = os.path.relpath("icon/up-right-arrow.png")  # Adjust the folder structure as needed
        icon_AR = tk.PhotoImage(file=arrow_icon_path)
        self.arrow_icon = icon_AR.subsample(27, 27)
        
        #arrow
        single_arrow_button = tk.Button(image_window, command=lambda: self.activate_single_ended_arrow(ax, canvas),image=self.arrow_icon            )
        
             
        # Load a horizon flip icon image
        Hflip_icon_path = os.path.relpath("icon/flip.png")  
        icon_HF = tk.PhotoImage(file=Hflip_icon_path)
        self.Hflip_icon = icon_HF.subsample(27, 27)
        # Flip horizontally button in the new window
        flip_horizontal_button = tk.Button(image_window, command=lambda: self.flip_image(ax, canvas, horizontal=True),image=self.Hflip_icon)
        

        # Load a vertical flip icon image
        Vflip_icon_path = os.path.relpath("icon/vertical-flip.png")  
        icon_VF = tk.PhotoImage(file=Vflip_icon_path)
        self.Vflip_icon = icon_VF.subsample(27, 27)
        # Flip vertically button in the new window

        flip_vertical_button = tk.Button(image_window, command=lambda: self.flip_image(ax, canvas, vertical=True),image=self.Vflip_icon)
        
       
        # Load a rotate right icon image
        RotateR_icon_path = os.path.relpath("icon/rotate-right.png")  
        icon_RR = tk.PhotoImage(file=RotateR_icon_path)
        self.RotateR_icon = icon_RR.subsample(27, 27)
        # Rotate button in the new window
        rotate_button_clockwise = tk.Button(image_window,command=lambda: self.rotate_image(ax, canvas, clockwise=False),image=self.RotateR_icon)

        # Load a rotate right icon image
        RotateL_icon_path = os.path.relpath("icon/rotate-left.png")  
        icon_RL = tk.PhotoImage(file=RotateL_icon_path)
        self.RotateL_icon = icon_RL.subsample(27, 27)
        # Rotate counterclockwise button in the new window
        rotate_button_counterclockwise = tk.Button(image_window, command=lambda: self.rotate_image(ax, canvas, clockwise=True),image=self.RotateL_icon)
        # Variable for tracking whether dragging is enabled
        self.drag_enabled = True
        # Create buttons
        rect_button = tk.Button(image_window, text="Draw Rectangle", command=lambda: self.activate_rectangle(ax,canvas))
        
        ellip_button = tk.Button(image_window, text="Draw Ellipse", command=lambda :self.activate_ellip(ax,canvas))
        
        

        # Variables for dragging
        self._drag_data = {"x": 0, "y": 0, "item": None}
        
        # Bind mouse events for dragging
        self.canvas_widget.bind("<ButtonPress-1>", self.on_press)
        self.canvas_widget.bind("<B1-Motion>", lambda event: self.on_drag(event, ax, canvas))

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
        
        # Scale widget for contrast adjustment
        contrast_scale_label = tk.Label(info_frame, text="Contrast Adjustment")
        contrast_scale = Scale(info_frame, from_=-120, to=50, orient="horizontal", length=200, resolution=0.01, command=lambda value: self.adjust_brightness_and_contrast(float(value), brightness_scale.get(), ax, canvas))
        contrast_scale.set(-35)  # Set initial value

        # Scale widget for brightness adjustment
        brightness_scale_label = tk.Label(info_frame, text="Brightness Adjustment")
        brightness_scale = Scale(info_frame, from_=-255, to=255, resolution=0.01, orient="horizontal", length=200, command=lambda value: self.adjust_brightness_and_contrast(contrast_scale.get(), value, ax, canvas))
        brightness_scale.set(1.0)  # Set initial value



        #place widjet
        left_frame.pack(side=tk.LEFT,anchor='w', padx=10, pady=10, fill=tk.BOTH, expand=True)
        series_listbox.pack(side=tk.LEFT,anchor='w', pady=10,fill=tk.Y, expand=True)
        self.canvas_widget.pack(side=tk.BOTTOM, expand=True, padx=5, pady=5,anchor="sw",fill=tk.X)
        self.toggle_drag_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        next_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        prev_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        zoom_in_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        zoom_out_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        self.freehand_button.pack(side=tk.LEFT, padx=1, pady=5, anchor="nw", expand=True,fill="x")
        straight_line_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        dashed_line_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        single_arrow_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        flip_horizontal_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        flip_vertical_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        rotate_button_clockwise.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        rotate_button_counterclockwise.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        rect_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        ellip_button.pack(side=tk.LEFT, padx=1, pady=5,anchor="nw",expand=True,fill="x")
        tags_listbox.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        info_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        contrast_scale_label.pack(pady=1,padx=1, expand=True)
        contrast_scale.pack(pady=1,padx=1, expand=True)
        brightness_scale_label.pack(pady=1,padx=1, expand=True)
        brightness_scale.pack(pady=1,padx=1,expand=True)
    def activate_freehand_drawing(self):
        # Activate the freehand drawing tool
        if not self.freehand_enabled:
            self.freehand_enabled = True
            self.freehand_button.config(text="Disable Freehand")
            self.freehand_points = []  # Reset the list of points

            # Connect the right mouse button press event to start drawing
            self.cid_right_press = self.fig.canvas.mpl_connect("button_press_event", self.on_right_press)
        else:
            self.freehand_enabled = False
            self.freehand_button.config(text="Freehand Draw")

            # Disconnect the right mouse button press event
            if self.cid_right_press:
                self.fig.canvas.mpl_disconnect(self.cid_right_press)

            # Draw the freehand line on the image
            if self.freehand_points:
                self.draw_freehand_line()
    

    def on_motion(self, event):
        # Record the mouse movement for freehand drawing
        if self.freehand_enabled:
            self.freehand_points.append((event.xdata, event.ydata))

            # Draw the freehand line on the image in real-time
            self.draw_freehand_line_realtime()

    def draw_freehand_line_realtime(self):
        # Draw the freehand line on the image in real-time
        if self.file_paths:
            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(self.file_paths[self.current_index])

                # Draw the freehand line on the image using matplotlib
                ax = self.fig.axes[0]
                for i in range(1, len(self.freehand_points)):
                    start_point = self.freehand_points[i - 1]
                    end_point = self.freehand_points[i]
                    ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='b', linestyle='-', linewidth=1)

        
                # Clear error message
                self.error_label.config(text="")
            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")    

    def on_right_press(self, event):
        # Start drawing on right mouse button press
        if self.freehand_enabled and event.button == 3:  # 3 corresponds to the right mouse button
            # Connect the mouse motion event to the drawing function
            self.cid_motion = self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)

    def on_motion(self, event):
        # Record the mouse movement for freehand drawing
        if self.freehand_enabled:
            self.freehand_points.append((event.xdata, event.ydata))

            # Draw the freehand line on the image in real-time
            self.draw_freehand_line_realtime()

    def draw_freehand_line_realtime(self):
        # Draw the freehand line on the image in real-time
        if self.file_paths:
            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(self.file_paths[self.current_index])

                # Draw the freehand line on the image using matplotlib
                ax = self.fig.axes[0]
                for i in range(1, len(self.freehand_points)):
                    start_point = self.freehand_points[i - 1]
                    end_point = self.freehand_points[i]
                    ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='b', linestyle='-', linewidth=1)

        
                # Clear error message
                self.error_label.config(text="")
            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")
 
    
    def toggle_drag(self):
        # Toggle the drag functionality on and off
        self.drag_enabled = not self.drag_enabled
        if self.drag_enabled:
            self.toggle_drag_button.config(text="Disable Drag")
            # Disconnect the drawing tool
            if self.cid_press:
                self.fig.canvas.mpl_disconnect(self.cid_press)
                self.cid_press = None
            if self.cid_release:
                self.fig.canvas.mpl_disconnect(self.cid_release)
                self.cid_release = None
        else:
            self.toggle_drag_button.config(text="Enable Drag")

    def on_press(self, event):
        if self.drag_enabled:
            # Update the starting point for the drag operation
            if event.state & 0x4:  # Check if Ctrl key is pressed
                self._drag_data["x"] = event.x
                self._drag_data["y"] = event.y
    def on_drag(self, event, ax, canvas):
        if self.drag_enabled and (event.state & 0x4):  # Check if Ctrl key is pressed
            # Update the coordinates of the drag rectangle as the mouse is dragged
            deltax = event.x - self._drag_data["x"]
            deltay = event.y - self._drag_data["y"]
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            ax.set_xlim(ax.get_xlim()[0] - deltax, ax.get_xlim()[1] - deltax)
            ax.set_ylim(ax.get_ylim()[0] - deltay, ax.get_ylim()[1] - deltay)
            canvas.draw()
    def rotate_image(self, ax, canvas, clockwise=True):
        if self.file_paths:
            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(self.file_paths[self.current_index])

                # Update rotation angle (rotate by 90 degrees in the specified direction)
                rotation_direction = 1 if clockwise else -1
                self.rotation_angle = (self.rotation_angle + rotation_direction * 90) % 360

                # Rotate the image
                rotated_image = np.rot90(dicom_data.pixel_array, k=self.rotation_angle // 90)

                # Display the rotated image using matplotlib
                ax.clear()
                ax.imshow(rotated_image, cmap=plt.cm.gray)
                ax.axis('off')  # Hide the axes
                canvas.draw()

                # Clear error message
                self.error_label.config(text="")
            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")
    def flip_image(self, ax, canvas, horizontal=False, vertical=False):
        if self.file_paths:
            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(self.file_paths[self.current_index])

                # Toggle flip states
                if horizontal:
                    self.is_flipped_horizontal = not self.is_flipped_horizontal
                elif vertical:
                    self.is_flipped_vertical = not self.is_flipped_vertical

                # Apply both horizontal and vertical flips if needed
                flipped_image = dicom_data.pixel_array
                if self.is_flipped_horizontal:
                    flipped_image = np.fliplr(flipped_image)
                if self.is_flipped_vertical:
                    flipped_image = np.flipud(flipped_image)

                # Display the flipped image using matplotlib
                ax.clear()
                ax.imshow(flipped_image, cmap=plt.cm.gray)
                ax.axis('off')  # Hide the axes
                canvas.draw()

                # Clear error message
                self.error_label.config(text="")
            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")
    

    
    

    def zoom_out(self, ax, canvas):
        ax.set_xlim(ax.get_xlim()[0] * 1.2, ax.get_xlim()[1] * 1.2)
        ax.set_ylim(ax.get_ylim()[0] * 1.2, ax.get_ylim()[1] * 1.2)
        canvas.draw()

    def zoom_in(self, ax, canvas):
        ax.set_xlim(ax.get_xlim()[0] / 1.2, ax.get_xlim()[1] / 1.2)
        ax.set_ylim(ax.get_ylim()[0] / 1.2, ax.get_ylim()[1] / 1.2)
        canvas.draw()

    
    def activate_straight_line(self, ax, canvas):
        # Activate the drawing tool to draw a straight line on the image
        canvas.draw()

        # Connect the mouse click and release events to the drawing function
        cid_press = self.fig.canvas.mpl_connect("button_press_event", lambda event: self.straight_on_press(event, ax, canvas))
        cid_release = self.fig.canvas.mpl_connect("button_release_event", lambda event: self.straight_on_release(event, ax, canvas))

        # Store the connection IDs for later disconnection
        self.cid_press_straight = cid_press
        self.cid_release_straight = cid_release


    # Draw staight when press and release
    def straight_on_press(self, event, ax, canvas):
        # Record the starting point of the line
        self.start_point = (event.xdata, event.ydata)

    def straight_on_release(self, event, ax, canvas):
        # Draw the straight line on the image
        if hasattr(self, 'start_point'):
            end_point = (event.xdata, event.ydata)
            ax.plot([self.start_point[0], end_point[0]], [self.start_point[1], end_point[1]], color='r', linestyle='-', linewidth=1)
            canvas.draw()

            # Disconnect the drawing tool after drawing the line
            self.fig.canvas.mpl_disconnect(self.cid_press_straight)
            self.fig.canvas.mpl_disconnect(self.cid_release_straight)
            ax.set_title("")  # Clear the title
            del self.start_point
    def activate_ellip(self, ax, canvas):
        # Activate the drawing tool to draw an oval on the image
        canvas.draw()

        # Connect the mouse click and release events to the drawing function
        cid_press = self.fig.canvas.mpl_connect("button_press_event", lambda event: self.ellip_on_press(event, ax, canvas))
        cid_release = self.fig.canvas.mpl_connect("button_release_event", lambda event: self.ellip_on_release(event, ax, canvas))

        # Store the connection IDs for later disconnection
        self.cid_press_ellip = cid_press
        self.cid_release_ellip = cid_release

    # Draw an oval when press and release
    def ellip_on_press(self, event, ax, canvas):
        # Record the starting point of the oval
        self.start_point = (event.xdata, event.ydata)

    def ellip_on_release(self, event, ax, canvas):
        # Draw the oval on the image
        if hasattr(self, 'start_point'):
            end_point = (event.xdata, event.ydata)
            
            # Calculate the center and radii of the oval
            center = ((self.start_point[0] + end_point[0]) / 2, (self.start_point[1] + end_point[1]) / 2)
            radius_x = abs(end_point[0] - self.start_point[0]) / 2
            radius_y = abs(end_point[1] - self.start_point[1]) / 2
            
            # Draw the oval using Ellipse
            ellipse = plt.matplotlib.patches.Ellipse(center, width=radius_x * 2, height=radius_y * 2, color='cyan', fill=False, linestyle='-', linewidth=1)
            ax.add_patch(ellipse)
            canvas.draw()

            # Disconnect the drawing tool after drawing the oval
            self.fig.canvas.mpl_disconnect(self.cid_press_ellip)
            self.fig.canvas.mpl_disconnect(self.cid_release_ellip)
            ax.set_title("")  # Clear the title
            del self.start_point

    def activate_rectangle(self, ax, canvas):
        # Activate the drawing tool to draw a rectangle on the image
        canvas.draw()

        # Connect the mouse click and release events to the drawing function
        cid_press = self.fig.canvas.mpl_connect("button_press_event", lambda event: self.rectangle_on_press(event, ax, canvas))
        cid_release = self.fig.canvas.mpl_connect("button_release_event", lambda event: self.rectangle_on_release(event, ax, canvas))

        # Store the connection IDs for later disconnection
        self.cid_press_rectangle = cid_press
        self.cid_release_rectangle = cid_release

    # Draw a rectangle when press and release
    def rectangle_on_press(self, event, ax, canvas):
        # Record the starting point of the rectangle
        self.start_point = (event.xdata, event.ydata)

    def rectangle_on_release(self, event, ax, canvas):
        # Draw the rectangle on the image
        if hasattr(self, 'start_point'):
            end_point = (event.xdata, event.ydata)
            
            # Calculate the width and height of the rectangle
            width = abs(end_point[0] - self.start_point[0])
            height = abs(end_point[1] - self.start_point[1])
            
            # Draw the rectangle using Rectangle
            rectangle = plt.matplotlib.patches.Rectangle(self.start_point, width, height, edgecolor='purple', fill=False, linestyle='-', linewidth=1)
            ax.add_patch(rectangle)
            canvas.draw()

            # Disconnect the drawing tool after drawing the rectangle
            self.fig.canvas.mpl_disconnect(self.cid_press_rectangle)
            self.fig.canvas.mpl_disconnect(self.cid_release_rectangle)
            ax.set_title("")  # Clear the title
            del self.start_point

    #Draw staight when press and release
    def activate_dashed_line(self, ax, canvas):
        # Activate the drawing tool to draw a dashed line on the image
        canvas.draw()

        # Connect the mouse click and release events to the drawing function
        cid_press = self.fig.canvas.mpl_connect("button_press_event", lambda event: self.dashed_on_press(event, ax, canvas))
        cid_release = self.fig.canvas.mpl_connect("button_release_event", lambda event: self.dashed_on_release(event, ax, canvas))

        # Store the connection IDs for later disconnection
        self.cid_press_dashed = cid_press
        self.cid_release_dashed = cid_release
    #Draw dashed line when press and release
    def dashed_on_press(self, event, ax, canvas):
        # Record the starting point of the line
        self.start_point = (event.xdata, event.ydata)
    def dashed_on_release(self, event, ax, canvas):
        # Draw the dashed line on the image
        if hasattr(self, 'start_point'):
            end_point = (event.xdata, event.ydata)
            ax.plot([self.start_point[0], end_point[0]], [self.start_point[1], end_point[1]], color='y', linestyle='--', linewidth=1)
            canvas.draw()

          # Disconnect the drawing tool after drawing the line
            self.fig.canvas.mpl_disconnect(self.cid_press_dashed)
            self.fig.canvas.mpl_disconnect(self.cid_release_dashed)
            ax.set_title("")  # Clear the title
            del self.start_point

    def activate_single_ended_arrow(self, ax, canvas):
        # Activate the drawing tool to draw a single-ended arrow on the image
        canvas.draw()

        # Connect the mouse click and release events to the drawing function
        cid_press = self.fig.canvas.mpl_connect("button_press_event", lambda event: self.single_arrow_on_press(event, ax, canvas))
        cid_release = self.fig.canvas.mpl_connect("button_release_event", lambda event: self.single_arrow_on_release(event, ax, canvas))

        # Store the connection IDs for later disconnection
        self.cid_press = cid_press
        self.cid_release = cid_release

    def single_arrow_on_press(self, event, ax, canvas):
        # Record the starting point of the arrow
        self.start_point = (event.xdata, event.ydata)

    def single_arrow_on_release(self, event, ax, canvas):
        # Draw the single-ended arrow on the image
        if hasattr(self, 'start_point'):
            end_point = (event.xdata, event.ydata)

            # Draw the arrow using annotation in matplotlib
            arrow = plt.annotate("", xy=end_point, xytext=self.start_point, arrowprops=dict(arrowstyle='->', color='g', linewidth=1))
            ax.add_artist(arrow)
            canvas.draw()

            # Disconnect the drawing tool after drawing the arrow
            self.fig.canvas.mpl_disconnect(self.cid_press)
            self.fig.canvas.mpl_disconnect(self.cid_release)
            ax.set_title("")  # Clear the title
            del self.start_point
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
                # Filter file paths based on whether the selected series is part of the SeriesDescription
                matching_series = [series for series in self.file_paths if selected_series.lower() in pydicom.dcmread(series).get("SeriesDescription", "").lower()]

                if matching_series:
                    # Update the file paths and reset the current index
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
    def adjust_brightness_and_contrast(self, contrast_value, brightness_value, ax, canvas):
        if self.file_paths:
            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(self.file_paths[self.current_index]).pixel_array

                # Normalize pixel values to the range [0, 255]
                dicom_data = (dicom_data / np.max(dicom_data) * 255).astype(np.uint8)
                
                # Adjust brightness
                if float(brightness_value) >= 0:
                    bright_image = cv2.add(dicom_data, float(brightness_value))
                else:
                    bright_image = cv2.subtract(dicom_data, -float(brightness_value))

                # Adjust contrast
                adjusted_image = cv2.convertScaleAbs(bright_image, alpha=float(np.power(400, (contrast_value / 127.0))))

                # Clip pixel values to ensure they are in the range [0, 255]
                adjusted_image = np.clip(adjusted_image, 0, 255)

                # Clear axis and display the adjusted image
                ax.clear()
                ax.imshow(adjusted_image, cmap=plt.cm.gray)
                ax.axis('off')  # Hide the axes
                canvas.draw()

                # Clear error message
                self.error_label.config(text="")
                
            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")
   
#main
if __name__ == "__main__":
    root = tk.Window(themename="yeti")
    root.geometry("670x200")
    viewer = DICOMViewer(root)
    root.mainloop()
