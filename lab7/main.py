import os

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from premises import Room, Apartment, House

Window.size = (950, 520)


class PremisesApp(App):
    def build(self):
        self.title = 'Помещения (Kivy): площадь и тепловая мощность'
        self.house = House('Многоэтажный дом', floors=9)
        self.apt_num = 1
        self.current = Apartment(f'Квартира {self.apt_num}')

        root = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        left = BoxLayout(orientation='vertical', spacing=5, size_hint_x=0.55)
        left.add_widget(Label(text='Комната', size_hint_y=None, height=30, bold=True))

        form = GridLayout(cols=2, spacing=5, size_hint_y=None)
        form.bind(minimum_height=form.setter('height'))
        self.inputs = {}
        for key, title, default in [('name', 'Название:', 'Кухня'),
                                    ('width', 'Ширина, м:', '3.5'),
                                    ('length', 'Длина, м:', '4.0'),
                                    ('height', 'Высота, м:', '2.7')]:
            form.add_widget(Label(text=title, size_hint_y=None, height=36))
            ti = TextInput(text=default, multiline=False, size_hint_y=None, height=36)
            self.inputs[key] = ti
            form.add_widget(ti)
        left.add_widget(form)

        btn_room = Button(text='Добавить комнату', size_hint_y=None, height=40)
        btn_room.bind(on_press=self.add_room)
        left.add_widget(btn_room)

        self.rooms_label = Label(text='Комнат пока нет', size_hint_y=1)
        left.add_widget(self.rooms_label)

        btn_apt = Button(text='Добавить квартиру в дом', size_hint_y=None, height=40)
        btn_apt.bind(on_press=self.add_apartment)
        left.add_widget(btn_apt)

        right = BoxLayout(orientation='vertical', spacing=5, size_hint_x=0.45)
        right.add_widget(Label(text='Результаты', size_hint_y=None, height=30, bold=True))
        self.lbl_apt = Label(text='', size_hint_y=0.3)
        right.add_widget(self.lbl_apt)
        self.lbl_house = Label(text='', size_hint_y=0.5)
        right.add_widget(self.lbl_house)
        btn_save = Button(text='Сохранить отчёт (.docx)', size_hint_y=None, height=40)
        btn_save.bind(on_press=self.save_report)
        right.add_widget(btn_save)

        root.add_widget(left)
        root.add_widget(right)
        self.refresh()
        return root

    def show_popup(self, title, text):
        Popup(title=title, content=Label(text=text),
              size_hint=(None, None), size=(420, 180)).open()

    def add_room(self, *args):
        try:
            room = Room(self.inputs['name'].text.strip() or 'Комната',
                        self.inputs['width'].text,
                        self.inputs['length'].text,
                        self.inputs['height'].text)
        except ValueError as e:
            self.show_popup('Ошибка', f'Некорректные значения:\n{e}')
            return
        self.current.add_room(room)
        self.refresh()

    def add_apartment(self, *args):
        if len(self.current) == 0:
            self.show_popup('Внимание', 'В квартире нет ни одной комнаты')
            return
        self.house.add_apartment(self.current)
        self.apt_num += 1
        self.current = Apartment(f'Квартира {self.apt_num}')
        self.refresh()

    def refresh(self):
        rooms = [str(r) for r in self.current] 
        self.rooms_label.text = '\n'.join(rooms) if rooms else 'Комнат пока нет'
        self.lbl_apt.text = str(self.current)  
        self.lbl_house.text = str(self.house)   

    def save_report(self, *args):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text='Имя файла отчёта:', size_hint_y=None, height=30))
        self.e_filename = TextInput(text='report.docx', multiline=False,
                                    size_hint_y=None, height=36)
        content.add_widget(self.e_filename)
        btn = Button(text='Сохранить на Рабочий стол', size_hint_y=None, height=40)
        content.add_widget(btn)
        popup = Popup(title='Сохранение отчёта', content=content,
                      size_hint=(None, None), size=(420, 220))
        btn.bind(on_press=lambda *a: self._write_report(popup))
        popup.open()

    def _write_report(self, popup):
        name = self.e_filename.text.strip() or 'report.docx'
        if not name.endswith('.docx'):
            name += '.docx'
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        if not os.path.isdir(desktop):
            desktop = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop')
        if not os.path.isdir(desktop):
            desktop = os.getcwd()  
        full = os.path.join(desktop, name)
        try:
            from docx import Document
        except ImportError:
            popup.dismiss()
            self.show_popup('Ошибка', 'Не установлен python-docx:\npip install python-docx')
            return
        doc = Document()
        doc.add_heading('Отчёт по расчёту помещений', 0)
        for apt in self.house:
            doc.add_heading(apt.name, level=1)
            table = doc.add_table(rows=1, cols=6)
            table.style = 'Table Grid'
            for i, title in enumerate(['Комната', 'Ширина, м', 'Длина, м',
                                       'Высота, м', 'Площадь, м2', 'Мощность, Вт']):
                table.rows[0].cells[i].text = title
            for r in apt:
                c = table.add_row().cells
                c[0].text = r.name
                c[1].text = f'{r.width:.2f}'
                c[2].text = f'{r.length:.2f}'
                c[3].text = f'{r.height:.2f}'
                c[4].text = f'{r.area():.2f}'
                c[5].text = f'{r.heating_power():.0f}'
            doc.add_paragraph(f'Площадь квартиры: {apt.area():.2f} м2, '
                              f'тепловая мощность: {apt.heating_power():.0f} Вт')
        doc.add_heading('Итоги по дому', level=1)
        doc.add_paragraph(f'Квартир: {len(self.house)}, комнат: {self.house.rooms_count()}')
        doc.add_paragraph(f'Общая площадь: {self.house.area():.2f} м2')
        doc.add_paragraph(f'Общая тепловая мощность: {self.house.heating_power():.0f} Вт')
        doc.save(full)
        popup.dismiss()
        self.show_popup('Отчёт', f'Отчёт сохранён:\n{full}')


if __name__ == '__main__':
    PremisesApp().run()