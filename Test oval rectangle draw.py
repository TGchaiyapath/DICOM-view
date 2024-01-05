import tkinter as tk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Drawing App")
        
        # Create a Canvas widget
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg='white')
        self.canvas.pack(padx=10, pady=10)
        
        # Create buttons
        self.rect_button = tk.Button(self.root, text="Draw Rectangle", command=self.select_rectangle)
        self.rect_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.oval_button = tk.Button(self.root, text="Draw Oval", command=self.select_oval)
        self.oval_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Binding mouse events
        self.canvas.bind("<Button-1>", self.start_shape)
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        
        # Variables
        self.start_x, self.start_y = None, None
        self.current_shape = None
        self.selected_shape = 'rectangle'  # Default shape is rectangle
        
    def select_rectangle(self):
        self.selected_shape = 'rectangle'
        
    def select_oval(self):
        self.selected_shape = 'oval'
        
    def start_shape(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.selected_shape == 'rectangle':
            self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='black')
        elif self.selected_shape == 'oval':
            self.current_shape = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, outline='black')
        
    def draw_shape(self, event):
        if self.selected_shape == 'rectangle':
            self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
        elif self.selected_shape == 'oval':
            self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
