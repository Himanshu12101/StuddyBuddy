#importing required libraries 
from tkinter import*
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import date
import periodictable

#creating window
root=Tk()
root.geometry('700x720')
root.resizable(False,False)
root.config(background="white")

#Adding title and icon
root.title("StudyBuddy")
app_icon=PhotoImage(file='study buddy logo.png')
root.iconphoto(True,app_icon)

#Displaying welcome message
welcome_message_img=PhotoImage(file="welcome message.png")
welcome_message_lbl=Label(root,image=welcome_message_img,bg="white",relief="flat")
welcome_message_lbl.place(x=41,y=34)

#timings for pomodoro
work_duration=25*60
break_duration=5*60
remaining_time=work_duration

#defining commands for To Do  App
def open_to_do_app():
    to_do_app=Tk()
    to_do_app.title("To Do")
    to_do_app.resizable(False,False)
    
    #Command for adding task
    def add():
        task=task_entry.get()
        if task=="":
            messagebox.showerror("Error","Please enter something to add task")
        if task!="":
            task_list.insert(END,task)
            task_entry.delete(0,END)

            #Adding task in file because when user reopen app he/she gets undeleted and incompleted task
            adding_task_in_file=open(file='added task.txt',mode='a')
            adding_task_in_file.write(task+'\n')

    def delete():
        deleting_task_from_file=open(file='added task.txt',mode='r')
        tasks=deleting_task_from_file.readlines()
        item=task_list.curselection()
        item=item[0]
        item=int(item)
        for i in range(len(tasks)):
            if i==item:
                tasks.pop(i)#removing deleted or completed task from text file
        task_list.delete(item)
        again_adding_task=open(file='added task.txt',mode='w')
        again_adding_task.writelines(tasks)#to get remaining task that are not deleted or completed
         
    task_lbl=Label(to_do_app,text="Task",font=("arial",20,"bold"),width=20)
    task_lbl.pack()

    frame=Frame(to_do_app)
    frame.pack()
    scrollbar=Scrollbar(frame,orient=VERTICAL)
    scrollbar.pack(side=RIGHT)

    task_list=Listbox(frame,font=("arial",16),width=30,yscrollcommand=scrollbar.set)
    task_list.pack(side=RIGHT)

    task_history_file=open(file='added task.txt',mode='r')
    task_history=task_history_file.readlines()
    for i in range(len(task_history)):
        task_list.insert(END,task_history[i])

    scrollbar.config(command=task_list.yview)

    task_entry=Entry(to_do_app,font="arial 16",bd=10,insertwidth=2,width=30)
    task_entry.pack()

    add_task=Button(to_do_app,text="Add task",font="arial 18 bold",background="green",foreground="white",
                    activebackground="green",width=25,command=add)
    add_task.pack()

    delete_task=Button(to_do_app,text="Delete task",font="arial 18 bold",background="red",foreground="white",
                       activebackground="red",width=25,command=delete)
    delete_task.pack()
    
    mark_as_done=Button(to_do_app,text="Mark as Done",font="arial 18 bold",background="#3a86ff",foreground="white",
                        activebackground="green",width=25,command=delete)
    mark_as_done.pack()
    to_do_app.mainloop()    

