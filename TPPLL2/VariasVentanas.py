#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from FuncionesMenu import *
from os import curdir
from tkinter import messagebox
from tkinter import ttk

#Pantalla Clientes

class FrameClientes()

# import tkinter as tk
#
# def createNewWindow():
#     newWindow = tk.Toplevel(app)
#     labelExample = tk.Label(newWindow, text = "New Window")
#     buttonExample = tk.Button(newWindow, text = "New Window button")
#
#     labelExample.pack()
#     buttonExample.pack()
#
# app = tk.Tk()
# buttonExample = tk.Button(app,
#               text="Create new window",
#               command=createNewWindow)
# buttonExample.pack()
#
# app.mainloop()

# import tkinter as tk
#
# class Aplicacion:
#     def __init__(self):
#         self.ventana1=tk.Tk()
#         menubar1 = tk.Menu(self.ventana1)
#         self.ventana1.config(menu=menubar1)
#         opciones1 = tk.Menu(menubar1)
#         opciones1.add_command(label="Rojo", command=self.fijarrojo)
#         opciones1.add_command(label="Verde", command=self.fijarverde)
#         opciones1.add_command(label="Azul", command=self.fijarazul)
#         menubar1.add_cascade(label="Colores", menu=opciones1)
#
#         opciones2 = tk.Menu(menubar1)
#         opciones2.add_command(label="640x480", command=self.ventanachica)
#         opciones2.add_command(label="1024x800", command=self.ventanagrande)
#
#         submenu1=tk.Menu(menubar1)
#         submenu1.add_command(label="1024x1024", command=self.tamano1)
#         submenu1.add_command(label="1280x1024", command=self.tamano2)
#
#         opciones2.add_cascade(label="Otros tamaños", menu= submenu1)
#
#         menubar1.add_cascade(label="Tamaños", menu=opciones2)
#         self.ventana1.mainloop()
#
#     def fijarrojo(self):
#         self.ventana1.configure(background="red")
#
#     def fijarverde(self):
#         self.ventana1.configure(background="green")
#
#     def fijarazul(self):
#         self.ventana1.configure(background="blue")
#
#     def ventanachica(self):
#         self.ventana1.geometry("640x480")
#
#     def ventanagrande(self):
#         self.ventana1.geometry("1024x800")
#
#     def tamano1(self):
#         self.ventana1.geometry("1024x1024")
#
#     def tamano2(self):
#         self.ventana1.geometry("1280x1024")
#
# aplicacion1=Aplicacion()


# from tkinter import *
# from tkinter.ttk import *
#
# master = Tk()
#
# master.geometry("200x200")
#
#
# def openNewWindow():
#     newWindow = Toplevel(master)
#
#     newWindow.title("New Window")
#
#     newWindow.geometry("200x200")
#
#     Label(newWindow,
#           text="This is a new window").pack()
#
#
# label = Label(master,
#               text="This is the main window")
#
# label.pack(pady=10)
#
# btn = Button(master,
#              text="Click to open a new window",
#              command=openNewWindow)
# btn.pack(pady=10)
#
# mainloop()


# from tkinter import *
# from tkinter.ttk import *
#
#
# class NewWindow(Toplevel):
#
#     def __init__(self, master=None):
#         super().__init__(master=master)
#         self.title("New Window")
#         self.geometry("200x200")
#         label = Label(self, text="This is a new Window")
#         label.pack()
#
#
# master = Tk()
#
# master.geometry("200x200")
#
# label = Label(master, text="This is the main window")
# label.pack(side=TOP, pady=10)
#
# btn = Button(master,
#              text="Click to open a new window")
#
# btn.bind("<Button>",
#          lambda e: NewWindow(master))
#
# btn.pack(pady=10)
#
# mainloop()