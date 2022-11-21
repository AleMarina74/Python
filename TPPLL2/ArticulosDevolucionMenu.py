#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from os import curdir
from tkinter import messagebox, scrolledtext
from tkinter import ttk

import ArticulosDevolucion
import Proveedores
import Articulos
import StockMenu
import PkUtilidades
import VentanaGrilla
import datetime
import mariadb

dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit=True
)
cur = dbPk.cursor()

Art_Devolver_Campos = ('id_Articulo','Fecha','Cantidad','Estado','Motivo', 'Descripcion')
CamposInt = (0,2)
CamposFloat = ()
CamposChar = (3,4,5)
CamposDate = (1,)
FechaActual = datetime.date.today()
comboConsultasArticulosDevol = ('id_Articulo','Fecha','Estado','Motivo')

def menuDevoluciones(opcion,*args):
    if len(args) > 0:
        idArticulo = args[0]
        nombre = args[1]
        cantidad = args[2]

    def limpiarvar():
        codigoBarrasVar.set(0)
        nombreVar.set('')
        stockVar.set(0)
        stockMaxVar.set(0)
        stockMinVar.set(0)
        cantidadVar.set(0)

    def componenteshabilitar(valor):  # Valores 'disabled' o 'normal'
        IdArticulo_input.config(state=valor)
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
        IdArticulo_input.delete(0, tk.END)
        IdArticulo_input.select_range(0, tk.END)
        IdArticulo_input.focus()
        nombre_combo.current(0)
        stock_input.delete(0, tk.END)
        stockMax_input.delete(0, tk.END)
        stockMin_input.delete(0, tk.END)
        cantidad_input.delete(0, tk.END)

    def llenarcampos(articulo):

        nombreVar.set(articulo.nombre)
        # Rubro = listarcombo('Rubros','Detalle') # 0=detalle, 1=idRubro
        asignarComboporId('ARTICULOS', nombre_combo, articulo.nombre)
        motivoVar.set(articulo.motivo)
        descripcionVar.set(articulo.descripcion)

