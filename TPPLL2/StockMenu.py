#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from os import curdir
from tkinter import messagebox
from tkinter import ttk

import ArticulosDevolucionMenu
import Proveedores
import Articulos
import PkUtilidades
import VentanaGrilla
import mariadb

import re


dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit=True
)
cur = dbPk.cursor()

Articulos_Campos = ('id_Articulo','CodigoBarras','Nombre','id_Rubro','CostoUnitario','PrecioFinal','id_Proveedor',
                    'UltimoPrecio','Stock_Minimo','Stock_Maximo','Cant_Stock')

def menuStock(opcion): # stockInicial, Baja, Modificacion Consultas por articulo, general
    
    def limpiarvar():
        codigoBarrasVar.set(0)
        nombreVar.set('')
        stockVar.set(0)
        stockMaxVar.set(0)
        stockMinVar.set(0)
        cantidadVar.set(0)

    def componenteshabilitar(valor): #Valores 'disabled' o 'normal'
        codigoBarras_input.config(state=valor)
        nombre_combo.config(state=valor)
        stock_input.config(state=valor)
        stockMin_input.config(state=valor)
        stockMax_input.config(state=valor)
        cantidad_input.config(state=valor)


    def deshabilitarbotones(valor):
        boton_Alta.config(state=valor)
        boton_Buscar.config(state=valor)
        boton_Actualizar.config(state=valor)
        boton_Eliminar.config(state=valor)


    def limpiarCampos():
        codigoBarras_input.delete(0,tk.END)
        codigoBarras_input.select_range(0,tk.END)
        codigoBarras_input.focus()
        nombre_combo.current(0)
        stock_input.delete(0,tk.END)
        stockMax_input.delete(0,tk.END)
        stockMin_input.delete(0,tk.END)
        cantidad_input.delete(0,tk.END)


    def llenarcampos(articulo):

        nombreVar.set(articulo.nombre)
        # Rubro = listarcombo('Rubros','Detalle') # 0=detalle, 1=idRubro
        asignarComboporId('ARTICULOS',nombre_combo,articulo.nombre)
        stockVar.set(articulo.stock)
        stockMinVar.set(articulo.stockMin)
        stockMaxVar.set(articulo.stockMax)

####EVENTOS
    def buscarCodigoBarrasEnter(event):
        buscarCodigoBarras()
        if opcion == 'Modificacion':
            cantidad_input.config(state='disabled')
            stockMax_input.config(state='normal')
            stockMin_input.config(state='normal')
            boton_Actualizar.config(state='normal')
            stockMin_input.select_range(0,tk.END)
            stockMin_input.focus()
        else:
            cantidad_input.config(state='normal')
            cantidad_input.select_range(0, tk.END)
            cantidad_input.focus()

    def llenarCamposEvento(event):
        indice = articulosListado[0].index(nombreVar.get())
        listaCodigosAux = articulosListado[1]
        codigoAbuscar = listaCodigosAux[indice]
        codigoBarrasVar.set(codigoAbuscar)
        buscarCodigoBarras()
        if opcion == 'Modificacion':
            cantidad_input.config(state='disabled')
            stockMax_input.config(state='normal')
            stockMin_input.config(state='normal')
            boton_Actualizar.config(state='normal')
            stockMin_input.select_range(0,tk.END)
            stockMin_input.focus()
        else:
            cantidad_input.config(state='normal')
            cantidad_input.select_range(0, tk.END)
            cantidad_input.focus()


####VALIDACIONES
    def ValidarNumero(VentanaPadre, componente):
        while True:
            try:
                validacion = True
                varingresada = int(componente.get())

            except:
                messagebox.showerror('Validacion Campo', f'Debe ingresar un valor entero Valido')
                componente.delete(0, tk.END)
                componente.select_range(0, tk.END)
                componente.focus()
                VentanaPadre.focus()
                validacion = False

            finally:
                return validacion

