import tkinter as tk
from tkinter import messagebox, filedialog

from premises import Room, Apartment, House


class App:
    def __init__(self, root):
        self.root = root
        root.title('Помещения: площадь и тепловая мощность')

        self.house = House('Многоэтажный дом')
        self.apt_num = 1
        self.current = Apartment(f'Квартира {self.apt_num}')

        frm = tk.LabelFrame(root, text='Комната', padx=8, pady=8)
        frm.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        tk.Label(frm, text='Название:').grid(row=0, column=0, sticky='w')
        self.e_name = tk.Entry(frm, width=15)
        self.e_name.grid(row=0, column=1)
        self.e_name.insert(0, 'Кухня')

        tk.Label(frm, text='Ширина, м:').grid(row=1, column=0, sticky='w')
        self.e_width = tk.Entry(frm, width=15)
        self.e_width.grid(row=1, column=1)
        self.e_width.insert(0, '3.5')

        tk.Label(frm, text='Длина, м:').grid(row=2, column=0, sticky='w')
        self.e_length = tk.Entry(frm, width=15)
        self.e_length.grid(row=2, column=1)
        self.e_length.insert(0, '4.0')

        tk.Label(frm, text='Высота потолка, м:').grid(row=3, column=0, sticky='w')
        self.e_height = tk.Entry(frm, width=15)
        self.e_height.grid(row=3, column=1)
        self.e_height.insert(0, '2.7')

        tk.Button(frm, text='Добавить комнату', command=self.add_room).grid(
            row=4, column=0, columnspan=2, pady=5)

        self.room_list = tk.Listbox(frm, width=42, height=6)
        self.room_list.grid(row=5, column=0, columnspan=2)

        tk.Button(frm, text='Добавить квартиру в дом', command=self.add_apartment).grid(
            row=6, column=0, columnspan=2, pady=5)

        res = tk.LabelFrame(root, text='Результаты', padx=8, pady=8)
        res.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.lbl_apt = tk.Label(res, text='', justify='left')
        self.lbl_apt.grid(row=0, column=0, sticky='w')
        self.lbl_house = tk.Label(res, text='', justify='left')
        self.lbl_house.grid(row=1, column=0, sticky='w', pady=(10, 0))

        tk.Button(res, text='Сохранить отчёт (.docx)', command=self.save_report).grid(
            row=2, column=0, pady=10)

        self.refresh()

    def add_room(self):
        try:
            name = self.e_name.get().strip() or 'Комната'
            width = float(self.e_width.get())
            length = float(self.e_length.get())
            height = float(self.e_height.get())
        except ValueError:
            messagebox.showerror('Ошибка', 'Введите числа для ширины, длины и высоты')
            return
        self.current.add_room(Room(name, width, length, height))
        self.refresh()

    def add_apartment(self):
        if not self.current.rooms:
            messagebox.showwarning('Внимание', 'В квартире нет ни одной комнаты')
            return
        self.house.add_apartment(self.current)
        self.apt_num += 1
        self.current = Apartment(f'Квартира {self.apt_num}')
        self.refresh()

    def refresh(self):
        self.room_list.delete(0, tk.END)
        for r in self.current.rooms:
            self.room_list.insert(tk.END, f'{r.name}: {r.area():.2f} м2, {r.heating_power():.0f} Вт')
        self.lbl_apt.config(
            text=f'{self.current.name}\n'
                 f'Комнат: {len(self.current.rooms)}\n'
                 f'Площадь: {self.current.total_area():.2f} м2\n'
                 f'Мощность: {self.current.total_heating_power():.0f} Вт')
        self.lbl_house.config(
            text=f'{self.house.name}\n'
                 f'Квартир: {len(self.house.apartments)}\n'
                 f'Комнат: {self.house.rooms_count()}\n'
                 f'Площадь: {self.house.total_area():.2f} м2\n'
                 f'Мощность: {self.house.total_heating_power():.0f} Вт')

    def save_report(self):
        try:
            from docx import Document
        except ImportError:
            messagebox.showerror('Ошибка', 'Не установлен python-docx:\npip install python-docx')
            return
        path = filedialog.asksaveasfilename(
            defaultextension='.docx',
            filetypes=[('Документ Word', '*.docx')])
        if not path:
            return
        doc = Document()
        doc.add_heading('Отчёт по расчёту помещений', 0)
        for apt in self.house.apartments:
            doc.add_heading(apt.name, level=1)
            table = doc.add_table(rows=1, cols=6)
            table.style = 'Table Grid'
            for i, title in enumerate(['Комната', 'Ширина, м', 'Длина, м',
                                       'Высота, м', 'Площадь, м2', 'Мощность, Вт']):
                table.rows[0].cells[i].text = title
            for r in apt.rooms:
                c = table.add_row().cells
                c[0].text = r.name
                c[1].text = f'{r.width:.2f}'
                c[2].text = f'{r.length:.2f}'
                c[3].text = f'{r.height:.2f}'
                c[4].text = f'{r.area():.2f}'
                c[5].text = f'{r.heating_power():.0f}'
            doc.add_paragraph(f'Площадь квартиры: {apt.total_area():.2f} м2, '
                              f'тепловая мощность: {apt.total_heating_power():.0f} Вт')
        doc.add_heading('Итоги по дому', level=1)
        doc.add_paragraph(f'Квартир: {len(self.house.apartments)}, комнат: {self.house.rooms_count()}')
        doc.add_paragraph(f'Общая площадь: {self.house.total_area():.2f} м2')
        doc.add_paragraph(f'Общая тепловая мощность: {self.house.total_heating_power():.0f} Вт')
        doc.save(path)
        messagebox.showinfo('Отчёт', f'Отчёт сохранён:\n{path}')


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()