####EVENTOS
    def buscarCodigoBarrasEnter(event):
        buscarCodigoBarras()
        if opcion == 'Modificacion':
            cantidad_input.config(state='disabled')
            stockMax_input.config(state='normal')
            stockMin_input.config(state='normal')
            boton_Actualizar.config(state='normal')
            stockMin_input.select_range(0, tk.END)
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
            stockMin_input.select_range(0, tk.END)
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
    def asignarComboporId(tabla, componente, dato):
        combodatos = listarcombo(tabla, 'Id')
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

        return listadelcombo, id_campo

    # def EncontrarArticulo():
    #     sqlbusqueda = 'SELECT * FROM articulos WHERE nombre = ' + str(id_ArticuloVar.get())
    #     cur.execute(sqlbusqueda)
    #     Resultado = cur.fetchall()
    #
    #     if len(Resultado) > 0:
    #         protupla = []
    #         for ind in Resultado:
    #             for i in range(1, len(ind)):
    #                 protupla.append(ind[i])
    #             ArticuloEncontrado = Articulos.Articulos(tuple(protupla))
    #             ArticuloEncontrado.idArticulos = ind[0]
    #     return ArticuloEncontrado

    ####FUNCIONES DE BUSQUEDA
    # def buscarCodigoBarras():
    #     if ValidarNumero(DevolucionesVent, IdArticulo_input):
    #         buscaCodigo = codigoBarrasVar.get()
    #
    #         if buscaCodigo == 0 or buscaCodigo > 99999999999999999999:
    #             messagebox.showerror('Verificacion de Datos', 'Debe ingresar un valor valido de CODIGO DE BARRAS')
    #             DevolucionesVent.focus()
    #             IdArticulo_input.delete(0, tk.END)
    #             IdArticulo_input.select_range(0, tk.END)
    #             IdArticulo_input.focus()
    #         else:
    #             sqlbusqueda = 'SELECT * FROM articulos WHERE CodigoBarras = ' + str(buscaCodigo)
    #             cur.execute(sqlbusqueda)
    #             Resultado = cur.fetchall()
    #
    #             if len(Resultado) > 0:
    #                 protupla = []
    #                 for ind in Resultado:
    #                     for i in range(1, len(ind)):
    #                         protupla.append(ind[i])
    #                     ArticuloEncontrado = Articulos.Articulos(tuple(protupla))
    #                     ArticuloEncontrado.idArticulos = ind[0]
    #                 if opcion == 'Baja':
    #                     llenarcampos(ArticuloEncontrado)
    #                     componenteshabilitar('normal')
    #                     stockMin_input.config(state='disabled')
    #                     stockMax_input.config(state='disabled')
    #                     stock_input.config(state='disabled')
    #                     boton_Eliminar.config(state='normal')
    #                     boton_Eliminar.focus()
    #                     del Resultado
    #                 elif opcion == 'StockInicial':
    #                     llenarcampos(ArticuloEncontrado)
    #                     # messagebox.showwarning('Advertencia',f'El Articulo ya existe {ArticuloEncontrado.nombre}')
    #                     boton_Alta.config(state='normal')
    #                     componenteshabilitar('normal')
    #                     stock_input.config(state='disabled')
    #                     IdArticulo_input.config(state='disabled')
    #                     IdArticulo_input.focus()
    #                     nombre_combo.config(state='normal')
    #                     nombre_combo.current(0)
    #                     del Resultado
    #                 elif opcion == 'Modificacion':
    #                     llenarcampos(ArticuloEncontrado)
    #                     boton_Actualizar.config(state='normal')
    #                     componenteshabilitar('normal')
    #                     stock_input.config(state='disabled')
    #                     cantidad_input.config(state='disabled')
    #                     stockMax_input.config(state='normal')
    #                     stockMin_input.config(state='normal')
    #                     stockMin_input.select_range(0, tk.END)
    #                     stockMin_input.focus()
    #                     del Resultado
    #                 elif opcion == 'BuscarCodigoBarras':
    #                     llenarcampos(ArticuloEncontrado)
    #                     boton_Buscar.config(state='normal')
    #                     stock_input.config(state='disabled')
    #                     IdArticulo_input.select_range(0, tk.END)
    #                     IdArticulo_input.focus()
    #
    #             elif len(Resultado) < 1:
    #
    #                 # opcion == 'Baja' or opcion == 'Modificacion' or opcion == 'buscarCodigoBarras' or opcion == 'BuscarNombre' :
    #                 messagebox.showwarning('Advertencia',
    #                                        f'No existe el Articulo Solicitado\n con el Codigo de Barras: {buscaCodigo}')
    #                 del Resultado
    #                 DevolucionesVent.focus()
    #                 limpiarCampos()
    #                 limpiarvar()
    #                 IdArticulo_input.delete(0, tk.END)
    #                 IdArticulo_input.select_range(0, tk.END)
    #                 IdArticulo_input.focus()
    #                 nombre_combo.current(0)
    #
    #
    #
    #     else:
    #         DevolucionesVent.focus()
    #         IdArticulo_input.delete(0, tk.END)
    #         IdArticulo_input.select_range(0, tk.END)
    #         IdArticulo_input.focus()

    # def BuscarNombre():
    #     indice = articulosListado[0].index(nombreVar.get())
    #     listaCodigosAux = articulosListado[1]
    #     codigoAbuscar = listaCodigosAux[indice]
    #     codigoBarrasVar.set(codigoAbuscar)
    #     sqlbusqueda = 'SELECT * FROM articulos WHERE nombre = ' + str()
    #     cur.execute(sqlbusqueda)
    #     Resultado = cur.fetchall()
    #
    #     if len(Resultado) > 0:
    #         protupla = []
    #         for ind in Resultado:
    #             for i in range(1, len(ind)):
    #                 protupla.append(ind[i])
    #             ArticuloEncontrado = Articulos.Articulos(tuple(protupla))
    #             ArticuloEncontrado.idArticulos = ind[0]
    #     llenarcampos(ArticuloEncontrado)
