import random
import time
from copy import copy

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
import calculations as calc
from tkinter import messagebox


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
        self.canvas = None
        self.ax = None

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

        # threads
        self.threads = {}

        # frames
        self.frames = {}
        self.create_frames()

        # buttons
        self.buttons = {}
        self.create_buttons()

        # canvas
        self.num_of_pos = 50
        self.num_of_neg = 50
        self.positive = []
        self.negative = []
        self.charges = []
        self.charge = 1.
        self.inside = []

        # drawing
        self.FPS = 30

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

    def create_play_button(self):
        # play
        play = ctk.CTkButton(master=self.frames['buttons'], text='Play', font=self.font_desc, fg_color='green',
                             command=self.play_action)
        play.place(relx=0.1, rely=0.5, anchor=tk.CENTER)
        self.buttons['play'] = play

    def create_restart_and_pause(self):
        # restart
        restart = ctk.CTkButton(master=self.frames['buttons'], text='R', font=self.font_desc, fg_color='green',
                                command=self.restart_action)
        restart.place(relx=0.15, rely=0.5, anchor=tk.CENTER)
        self.buttons['restart'] = restart

        # pause
        pause = ctk.CTkButton(master=self.frames['buttons'], text='P', font=self.font_desc, fg_color='green',
                              command=self.pause_action)
        pause.place(relx=0.05, rely=0.5, anchor=tk.CENTER)
        self.buttons['pause'] = pause

    def create_buttons(self):
        # play
        self.create_play_button()

        # upload
        upload = ctk.CTkButton(master=self.frames['buttons'], text='Upload', font=self.font_desc,
                               command=self.upload_action)
        upload.place(relx=0.9, rely=0.5, anchor=tk.CENTER)
        self.buttons['upload'] = upload

        # number label
        number_label = ctk.CTkLabel(master=self.frames['buttons'], text='Positive', font=self.font_input)
        number_label.place(relx=0.3, rely=0.2, anchor=tk.CENTER)

        # number of charges
        num_of_charges = ctk.CTkSlider(master=self.frames['buttons'], from_=0, to=100, command=self.slider_pos)
        num_of_charges.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        self.buttons['num_of_charges'] = num_of_charges

        # number display
        num_display = ctk.CTkLabel(master=self.frames['buttons'], text=str(50), font=self.font_little)
        num_display.place(relx=0.3, rely=0.83, anchor=tk.CENTER)
        self.buttons['num_display'] = num_display

        # number neg label
        num_label = ctk.CTkLabel(master=self.frames['buttons'], text='Negative', font=self.font_input)
        num_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # number of charges neg
        num_of_neg = ctk.CTkSlider(master=self.frames['buttons'], from_=0, to=100, command=self.slider_neg)
        num_of_neg.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.buttons['num_of_neg'] = num_of_neg

        # number display neg
        num_display = ctk.CTkLabel(master=self.frames['buttons'], text=str(50), font=self.font_little)
        num_display.place(relx=0.5, rely=0.83, anchor=tk.CENTER)
        self.buttons['neg_display'] = num_display

        # speed label
        speed_label = ctk.CTkLabel(master=self.frames['buttons'], text='FPS', font=self.font_input)
        speed_label.place(relx=0.7, rely=0.2, anchor=tk.CENTER)

        # speed
        speed = ctk.CTkSlider(master=self.frames['buttons'], from_=0, to=60, command=self.slider_speed)
        speed.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
        self.buttons['speed'] = speed

        # speed display
        speed_display = ctk.CTkLabel(master=self.frames['buttons'], text='30.00', font=self.font_little)
        speed_display.place(relx=0.7, rely=0.83, anchor=tk.CENTER)
        self.buttons['speed_display'] = speed_display

        self.createWidgets()

    def play_action(self):
        if not self.image:
            messagebox.showerror('Error', 'Cannot play the simulation until an image is uploaded!')
        else:
            print("iiiiiiin motioooooon")
            play = Thread(target=self.loop)
            self.looping = True
            play.start()
            # self.buttons['play'].configure(text='Restart')
            self.buttons['play'].destroy()
            self.buttons.pop('play')
            self.create_restart_and_pause()

    def restart_action(self):
        print('Restarting...')
        self.image = None
        self.looping = False
        self.buttons['restart'].destroy()
        self.buttons.pop('restart')
        self.buttons['pause'].destroy()
        self.buttons.pop('pause')
        self.create_play_button()
        self.ax.clear()

    def pause_action(self):
        if self.FPS != 0:
            self.FPS = 0
        else:
            self.FPS = 30
            self.buttons['speed_display'].configure(text='30.00')

    def upload_action(self):
        self.looping = False
        time.sleep(1 / self.FPS)
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
        print("INSIDE:", self.inside)
        self.update_image()

    def slider_speed(self, value):
        self.FPS = value
        self.buttons['speed_display'].configure(text=str(round(value, 2)))

    def slider_pos(self, value):
        self.num_of_pos = int(value)
        self.buttons['num_display'].configure(text=str(int(value)))

    def slider_neg(self, value):
        self.num_of_neg = int(value)
        self.buttons['neg_display'].configure(text=str(int(value)))

    def update_image(self):
        # self.figure = plt.Figure(figsize=(self.width // 10, self.height // 10))
        # self.ax = self.figure.add_subplot(111)
        # chart_type = FigureCanvasTkAgg(self.figure, self.frames['canvas'])
        # chart_type.get_tk_widget().pack()
        # print(self.charges)
        if not self.charges:
            self.ax.imshow(self.image)
            self.scatter_charges()
            # print("setting up")
        else:
            self.ax.imshow(self.image)
            self.scatter_update()
            # print("updating")

    def createWidgets(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frames['canvas'])
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()
        # print("canvas = ", self.canvas)

    def scatter_update(self):
        self.ax.clear()
        # print(self.canvas)
        for particle in self.charges:
            self.ax.scatter(particle.x, particle.y, marker='o',
                            c=particle.get_color())
        self.ax.imshow(self.image)
        self.canvas.draw()

    def draw(self):
        for particle in self.charges:
            # 1. update acceleration
            particle = calc.acceleration(particle, self.charges)
            # 2. update other parameters
            particle = calc.update_particle(particle, self.image_array, self.inside)
            # 3. check if in bounds. if not, set velocity to negative and calculate again
            particle.last_inside = Point(copy(particle.x), copy(particle.y))

        self.update_image()
        # print('drew frame')

    def loop(self):
        while self.looping:
            while self.FPS == 0:
                print('paused')
            self.draw()
            while self.FPS == 0:
                print('paused')
            time.sleep(1 / self.FPS)

    def scatter_charges(self):
        # print("neg = ", self.num_of_neg)
        # print("pos =", self.num_of_pos)
        # positive
        for i in range(self.num_of_pos):
            point: Point = random.choice(self.inside)
            charge = Charge(point.x, point.y, self.charge)
            self.positive.append(charge)
            self.ax.scatter(charge.x, charge.y, c=charge.get_color())

        # negative
        for i in range(self.num_of_neg):
            point: Point = random.choice(self.inside)
            charge = Charge(point.x, point.y, -self.charge)
            self.negative.append(charge)
            self.ax.scatter(charge.x, charge.y, c=charge.get_color())

        # all charges
        self.charges = self.positive + self.negative
        # print(self.image)
        self.ax.imshow(self.image)
        self.canvas.draw()
        # print(f'Positives: {self.positive}', '\n', f'Negatives: {self.negative}')
        # print(self.charges)


def main():
    WIDTH = 1200
    HEIGHT = 800
    App(WIDTH, HEIGHT)


if __name__ == '__main__':
    main()
