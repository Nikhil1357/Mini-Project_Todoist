import tkinter as tk
from tkinter import *
import tkinter.messagebox as tkmb
import tkinter.font as ft
from tkinter import font

import matplotlib.pyplot as plt
import numpy as np
import sqlite3

l1 = []
l2 = []
d_prior = {}

conn = sqlite3.connect('Todotasks.db')
c = conn.cursor()
c.execute("""CREATE TABLE if not exists todo_list(list_item CHAR(30));""")
conn.commit()
conn.close()

conn2 = sqlite3.connect('Todotasksckd.db')
c2 = conn2.cursor()
c2.execute("""CREATE TABLE if not exists todo_listckd(list_itemckd CHAR(30));""")
conn2.commit()
conn2.close()

conn = sqlite3.connect('Todotasks.db')
c = conn.cursor()
c.execute("SELECT * FROM todo_list")
records = c.fetchall()
conn.commit()
conn.close()

for i in records:
    l1.append(i[0])

conn2 = sqlite3.connect('Todotasksckd.db')
c2 = conn2.cursor()
c2.execute("SELECT * FROM todo_listckd")
records_ckd = c2.fetchall()
conn2.commit()
conn2.close()


for i in records_ckd:
    l2.append(i[0])





root = tk.Tk()
root.title("ToDoist - Todo List")
root.configure(bg="#cce6ff")
root.geometry("500x500")

lblTodo = Label(root, text="TODOIST", font=("Lato", 50), fg="#404040",bg="#cce6ff")#.place(x=120,y=65)

lblTodo.pack()


myFont = ft.Font(family='helvetica')

def showtask():

    if(len(l1)==0):

        tkmb.showinfo(title="Tasks",message = "The Tasks List is Empty !!")
    else:

        top = Toplevel()
        top.title("Tasks")
        top.configure(bg="#d1b3ff")
        lblTasks= Label (top,text="The Tasks are",font=("comicsans",10), fg="#000000")
        lblTasks.pack()
        T = Text(top, height=20, width=30)
        T.place(x=90,y=60)
        lblTasks.pack()
        top.geometry("400x400")
        ct = 0
        for i in l1:
            ct = ct+1
            i = str(ct)+") "+i+"\n"
            T.insert(tk.END, i)
        T.configure(state='disabled')



def get(event):
    task_Entered = AddTask_Entry.get()

    if (task_Entered == ""):
        tkmb.showwarning(title="Warning !", message="Please give a task name")
    else:
        top_added = Toplevel()
        top_added.title("Task")
        top_added.configure(bg="#cce6ff")
        lbladded = Label(top_added, text="\n\nTask "+task_Entered+" Added !!\n\n Make time to do it !!",font=("Calibri", 12), fg="#262626",bg="#cce6ff")#,img="java.png")
        lbladded.pack()
        top_added.geometry("200x180")
        l1.append(task_Entered)



def delete(event):
    task_Rem = AddTask_Entry.get()
    if (task_Rem == ""):
        tkmb.showwarning(title="Warning !", message="Please give a task name")
    else:
        if (task_Rem not in l1):
            tkmb.showwarning(title="Warning !", message="Task DNE")
        else:
            tkmb.showinfo(title="Task ",message ="GG !! Task "+task_Rem+" is checked off")
            l2.append(task_Rem)
            l1.remove(task_Rem)


def removeTask():
    global RemTask

    AddTask_Entry.place(x=225,y=150)
    lblenter.place(x=70,y=150)
    lblenter.config(text="Enter the task to be deleted :")
    #AddTask_Priority.destroy()
    AddTask_Entry.bind('<Return>',delete)


def addTask():
    global lblenter
    lblenter = Label(root, text="           Enter the task:     ")#.place(x=25,y=150)
    lblenter.place(x=65,y=150)
    if(checkvar1.get()==1):
        lblenter.configure(bg="#4d4d4d")

    else:
        lblenter.configure(bg="#cce6ff")
    global AddTask_Entry
    AddTask_Entry = tk.Entry(root, width=20)
    AddTask_Entry.place(x=180, y=150)
    AddTask_Entry.bind('<Return>', get)

def chart():
    try:
        x = len(l1)
        y = len(l2)
        if(x ==0 and y==0):
            tkmb.showinfo(title="Productivity !!", message="No tasks yet ")

        else:
            if(y>=x):
                tkmb.showinfo(title="Productivity !!", message="GG !! Tasks Checked are more than tasks unchecked \U0001F44F")

            pie = np.array([x, y])
            mylbl = ["Unchecked", "Checked"]

            plt.pie(pie, labels=mylbl)
            plt.legend()
            plt.title("Productivity pie")
            plt.show()
    except:
        tkmb.showwarning(title="Productivity !!", message="Unknown error occurred !!")


