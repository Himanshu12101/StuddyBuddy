from tkinter import*
from tkinter import messagebox 

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
    
#timings
work_duration=25*60
break_duration=5*60
remaining_time=work_duration

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
        break_lbl=Label(break_frame,text="Break Time",font='Arial 18 bold',bg='white')
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

        break_start_btn=Button(break_frame,text='Start',font='arial 18 bold',relief='flat',activebackground='#e63946',activeforeground='white',background='#e63946',bd=0,width=10,command=start_break)
        break_start_btn.place(x=20,y=238)

        break_stop_btn=Button(break_frame,text='Stop',font='arial 18 bold',relief='flat',activebackground='#e63946',activeforeground='white',background='#e63946',bd=0,width=10,command=stop_break,state=DISABLED)
        break_stop_btn.place(x=202,y=238)
        
        exit_btn=Button(break_frame,text='Exit',font='arial 18 bold',relief='flat',activebackground='#e63946',activeforeground='white',background='#e63946',bd=0,width=10,command=exit_break)
        exit_btn.place(x=20,y=300)

#creating buttons
start_btn=Button(pomodoro,text='Start',font='arial 18 bold',relief='flat',activebackground='#e63946',activeforeground='white',background='#e63946',bd=0,width=10,command=start_timer)
start_btn.place(x=20,y=238)

stop_btn=Button(pomodoro,text='Stop',font='arial 18 bold',relief='flat',activebackground='#e63946',activeforeground='white',background='#e63946',bd=0,width=10,command=stop_timer,state=DISABLED)
stop_btn.place(x=202,y=238)

pomodoro.mainloop()