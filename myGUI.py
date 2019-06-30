from tkinter import *
from PIL import Image, ImageTk
import os

def onclick():
    os.system('main.py')


def stop():
    quit()


def run():
    root = Tk()

    root.geometry("700x670")

    root.minsize(450, 300)

    root.title("VOICE ASSISTANT = JARVIS")

    hi = Label(text="Hello  I  Am  \"ECHO\"", bg='black', fg="white", padx=20, pady=15,
               borderwidth=4, relief=RIDGE, font='comicsansms 14 bold')

    hi.pack(fill='x')

    by = Label(text="© developed by NvN", bg='black', fg="white", padx=20, pady=12,
               borderwidth=4, relief=RIDGE, font='comicsansms 14 bold')

    by.pack(fill='x', side=BOTTOM)

    by1 = Label(bg='green', fg="white", padx=20, pady=10,
                borderwidth=4, relief=SUNKEN, font='comicsansms 14 bold')

    by1.pack(fill='x', side=BOTTOM, pady=5)

    b1 = Button(by1, fg='red', bg='black', text='Start', pady=10, padx=10, font='bold', command=onclick)
    b1.pack(side=LEFT, padx=150)

    b2 = Button(by1, fg='white', bg='black', text='Quit', pady=10, padx=10, font='bold', command=stop)
    b2.pack(side=LEFT, padx=100)

    image = Image.open("1.jpg")
    photo = ImageTk.PhotoImage(image)

    my_label = Label(image=photo)

    my_label.pack()

    root.maxsize(1000, 700)

    root.mainloop()


if __name__ == "__main__":
    run()