#Defining command for opening pomodoro app
def  open_pomodoro_app():
    #creating window for pomodoro app
    pomodoro=Tk()
    pomodoro.title('Pomodoro Timer')
    pomodoro.geometry('382x380')
    pomodoro.config(background='white')
    pomodoro.resizable(False,False)

    #displaying title
    title_lbl=Label(pomodoro,text='Pomodoro',font='arial 30 bold',bg='white')
    title_lbl.place(x=20,y=20)

    #Formating time
    def format_time(duration):
        mins,secs=divmod(duration,60)
        return f"{mins:02d}:{secs:02d}"
        
    #Creating timing label
    time_lbl=Label(pomodoro,text=format_time(work_duration),font="Arial 70 bold",bg='white')
    time_lbl.place(x=20,y=72)

    #defining command for stopping timer
    def stop_timer():
        pomodoro.after_cancel(pomodoro.var_after)
        start_btn.config(state=NORMAL)
        stop_btn.config(state=DISABLED)

    #defining command for starting timer
    def start_timer():
        start_btn.config(state=DISABLED)
        stop_btn.config(state=NORMAL)
        global remaining_time
        if remaining_time>0:
            remaining_time-=1
            time_lbl.config(text=format_time(remaining_time))
            var_after=pomodoro.after(1000,start_timer)
            pomodoro.var_after=var_after
        
        if remaining_time==0:
            global break_duration
            pomodoro.after_cancel(pomodoro.var_after)
            start_btn.config(state=NORMAL)
            messagebox.showinfo('Session Completed','Well done!, you have completed your task.Now take a break')

            #Break session
            break_frame=Frame(pomodoro,bg='white',width=382,height=380)
            break_frame.place(x=0,y=0)
            break_lbl=Label(break_frame,text="Break Time",font='Arial 30 bold',bg='white')
            break_lbl.place(x=20,y=20)
            break_time_lbl=Label(break_frame,text=format_time(break_duration),font="Arial 70 bold",bg='white')
            break_time_lbl.place(x=20,y=72)
            def start_break():
                break_start_btn.config(state=DISABLED)
                break_stop_btn.config(state=NORMAL)
                global break_duration
                if break_duration>0:
                    break_duration-=1
                    break_time_lbl.config(text=format_time(break_duration))
                    frame_var_after=break_frame.after(1000,start_break)
                    break_frame.frame_var_after=frame_var_after
                if break_duration==0:
                    global remaining_time
                    global time_lbl
                    break_frame.after_cancel(break_frame.frame_var_after)
                    messagebox.showinfo('Break completed',"Let's get back to work!")
                    break_frame.destroy()
                    remaining_time=work_duration
                    time_lbl.config(text=format_time(remaining_time))


            def stop_break():
                break_frame.after_cancel(break_frame.frame_var_after)
                break_start_btn.config(state=NORMAL)
                break_stop_btn.config(state=DISABLED)

            def exit_break():
                global remaining_time
                global time_lbl
                break_frame.destroy()
                remaining_time=work_duration
                time_lbl.config(text=format_time(remaining_time))

            break_start_btn=Button(break_frame,text='Start',font='arial 18 bold',relief='flat',
                                   activebackground='#e63946',activeforeground='white',background='#e63946',
                                   bd=0,width=10,command=start_break)
            break_start_btn.place(x=20,y=238)

            break_stop_btn=Button(break_frame,text='Stop',font='arial 18 bold',relief='flat',
                                  activebackground='#e63946',activeforeground='white',background='#e63946',
                                  bd=0,width=10,command=stop_break,state=DISABLED)
            break_stop_btn.place(x=202,y=238)
            
            exit_btn=Button(break_frame,text='Exit',font='arial 18 bold',relief='flat',
                            activebackground='#e63946',activeforeground='white',background='#e63946',
                            bd=0,width=10,command=exit_break)
            exit_btn.place(x=20,y=300)

    #creating buttons
    start_btn=Button(pomodoro,text='Start',font='arial 18 bold',relief='flat',activebackground='#e63946',
                     activeforeground='white',background='#e63946',bd=0,width=10,command=start_timer)
    start_btn.place(x=20,y=238)

    stop_btn=Button(pomodoro,text='Stop',font='arial 18 bold',relief='flat',activebackground='#e63946',
                    activeforeground='white',background='#e63946',bd=0,width=10,command=stop_timer,state=DISABLED)
    stop_btn.place(x=202,y=238)

    pomodoro.mainloop()

#defining app for calendar app
def open_calendar_app():
    current_date=str(date.today())
    date_split=current_date.split('-')
    current_year=date_split[0]
    current_month=date_split[1]
    current_day=date_split[2]

    calendar_app=Tk()
    calendar_app.resizable(False,False)
    calendar_app.title('Calendar')

    cal=Calendar(calendar_app,selectmode="day",date_patetrn="yyyy-mm-dd",year=int(current_year),
                 month=int(current_month),day=int(current_day))
    cal.pack()
    calendar_app.mainloop()

#defining command for calculator app
def open_calculator_app():
    calculator_app=Tk()
    calculator_app.title("Calculator")
    calculator_app.resizable(False,False)

    #creating entry
    entry=Entry(calculator_app,font='arial 16')
    entry.grid(row=0,columnspan=4)

    #defining commands
    def click(a):
        value=entry.get()
        value=value+a
        entry.delete(0,END)
        entry.insert(0,value)

    def equate():
        try:
            global value
            value=entry.get()
            value=eval(value)
            entry.delete(0,END)
            entry.insert(0,value)
        except:
           messagebox.showerror("Error","An error occured.Please check your calculations again!")
    
    def clear():
        entry.delete(0,END)

    def percent():
        global value
        value=float(entry.get())
        value=value/100
        entry.delete(0,END)
        entry.insert(0,value)
    #creating buttons
    brac1=Button(calculator_app,text="(",font='arial 16',width=4,command=lambda:click("("))
    brac1.grid(row=1,column=0)

    brac2=Button(calculator_app,text=")",font='arial 16',width=4,command=lambda:click(")"))
    brac2.grid(row=1,column=1)

    clear=Button(calculator_app,text="C",font='arial 16',width=4,command=clear)
    clear.grid(row=1,column=2)

    percentage=Button(calculator_app,text="%",font='arial 16',width=4,command=percent)
    percentage.grid(row=1,column=3)

    b7=Button(calculator_app,text="7",font='arial 16',width=4,command=lambda:click("7"))
    b7.grid(row=2,column=0)

    b8=Button(calculator_app,text="8",font='arial 16',width=4,command=lambda:click("8"))
    b8.grid(row=2,column=1)

    b9=Button(calculator_app,text="9",font='arial 16',width=4,command=lambda:click("9"))
    b9.grid(row=2,column=2)

    add=Button(calculator_app,text="+",font='arial 16',width=4,command=lambda:click("+"))
    add.grid(row=2,column=3)

    b4=Button(calculator_app,text="4",font='arial 16',width=4,command=lambda:click("4"))
    b4.grid(row=3,column=0)

    b5=Button(calculator_app,text="5",font='arial 16',width=4,command=lambda:click("5"))
    b5.grid(row=3,column=1)

    b6=Button(calculator_app,text="6",font='arial 16',width=4,command=lambda:click("6"))
    b6.grid(row=3,column=2)

    sub=Button(calculator_app,text="-",font='arial 16',width=4,command=lambda:click("-"))
    sub.grid(row=3,column=3)

    b1=Button(calculator_app,text="1",font='arial 16',width=4,command=lambda:click("1"))
    b1.grid(row=4,column=0)

    b2=Button(calculator_app,text="2",font='arial 16',width=4,command=lambda:click("2"))
    b2.grid(row=4,column=1)

    b3=Button(calculator_app,text="3",font='arial 16',width=4,command=lambda:click("3"))
    b3.grid(row=4,column=2)

    multiply=Button(calculator_app,text="*",font='arial 16',width=4,command=lambda:click("*"))
    multiply.grid(row=4,column=3)

    decimal=Button(calculator_app,text=".",font='arial 16',width=4,command=lambda:click("."))
    decimal.grid(row=5,column=0)

    b0=Button(calculator_app,text="0",font='arial 16',width=4,command=lambda:click("0"))
    b0.grid(row=5,column=1)

    equal=Button(calculator_app,text="=",font='arial 16',width=4,command=equate)
    equal.grid(row=5,column=2)

    divide=Button(calculator_app,text="/",font='arial 16',width=4,command=lambda:click("/"))
    divide.grid(row=5,column=3)


