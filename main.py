import os
import random
import time
import tkinter as tk
from copy import copy
from threading import Thread
from tkinter import filedialog
from tkinter import messagebox

import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import calculations as calc
from image_parser import get_inside, get_edges
from point import Charge, Constants
from point import Point


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
        self.num_of_pos = 15
        self.num_of_neg = 15
        self.positive = []
        self.negative = []
        self.charges = []
        self.charge = 1.0
        self.inside = []
        self.scaling = 1.0
        self.average_velocity = 0.0
        self.grid_toggled= False

        # drawing
        self.FPS = 30

        self.mainloop()

    def create_frames(self):
        # top frame
        buttons = ctk.CTkFrame(master=self, width=self.width - 20, height=self.height // 8)
        buttons.place(relx=0.5, rely=0.01, anchor=tk.N)
        self.frames['buttons'] = buttons

        # side bar
        side_bar = ctk.CTkFrame(master=self, width=self.width // 6, height=self.height - (self.height // 8 - 5))
        side_bar.place(relx=0.1, rely=0.6, anchor=tk.CENTER)
        self.frames['side_bar'] = side_bar

        # main canvas frame
        canvas = ctk.CTkFrame(master=self, width=self.width - 20, height=self.height - 80)
        canvas.place(relx=0.6, rely=0.525, anchor=tk.CENTER)
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
                                command=self.restart_action, width=20, height=20)
        restart.place(relx=0.15, rely=0.5, anchor=tk.CENTER)
        self.buttons['restart'] = restart

        # pause
        pause = ctk.CTkButton(master=self.frames['buttons'], text='P', font=self.font_desc, fg_color='green',
                              command=self.pause_action, width=20, height=20)
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
        num_of_charges = ctk.CTkSlider(master=self.frames['buttons'], from_=0, to=30, command=self.slider_pos)
        num_of_charges.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
        self.buttons['num_of_charges'] = num_of_charges

        # number display
        num_display = ctk.CTkLabel(master=self.frames['buttons'], text=str(15), font=self.font_little)
        num_display.place(relx=0.3, rely=0.83, anchor=tk.CENTER)
        self.buttons['num_display'] = num_display

        # number neg label
        num_label = ctk.CTkLabel(master=self.frames['buttons'], text='Negative', font=self.font_input)
        num_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # number of charges neg
        num_of_neg = ctk.CTkSlider(master=self.frames['buttons'], from_=0, to=30, command=self.slider_neg)
        num_of_neg.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.buttons['num_of_neg'] = num_of_neg

        # number display neg
        neg_display = ctk.CTkLabel(master=self.frames['buttons'], text=str(15), font=self.font_little)
        neg_display.place(relx=0.5, rely=0.83, anchor=tk.CENTER)
        self.buttons['neg_display'] = neg_display

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
        self.create_sidebar_widgets()

    def create_sidebar_widgets(self):
        side_bar = self.frames['side_bar']

        # charge label
        charge_label = ctk.CTkLabel(master=side_bar, text='Charge', font=self.font_little)
        charge_label.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
        # charge
        charge = ctk.CTkSlider(master=side_bar, from_=0.0, to=5.0, command=self.slider_charge,
                               width=self.width // 6 - 50)
        charge.set(1.0)
        charge.place(relx=0.4, rely=0.1, anchor=tk.CENTER)
        self.buttons['charge'] = charge
        # charge display
        charge_display = ctk.CTkLabel(master=side_bar, text='1.00')
        charge_display.place(relx=0.87, rely=0.1, anchor=tk.CENTER)
        self.buttons['charge_display'] = charge_display

        # scaling
        scaling_label = ctk.CTkLabel(master=side_bar, text='Tail scaling', font=self.font_little)
        scaling_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        # charge
        scaling = ctk.CTkSlider(master=side_bar, from_=0.0, to=5.0, command=self.slider_scaling,
                                width=self.width // 6 - 50)
        scaling.set(1.0)
        scaling.place(relx=0.4, rely=0.26, anchor=tk.CENTER)
        self.buttons['scaling'] = scaling
        # charge display
        scaling_display = ctk.CTkLabel(master=side_bar, text='1.00')
        scaling_display.place(relx=0.87, rely=0.26, anchor=tk.CENTER)
        self.buttons['scaling_display'] = scaling_display

        # max velocity
        max_velocity_label = ctk.CTkLabel(master=side_bar, text='Max. velocity', font=self.font_little)
        max_velocity_label.place(relx=0.485, rely=0.4, anchor=tk.CENTER)
        # charge
        max_velocity = ctk.CTkSlider(master=side_bar, from_=0.0, to=50, command=self.slider_max_velocity,
                                     width=self.width // 6 - 50)
        max_velocity.set(15.0)
        max_velocity.place(relx=0.4, rely=0.46, anchor=tk.CENTER)
        self.buttons['max_velocity'] = max_velocity
        # charge display
        max_velocity_display = ctk.CTkLabel(master=side_bar, text='15.00')
        max_velocity_display.place(relx=0.87, rely=0.46, anchor=tk.CENTER)
        self.buttons['max_velocity_display'] = max_velocity_display

        # toggle grid
        toggle_grid = ctk.CTkButton(master=side_bar, command=self.button_grid, text='Grid: off', font=self.font_little,
                                    fg_color='gray', width=self.width // 6 - 50)
        toggle_grid.place(relx=0.5, rely=0.56, anchor=tk.CENTER)
        self.buttons['toggle_grid'] = toggle_grid

        # save image
        save_fig = ctk.CTkButton(master=side_bar, command=self.button_save, text='Save', font=self.font_little,
                                 fg_color='blue', width=self.width // 6 - 50)
        save_fig.place(relx=0.5, rely=0.66, anchor=tk.CENTER)
        self.buttons['save_fig'] = save_fig

        # save image
        reset_velocities = ctk.CTkButton(master=side_bar, command=self.reset_velocities,
                                         text='Reset\nforces and\nvelocities', font=self.font_little,
                                         width=self.width // 6 - 50)
        reset_velocities.place(relx=0.5, rely=0.72, anchor=tk.N)
        self.buttons['reset_velocities'] = reset_velocities

    def reset_velocities(self):
        for p in self.charges:
            p.vx = 0
            p.vy = 0

    def slider_charge(self, value):
        self.charge = float(value)
        # print(self.charge)
        self.buttons['charge_display'].configure(text=str(round(value, 2)))

    def button_save(self):
        if self.image:
            figname = f'figure{random.randint(2137, 69420)}.png'
            folder = filedialog.askdirectory(initialdir=r'C:\Users\julia\OneDrive\Pulpit')
            path = os.path.join(folder, figname)
            self.fig.savefig(path)
            messagebox.showinfo('Success', 'Image saved')
        else:
            messagebox.showerror('Error', 'Cannot save no figure!')

    def button_grid(self):
        if not self.grid_toggled:
            self.buttons['toggle_grid'].configure(text='Grid: on')
            self.buttons['toggle_grid'].configure(fg_color='green')
            self.ax.grid(linestyle='--')
            self.grid_toggled = True
        else:
            self.buttons['toggle_grid'].configure(text='Grid: off')
            self.buttons['toggle_grid'].configure(fg_color='gray')
            self.ax.grid(b=None)
            self.grid_toggled = False

    def slider_max_velocity(self, value):
        Constants.max_velocity = float(value)
        # print(self.charge)
        self.buttons['max_velocity_display'].configure(text=str(round(value, 2)))

    def slider_scaling(self, value):
        self.scaling = float(value)
        self.buttons['scaling_display'].configure(text=str(round(value, 2)))

    def play_action(self):
        if not self.image:
            messagebox.showerror('Error', 'Cannot play the simulation until an image is uploaded!')
        else:
            # print("iiiiiiin motioooooon")
            play = Thread(target=self.loop)
            self.looping = True
            play.start()
            # self.buttons['play'].configure(text='Restart')
            self.buttons['play'].destroy()
            self.buttons.pop('play')
            self.create_restart_and_pause()

    def restart_action(self):
        # print('Restarting...')
        self.image = None
        self.looping = False
        self.buttons['restart'].destroy()
        self.buttons.pop('restart')
        self.buttons['pause'].destroy()
        self.buttons.pop('pause')
        self.create_play_button()
        self.positive = []
        self.negative = []
        self.inside = []
        self.ax.clear()
        self.FPS = float(self.buttons['speed'].cget('value'))
        self.canvas.draw()

    def pause_action(self):
        if self.FPS != 0:
            self.FPS = 0
        else:
            self.FPS = 30
            self.buttons['speed_display'].configure(text='30.00')

    def upload_action(self):
        self.looping = False
        # print("Uploading...")
        filetypes = (
            ('Bitmaps', '*.bmp'),
        )
        image_path = filedialog.askopenfilename(title='Wybierz obraz przewodnika',
                                                initialdir=r'C:\Users\Julian\Desktop',
                                                filetypes=filetypes)
        if image_path != '' and image_path is not None:
            self.image = Image.open(image_path)
            self.image_array = np.asarray(self.image)
            self.inside = get_inside(self.image_array)
            self.edge = get_edges(self.image_array)
            # print("INSIDE:", self.inside)
            self.update_image()
        else:
            print('File not chosen!')

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
        self.fig = plt.figure(figsize=(14, 9), dpi=80)
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
            self.draw_trace(particle)
        self.ax.imshow(self.image)
        if self.grid_toggled:
            print('grid toggled')
            self.ax.grid(linestyle='--')
        self.canvas.draw()

    def draw_trace(self, particle: Charge):
        self.ax.plot([particle.x, particle.last_inside.x - (particle.vx * self.scaling)],
                     [particle.y, particle.last_inside.y - (particle.vy * self.scaling)],
                     c=particle.get_color(),
                     linestyle='--')
        # print(particle.vx, particle.vy)

    def draw(self):
        for particle in self.charges:
            # for e in self.edge:
            #     if particle.normalised_point() == e.p:
            #         print("PARTICLE POINT:", particle.normalised_point())
            #         print("EDGE:", e)
            #         v = e.v.tangent()
            #         particle = particle.project(v)
            #         break
            # 1. update acceleration
            particle = calc.acceleration(particle, self.charges)
            # 2. update other parameters
            particle.update_position()
            # 3. check if in bounds. if not, set velocity to negative and calculate again
            for e in self.edge:
                if particle.normalised_point() == e.p:
                    # print("PARTICLE POINT:", particle.normalised_point())
                    # print("EDGE:", e)
                    v = e.v.tangent()
                    particle = particle.project(v)
                    break
            particle = calc.update_particle(particle, self.image_array, self.inside)
            particle.update_velocity()

            particle.last_inside = Point(particle.x, particle.y)

        self.update_image()
        # print('drew frame')

    def loop(self):
        while self.looping:
            while self.FPS == 0:
                pass
                # print('paused')
            self.draw()
            while self.FPS == 0:
                pass
                # print('paused')
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