dta=0
def database():
    global dta
    dta=1
    conn = sqlite3.connect('Todotasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM todo_list;', )
    conn.commit()
    conn.close()

    conn2 = sqlite3.connect('Todotasksckd.db')
    c2 = conn2.cursor()
    c2.execute('DELETE FROM todo_listckd;', )
    conn2.commit()
    conn2.close()


def showcheck():
    if(len(l2)==0):
        tkmb.showinfo(title="Tasks", message="The Tasks List is Empty !!")
        #lblTasksckd = Label(topck,text = "The Tasks list is Empty",font=("Calibri", 10), fg="#595959")
        #lblTasksckd.place(x=43,y=57)
        #topck.geometry("200x200")
    else:
        topck = Toplevel()
        topck.title("Tasks")
        topck.configure(bg="#d1b3ff")
        lblTasksckd = Label (topck,text="The Checked tasks are",font=("comicsans",10))
        lblTasksckd.pack()
        Tckd = Text(topck, height=20, width=30)
        Tckd.place(x=90,y=60)
        lblTasksckd.pack()
        topck.geometry("400x400")
        ct = 0
        for i in l2:
            ct = ct+1
            i = str(ct)+") "+i+"\n"
            Tckd.insert(tk.END, i)
        Tckd.configure(state='disabled')

try:
    button_add = tk.Button(root, text="Add Task", width=20, command=addTask, bg="#d9d9d9")  # ,font=myFont)
    button_add.place(x=170, y=200)
    button_Remove = tk.Button(root, text="Remove Task/Check Task", width=20, command=removeTask, bg="#d9d9d9")
    button_Remove.place(x=170, y=250)
    button_ShowUn = tk.Button(root, text="Show Checked tasks", width=20, bg="#d9d9d9", command=showcheck)
    button_ShowUn.place(x=170, y=400)
    button_ShowTask = tk.Button(root, text="Show Tasks", width=20, bg="#d9d9d9", command=showtask)
    button_ShowTask.place(x=170, y=300)
    button_ShowChart = tk.Button(root, text="Productivity Chart", width=20, bg="#d9d9d9", command=chart)
    button_ShowChart.place(x=170, y=350)
    button_data = tk.Button(root, text="Clear Data", width=8, bg="#cce6ff", command=database)
    button_data.place(x=400, y=400)

except:
    tkmb.showwarning(title="Warning ",message="Unknown error occurred")

def toggle():
    if(checkvar1.get()==1):
        root.configure(bg="#4d4d4d")
        lblTodo.configure(bg="#4d4d4d",fg="#e6e6e6")
        chkbtn1.configure(bg="#4d4d4d",fg="#e6e6e6")
        button_data.config(bg="#4d4d4d",fg="#f2f2f2")

    elif(checkvar1.get()==0):
        root.configure(bg = "#cce6ff")
        lblTodo.configure(fg = "#404040", bg = "#cce6ff")
        chkbtn1.configure(fg = "#404040", bg = "#cce6ff")
        button_data.config(bg = "#cce6ff",fg="#262626")

global checkvar1
checkvar1 = IntVar()
global chkbtn1
chkbtn1 = Checkbutton(root, text="Dark", variable=checkvar1, onvalue=1, offvalue=0, height=2, width=2,command=toggle)
chkbtn1.place(x=420,y=70)

chkbtn1.configure(fg = "#404040", bg = "#cce6ff")



root.mainloop()

conn = sqlite3.connect('Todotasks.db')
c = conn.cursor()
c.execute('DELETE FROM todo_list;', )
items = l1

conn2 = sqlite3.connect('Todotasksckd.db')
c2 = conn2.cursor()
c2.execute('DELETE FROM todo_listckd;', )
items_ckd = l2

if(dta==0):

    for item in items:
        item = str(item)
        c.execute("""INSERT INTO todo_list VALUES (:item)""",
                  {
                      'item':str(item)
                  })

    conn.commit()
    conn.close()

    for itemckd in items_ckd:
        itemckd = str(itemckd)
        c2.execute("""INSERT INTO todo_listckd VALUES (:itemckd)""",
                  {
                      'itemckd':str(itemckd)
                  })
    conn2.commit()
    conn2.close()

