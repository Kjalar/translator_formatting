from tkinter import *
from tkinter import scrolledtext
import re
from tkinter import filedialog
from tkinter import messagebox 
from tkinter.ttk import Combobox 
import pyperclip


def formating_text(text):
    text_list = text.split('\n')
    result = ''
    for index, line in enumerate(text_list):
        if line == '':
            continue
        if re.search(r'[!?.]', line[-1]):
            if result == '' or result[-1] == '\n':
                result = result + line + '\n\n'
            else:
                result = ' '.join([result, line + '\n\n'])
        else:
            if result == '' or result[-1] == '\n':
                result += line
            else:
                result = ' '.join([result, line])
    return result


def formating():  
    res = txt.get('1.0','end-1c')
    result = formating_text(res)
    lbl.configure(text="Отформатированный текст:") 
    txt.delete(1.0, END)
    txt.insert(INSERT, result)


def clear():
    lbl.configure(text="Введите текст:") 
    txt.delete(1.0, END)


def check_file():
    file = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")))
    if file:
        try:
            clear()  
            with open(file, 'r', encoding='UTF-8') as file:
                text = file.read()
                txt.delete(1.0, END)
                txt.insert(INSERT, text)
        except Exception as err:
            messagebox.showerror('Что-то пошло не так...', err)


def paste_text():
    txt.insert(INSERT, pyperclip.paste())


def copy_text():
    pyperclip.copy(txt.get('1.0','end-1c'))


def main():
    window = Tk()
    w = window.winfo_screenwidth()  # ширина экрана
    h = window.winfo_screenheight()  # высота экрана
    window.minsize(int(w * 0.45), int(h * 0.5))
    window.geometry(f'{int(w * 0.45)}x{int(h * 0.5)}')
    window.title(u'Форматирование текста')

    btn = Button(window, text="Загрузить с файла", command=check_file)
    btn.place(x=10, y=10, width=160, height=30)

    btn = Button(window, text="Вставить", command=paste_text)
    btn.place(x=173, y=10, width=160, height=30)

    btn = Button(window, text="Отформатировать", command=formating)
    btn.place(x=336, y=10, width=160, height=30)

    btn = Button(window, text="Копировать", command=copy_text)
    btn.place(x=499, y=10, width=160, height=30)

    btn = Button(window, text="Очистить", command=clear)
    btn.place(x=662, y=10, width=160, height=30)

    global lbl 
    lbl = Label(window, text="Введите текст:", font=("Monospace", 12))
    lbl.place(relx=0.3, y=40, relwidth=0.4, height=55)

    global txt 
    txt = scrolledtext.ScrolledText(window)
    txt.place(x=10, y=90, relwidth=0.99, relheight=0.7)
    txt.focus()

    window.mainloop()

main()
