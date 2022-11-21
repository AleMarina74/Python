#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from os import curdir
from tkinter import messagebox
from tkinter import ttk
import mariadb

dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit = True
)
cur = dbPk.cursor()

def buscarindice(tupla,valor):
    for i in range(0,len(tupla)):
        if valor == tupla[i]:
            Resul = True
            break
        else:
            Resul = False
    return Resul

def CreaVariabledesdeLista(Campos,indiceint,indicefloat):
    # Campos = (
    #     'id_Articulo', 'CodigoBarras', 'Nombre', 'id_Rubro', 'CostoUnitario', 'PrecioFinal', 'id_Proveedor',
    #     'UltimoPrecio',
    #     'Stock_Minimo', 'Stock_Maximo', 'Cant_Stock')
    # indiceint = (0, 1, 3, 6, 8, 9, 10)
    # indicefloat=()
    for i in range(0, len(Campos)):
        if len(indiceint) > 0:
            if i in indiceint:
                exec(f'{Campos[i]} = 0')
        elif len(indicefloat) >0 :
            if i in indicefloat:
                exec(f'{Campos[i]} = 0')
        else:
            exec(f'{Campos[i]} = \'\'')

def mostrar_listado_variables(variables):
    for v in variables:
        if not v.startswith('__'):
            print(v)



#Conectar
def conectar():
    global dbPk
    global cur

    dbPk = mariadb.connect(
        host='127.0.0.1',
        user='root',
        password='root',
        database='Pk'
    )
    cur = dbPk.cursor()


#Salir
# def salir():
#     rta = messagebox.askquestion('Confirme','Desea salir de la aplicacion?')
#     if rta == 'yes':
#         # dbPk.close()
#         raiz.destroy()



#---- MENU ACERDA DE...
def mostrar_licencia():
    gnuglp = '''
        Sistema de Gestion Comercial de Tech-Hard en Python 
        Copyright (C) 2022 - 4 Panas
        Email: desarrollo@4panas.com.ar\n======================================
        This program is free software: you can redistribute it
        and/or modify it under the terms of the GNU General Public
        License as published by the Free Software Foundation,
        either version 3 of the License, or (at your option) any
        later version.
        This program is distributed in the hope that it will be
        useful, but WITHOUT ANY WARRANTY; without even the
        implied warranty of MERCHANTABILITY or FITNESS FOR A
        PARTICULAR PURPOSE.  See the GNU General Public License
        for more details.
        You should have received a copy of the GNU General Public
        License along with this program.
        If not, see <https://www.gnu.org/licenses/>.'''
    messagebox.showinfo("LICENCIA", gnuglp)

def mostrar_acerca():
    messagebox.showinfo("ACERCA DE...",
                        'Creado por 4 Panas\n para Tech-Hard\n Noviembre, 2022 \n Email: desarrollo@4panas.com.ar')

#FUNCIONES VARIAS



#   Limpiar box
def limpiar():
    legajo.set("")
    alumno.set("")
    email.set("")
    calificacion.set("")
    escuela.set("Seleccione")
    localidad.set("")
    provincia.set("")
    legajo_input.config(state='normal')


#FUNCIONES CRUD(CREATE - READ - UPDATE - DELETE)

def listar():
    class Table():
        def __init__(self, raiz2):
            nombre_cols = ['Legajo', 'Alumno', 'Calificación', 'Email',
                           'Escuela', 'Localidad', 'Provincia']
            for i in range(cant_cols):
                self.e = Entry(frameppal)
                self.e.config(bg='black', fg='white')
                self.e.grid(row=0, column=i)
                self.e.insert(END, nombre_cols[i])

            for fila in range(cant_filas):
                for col in range(cant_cols):
                    self.e = Entry(frameppal)
                    self.e.grid(row=fila + 1, column=col)
                    self.e.insert(END, resultado[fila][col])
                    self.e.config(state='readonly')

    raiz2 = Tk()
    raiz2.title('Listado alumnos')
    frameppal = Frame(raiz2)
    frameppal.pack(fill='both')
    framecerrar = Frame(raiz2)
    framecerrar.config(bg=color_texto_boton)
    framecerrar.pack(fill='both')

    boton_cerrar = Button(framecerrar, text="CERRAR", command=raiz2.destroy)
    boton_cerrar.config(bg=color_fondo_boton, fg=color_texto_boton, pady=10, padx=0)
    boton_cerrar.pack(fill='both')

    # obtengo los datos -> Messirve el query1 del ejemplo de sqlite
    con = sq3.connect('mi_db.db')
    cur = con.cursor()
    query1 = '''
            SELECT alumnos.legajo, alumnos.nombre, alumnos.nota, alumnos.email, 
            escuelas.nombre, escuelas.localidad, escuelas.provincia
            FROM alumnos INNER JOIN escuelas
            ON alumnos.id_escuela = escuelas._id
            '''
    cur.execute(query1)
    resultado = cur.fetchall()
    cant_filas = len(resultado)  # la cantidad de registros para saber cuántas filas
    cant_cols = len(resultado[0])  # obtengo la cantidad de columnas

    tabla = Table(frameppal)
    con.close()
    raiz2.mainloop()


if __name__ == '__main__':
    # Campos = (
    #     'id_Articulo', 'CodigoBarras', 'Nombre', 'id_Rubro', 'CostoUnitario', 'PrecioFinal', 'id_Proveedor',
    #     'UltimoPrecio',
    #     'Stock_Minimo', 'Stock_Maximo', 'Cant_Stock')
    # indiceint = (0, 1, 3, 6, 8, 9, 10)
    # indicefloat=()
    # for i in range(0, len(Campos)):
    #     if len(indiceint) > 0:
    #         if i in indiceint:
    #             exec(f'Art{Campos[i]} = 0')
    #     elif len(indicefloat) > 0:
    #         if i in indicefloat:
    #             exec(f'{Campos[i]} = 0')
    #     else:
    #         exec(f'{Campos[i]} = \'\'')
    #
    # mostrar_listado_variables(dir())

    email = "ankitrai326@gmail.com"

    if check(email):
        print('mail correcto')
    else:
        print('mail incorrecto')

    email = "my.ownsite@ourearth.org"
    if check(email):
        print('mail correcto')
    else:
        print('mail incorrecto')

    email = "ankitrai326.com"
    if check(email):
        print('mail correcto')
    else:
        print('mail incorrecto')
