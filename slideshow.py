#!/usr/bin/env python3

from itertools import cycle
from PIL import ImageTk, Image, ImageFilter
from random import shuffle
import tkinter as tk
import glob
import argparse
from os.path import isdir


class App(tk.Tk):

    def __init__(self, image_files, delay):
        # root is self
        tk.Tk.__init__(self)
        self.attributes("-fullscreen", True)
        self.config(cursor='none')
        self.width, self.height = self.winfo_screenwidth(), self.winfo_screenheight()

        self.delay = delay * 1000
        # shuffle then loop through the photos
        self.image_files = image_files
        shuffle(self.image_files)
        self.pictures = cycle(self.image_files)
        self.num_img_files = len(self.image_files)
        self.pic_ctr = self.num_img_files

        self.window = tk.Label(self)
        self.window.pack()

    def show_slides(self):
        # shuffle the order of the photos each time we loop through them all
        if self.pic_ctr == 0:
            shuffle(self.image_files)
            self.pictures = cycle(self.image_files)
            self.pic_ctr = self.num_img_files

        img_path = next(self.pictures)
        self.pic_ctr -= 1

        img_object = Image.open(img_path)

        # resize the image to fit the screen
        img_width, img_height = img_object.size
        wscale = self.width / img_width
        hscale = self.height / img_height
        scale = min(wscale, hscale)
        foreground = img_object.resize((int(img_width * scale), int(img_height * scale)), Image.BICUBIC)

        # use the foreground to make a blurred background
        background = self.blur_background(foreground)

        # slide the photo to the centre of the screen
        fwidth, fheight = foreground.size
        foreground_centre = (self.width//2 - fwidth//2, self.height//2 - fheight//2)
        # overlay the foreground over the blurred background
        background.paste(foreground, foreground_centre)

        # show the image
        self.window.image = ImageTk.PhotoImage(background)  # to avoid garbage collection
        self.window.config(image=self.window.image)

        self.after(self.delay, self.show_slides)

    def blur_background(self, foreground):
        width, height = foreground.size
        wscale = self.width / width
        hscale = self.height / height
        scale = max(wscale, hscale)
        # expand the background so it fills areas around the foreground image
        background = foreground.resize((int(width * scale), int(height * scale)))
        width, height = background.size

        # crop the background to the size of the screen, then blur
        background = background.crop((
            width//2 - self.width//2,
            height//2 - self.height//2,
            width//2 + self.width//2,
            height//2 + self.height//2)
        ).filter(ImageFilter.GaussianBlur(radius=10))

        return background

    def run(self):
        self.show_slides()
        self.mainloop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path', help='absolute path to folder of images')
    parser.add_argument('delay', help='seconds between changing images', type=int)
    args = parser.parse_args()

    delay = args.delay
    folderpath = args.folder_path

    if not isdir(folderpath):
        print(folderpath + ' is not a folder or is not an absolute path')
        raise SystemExit
    folderpath = folderpath.rstrip('/\\') + '/*'

    filenames = []
    for filename in glob.glob(folderpath, recursive=True):
        filenames.append(filename)

    app = App(filenames, delay)
    app.run()
