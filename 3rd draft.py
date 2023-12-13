from tkinter import * #1นำเข้า module tkinter or tk interface for python 3.xx.xx
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk

root = tk.Tk() #2สร้างwidjet
root.title("GUI draft") #3สร้างหัวชื่อ(title)โปรแกรม
root.geometry("600x500")#4กำหนดขนาดเริ่มต้นหน้าจอ(กว้าง*ยาว) #ใช้ +x+y ในการกำหนดตำแหน่งเริ่มของหน้าจอ

#1)HN la
HNLabel= Label(root,text="HN",fg="black",font=("Times New Roman", 15)).place(x=0,y=20)
#2)Accesion label
ACLabel= Label(root,text="Accesion",fg="black",font=("Times New Roman",15)).place(x=170,y=20)


                                                    
#3)list title
listLabel= Label(root,text="List",fg="black",font=("Times New Roman",16)).place(x=0,y=70)

def on_select(event):
    # Get the current selected item in the Treeview
    selected_item = tree.selection()
    item_values = tree.item(selected_item, "values")

#function hn search
def search_HN():
    search_text = entry.get().lower()
    tree.delete(*tree.get_children())  # Clear the Treeview

    # Populate the Treeview with matching items
    for item in all_items:
         if search_text in item[0].lower():
            tree.insert("", tk.END, values=item)

#function ac search
def search_AC():
    search_text1 = entry2.get().lower()
    tree.delete(*tree.get_children())  # Clear the Treeview

    # Populate the Treeview with matching items
    for item in all_items:
         if search_text1 in item[1].lower():
            tree.insert("", tk.END, values=item)            
       


all_items = [   ("Apple", "Fruit"),
    ("Apple", "Vegetable"),
    ("Carrot", "Vegetable"),
    ("Grapes", "Fruit"),
    ("Broccoli", "Vegetable"),
    ("Orange", "Fruit"),
    ("Tomato", "Vegetable"),
    ("Pear", "Fruit"),
    ("Cucumber", "Vegetable"),
    ("Strawberry", "Fruit"),
    ("Watermelon", "Fruit")]
            
#Create Listbox widjet
tree = ttk.Treeview(root, columns=("Item", "Category"), show="headings", selectmode=tk.BROWSE)
tree.place(x=0,y=100)


#HN entry box
entry = tk.Entry(root, width=20)
entry.place(x=40,y=25)
entry.bind("<KeyRelease>", lambda event: search_HN())

#ac entry box
entry2 = tk.Entry(root, width=20)
entry2.place(x=255,y=25)
entry2.bind("<KeyRelease>", lambda event: search_HN())
# Define column headings
tree.heading("Item", text="Item")
tree.heading("Category", text="Category")

# Set column widths
tree.column("Item", width=150)
tree.column("Category", width=150)

# Add items to the Treeview
for item in all_items:
    tree.insert("", tk.END, values=item)



#4)display
displayLabel= Label(root,text="Display",fg="black",font=20).place(x=0,y=360)

#funtionเมื่อคลิกเลือกitemใน list
def Click(event):
    selected_index = displaybox.curselection()
    if selected_index:
        selected_item = displaybox.get(selected_index)
        open_new_window(selected_item)


#funtion1Q  1Qwindowใหม่
def open_new_window(selected_item):
    new_window = tk.Toplevel(root)
    new_window.title(f"Details for {selected_item}")
    new_window.geometry('600x400')

    # Add content to the new window
    AcIMG = tk.Label(new_window, text=f"image of {selected_item}")
    AcIMG.place(x=250,y=150)

    HN = tk.Label(new_window,text="HN",font=20)
    HN.place(x=0,y=350)
    AC = tk.Label(new_window,text="Accesion",font=20)
    AC.place(x= 200,y=350)
    Acces = tk.Label(new_window,text=f"{selected_item}")
    Acces.place(x= 300,y=355)
    #ลูกศร
    Larrow = Button(new_window,text="<",fg="black").place(x=500,y=350)
    Rarrow = Button(new_window,text=">",fg="black").place(x=525,y=350)
    

#Create displaybox
displaybox = tk.Listbox(root,selectmode=tk.SINGLE, width=30, height=5)
#Place the displaybox
displaybox.place(x=0,y=390)

for item in all_items:   
    displaybox.insert(tk.END, item[1])


# Bind the selection event
displaybox.bind('<<ListboxSelect>>', Click)


#5search button
#btn1 = Button(root,text="Search",fg="White",bg="green").place(x=500,y=400)



root.mainloop() #loopcheckเรื่อยๆระหว่างรันโปรแกรม