#### FUNCIONES BOTONES
    def cargaDevolucion():
        if IdArticulo_input.get() == '':
            messagebox.showerror(f'Carga de Devoluciones',
                                 'No ha seleccionado ningun articulo o no ha ingresado codigo de barras.')
            DevolucionesVent.focus()
        else:
            articuloEncontrado = EncontrarArticulo()
            articuloAdevolver = (articuloEncontrado.idArticulos,fechaVar.get(),cantidadVar.get(),'Devuelto',motivoVar.get(),descripcionVar.get())
            articuloDevolver = ArticulosDevolucion.ArticulosDevolucion(articuloAdevolver)
            if opcion == 'Devolucion':
                articuloDevolver.CargarDevolucionArticulo()

                # if messagebox.askquestion(f'Carga de Stock del Articulo {articuloStockCarga.nombre}',
                #                           f'Esta seguro de cargar el Stock Inicial del articulo?') == 'yes':
                #     articuloStockCarga.aumentarStock(cantidadVar.get())
                #     dbPk.commit()
                #     stockVar.set(articuloStockCarga.stock)
                #     articuloStockCarga.modificaArticulo(articuloStockCarga.idArticulos)
                #     dbPk.commit()
                #     cantidadVar.set(0)
                #     DevolucionesVent.focus()
                # else:
                #     cantidadVar.set(0)
                #     DevolucionesVent.focus()
            else:
                if messagebox.askquestion(f'Carga de Stock del Articulo {articuloStockCarga.nombre}',
                                          f'Esta seguro de aumentar el Stock del articulo?') == 'yes':
                    articuloStockCarga.aumentarStock(cantidadVar.get())
                    dbPk.commit()
                    stockVar.set(articuloStockCarga.stock)
                    cantidadVar.set(0)
                    DevolucionesVent.focus()
                else:
                    cantidadVar.set(0)
                    DevolucionesVent.focus()

    def BajaStock():
        if IdArticulo_input.get() != '':
            articuloStockBaja = EncontrarArticulo()
            if cantidadVar.get() > articuloStockBaja.stock:
                if messagebox.askquestion(f'Baja de Stock del Articulo {articuloStockBaja.nombre}',
                                          f'La cantidad a dar de '
                                          f'Baja es mayor que el stock Actual '
                                          f'{articuloStockBaja.stock}\n'
                                          f'\n'
                                          f'Desea modificar la cantidad por una menor?') == 'yes':
                    cantidadVar.set(articuloStockBaja.stock)
                    cantidad_input.focus()
                    DevolucionesVent.focus()
                else:
                    cantidadVar.set(0)
                    DevolucionesVent.focus()
            else:
                # ir a ventana de devoluciones o bajas
                pass
        else:
            messagebox.showerror(f'Carga de Articulos',
                                 'No ha seleccionado ningun articulo o no ha ingresado codigo de barras.')
            DevolucionesVent.focus()

    def actualizacionStock():
        if IdArticulo_input.get() != '':
            articulosActualizacion = EncontrarArticulo()
            if stockMaxVar.get() < 0:
                stockMaxVar.set(0)
            if stockMinVar.get() < 0:
                stockMinVar.set(0)
            articulosActualizacion.stockMin = stockMinVar.get()
            articulosActualizacion.stockMax = stockMaxVar.get()
            articulosActualizacion.modificaArticulo(articulosActualizacion.idArticulos)
            if messagebox.askquestion(
                    f'Actualizacion de Stock Minimo y/o Maximo del Articulo {articulosActualizacion.nombre}',
                    f'Actualizacion de stock Minimo y Maximo EXITOSA\n'
                    f'\n'
                    f'Desea Actualizar otro Articulo?') == 'yes':
                nombre_combo.current(0)
                stockMaxVar.set(0)
                stockMinVar.set(0)
                DevolucionesVent.focus()
            else:
                DevolucionesVent.destroy()
        else:
            messagebox.showerror(f'Carga de Articulos',
                                 'No ha seleccionado ningun articulo o no ha ingresado codigo de barras.')
            DevolucionesVent.focus()

    ####VENTANA ARTICULOS
    DevolucionesVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idClienteVent = ClienteVent.winfo_id()
    DevolucionesVent.title('Tech-Hard - Devolucion de Articulos')  # pone titulo a la ventana principal
    DevolucionesVent.geometry('500x600')  # Tamaño en pixcel de la ventana
    DevolucionesVent.iconbitmap('imagenHT.ico')  # icono
    DevolucionesVent.minsize(500, 600)
    DevolucionesVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar

    framecampoStock = tk.Frame(DevolucionesVent)
    framecampoStock.config(width=500, height=600)
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

    id_ArticuloVar = tk.IntVar()
    nombreVar = tk.StringVar()
    fechaVar = tk.StringVar()
    cantidadVar = tk.IntVar()
    estadoVar = tk.StringVar()
    motivoVar = tk.StringVar()
    descripcionVar = tk.StringVar()
   

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
    # label/entry/botones

    IdArticulo_label = tk.Label(framecampoStock, text='Id_Articulo')
    config_label(IdArticulo_label, 3)
    IdArticulo_label.pack_forget()

    IdArticulo_input = tk.Entry(framecampoStock, width=20, justify=tk.RIGHT, textvariable=id_ArticuloVar)
    IdArticulo_input.grid(row=3, column=51, padx=10, pady=10, sticky='w')
    IdArticulo_input.config(state='disabled')
    IdArticulo_input.pack_forget() #oculto el Id

    nombre_label = tk.Label(framecampoStock, text='Nombre')
    config_label(nombre_label, 4)
    if nombreVar != '':
        nombre_combo = tk.Entry(framecampoStock,width=30, justify=tk.RIGHT, textvariable=nombreVar)
    else:
        articulosListado = listarcombo('Articulos', 'Detalle')
        nombre_combo = ttk.Combobox(framecampoStock, width=30, state='readonly', textvariable=nombreVar,
                                values=articulosListado[0])
        nombre_combo.bind('<<ComboboxSelected>>', llenarCamposEvento)  # llenar campos de stock
    nombre_combo.grid(row=4, column=51, padx=10, pady=10, sticky='w')


    fecha_label = tk.Label(framecampoStock, text='Fecha')
    config_label(fecha_label, 5)
    fecha_input = tk.Entry(framecampoStock, width=20, justify=tk.RIGHT, textvariable=fechaVar)
    fecha_input.grid(row=5, column=51, padx=10, pady=10, sticky='w')

    cantidad_label = tk.Label(framecampoStock, text='Cantidad')
    config_label(cantidad_label, 5)
    cantidad_input = tk.Entry(framecampoStock, width=20, justify=tk.RIGHT, textvariable=cantidadVar)
    cantidad_input.grid(row=5, column=51, padx=10, pady=10, sticky='w')

    # estado_label = tk.Label(framecampoStock, text='Estado')
    # config_label(estado_label, 14)
    # estado_radioboton = tk.Radiobutton(framecampoStock, justify=tk.RIGHT, textvariable=estadoVar)
    # estado_radioboton.grid(row=14, column=51, padx=10, pady=10, sticky='w')

    motivo_label = tk.Label(framecampoStock, text='Motivo')
    config_label(motivo_label, 6)
    motivos = ['Roto','Vencido','Otro']
    motivo_combo = ttk.Combobox(framecampoStock, width=30, state='readonly', textvariable=motivoVar,
                                values=motivos)
    motivo_combo.grid(row=6, column=51, padx=10, pady=10, sticky='w')

    descripcion_label = tk.Label(framecampoStock, text='Descripcion')
    config_label(descripcion_label, 7)
    descripcion_input = scrolledtext.ScrolledText(framecampoStock, width=30, height=10, wrap=tk.WORD)
    descripcion_input.grid(row=7, column=51, padx=10, pady=10, sticky='w')
    # descripcion_input.grid(tk.INSERT,'Texto a ingresar') #para insertar texto

    ##### FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesArticulos = tk.Frame(DevolucionesVent)
    framebotonesArticulos.pack()

    boton_Alta = tk.Button(framebotonesArticulos, text='Cargar Devolucion', command=cargaDevolucion())
    boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)

    boton_Buscar = tk.Button(framebotonesArticulos, text='Buscar', command=buscarNombre)
    boton_Buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesArticulos, text='Actualizar Devolucion')
    boton_Actualizar.grid(row=0, column=3, padx=5, pady=10, ipadx=7)

    # boton_Eliminar = tk.Button(framebotonesArticulos, text='Eliminar', command=BajaStock)
    # boton_Eliminar.grid(row=0, column=4, padx=5, pady=10, ipadx=7)

    if opcion == 'StockInicial':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        boton_Buscar.bind('<Return>', buscarCodigoBarrasEnter)
        limpiarCampos()

        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        IdArticulo_input.config(state='normal')
        IdArticulo_input.select_range(0, tk.END)
        IdArticulo_input.focus()

    elif opcion == 'Devolucion':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
        boton_Alta.config(state='normal')
        motivo_combo.current(0)
        motivo_combo.focus()
        if len(args) > 0:
            idArticulo = args[0]
            nombre = args[1]
            cantidad = args[2]

        id_ArticuloVar.set(idArticulo)
        nombreVar.set(nombre)
        cantidadVar.set(cantidad)
        motivo_combo.config(state='normal')
        motivo_combo.current(0)

    elif opcion == 'Baja':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
        boton_Eliminar.config(state='normal')
        IdArticulo_input.config(state='normal')
        IdArticulo_input.select_range(0, tk.END)
        IdArticulo_input.focus()
        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        cantidad_input.config(state='normal')
        cantidad_input.select_range(0, tk.END)
        cantidad_input.focus()

    elif opcion == 'Modificacion':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        boton_Actualizar.config(state='normal')
        limpiarCampos()
        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        IdArticulo_input.config(state='normal')
        IdArticulo_input.select_range(0, tk.END)
        IdArticulo_input.focus()

    elif opcion == 'BuscarCodigoBarras':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
        IdArticulo_input.config(state='normal')
        IdArticulo_input.select_range(0, tk.END)
        IdArticulo_input.focus()

    elif opcion == 'BuscarNombre':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal', command=BuscarNombre)  # cambiar comman para buscar por nombre armar funcion
        limpiarCampos()
        nombre_combo.config(state='normal')
        nombre_combo.current(0)
        nombre_combo.select_range(0, tk.END)
    

