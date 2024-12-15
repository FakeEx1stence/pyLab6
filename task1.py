from tkinter.filedialog import askopenfile
import tkinter
from tkinter import messagebox


from PIL import ImageFilter, Image

import os
"""import sys"""                         #Для перезагрузки скрипта


class Window1(tkinter.Frame):
    def __init__(self, parent):
        # settings

        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tkinter.BOTH, expand=1)
        self.config(bg="#000033")
        self.create_widgets()

        self.file_path = tkinter.StringVar(value="None")

        #objects
    def create_widgets(self):
        """labels"""
        self.lb1 = tkinter.Label(self, text="Выберите изображение", bg="#000033", fg="#ADD8E6", font=("Helvetica", 20))
        self.lb2 = tkinter.Label(self, text="Имя файла:", bg="#000033", fg="#ADD8E6", font=("Helvetica", 14))
        self.file_name = tkinter.StringVar(value="empty")
        self.info=tkinter.StringVar(value="")

        self.lb3 = tkinter.Label(self, textvariable=self.file_name,bg="#000033", fg="#ADD8E6", font=("Helvetica", 14))
        self.lb4 = tkinter.Label(self, text="Укажите градус поворота изображения:", bg="#000033", fg="#ADD8E6", font=("Helvetica", 14))
        self.lb5 = tkinter.Label(self, textvariable=self.info, bg="#000033", fg="#ADD8E6", font=("Helvetica", 14))



        """buttons & enter fields"""
        self.img_choose_btn = tkinter.Button(self,text="Указать путь к изображению", command=self.image_choose)
        self.open_img_btn = tkinter.Button(self,text="Открыть изображение", command=self.image_open)
        self.change_degree_btn = tkinter.Button(self,text="Изменить градус изображения",command=self.change_degree)

        self.degree_entr=tkinter.Entry(self, font=("Helvetica", 14))



        """self.restart_btn=tkinter.Button(self, text="Restart", command=self.restart_module)"""      #Кнопка перезагрузки

        #placement

        """labels"""

        self.lb1.place(x=10, y=10)
        self.lb2.place(x=10, y=70)
        self.lb3.place(x=115, y=70)
        self.lb4.place(x=10, y=120)
        self.lb5.place(x=10, y=150)

        """buttons & enter fields"""

        self.img_choose_btn.place(x=400, y= 40)
        self.open_img_btn.place(x=400,y=80)
        self.change_degree_btn.place(x=600, y= 122)

        self.degree_entr.place(x=370, y=122)

        """self.restart_btn.place(x=600, y=10)"""   # Размещение кнопки перезагрузки


    """def restart_module(self):
        self.parent.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)"""  #Функция перезагрузки

    def image_choose(self):
        f = askopenfile(mode='rb', defaultextension=".jpg",
                        filetypes=(("Image files", "*.jpg"), ("All files", "*. *")))

        if f is not None:
            full_path = f.name
            self.file_path = f.name
            filename = os.path.basename(full_path)
            self.file_name.set(filename)

    def image_open(self):
        if self.file_path is not None:
            try:
                with Image.open(self.file_path) as img:
                    img.load()
                    img1 = img.filter(ImageFilter.EMBOSS)
                    img1 = img1.resize((100, 75))
                    width, height = img.size
                    img.paste((255, 0, 0), (width-117, 9, width-9, 86))
                    img.paste(img1, (width-113, 10))
                    img_32bit=img.convert('RGBA')
                    img_32bit.show()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл/Файл не выбран")
        else:
            messagebox.showerror("Ошибка","Файл не указан/указан неверно")

    def change_degree(self):
        if self.file_path is not None:
            try:
                with Image.open(self.file_path) as img:
                    img.load()
                    try:
                        self.degree = int(self.degree_entr.get())
                    except ValueError:
                        messagebox.showerror("Ошибка", "Некорректный ввод градуса поворота(!=0)")
                    else:
                        rotated_img = img.rotate(self.degree)
                        rotated_img.save(self.file_path)
                        self.info.set(f"Изображение повернуто на {self.degree} градусов и сохранено в исходной фотографии!")
            except Exception as e:
                messagebox.showerror("Ошибка", "Файл не указан/указан неверно")



"""if __name__ == '__main__':
    application = tkinter.Tk()
    Window1(application)
    application.geometry("1024x768+900+500")
    application.title("Lab6_1-322-v01-Shaienko-Vitaliy")
    application.mainloop() """                                 # Для функции кнопки restart и удобной настройки