#####FUNCIONES
    def asignarComboporId(tabla,componente,dato):
        combodatos = listarcombo(tabla,'Id')
        idDato = combodatos[0]
        indice = idDato.index(dato)
        componente.current(indice)

    def listarcombo(tabla, campo):
        buscarcombo = 'SELECT * FROM ' + tabla + ' ORDER BY Nombre ASC'
        cur.execute(buscarcombo)
        resultado = cur.fetchall()
        listadelcombo = []
        id_campo = []
        if len(resultado) < 0:
            messagebox.showwarning(f'LISTADO DE {tabla.upper()}',
                                   f'No tiene ningun dato cargado en la tabla {tabla.upper()}')
            PedidosVent.focus()
        else:
            for ind in resultado:
                if tabla.upper() == 'ARTICULOS':
                    listadelcombo.append(ind[2])
                    id_campo.append(ind[1])

        return listadelcombo,id_campo

    def EncontrarArticulo():
        sqlbusqueda = 'SELECT * FROM articulos WHERE CodigoBarras = ' + str(codigoBarrasVar.get())
        cur.execute(sqlbusqueda)
        Resultado = cur.fetchall()

        if len(Resultado) > 0:
            protupla = []
            for ind in Resultado:
                for i in range(1, len(ind)):
                    protupla.append(ind[i])
                ArticuloEncontrado = Articulos.Articulos(tuple(protupla))
                ArticuloEncontrado.idArticulos = ind[0]
        return ArticuloEncontrado

####FUNCIONES DE BUSQUEDA
    def buscarCodigoBarras():
        if ValidarNumero(StockVent,codigoBarras_input):
            buscaCodigo = codigoBarrasVar.get()

            if buscaCodigo == 0 or buscaCodigo > 99999999999999999999:
                messagebox.showerror('Verificacion de Datos', 'Debe ingresar un valor valido de CODIGO DE BARRAS')
                StockVent.focus()
                codigoBarras_input.delete(0,tk.END)
                codigoBarras_input.select_range(0,tk.END)
                codigoBarras_input.focus()
            else:
                sqlbusqueda='SELECT * FROM articulos WHERE CodigoBarras = ' +str(buscaCodigo)
                cur.execute(sqlbusqueda)
                Resultado = cur.fetchall()

                if len(Resultado) > 0:
                    protupla = []
                    for ind in Resultado:
                        for i in range(1,len(ind)):
                            protupla.append(ind[i])
                        ArticuloEncontrado = Articulos.Articulos(tuple(protupla))
                        ArticuloEncontrado.idArticulos = ind[0]
                    if opcion == 'Baja':
                        llenarcampos(ArticuloEncontrado)
                        componenteshabilitar('normal')
                        stockMin_input.config(state='disabled')
                        stockMax_input.config(state='disabled')
                        stock_input.config(state='disabled')
                        boton_Eliminar.config(state='normal')
                        boton_Eliminar.focus()
                        del Resultado
                    elif opcion == 'StockInicial':
                        llenarcampos(ArticuloEncontrado)
                        # messagebox.showwarning('Advertencia',f'El Articulo ya existe {ArticuloEncontrado.nombre}')
                        boton_Alta.config(state='normal')
                        componenteshabilitar('normal')
                        stock_input.config(state='disabled')
                        codigoBarras_input.config(state='disabled')
                        codigoBarras_input.focus()
                        nombre_combo.config(state='normal')
                        nombre_combo.current(0)
                        del Resultado
                    elif opcion == 'Modificacion':
                        llenarcampos(ArticuloEncontrado)
                        boton_Actualizar.config(state='normal')
                        componenteshabilitar('normal')
                        stock_input.config(state='disabled')
                        cantidad_input.config(state='disabled')
                        stockMax_input.config(state='normal')
                        stockMin_input.config(state='normal')
                        stockMin_input.select_range(0, tk.END)
                        stockMin_input.focus()
                        del Resultado
                    elif opcion == 'BuscarCodigoBarras':
                        llenarcampos(ArticuloEncontrado)
                        boton_Buscar.config(state='normal')
                        stock_input.config(state='disabled')
                        codigoBarras_input.select_range(0, tk.END)
                        codigoBarras_input.focus()

                elif len(Resultado) < 1:

                    # opcion == 'Baja' or opcion == 'Modificacion' or opcion == 'buscarCodigoBarras' or opcion == 'BuscarNombre' :
                    messagebox.showwarning('Advertencia', f'No existe el Articulo Solicitado\n con el Codigo de Barras: {buscaCodigo}')
                    del Resultado
                    StockVent.focus()
                    limpiarCampos()
                    limpiarvar()
                    codigoBarras_input.delete(0, tk.END)
                    codigoBarras_input.select_range(0, tk.END)
                    codigoBarras_input.focus()
                    nombre_combo.current(0)



        else:
            StockVent.focus()
            codigoBarras_input.delete(0, tk.END)
            codigoBarras_input.select_range(0, tk.END)
            codigoBarras_input.focus()

    def BuscarNombre():
        indice = articulosListado[0].index(nombreVar.get())
        listaCodigosAux = articulosListado[1]
        codigoAbuscar = listaCodigosAux[indice]
        codigoBarrasVar.set(codigoAbuscar)
        sqlbusqueda = 'SELECT * FROM articulos WHERE CodigoBarras = ' + str(codigoAbuscar)
        cur.execute(sqlbusqueda)
        Resultado = cur.fetchall()

        if len(Resultado) > 0:
            protupla = []
            for ind in Resultado:
                for i in range(1, len(ind)):
                    protupla.append(ind[i])
                ArticuloEncontrado = Articulos.Articulos(tuple(protupla))
                ArticuloEncontrado.idArticulos = ind[0]
        llenarcampos(ArticuloEncontrado)

