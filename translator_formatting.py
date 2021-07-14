from tkinter import Tk, Label, END, INSERT, StringVar
from tkinter.ttk import Combobox, Style, Button
from tkinter import scrolledtext
import re
from tkinter import filedialog
from tkinter import messagebox
from googletrans import Translator


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


class StartApp:
    def __init__(self, window):
        self.window = window
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        self.window.minsize(int(width * 0.45), int(height * 0.5))
        self.window.geometry(f'{int(width * 0.45)}x{int(height * 0.5)}')
        self.window.title(u'Форматирование и перевод текста')

        self.translator = Translator()

        style = Style()
        style.configure('TButton',
                        font=('Monospace', 11))
        style_arrows = Style()
        style_arrows.configure('W.TButton', font=('Monospace', 17))

        lbl_input = Label(window, text="Введите текст:", font=("Monospace", 12))
        lbl_input.place(relx=0.25, rely=0.05, relwidth=0.15, relheight=0.07, anchor='ne')

        lbl_result = Label(window, text="Результат:", font=("Monospace", 12))
        lbl_result.place(relx=0.75, rely=0.05, relwidth=0.15, relheight=0.07, anchor='nw')

        btn = Button(window, text="\u27F7", style='W.TButton', command=self.change)
        btn.place(relx=0.5, rely=0.04, relwidth=0.16, relheight=0.07, anchor='n')

        btn = Button(window, text="Отформатировать", command=self.start_formating)
        btn.place(relx=0.5, rely=0.13, relwidth=0.16, relheight=0.05, anchor='n')

        btn = Button(window, text="Перевести", command=self.translate)
        btn.place(relx=0.5, rely=0.20, relwidth=0.16, relheight=0.05, anchor='n')

        lbl_input = Label(window, text="Переводчик:", font=("Monospace", 11))
        lbl_input.place(relx=0.5, rely=0.27, relwidth=0.16, relheight=0.05, anchor='n')

        n1 = StringVar()
        self.translators = Combobox(window, textvariable=n1)
        self.translators['values'] = 'Google'
        self.translators.place(relx=0.5, rely=0.34, relwidth=0.16, relheight=0.05, anchor='n')
        self.translators.current(0)

        lbl_input = Label(window, text="Перевести на:", font=("Monospace", 11))
        lbl_input.place(relx=0.5, rely=0.41, relwidth=0.16, relheight=0.05, anchor='n')

        n2 = StringVar()
        self.lang = Combobox(window, textvariable=n2)
        self.lang['values'] = ('Английский', 'Русский')
        self.lang.place(relx=0.5, rely=0.48, relwidth=0.16, relheight=0.05, anchor='n')
        self.lang.current(1)

        btn = Button(window, text="Очистить", command=self.clear)
        btn.place(relx=0.5, rely=0.55, relwidth=0.16, relheight=0.05, anchor='n')

        self.txt_input = scrolledtext.ScrolledText(window)
        self.txt_input.place(relx=0.4, rely=0.13, relwidth=0.4, relheight=0.7, anchor='ne')
        self.txt_input.focus()

        self.txt_result = scrolledtext.ScrolledText(window)
        self.txt_result.place(relx=0.6, rely=0.13, relwidth=0.4, relheight=0.7, anchor='nw')

        btn = Button(window, text="Загрузить из...", style='TButton', command=self.input_from_file)
        btn.place(relx=0.25, rely=0.85, relwidth=0.16, relheight=0.05, anchor='ne')

        btn = Button(window, text="Сохранить в...", style='TButton', command=self.save_to_file)
        btn.place(relx=0.75, rely=0.85, relwidth=0.16, relheight=0.05, anchor='nw')

        window.mainloop()

    def translate(self):
        text_input = self.txt_input.get('1.0', 'end-1c')
        if self.lang.get() == 'Английский':
            lang = 'en'
        elif self.lang.get() == 'Русский':
            lang = 'ru'
        result = self.translator.translate(text_input, dest=lang).text
        self.txt_result.delete(1.0, END)
        self.txt_result.insert(INSERT, result)

    def change(self):
        text_input = self.txt_input.get('1.0', 'end-1c')
        text_result = self.txt_result.get('1.0', 'end-1c')
        self.txt_input.delete(1.0, END)
        self.txt_input.insert(INSERT, text_result)
        self.txt_result.delete(1.0, END)
        self.txt_result.insert(INSERT, text_input)

    def start_formating(self):
        result = self.txt_input.get('1.0', 'end-1c')
        result = formating_text(result)
        self.txt_result.delete(1.0, END)
        self.txt_result.insert(INSERT, result)

    def clear(self):
        self.txt_result.delete(1.0, END)
        self.txt_input.delete(1.0, END)

    def input_from_file(self):
        file = filedialog.askopenfilename(
            title='Загрузить текст из файла',
            filetypes=(("Text files", "*.txt"), ("all files", "*.*"))
        )
        if file:
            try:
                self.clear()
                with open(file, 'r', encoding='UTF-8') as f:
                    text = f.read()
                    self.txt_input.delete(1.0, END)
                    self.txt_input.insert(INSERT, text)
            except Exception as err:
                messagebox.showerror('Что-то пошло не так...', err)

    def save_to_file(self):
        result = self.txt_result.get('1.0', 'end-1c')
        file = filedialog.asksaveasfile(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=(("Текстовый файл", "*.txt"),)
        )
        if file:
            try:
                with open(file.name, 'w', encoding='UTF-8') as f:
                    f.write(result)
            except Exception as err:
                print(err)
                messagebox.showerror('Что-то пошло не так...', err)


def main():
    window = Tk()
    app = StartApp(window)


if __name__ == '__main__':
    main()
