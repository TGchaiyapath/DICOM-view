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
        image_window.geometry("950x700")
        # Matplotlib figure for displaying the image in the new window
        self.fig, ax = plt.subplots(figsize=(6.5, 6.5))
        canvas = FigureCanvasTkAgg(self.fig, master=image_window)
        self.canvas_widget = canvas.get_tk_widget()  # Fix here
        self.canvas_widget.place(x=0,y=30)

        # Load the DICOM image in the new window    
        self.load_dicom_image_internal(ax, canvas)


        # Button to toggle drag functionality
        self.toggle_drag_button = tk.Button(image_window, text="Toggle Drag", command=self.toggle_drag)
        self.toggle_drag_button.place(x=10,y=0)

        # Next and Previous buttons in the new window
        next_button = tk.Button(image_window, text="Next", command=lambda: self.show_next(ax, canvas))
        next_button.place(x=90,y=0)
        image_window.bind("<Right>", lambda event: self.show_next(ax, canvas))
        prev_button = tk.Button(image_window, text="Previous", command=lambda: self.show_previous(ax, canvas))
        prev_button.place(x=130,y=0)
        image_window.bind("<Left>", lambda event: self.show_previous(ax, canvas))

        # Load a zoom in icon image
        ZM_icon_path = os.path.abspath(r"C:\Users\Admin\Desktop\TG\TEST\icon\zoom-in.png")  
        icon_ZM = tk.PhotoImage(file=ZM_icon_path)
        self.zoom_in_icon = icon_ZM.subsample(27, 27)

        # Zoom in button with icon
        zoom_in_button = tk.Button(image_window, command=lambda: self.zoom_in(ax, canvas), image=self.zoom_in_icon, )
        zoom_in_button.place(x=190,y=0)
        image_window.bind("<Key-z>", lambda event: self.zoom_in(ax, canvas))

        # Load a zoom out icon image
        ZO_icon_path = os.path.abspath(r"C:\Users\Admin\Desktop\TG\TEST\icon\magnifying-glass.png")  
        icon_ZO = tk.PhotoImage(file=ZO_icon_path)
        self.zoom_out_icon = icon_ZO.subsample(27, 27)
        #Zoom out button
        zoom_out_button = tk.Button(image_window, command=lambda: self.zoom_out(ax, canvas),image=self.zoom_out_icon)
        zoom_out_button.place(x=220,y=0)
        image_window.bind("<Key-x>", lambda event: self.zoom_out(ax, canvas))
        
        # Load a straight icon image
        straight_icon_path = os.path.abspath(r"C:\Users\Admin\Desktop\TG\TEST\icon\shape.png")  
        icon_ST = tk.PhotoImage(file=straight_icon_path)
        self.straight_icon = icon_ST.subsample(27, 27)
        # Add drawing tool button in the new window
        straight_line_button = tk.Button(image_window, command=lambda: self.activate_straight_line(ax, canvas),image=self.straight_icon)
        straight_line_button.place(x=250,y=0)

        # Load a dashe icon image
        dashed_icon_path = os.path.abspath(r"C:\Users\Admin\Desktop\TG\TEST\icon\dashed line.png")  
        icon_D = tk.PhotoImage(file=dashed_icon_path)
        self.dashed_icon = icon_D.subsample(27, 27)
        #dash line button
        dashed_line_button = tk.Button(image_window, command=lambda: self.activate_dashed_line(ax, canvas),image=self.dashed_icon)
        dashed_line_button.place(x=280,y=0)

        # Load a dashe icon image
        arrow_icon_path = os.path.abspath(r"C:\Users\Admin\Desktop\TG\TEST\icon\up-right-arrow.png")  
        icon_AR = tk.PhotoImage(file=arrow_icon_path)
        self.arrow_icon = icon_AR.subsample(27, 27)
        #arrow
        single_arrow_button = tk.Button(image_window, command=lambda: self.activate_single_ended_arrow(ax, canvas),image=self.arrow_icon            )
        single_arrow_button.place(x=310,y=0)

        # Rotate/Flip button in the new window
        rotate_flip_button = tk.Button(image_window, text="Rotate/Flip", command=self.show_rotate_flip_menu)
        rotate_flip_button.place(x=340, y=0)  # Adjust the coordinates as needed

        # Display the menu at the button location in the image window
        self.rotate_flip_button = tk.Button(image_window, text="Rotate/Flip", command=self.show_rotate_flip_menu)
        self.rotate_flip_button.place(x=340, y=0)  # Adjust the coordinates as needed
        
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
        # Contrast adjustment slider
        contrast_label = tk.Label(image_window, text="Contrast:")
        contrast_label.place(x=460, y=30)

        contrast_slider = tk.Scale(image_window, from_=0, to=2, resolution=0.01, orient=tk.HORIZONTAL, length=150, command=lambda value: self.adjust_contrast(value, ax, canvas))
        contrast_slider.set(0)  # Default contrast
        contrast_slider.place(x=520, y=30)
        # Listbox to display DICOM tags
        tags_listbox = Listbox(image_window, selectbackground='lightgray', selectmode=tk.SINGLE, height=10, width=30)
        tags_listbox.place(x=675,y=50)

        # Load DICOM tags into the Listbox
        self.load_dicom_tags(tags_listbox)

        # Function to update Listbox when a new image is displayed
        def update_tags_listbox(ax, canvas):
            tags_listbox.delete(0, tk.END)  # Clear existing items
            self.load_dicom_tags(tags_listbox)  # Load DICOM tags for the current image

        # Bind the update function to the canvas redraw event
        canvas.mpl_connect('draw_event', lambda event: update_tags_listbox(ax, canvas))
    def adjust_contrast(self, contrast_factor, ax, canvas):
        if self.file_paths:
            try:
                # Read the DICOM file
                dicom_data = pydicom.dcmread(self.file_paths[self.current_index])

                # Apply contrast adjustment
                adjusted_image = dicom_data.pixel_array * float(contrast_factor)

                # Clip pixel values to ensure they are within the valid range
                adjusted_image = np.clip(adjusted_image, 0, 255)

                # Display the adjusted image using matplotlib
                ax.clear()
                ax.imshow(adjusted_image, cmap=plt.cm.gray)
                ax.axis('off')  # Hide the axes
                canvas.draw()

                # Clear error message
                self.error_label.config(text="")
            except Exception as e:
                # Display an error message if there is an issue
                self.error_label.config(text=f"Error: {str(e)}")    
    def show_rotate_flip_menu(self):
        # Create a menu for rotate and flip options
        rotate_flip_menu = Menu(self.master, tearoff=0)

        # Add rotation options to the menu
        rotate_menu = Menu(rotate_flip_menu, tearoff=0)
        rotate_menu.add_command(label="Clockwise", command=lambda: self.rotate_image(clockwise=True))
        rotate_menu.add_command(label="Counterclockwise", command=lambda: self.rotate_image(clockwise=False))
        rotate_flip_menu.add_cascade(label="Rotate", menu=rotate_menu)

        # Add flip options to the menu
        flip_menu = Menu(rotate_flip_menu, tearoff=0)
        flip_menu.add_command(label="Horizontal", command=lambda: self.flip_image(horizontal=True))
        flip_menu.add_command(label="Vertical", command=lambda: self.flip_image(vertical=True))
        rotate_flip_menu.add_cascade(label="Flip", menu=flip_menu)

        # Display the menu just below the button
        self.rotate_flip_button.update()
        rotate_flip_menu.post(self.rotate_flip_button.winfo_rootx(), self.rotate_flip_button.winfo_rooty() + self.rotate_flip_button.winfo_height())

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
    


# MAIN window
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x400")
    viewer = DICOMViewer(root)
    root.mainloop()
