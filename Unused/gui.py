import tkinter as tk
import tkinter.messagebox as msgbox
top = tk.Tk()


def hi():
    msgbox.showinfo('Title', 'Contents')

B = tk.Button(top, text='View Benchmarks', command=hi)

B.pack()
top.mainloop()