#defining commands for periodic table
def open_periodictable_app():
    periodic_table_app=Tk()
    periodic_table_app.title("Periodic Table")
    periodic_table_app.geometry("320x300")
    periodic_table_app.config(bg='white')
    periodic_table_app.resizable(False,False)

    search_lbl=Label(periodic_table_app,text="Enter element name to search",font="arial 16 bold",bg='white')
    search_lbl.place(x=0,y=0)
    element_entry=Entry(periodic_table_app,font='arial 16',width=25,bd=10)
    element_entry.place(x=0,y=40)

    #defining commands
    def search_element():
        try:
            element=element_entry.get().lower()
            element=periodictable.elements.name(element)
            element_symbol_lbl.config(text=element.symbol)
            element_atomic_number_lbl.config(text=element.number)
            element_atomic_mass_lbl.config(text=element.mass)
        except:
            messagebox.showerror("Error","Element not found!")
            

    search_btn=Button(periodic_table_app,text="Search",font='arial 16 bold',background="green",bd=3,command=search_element)
    search_btn.place(x=0,y=100)

    symbol_lbl=Label(periodic_table_app,text='Symbol:',font='arial 16',bg='white')
    symbol_lbl.place(x=0,y=160)

    element_symbol_lbl=Label(periodic_table_app,font='arial 16',bg='white')
    element_symbol_lbl.place(x=80,y=160)

    atomic_number_lbl=Label(periodic_table_app,text='Atomic number:',font='arial 16',bg='white')
    atomic_number_lbl.place(x=0,y=200)

    element_atomic_number_lbl=Label(periodic_table_app,font='arial 16',bg='white')
    element_atomic_number_lbl.place(x=150,y=200)

    atomic_mass_lbl=Label(periodic_table_app,text='Atomic mass:',font='arial 16',bg='white')
    atomic_mass_lbl.place(x=0,y=240)

    element_atomic_mass_lbl=Label(periodic_table_app,font='arial 16',bg='white')
    element_atomic_mass_lbl.place(x=130,y=240)

    periodic_table_app.mainloop()

#Creating icons of applications on main window
    
#Icon for pomodoro
pomodoro_img=PhotoImage(file="Pomodoro.png")
pomodoro_icon=Button(root,image=pomodoro_img,bg="white",relief="flat",bd=0,activebackground='white',
                     command=open_pomodoro_app)
pomodoro_icon.place(x=37,y=165)

#Icon for to-do
to_do_img=PhotoImage(file="to do.png")
to_do_icon=Button(root,image=to_do_img,bg="white",relief="flat",bd=0,activebackground='white',
                  command=open_to_do_app)
to_do_icon.place(x=258,y=165)

#Icon for calendar
calendar_img=PhotoImage(file='calendar.png')
calendar_icon=Button(root,image=calendar_img,bg="white",relief="flat",bd=0,activebackground='white',
                     command=open_calendar_app)
calendar_icon.place(x=37,y=414)

#Icon for calculator
calculator_img=PhotoImage(file='calculator.png')
calculator_icon=Button(root,image=calculator_img,bg="white",relief="flat",bd=0,activebackground='white',
                       command=open_calculator_app)
calculator_icon.place(x=258,y=414)

#Icon for periodic table
periodic_table_img=PhotoImage(file='periodic table.png')
periodic_table_icon=Button(root,image=periodic_table_img,bg="white",relief="flat",bd=0,activebackground='white',
                           command=open_periodictable_app)
periodic_table_icon.place(x=479,y=165)

#for running app
root.mainloop()