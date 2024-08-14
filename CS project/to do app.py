from tkinter import*
from tkinter import messagebox

added_task=open(file="added task.txt",mode="w")
to_do_app=Tk()
to_do_app.title("To Do")
to_do_app.resizable(False,False)

def add():
    
    task=task_entry.get()
    if task=="":
        messagebox.showerror("Error","Please enter something to add task")
    if task!="":
        added_task1=open(file="added task.txt",mode="a")
        task_list.insert(END,task)
        task_entry.delete(0,END)
        added_task1.write(task+"\n")

def delete():
    item=task_list.curselection()
    task_list.delete(item)

task_lbl=Label(to_do_app,text="Task",font=("arial",20,"bold"),width=20)
task_lbl.pack()

frame=Frame(to_do_app)
frame.pack()
scrollbar=Scrollbar(frame,orient=VERTICAL)
scrollbar.pack(side=RIGHT)

task_list=Listbox(frame,font=("arial",16),width=30,yscrollcommand=scrollbar.set)
task_list.pack(side=RIGHT)

scrollbar.config(command=task_list.yview)

task_entry=Entry(to_do_app,font="arial 16",bd=10,insertwidth=2,width=30)
task_entry.pack()

add_task=Button(to_do_app,text="Add task",font="arial 18 bold",background="green",foreground="white",activebackground="green",width=25,command=add)
add_task.pack()

delete_task=Button(to_do_app,text="Delete task",font="arial 18 bold",background="red",foreground="white",activebackground="red",width=25,command=delete)
delete_task.pack()

to_do_app.mainloop()