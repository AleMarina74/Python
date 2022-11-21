#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
import mariadb
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import sqlite3 as sq
# conn = sql3.connect('/work/data/articles.db')
dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit = True
)
cur = dbPk.cursor()

def EstadisticaGrafico(opcion,fileImagen):
####VENTANA ARTICULOS
    StockVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idClienteVent = ClienteVent.winfo_id()
    StockVent.title('Tech-Hard - Stock Estadisticas')  # pone titulo a la ventana principal
    StockVent.geometry('600x600')  # Tamaño en pixcel de la ventana
    StockVent.iconbitmap('imagenHT.ico')  # icono
    StockVent.minsize(625, 625)
    StockVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar

    framecampoStock = tk.Frame(StockVent)
    framecampoStock.config(width=625, height=625)
    # framecampoStock.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoStock.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoStock.config(bd=25)  # tamano del borde en pixeles
    framecampoStock.pack(fill='x')  # ancho como el padre
    framecampoStock.pack(fill='y')  # alto igual que el padre
    framecampoStock.pack(fill='both')  # ambas opciones
    framecampoStock.pack(fill='both', expand=1)  # expandirese para ocupar el espacio
    miImagen = tk.PhotoImage(file=fileImagen)
    imagen = tk.Label(framecampoStock, image=miImagen)  # png y gif
    imagen.pack(anchor='center',fill='both',expand=1)
    StockVent.mainloop()



def grafico():
    sql_query = pd.read_sql_query('SELECT * FROM ventasitems', dbPk)
    df_articles = pd.DataFrame(sql_query,columns=['id_Articulo','Detalle','Precio_Unitario','Cantidad'])
    df_articles.set_index('id_Articulo', inplace=True)
    print(df_articles)

    my_df2 = df_articles.groupby('id_Articulo').sum()
    por_cant = df_articles.sort_values('id_Articulo',ascending = False)
    print(por_cant['Cantidad'].head(1))

    # RESOLUCIÓN GRÁFICA ponerlos mas bonitos, mejor y mas bonitos, y poner titulo
    sns.displot(df_articles,x='Detalle')
    plt.xticks(rotation=90)
    plt.show()


    # my_df3 = (df_articles.groupby('id_Articulo').sum()).sort_values('Detalle', ascending=False).head(5)
    # print(my_df3['Detalle'])
    # RESOLUCIÓN GRÁFICA
    plt.pie(x=my_df2['id_Articulo'],labels= df_articles.index)
    plt.show()