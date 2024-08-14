import periodictable
from tkinter import*
from tkinter import messagebox
periodic_table_app=Tk()
periodic_table_app.title("Periodic Table")
periodic_table_app.geometry("320x300")
periodic_table_app.config(bg='white')

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