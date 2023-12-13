import os
import tkinter as tk
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
        self.hn_entry.bind("<Return>", self.load_dicom_from_directory)

        self.accession_label = tk.Label(self.master, text="Accession:")
        self.accession_label.pack(pady=5)

        self.accession_entry = tk.Entry(self.master, textvariable=self.accession_number, width=20)
        self.accession_entry.pack(pady=5)

        # Load button
        self.load_button = tk.Button(self.master, text="Load DICOM", command=self.load_dicom_image)
        self.load_button.pack(side=tk.RIGHT, pady=10)

        # Label for displaying error messages
        self.error_label = tk.Label(self.master, text="", fg="red")
        self.error_label.pack(pady=5)

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

    def create_image_window(self):
            # Create a new window to display the DICOM image with next, previous, zoom in, and zoom out buttons
        image_window = tk.Toplevel(self.master)
        image_window.title("DICOM Image Viewer")

             # Matplotlib figure for displaying the image in the new window
        self.fig, ax = plt.subplots(figsize=(6, 6))
        canvas = FigureCanvasTkAgg(self.fig, master=image_window)
        self.canvas_widget = canvas.get_tk_widget()  # Fix here
        self.canvas_widget.pack()

            # Load the DICOM image in the new window
        self.load_dicom_image_internal(ax, canvas)
        
        # Button to toggle drag functionality
        self.toggle_drag_button = tk.Button(image_window, text="Toggle Drag", command=self.toggle_drag)
        self.toggle_drag_button.pack(side=tk.LEFT, padx=5)

        # Next and Previous buttons in the new window
        next_button = tk.Button(image_window, text="Next", command=lambda: self.show_next(ax, canvas))
        next_button.pack(side=tk.LEFT, padx=5)
        image_window.bind("<Right>", lambda event: self.show_next(ax, canvas))
        prev_button = tk.Button(image_window, text="Previous", command=lambda: self.show_previous(ax, canvas))
        prev_button.pack(side=tk.LEFT, padx=5)
        image_window.bind("<Left>", lambda event: self.show_previous(ax, canvas))

        # Zoom in and Zoom out buttons in the new window
        zoom_in_button = tk.Button(image_window, text="Zoom In", command=lambda: self.zoom_in(ax, canvas))
        zoom_in_button.pack(side=tk.LEFT, padx=5)
        image_window.bind("<Key-z>", lambda event: self.zoom_in(ax, canvas))
    
        zoom_out_button = tk.Button(image_window, text="Zoom Out", command=lambda: self.zoom_out(ax, canvas))
        zoom_out_button.pack(side=tk.LEFT, padx=5)
        image_window.bind("<Key-x>", lambda event: self.zoom_out(ax, canvas))
        
        # Add drawing tool button in the new window
        straight_line_button = tk.Button(image_window, text="Draw Straight Line", command=lambda: self.activate_straight_line(ax, canvas))
        straight_line_button.pack(side=tk.LEFT, padx=5)
        # Add drawing tool button in the new window
        dashed_line_button = tk.Button(image_window, text="Draw Dashed Line", command=lambda: self.activate_dashed_line(ax, canvas))
        dashed_line_button.pack(side=tk.LEFT, padx=5)
        #arrow
        single_arrow_button = tk.Button(image_window, text="Draw Single Arrow", command=lambda: self.activate_single_ended_arrow(ax, canvas))
        single_arrow_button.pack(side=tk.LEFT, padx=5)

        # Flip horizontally button in the new window
        flip_horizontal_button = tk.Button(image_window, text="Flip Horizontally", command=lambda: self.flip_image(ax, canvas, horizontal=True))
        flip_horizontal_button.pack(side=tk.LEFT, padx=5)

        # Flip vertically button in the new window
        flip_vertical_button = tk.Button(image_window, text="Flip Vertically", command=lambda: self.flip_image(ax, canvas, vertical=True))
        flip_vertical_button.pack(side=tk.LEFT, padx=5)

        # Rotate button in the new window
        rotate_button_clockwise = tk.Button(image_window, text="Rotate Clockwise", command=lambda: self.rotate_image(ax, canvas, clockwise=False))
        rotate_button_clockwise.pack(side=tk.LEFT, padx=5)

        # Rotate counterclockwise button in the new window
        rotate_button_counterclockwise = tk.Button(image_window, text="Rotate Counterclockwise", command=lambda: self.rotate_image(ax, canvas, clockwise=True))
        rotate_button_counterclockwise.pack(side=tk.LEFT, padx=5)
        
        # Variable for tracking whether dragging is enabled
        self.drag_enabled = True

        # Variables for dragging
        self._drag_data = {"x": 0, "y": 0, "item": None}
        
        # Bind mouse events for dragging
        self.canvas_widget.bind("<ButtonPress-1>", self.on_press)
        self.canvas_widget.bind("<B1-Motion>", lambda event: self.on_drag(event, ax, canvas))

        # Connect the mouse click and release events to the drawing function
        self.cid_press = None
        self.cid_release = None


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
        self.accession_entry.delete(0, tk.END)
        self.accession_entry.insert(tk.END, self.accession_number.get())

        self.hn_entry.delete(0, tk.END)
        self.hn_entry.insert(tk.END, self.hospital_number.get())

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
        self.cid_press = cid_press
        self.cid_release = cid_release

    def activate_straight_line(self, ax, canvas):
        # Activate the drawing tool to draw a straight line on the image
        canvas.draw()

        # Connect the mouse click and release events to the drawing function
        cid_press = self.fig.canvas.mpl_connect("button_press_event", lambda event: self.straight_on_press(event, ax, canvas))
        cid_release = self.fig.canvas.mpl_connect("button_release_event", lambda event: self.straight_on_release(event, ax, canvas))

        # Store the connection IDs for later disconnection
        self.cid_press_straight = cid_press
        self.cid_release_straight = cid_release

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
    


# MAIN window
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")
    viewer = DICOMViewer(root)
    root.mainloop()