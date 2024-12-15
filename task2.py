from tkinter.filedialog import askopenfile
import cv2
import tkinter
import numpy as np
from tkinter import messagebox

"""import os                              #Библиотеки для перезагрузки скрипта
#import sys     """

class Window2(tkinter.Frame):
    def __init__(self, parent):
        # settings

        super().__init__(parent)
        self.parent = parent
        self.pack(fill=tkinter.BOTH, expand=1)
        self.config(bg="#420d36")
        self.create_widgets()

        self.file_path = None

    def create_widgets(self):
        """labels"""

        self.lb1 = tkinter.Label(self, text="Выберите изображение(В пути не должно быть кириллицы!)", bg="#420d36", fg="#e5b209", font=("Helvetica", 15))
        self.lb2 = tkinter.Label(self, text="Имя файла:", bg="#420d36", fg="#e5b209", font=("Helvetica", 14))
        self.file_name = tkinter.StringVar(value="empty")
        self.info = tkinter.StringVar(value="")

        self.lb3 = tkinter.Label(self, textvariable=self.file_name, bg="#420d36", fg="#e5b209", font=("Helvetica", 14))
        self.lb4 = tkinter.Label(self, text="Изображение с применением проектного превращения", bg="#420d36", fg="#E5B209",
                                 font=("Helvetica", 14))
        self.lb5 = tkinter.Label(self, text="Изображение с применением эффекта Blur", bg="#420d36", fg="#E5B209",
                                 font=("Helvetica", 14))
        self.lb6 = tkinter.Label(self, text="Изображение с применением выделения границ методом Roberts", bg="#420d36", fg="#E5B209",
                                 font=("Helvetica", 14))

        """buttons & enter fields"""

        self.img_choose_btn = tkinter.Button(self, text="Указать путь к изображению", command=self.cv2_choose_file)
        self.open_img_btn = tkinter.Button(self, text="Открыть изображение", command=self.cv2_open_file)
        self.open_tf_img_btn = tkinter.Button(self, text="Открыть изображение с применением проектного превращения",command=self.cv2_tf_image)
        self.open_blurred_img_btn = tkinter.Button(self, text="Открыть изображение с эффектом Blur", command=self.cv2_blur_image)
        self.open_roberts_img_btn = tkinter.Button(self,text = "Открыть изображение с выделенными границами", command=self.cv2_roberts_image)

        """self.restart_btn = tkinter.Button(self, text="Restart", command=self.restart_module)  # Кнопка перезагрузки"""

        # placement

        """labels"""

        self.lb1.place(x=10, y=10)
        self.lb2.place(x=10, y=70)
        self.lb3.place(x=115, y=70)
        self.lb4.place(x=10, y=120)
        self.lb5.place(x=10, y=170)
        self.lb6.place(x=10, y=230)

        """buttons & enter fields"""

        self.img_choose_btn.place(x=710, y=45)
        self.open_img_btn.place(x=745, y=80)
        self.open_tf_img_btn.place(x=510, y=123)
        self.open_blurred_img_btn.place(x=404, y=172)
        self.open_roberts_img_btn.place(x=604, y=232)

        """self.restart_btn.place(x=830, y=10)  # Размещение кнопки перезагрузки"""

    """def restart_module(self):
           self.parent.destroy()
           python = sys.executable
           os.execl(python, python, *sys.argv)  #Функция перезагрузки """

    def cv2_choose_file (self):
            f = askopenfile (mode = 'rb', defaultextension = ".jpg",
                            filetypes = (( "Image files", "* .jpg"), ("All files", "*. *")))

            if f is not None:
                self.file_path = f.name
                self.file_name.set(f.name)

    def cv2_open_file(self):
        if self.file_path is not None:
            try:
                img = cv2.imread(self.file_path)
                img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
                cv2.imshow("Original Image", img)
                cv2.imshow("YUV Image", img_yuv)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except Exception:
                messagebox.showerror("Ошибка", "Не удалось открыть файл!")
        else:
            messagebox.showerror("Ошибка", "Изображение не загружено!")

    def cv2_tf_image(self):
        if self.file_path is not None:
            try:
                img = cv2.imread(self.file_path)
                height, width = img.shape[:2]
                src_points = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
                dst_points = np.float32([[50, 0], [width - 50, 0], [50, height], [width - 50, height]])

                matrix = cv2.getPerspectiveTransform(src_points, dst_points)

                tf_image = cv2.warpPerspective(img, matrix, (img.shape[1], img.shape[0]))

                cv2.imshow("Transformed image", tf_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except Exception:
                messagebox.showerror("Ошибка", "Не удалось открыть файл!")
        else:
            messagebox.showerror("Ошибка", "Изображение не загружено!")


    def cv2_blur_image(self):
        if self.file_path is not None:
            try:
                img = cv2.imread(self.file_path)
                kernel = np.ones((9, 9), np.float32) / 81
                blurred_img = cv2.filter2D(img, -1, kernel)
                cv2.imshow("Blurred Image", blurred_img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except Exception:
                messagebox.showerror("Ошибка", "Не удалось открыть файл!")
        else:
            messagebox.showerror("Ошибка", "Изображение не загружено!")

    def cv2_roberts_image(self):
        if self.file_path is not None:
            try:
                img = cv2.imread(self.file_path)
                roberts_x = np.array([[1, 0],
                                      [0, -1]], dtype=np.float32)

                roberts_y = np.array([[0, 1],
                                      [-1, 0]], dtype=np.float32)

                grad_x = cv2.filter2D(img, -1, roberts_x)
                grad_y = cv2.filter2D(img, -1, roberts_y)

                edges = cv2.add(np.abs(grad_x), np.abs(grad_y))

                _, edges_thresh = cv2.threshold(edges, 50, 255, cv2.THRESH_BINARY)

                cv2.imshow("Roberts Edges", edges_thresh)

                cv2.waitKey(0)
                cv2.destroyAllWindows()
            except Exception:
                messagebox.showerror("Ошибка", "Не удалось открыть файл!")
        else:
            messagebox.showerror("Ошибка", "Изображение не загружено!")


"""
if __name__ == '__main__':
    application = tkinter.Tk()
    Window2(application)
    application.geometry("1024x768+900+500")
    application.title("Lab6_1-322-v01-Shaienko-Vitaliy")
    application.mainloop()                                  # Для функции кнопки restart и удобной настройки
"""


