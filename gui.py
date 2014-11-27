#!/usr/bin/env python2.7
#-*- encoding: utf-8 -*-
# 

import ttk
import Tkinter
import tkFileDialog
import sys
import random
import preprocess
import cv2
import PIL
from PIL import Image
from scan import * 

def donothing():
    return

class Gui:
    def openfile(self):
        self.files.append(tkFileDialog.askopenfilename(parent=self.root))
        self.refresh()
        return

    def refresh(self):
        if len(self.files) == 0:
            return

        cv_image = cv2.cvtColor(preprocess.process_text(self.files[self.i]), cv2.COLOR_GRAY2RGB)
        pil_image = Image.fromarray(cv_image)
        pil_image = pil_image.resize((300,300), PIL.Image.ANTIALIAS)
        pil_image.save("/tmp/i.gif")

        gif1 = Tkinter.PhotoImage(file = "/tmp/i.gif")
        self.canvas.create_image(50, 10, image = gif1, anchor = Tkinter.NW)
        self.root.refresh()
                                
        return

    def nextfile(self):
        if len(self.files) > 0:
            self.i = (self.i + 1) % len(self.files)
            self.refresh()
        return

    def step1(self):
        self.text.insert(Tkinter.END, scan(self.knn, self.files[self.i]))
        self.root.update()
        
    def step2(self):
        self.text.insert(Tkinter.END, scantext(self.knn, self.files[self.i]))
        self.root.update()

    def __init__(self, opts, directory="dataset"):
        self.root = Tkinter.Tk()
        self.files = opts
        self.i = 0
        self.knn = learnLetter(directory)


        menubar = Tkinter.Menu(self.root)
        filemenu = Tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=donothing)
        filemenu.add_command(label="Close", command=donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)

        self.canvas = Tkinter.Canvas(self.root)
        self.canvas.grid(row=1, column=0, columnspan=6)
        self.text = Tkinter.Text(self.root)
        self.text.grid(row=1, column=7, columnspan=4)

        b = Tkinter.Button(self.root, text="Open File", command=self.openfile).grid(row=0, column=0, columnspan=1)
        c = Tkinter.Button(self.root, text="Next File", command=self.nextfile).grid(row=0, column=1, columnspan=1)
        d = Tkinter.Button(self.root, text="Step2", command=self.step2).grid(row=0, column=3, columnspan=1)
        e = Tkinter.Button(self.root, text="Step1", command=self.step1).grid(row=0, column=4, columnspan=1)

        self.root.config(menu=menubar)
    #label_image.place(x=0,y=0,width=150,height=150)
        try:
            if len(self.files) > 0:
                self.refresh()
        except:
            1 == 1
        self.root.mainloop()
        