#### FUNCIONES BOTONES
    def cargaStock():
        if codigoBarras_input.get() == '':
            messagebox.showerror(f'Carga de Articulos',
                                 'No ha seleccionado ningun articulo o no ha ingresado codigo de barras.')
            StockVent.focus()
        else:
            articuloStockCarga = EncontrarArticulo()
            if opcion == 'StockInicial':

                if messagebox.askquestion(f'Carga de Stock del Articulo {articuloStockCarga.nombre}',f'Esta seguro de cargar el Stock Inicial del articulo?') == 'yes':
                    articuloStockCarga.aumentarStock(cantidadVar.get())
                    dbPk.commit()
                    stockVar.set(articuloStockCarga.stock)
                    articuloStockCarga.modificaArticulo(articuloStockCarga.idArticulos)
                    dbPk.commit()
                    cantidadVar.set(0)
                    StockVent.focus()
                else:
                    cantidadVar.set(0)
                    StockVent.focus()
            else:
                if messagebox.askquestion(f'Carga de Stock del Articulo {articuloStockCarga.nombre}',f'Esta seguro de aumentar el Stock del articulo?') == 'yes':
                    articuloStockCarga.aumentarStock(cantidadVar.get())
                    dbPk.commit()
                    stockVar.set(articuloStockCarga.stock)
                    cantidadVar.set(0)
                    StockVent.focus()
                else:
                    cantidadVar.set(0)
                    StockVent.focus()



    def BajaStock():
        if codigoBarras_input.get() != '':
            articuloStockBaja = EncontrarArticulo()
            if cantidadVar.get() > articuloStockBaja.stock:
                if messagebox.askquestion(f'Baja de Stock del Articulo {articuloStockBaja.nombre}',f'La cantidad a dar de '
                                                                                                   f'Baja es mayor que el stock Actual '
                                                                                                   f'{articuloStockBaja.stock}\n'
                                                                                                   f'\n'
                                                                                                   f'Desea modificar la cantidad por una menor?') == 'yes':
                    cantidadVar.set(articuloStockBaja.stock)
                    cantidad_input.focus()
                    StockVent.focus()
                else:
                    cantidadVar.set(0)
                    StockVent.focus()
            else:
                if messagebox.askquestion(f'Baja de Stock',f'Esta seguro de disminuir el stock?\n'
                                                           f'\n'
                                                           f'Debera cargar el motivo de la baja de stock del articulo.') == 'yes':
                    articuloStockBaja.disminuirStock(cantidadVar.get())
                    dbPk.commit()
                    # ArticulosDevolucionMenu.menuDevoluciones('Devolucion',articuloStockBaja.idArticulos,articuloStockBaja.nombre,cantidadVar.get())
                    # StockVent.destroy()

        else:
            messagebox.showerror(f'Carga de Articulos','No ha seleccionado ningun articulo o no ha ingresado codigo de barras.')
            StockVent.focus()

    def actualizacionStock():
        if codigoBarras_input.get() != '':
            articulosActualizacion = EncontrarArticulo()
            if stockMaxVar.get() < 0:
                stockMaxVar.set(0)
            if stockMinVar.get() < 0:
                stockMinVar.set(0)
            articulosActualizacion.stockMin = stockMinVar.get()
            articulosActualizacion.stockMax = stockMaxVar.get()
            articulosActualizacion.modificaArticulo(articulosActualizacion.idArticulos)
            if messagebox.askquestion(f'Actualizacion de Stock Minimo y/o Maximo del Articulo {articulosActualizacion.nombre}',
                                      f'Actualizacion de stock Minimo y Maximo EXITOSA\n'
                                      f'\n'
                                      f'Desea Actualizar otro Articulo?') =='yes':
                nombre_combo.current(0)
                stockMaxVar.set(0)
                stockMinVar.set(0)
                StockVent.focus()
            else:
                StockVent.destroy()
        else:
            messagebox.showerror(f'Carga de Articulos','No ha seleccionado ningun articulo o no ha ingresado codigo de barras.')
            StockVent.focus()



