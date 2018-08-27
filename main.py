#!/usr/bin/env python3

from itertools import cycle
from PIL import ImageTk, Image
from random import shuffle
import tkinter as tk
import glob


class App(tk.Tk):

    def __init__(self, image_files, delay):
        # root is self
        tk.Tk.__init__(self)
        self.attributes("-fullscreen", True)
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()

        self.delay = delay * 1000
        # shuffle then loop through the photos
        shuffle(image_files)
        self.pictures = cycle(image_files)
        self.window = tk.Label(self)
        self.window.pack()

    def show_slides(self):
        img_path = next(self.pictures)

        img_object = Image.open(img_path)
        img_width, img_height = img_object.size
        # fit to screen
        wscale = self.width / img_width
        hscale = self.height / img_height
        scale = min(wscale, hscale)

        img = img_object.resize((int(img_width * scale), int(img_height * scale)), Image.BICUBIC)

        self.window.image = ImageTk.PhotoImage(img)  # to avoid garbage collection
        self.window.config(image=self.window.image)

        self.after(self.delay, self.show_slides)

    def run(self):
        self.show_slides()
        self.mainloop()


# seconds between images
delay = 1

filenames = []
for filename in glob.glob('./*'):
    filenames.append(filename)

app = App(filenames, delay)
app.run()
