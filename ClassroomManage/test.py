import tkinter as tk

def hit():
    l1 = tk.Label(window, text='True')
    l2 = tk.Label(window, text='False')

    if var1.get():
        l1.place(x=10, y=75)
        l2.forget()
    else:
        l2.place(x=10, y=75)
        l1.forget()

window = tk.Tk()
window.geometry('100x100')
var1 = tk.BooleanVar()
tk.Checkbutton(window, text='勾选', var=var1, onvalue=True, offvalue=False, command=hit).pack()
window.mainloop()