####VENTANA ARTICULOS
    StockVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idClienteVent = ClienteVent.winfo_id()
    StockVent.title('Tech-Hard - Stock Articulos')  # pone titulo a la ventana principal
    StockVent.geometry('500x400')  # Tamaño en pixcel de la ventana
    StockVent.iconbitmap('imagenHT.ico')  # icono
    StockVent.minsize(500, 400)
    StockVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar

    framecampoStock = tk.Frame(StockVent)
    framecampoStock.config(width=500, height=400)
    framecampoStock.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoStock.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoStock.config(bd=25)  # tamano del borde en pixeles
    framecampoStock.pack(fill='x')  # ancho como el padre
    framecampoStock.pack(fill='y')  # alto igual que el padre
    framecampoStock.pack(fill='both')  # ambas opciones
    framecampoStock.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    def config_label(mi_label, fila):
        espaciado_labels = {'column': 50, 'sticky': 'e', 'padx': 10, 'pady': 10}
        # color_labels ={'bg':color_fondo, 'fg':color_letra,'font':fuente}
        mi_label.grid(row=fila, **espaciado_labels)
        # mi_label.config(**color_labels)

    codigoBarrasVar = tk.IntVar()
    nombreVar = tk.StringVar()
    stockVar = tk.IntVar()
    stockMinVar = tk.IntVar()
    stockMaxVar = tk.IntVar()
    cantidadVar = tk.IntVar()

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
    # label/entry/botones

    codigoBarras_label = tk.Label(framecampoStock, text='Codigo de Barras')
    config_label(codigoBarras_label, 3)

    codigoBarras_input = tk.Entry(framecampoStock, width=20, justify=tk.RIGHT, textvariable=codigoBarrasVar)
    codigoBarras_input.grid(row=3, column=51, padx=10, pady=10, sticky='w')
    codigoBarras_input.delete(0, tk.END)
    codigoBarras_input.select_range(0, tk.END)
    codigoBarras_input.focus()
    codigoBarras_input.bind('<Return>', buscarCodigoBarrasEnter)  # crear funcion evento

    
    nombre_label = tk.Label(framecampoStock, text='Nombre')
    config_label(nombre_label, 4)
    articulosListado = listarcombo('Articulos', 'Detalle')
    nombre_combo = ttk.Combobox(framecampoStock, width=30, state='readonly', textvariable=nombreVar,
                                values=articulosListado[0])
    nombre_combo.grid(row=4, column=51, padx=10, pady=10, sticky='w')
    nombre_combo.current(0)
    nombre_combo.bind('<<ComboboxSelected>>',llenarCamposEvento) #llenar campos de stock



    stock_label = tk.Label(framecampoStock, text='Stock Actual')
    config_label(stock_label, 6)
    stock_input = tk.Entry(framecampoStock, justify=tk.RIGHT, textvariable=stockVar)
    stock_input.grid(row=6, column=51, padx=10, pady=10, sticky='w')

    stockMin_label = tk.Label(framecampoStock, text='Stock Minimo')
    config_label(stockMin_label, 13)
    stockMin_input = tk.Entry(framecampoStock, justify=tk.RIGHT, textvariable=stockMinVar)
    stockMin_input.grid(row=13, column=51, padx=10, pady=10, sticky='w')

    stockMax_label = tk.Label(framecampoStock, text='Stock Maximo')
    config_label(stockMax_label, 14)
    stockMax_input = tk.Entry(framecampoStock, justify=tk.RIGHT, textvariable=stockMaxVar)
    stockMax_input.grid(row=14, column=51, padx=10, pady=10, sticky='w')

    cantidad_label = tk.Label(framecampoStock, text='Cantidad')
    config_label(cantidad_label,20)
    cantidad_input = tk.Entry(framecampoStock, justify=tk.RIGHT, textvariable=cantidadVar)
    cantidad_input.grid(row=20, column=51, padx=10, pady=10, sticky='w')

##### FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesArticulos = tk.Frame(StockVent)
    framebotonesArticulos.pack()

    boton_Alta = tk.Button(framebotonesArticulos, text='Cargar', command=cargaStock)
    boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)

    boton_Buscar = tk.Button(framebotonesArticulos, text='Buscar', command=buscarCodigoBarras)
    boton_Buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesArticulos, text='Actualizar', command=actualizacionStock)
    boton_Actualizar.grid(row=0, column=3, padx=5, pady=10, ipadx=7)

    boton_Eliminar = tk.Button(framebotonesArticulos, text='Baja', command=BajaStock)
    boton_Eliminar.grid(row=0, column=4, padx=5, pady=10, ipadx=7)


    if opcion == 'StockInicial':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        boton_Buscar.bind('<Return>', buscarCodigoBarrasEnter)
        limpiarCampos()
        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        codigoBarras_input.config(state='normal')
        codigoBarras_input.select_range(0, tk.END)
        codigoBarras_input.focus()

    elif opcion == 'Carga':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
        boton_Alta.config(state='normal')
        codigoBarras_input.config(state='normal')
        codigoBarras_input.select_range(0, tk.END)
        codigoBarras_input.focus()
        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        cantidad_input.config(state='normal')
        cantidad_input.select_range(0,tk.END)
        cantidad_input.focus()

    elif opcion == 'Baja':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
        boton_Eliminar.config(state='normal')
        codigoBarras_input.config(state='normal')
        codigoBarras_input.select_range(0, tk.END)
        codigoBarras_input.focus()
        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        cantidad_input.config(state='normal')
        cantidad_input.select_range(0,tk.END)
        cantidad_input.focus()

    elif opcion == 'Modificacion':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        boton_Actualizar.config(state='normal')
        limpiarCampos()
        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        codigoBarras_input.config(state='normal')
        codigoBarras_input.select_range(0, tk.END)
        codigoBarras_input.focus()

    elif opcion == 'BuscarCodigoBarras':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
        codigoBarras_input.config(state='normal')
        codigoBarras_input.select_range(0, tk.END)
        codigoBarras_input.focus()

    elif opcion == 'BuscarNombre':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal', command=BuscarNombre)  # cambiar comman para buscar por nombre armar funcion
        limpiarCampos()
        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        nombre_combo.select_range(0, tk.END)

    