import tkinter as tk

def start_drag(event):
    global last_x, last_y
    last_x = event.x
    last_y = event.y

def drag_text(event):
    global last_x, last_y
    new_x, new_y = event.x, event.y
    dx = new_x - last_x
    dy = new_y - last_y
    canvas.move(text_id, dx, dy)
    last_x = new_x
    last_y = new_y

# Create the main window
root = tk.Tk()
root.title("Move Text Only by Dragging")

# Create a canvas widget
canvas = tk.Canvas(root, width=400, height=200, bg="white")
canvas.pack(padx=10, pady=10)

# Add text to the canvas
text_id = canvas.create_text(100, 100, text="Drag only me!", font=("Arial", 24), fill="blue")

# Bind mouse events to the text item
canvas.tag_bind(text_id, "<Button-1>", start_drag)
canvas.tag_bind(text_id, "<B1-Motion>", drag_text)

# Initialize variables to store the last mouse coordinates
last_x = 0
last_y = 0

# Run the Tkinter event loop
root.mainloop()
