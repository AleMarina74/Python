#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mariadb

dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit=True
)
cur = dbPk.cursor()

class GrillaTabla(tk.Tk):
    def __init__(self, tabla, columnas,lencolumnas, sql):
        super().__init__()
        self.tabla = tabla
        self.frame = tk.Frame(self)
        # self.campo = campo
        # self.valor = valor
        self.nombre_cols = list(columnas)
        self.width_cols = list(lencolumnas)

        self.title('Lista de' + self.tabla)
        self.frame.pack(fill='both')

        framecerrar = tk.Frame(self)

        framecerrar.pack(fill='both')

        boton_cerrar = tk.Button(framecerrar, text="CERRAR", command=self.destroy)
        boton_cerrar.config(pady=10, padx=0)
        boton_cerrar.pack(fill='both')

        self.obtenerdatos(sql)

        for i in range(self.cant_cols):
            self.e = tk.Entry(self.frame, width=lencolumnas[i])
            self.e.config(bg='black', fg='white')
            self.e.grid(row=0, column=i)
            self.e.insert(tk.END, self.nombre_cols[i])

        for fila in range(self.cant_filas):
            for col in range(self.cant_cols):
                self.e = tk.Entry(self.frame, width=lencolumnas[col])
                self.e.grid(row=fila + 1, column=col)
                self.e.insert(tk.END, self.resultado[fila][col])
                self.e.config(state='readonly')



    def obtenerdatos(self,sql):
        busquedatabla = sql
        cur.execute(busquedatabla)
        self.resultado = cur.fetchall()
        if len(self.resultado) > 0:
            self.cant_filas = len(self.resultado)  # la cantidad de registros para saber cuántas filas
            self.cant_cols = len(self.resultado[0])  # obtengo la cantidad de columnas
        else:
            messagebox.showwarning('Atencion','No se encontro el dato en la base, revise que este correcto.')
            self.destroy()



class grillaFrame(tk.Frame):
    def __init__(self, agrega, columnas,lencolumnas, resultado, frameoriginal):
        super().__init__()
        self.agrega = agrega
        self.frame = tk.Frame(frameoriginal)
        # self.campo = campo
        # self.valor = valor
        self.nombre_cols = list(columnas)
        self.width_cols = list(lencolumnas)
        self.resultado = resultado


        # self.title('Lista de' + self.tabla)
        self.frame.pack(fill='both')

        # framecerrar = tk.Frame(self)
        #
        # framecerrar.pack(fill='both')
        #
        # boton_cerrar = tk.Button(framecerrar, text="CERRAR", command=self.destroy)
        # boton_cerrar.config(pady=10, padx=0)
        # boton_cerrar.pack(fill='both')

        # self.obtenerdatos(sql)
        self.cant_filas = len(self.resultado)  # la cantidad de registros para saber cuántas filas
        self.cant_cols = len(self.resultado[0]) # obtengo la cantidad de columnas

        if self.agrega != 'Agregar':
            for i in range(self.cant_cols):
                self.e = tk.Entry(self.frame, width=lencolumnas[i])
                self.e.config(bg='black', fg='white')
                self.e.grid(row=0, column=i)
                self.e.insert(tk.END, self.nombre_cols[i])

        for fila in range(self.cant_filas):
            for col in range(self.cant_cols):
                self.e = tk.Entry(self.frame, width=lencolumnas[col])
                self.e.grid(row=fila + 1, column=col)
                self.e.insert(tk.END, self.resultado[fila][col])
                self.e.config(state='readonly')

class Scrollbar_Example:
    def __init__(self,componente):
        self.window = componente

        self.scrollbar = tk.Scrollbar(self.window)
        self.scrollbar.pack(side="right", fill="y")

        # self.listbox = tk.Listbox(self.window, yscrollcommand=self.scrollbar.set)
        # for i in range(100):
        #     self.listbox.insert("end", str(i))
        # self.listbox.pack(side="left", fill="both")
        #
        # self.scrollbar.config(command=self.listbox.yview)

        self.window.mainloop()

    # def obtenerdatos(self,sql):
    #     busquedatabla = sql
    #     cur.execute(busquedatabla)
    #     self.resultado = cur.fetchall()
    #     if len(self.resultado) > 0:
    #         self.cant_filas = len(self.resultado)  # la cantidad de registros para saber cuántas filas
    #         self.cant_cols = len(self.resultado[0])  # obtengo la cantidad de columnas
    #     else:
    #         messagebox.showwarning('Atencion','No se encontro el dato en la base, revise que este correcto.')
    #         self.destroy()


if __name__ == '__main__':
    # raiz2 = tk.Tk()
    # self.raiz2.title('Lista de' + self.tabla)
    # frameppal = tk.Frame(self.raiz2)
    # frameppal.pack(fill='both')
    # framecerrar = tk.Frame(raiz2)
    #
    # framecerrar.pack(fill='both')
    #
    # boton_cerrar = tk.Button(framecerrar, text="CERRAR", command=raiz2.destroy)
    # boton_cerrar.config(pady=10, padx=0)
    # boton_cerrar.pack(fill='both')

# # obtengo los datos -> Messirve el query1 del ejemplo de sqlite
# busquedatabla = 'SELECT * FROM ' + tabla
# cur.execute(busquedatabla)
# resultado = cur.fetchall()
# cant_filas = len(resultado)  # la cantidad de registros para saber cuántas filas
# cant_cols = len(resultado[0])  # obtengo la cantidad de columnas

    app = Scrollbar_Example(root)