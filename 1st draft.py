from tkinter import * #1นำเข้า module tkinter or tk interface for python 3.xx.xx
import tkinter.messagebox
from tkinter import ttk
import tkinter as tk
root = Tk() #2สร้างwidjet
root.title("GUI draft") #3สร้างหัวชื่อ(title)โปรแกรม
root.geometry("600x500")#4กำหนดขนาดเริ่มต้นหน้าจอ(กว้าง*ยาว) #ใช้ +x+y ในการกำหนดตำแหน่งเริ่มของหน้าจอ

#1)HN title and letterbox
myLabel1= Label(root,text="HN",fg="black",font=20).place(x=0,y=50)
txt=StringVar() #ตัวแปรเก็บค่าการกรอกข้อมูล
mytext=Entry(root,textvariable=txt).place(x=40,y=55)#กล่องHN

#2)Accesion title and letter box
myLabel2= Label(root,text="Accesion",fg="black",font=20).place(x=170,y=50)
txt=StringVar() #ตัวแปรเก็บค่าการกรอกข้อมูล
mytext=Entry(root,textvariable=txt).place(x=255,y=55)#กล่องAcces


#3)list title
listLabel= Label(root,text="List",fg="black",font=20).place(x=0,y=100)

#Create Listbox
listbox = ttk.Treeview(root, columns=('Column 1', 'Column 2'), show='headings')

#Column headings
listbox.heading('Column 1', text='HN')
listbox.heading('Column 2', text='Accesion')

# Insert HN and accesion into the Listbox
data = [('HN 1', 'Accesion 1'),
        ('HN 2', 'Accesion 2'),
        ('HN 3', 'Accesion 3'),
        ('HN 4', 'Accesion 4'),
        ('HN 5', 'Accesion 5'),
        ('HN 6', 'Accesion 6'),
        ('HN 7', 'Accesion 7'),
        ('HN 8', 'Accesion 8'),
        ('HN 9', 'Accesion 9'),
        ('HN 10', 'Accesion 10'),
        ('HN 11', 'Accesion 11'),
        ('HN 12', 'Accesion 12'),
        ('HN 13', 'Accesion 13'),
        ('HN 14', 'Accesion 14'),
        ('HN 15', 'Accesion 15'),
        # Add more data as needed
        ]

for item in data:
    listbox.insert("", "end", values=item)

#place the Listbox
listbox.place(x=0,y=130)


#4)display
displayLabel= Label(root,text="Display",fg="black",font=20).place(x=0,y=360)

#funtionเมื่อคลิกเลือกitemใน list
def on_select(event):
    selected_index = displaybox.curselection()
    if selected_index:
        selected_item = displaybox.get(selected_index)
        open_new_window(selected_item)

#funtionเปิดwindowใหม่
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

# Insert data into the displaybox
data = ['Accesion 1', 'Accesion 2', 'Accesion 3', 'Accesion 4', 'Accesion 5','Accesion 6','Accesion 7']

for item in data:   
    displaybox.insert(tk.END, item)

# Bind the selection event
displaybox.bind('<<ListboxSelect>>', on_select)
# Create a vertical scrollbar
scrollbar = tk.Scrollbar(root, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

#5search button
btn1 = Button(root,text="Search",fg="White",bg="green").place(x=500,y=400)



root.mainloop() #loopcheckเรื่อยๆระหว่างรันโปรแกรม