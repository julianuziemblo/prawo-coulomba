import random
import time
import numpy as np
import matplotlib.pyplot as plt
from point import Point
from point import Charge
from PIL import Image
from image_parser import get_inside
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread


class App(ctk.CTk):
    def __init__(self, width, height):
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.width = width
        self.height = height
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws // 2) - (self.width // 2)
        y = (hs // 2) - (self.height // 2)
        self.geometry(f'{self.width}x{self.height}+{x}+{y}')
        self.minsize(width, height)
        self.title('Symulacja rozkładu ładunków w przedowniku')

        # fonts
        self.font_header = ctk.CTkFont("Impact", self.width // 10, "bold")
        self.font_big_text = ctk.CTkFont("Sans", self.width // 15, "bold")
        self.font_desc = ctk.CTkFont("Arial", self.width // 22)
        self.font_input = ctk.CTkFont("Arial", self.width // 37)
        self.font_little = ctk.CTkFont("Arial", self.width // 35, slant="italic")

        # images
        self.play = ctk.CTkImage(Image.open('img/play.png'), size=(self.height // 8, self.height // 8))
        self.pause = ctk.CTkImage(Image.open('img/pause.png'), size=(self.height // 8, self.height // 8))
        self.image = None

        # flags
        self.looping = False

        # frames
        self.frames = {}
        self.create_frames()

        # threads
        self.threads = {}

        # buttons
        self.buttons = {}
        self.create_buttons()

        # canvas
        self.canvas = tk.Canvas(master=self)
        self.figure = None
        self.charges_pos = 0
        self.charges_neg = 0
        self.inside = []
        self.image_array = None
        self.ax = None

        # drawing
        self.FPS = 5

        self.mainloop()

    def create_frames(self):
        # top frame
        buttons = ctk.CTkFrame(master=self, width=self.width - 20, height=self.height // 8)
        buttons.pack(padx=10, pady=10, anchor=tk.N)
        self.frames['buttons'] = buttons
        # main canvas frame
        canvas = ctk.CTkFrame(master=self, width=self.width - 20, height=self.height - 80)
        canvas.pack(padx=10, anchor=tk.S)
        self.frames['canvas'] = canvas

    def create_buttons(self):
        # play
        play = ctk.CTkButton(master=self.frames['buttons'], text='Play', font=self.font_desc, fg_color='green',
                             command=self.play_action)
        play.place(relx=0.1, rely=0.5, anchor=tk.CENTER)
        self.buttons['play'] = play

        # upload
        upload = ctk.CTkButton(master=self.frames['buttons'], text='Upload', font=self.font_desc,
                               command=self.upload_action)
        upload.place(relx=0.9, rely=0.5, anchor=tk.CENTER)
        self.buttons['upload'] = upload

        # place charges
        place = ctk.CTkButton(master=self.frames['buttons'], text='Place charges', font=self.font_input,
                              command=self.place_charges)
        place.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
        self.buttons['place'] = place

        # number label
        number_label = ctk.CTkLabel(master=self.frames['buttons'], text='# of charges', font=self.font_input)
        number_label.place(relx=0.3, rely=0.2, anchor=tk.CENTER)

        # number of charges
        num_of_charges = ctk.CTkSlider(master=self.frames['buttons'], from_=0, to=100, command=self.slider_pos)
        num_of_charges.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        self.buttons['num_of_charges'] = num_of_charges

        # number display
        num_display = ctk.CTkLabel(master=self.frames['buttons'], text=str(50), font=self.font_little)
        num_display.place(relx=0.3, rely=0.83, anchor=tk.CENTER)
        self.buttons['num_display'] = num_display

        # speed label
        speed_label = ctk.CTkLabel(master=self.frames['buttons'], text='FPS', font=self.font_input)
        speed_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # speed
        speed = ctk.CTkSlider(master=self.frames['buttons'], from_=0, to=12, command=self.slider_speed)
        speed.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.buttons['speed'] = speed

        # speed display
        # number display
        speed_display = ctk.CTkLabel(master=self.frames['buttons'], text='6.00', font=self.font_little)
        speed_display.place(relx=0.5, rely=0.83, anchor=tk.CENTER)
        self.buttons['speed_display'] = speed_display

    def play_action(self):
        print("iiiiiiin motioooooon")
        play = Thread(target=self.loop)
        self.looping = True
        play.start()

    def upload_action(self):
        print("Uploading...")
        filetypes = (
            ('Bitmaps', '*.bmp'),
        )
        image_path = filedialog.askopenfilename(title='Wybierz obraz przewodnika',
                                                initialdir=r'C:\Users\Julian\Desktop',
                                                filetypes=filetypes)
        self.image = Image.open(image_path)
        self.image_array = np.asarray(self.image)
        self.inside = get_inside(self.image_array)
        self.create_image()

    def slider_speed(self, value):
        self.FPS = value
        self.buttons['speed_display'].configure(text=str(round(value, 2)))

    def slider_pos(self, value):
        self.charges_pos = value
        self.buttons['num_display'].configure(text=str(int(value)))

    def place_charges(self):
        self.buttons['place'].configure(state='DISABLED')
        pass

    def create_image(self):
        self.figure = plt.Figure(figsize=(self.width // 10, self.height // 10))
        self.ax = self.figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(self.figure, self.frames['canvas'])
        chart_type.get_tk_widget().pack()
        self.ax.imshow(self.image)
        self.scatter_charges()

    def draw(self):
        self.create_image()
        print('drew frame')

    def loop(self):
        while self.looping:
            self.draw()
            time.sleep(1 / self.FPS)

    def scatter_charges(self):
        for i in range(self.charges_pos):
            rand_point: Point = random.choice(self.inside)

            self.ax.scatter(rand_point.x, rand_point.y, c='r')


def main():
    image_path = r'C:\Users\Julian\Desktop\bitmapa.bmp'
    WIDTH = 1200
    HEIGHT = 800
    app = App(WIDTH, HEIGHT)


if __name__ == '__main__':
    main()
