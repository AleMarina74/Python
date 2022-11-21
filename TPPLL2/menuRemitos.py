#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import tkinter

import Articulos
import VentanaGrilla
import mariadb
import datetime
import FuncionesMenu
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Remitos

dbPk = mariadb.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='Pk',
    autocommit=True
)
cur = dbPk.cursor()

Remitos_Campos = ('Fecha', 'id_Proveedor', 'id_Articulo', 'cantidad', 'estado', 'nro_Remito', 'Total_Remito',
                  'Motivo')  # 'id_Remito', autoincremental
CamposInt = (1, 2, 3, 5)
CamposFloat = (6,)
CamposChar = (4, 7)
CamposDate = (0,)
FechaActual = datetime.date.today()
FechaHoy = datetime.date.today().strftime('%d-%m-%Y')
Remitos_columnasItems = ('NombreArticulo', 'Cantidad')
lenRemitosItems = (50, 10)


# ---- MENU REMITOS
def menuRemitos(opcion):
    def limpiarvar():
        idRemitoVar.set(0)
        fechaVar.set(FechaActual)
        cantidadVar.set(0)
        remitoVar.set(0)
        subtotalVar.set(0)
        costoVar.set('')

    def componenteshabilitarRemito(valor):  # Valores 'disabled' o 'normal'
        # if valor == 'normal' and opcion == 'Remitos':
        #     estado_combo.current(1)
        # else:
        #     estado_combo.config(state=valor)
        boton_Actualizar.config(state=valor)
        numeroRemito_input.config(state=valor)
        cantidad_input.config(state=valor)
        motivo_input.config(state=valor)

    def deshabilitarbotones(valor):
        boton_Alta.config(state=valor)
        boton_CargarArticulo.config(state=valor)
        boton_FinalizarRemito.config(state=valor)
        # boton_Buscar.config(state=valor)
        boton_Actualizar.config(state=valor)
        boton_Eliminar.config(state=valor)

    def limpiarCampos():
        cantidad_input.delete(0, tk.END)

        fecha_input.delete(0, tk.END)

        numeroRemito_input.delete(0, tk.END)
        subtotal_input.delete(0, tk.END)
        motivo_input.delete(0, tk.END)

    def nuevoRemito():
        limpiarvar()
        limpiarCampos()
        ultimoPed = buscarultimoRemito()
        nuevoRemito = ultimoPed + 1
        valores = tk.Listbox(idRemito_combo["values"])
        idRemito_combo["values"] = values + [nuevoRemito]
        idRemito_combo.set(nuevoRemito)

###EVENTOS
    def remitoNumeroEvento(event):
        numeroRemito_input.config(state='disabled')
        boton_CargarArticulo.config(state='normal')
        proveedores_combo.focus()

    def elegirProveedor(event):
        articulosprov = listarArticulosPorProveedor()
        articuloElegidoVar.set('')
        articulos_combo['values'] = articulosprov

        if len(articulosprov) > 0:
            articulos_combo.current(0)

        cantidad_input.config(state='normal')
        boton_CargarArticulo.config(state='normal')
        boton_FinalizarRemito.config(state='normal')
        articulos_combo.config(state='normal')

        articulos_combo.focus()

    def elegirNroRemito(event):
        RemitosEncontrados = buscarItemsRemitos()
        if len(RemitosEncontrados) > 0:
            for item in RemitosEncontrados:
                articuloEncontradoEleccion = buscarArticulo(item[4])
                itemMostrar = (articuloEncontradoEleccion.nombre, item[5])
                listaDeItemsRemito.append(itemMostrar)
                listaDelRemitos.append(item)
                articulosDelRemitoNombre.append(articuloEncontradoEleccion.nombre)
            registroAux = listaDelRemitos[0]
            idProveedor = registroAux[3]
            proveedor = buscarProveedorPorId(idProveedor)
            proveedorVar.set(proveedor)
            VentanaGrilla.grillaFrame('Cargar', Remitos_columnasItems, lenRemitosItems, listaDeItemsRemito,
                                      frameItemsRemito)
            proveedores_combo['values'] = proveedor
            proveedores_combo.config(state='disabled')
            articulos_combo['values'] = articulosDelRemitoNombre
            articulos_combo.current(0)
            articulos_combo.focus()

    def cargarItemEnterCantidad(event):
        if cantidadVar.get() == 0:
            for item in listaDelRemitos:
                if item[3] == idArticulo:
                    messagebox.showwarning(f'Carga de Remito', f'El item ya ha sido cargado.')
                    RemitosVent.focus()
                    # despues preguntaria si quiere eliminar el item
            cantidad_input.focus()
        else:
            agregarArticulo()

    ###FUNCIONES DE BUSQUEDA DE DATOS
    def listarArticulosPorProveedor():
        idprovencontrado = buscarProveedorPorRazonSocial()
        listaArticuloProveedor = 'SELECT * FROM articulos WHERE id_Proveedor = ' + str(idprovencontrado)
        cur.execute(listaArticuloProveedor)
        resultado = cur.fetchall()
        selArticulo = []
        if len(resultado) > 0:
            for ind in resultado:
                selArticulo.append(ind[2])
        return selArticulo

    def buscarProveedorPorRazonSocial():
        proveedorabuscar = 'SELECT id_proveedor FROM proveedores WHERE RazonSocial=\"' + proveedorVar.get() + '\"'
        cur.execute(proveedorabuscar)
        resultado = cur.fetchall()
        for ind in resultado:
            idprov = ind[0]
        return idprov

    def buscarProveedorPorId(id):
        proveedorBuscado = 'SELECT * FROM proveedores WHERE id_Proveedor=' + str(id)
        cur.execute(proveedorBuscado)
        resultado = cur.fetchall()
        for ind in resultado:
            nomresultado = ind[2]
        return nomresultado

    def listarcombo(tabla, campo):
        if tabla.upper() == 'RemitoS':
            if campo != '':
                buscarcombo = 'SELECT * FROM ' + tabla + ' GROUP BY ' + campo
        elif campo != '':
            idprovencontrado = buscarProveedorPorRazonSocial()
            buscarcombo = 'SELECT * FROM ' + tabla + ' WHERE id_Proveedor = ' + idprovencontrado
        else:
            buscarcombo = 'SELECT * FROM ' + tabla
        cur.execute(buscarcombo)
        resultado = cur.fetchall()
        listadelcombo = []
        id_campo = []
        if len(resultado) < 0:
            messagebox.showwarning(f'LISTADO DE {tabla.upper()}',
                                   f'No tiene ningun dato cargado en la tabla {tabla.upper()}')
            RemitosVent.focus()
        else:
            for ind in resultado:
                if tabla.upper() == 'PROVEEDORES':
                    listadelcombo.append(ind[2])
                    id_campo.append(ind[0])

                elif tabla.upper() == 'RUBROS':
                    listadelcombo.append(ind[1])
                    id_campo.append(ind[0])

                elif tabla.upper() == 'ARTICULOS':
                    listadelcombo.append(ind[2])
                    id_campo.append(ind[0])

                elif tabla.upper() == 'RemitoS':
                    listadelcombo.append(ind[1])
                    id_campo.append(ind[0])

        return listadelcombo

    def RemitosPendientes():
        RemitosPendientes = 'Select * From Remitos WHERE estado = \" PENDIENTE \" GROUP BY id_Proveedor'
        cur.execute(RemitosPendientes)
        resultadoRemitosPendientes = cur.fetchall()
        if len(resultadoRemitosPendientes) < 1:
            messagebox.showwarning('RemitoS PENDIENTES', f'No hay Remitos PENDIENTES')
            RemitosVent.destroy()
        else:

            idRemitoLista = []
            for reg in resultadoRemitosPendientes:
                idRemitoLista.append(reg[0])

            listaRemitoSet = set(idRemitoLista)
            listaRemito = list(listaRemitoSet)
            idRemito_combo['values'] = listaRemito
            idRemito_combo.current(0)
            return resultadoRemitosPendientes

    def buscarItemsRemitos():
        RemitoBusca = 'SELECT * FROM Remitos WHERE nroRemito = ' + str(idRemito_combo.get())
        cur.execute(RemitoBusca)
        resultado = cur.fetchall()
        if len(resultado) < 1:
            resultado = []
        return resultado

    def cargarRetmito():
        RemitosPendientes = RemitosPendientes()

    def buscarProveedor():
        if opcion == 'Alta':
            articulosprov = listarArticulosPorProveedor()
            articulos_combo[values] = ttk.Combobox(framecampoRemito, state='readonly', width=40,
                                                   values=articulosprov)  # ya que solo puede seleccionar los proveedores
            articulos_combo.grid(row=6, column=51, padx=10, pady=10, sticky='w')
            if len(articulos) > 0:
                if len(articulosprov) > 0:
                    articulos_combo.current(0)
                articulos_combo.focus()
                cantidad_input.config(state='normal')
                boton_CargarArticulo.config(state='normal')
                boton_FinalizarRemito.config(state='normal')

                return articulosprov
            else:
                messagebox.showwarning('BUSCAR ARTICULOS POR PROVEEDOR', 'El proveedor no tiene articulos cargados\n'
                                                                         'Elija otro proveedor')
                proveedores_combo.focus()

        else:
            listProveedores = 'SELECT * FROM proveedores'
            cur.execute(listProveedores)
            resultado = cur.fetchall()
            selProveedor = []
            if len(resultado) > 0:
                for ind in resultado:
                    selProveedor.append((ind[0], ind[2]))
            return selProveedor

    # def listarArticulos():
    #     listArticulo = 'SELECT * FROM articulos'
    #     cur.execute(listArticulo)
    #     resultado = cur.fetchall()
    #     selArticulos = []
    #     if len(resultado) > 0:
    #         for ind in resultado:
    #             selArticulos.append((ind[0],ind[2]))
    #     return selArticulos

    def buscarArticuloPorNombre():
        articulobuscar = 'SELECT id_articulo FROM articulos WHERE nombre=\"' + articulos_combo.get() + '\"'
        cur.execute(articulobuscar)
        resultado = cur.fetchall()
        for ind in resultado:
            idart = ind[0]
        return idart

    def buscarultimoRemito():
        # ultRemito = 'SELECT * FROM Remitos ORDER BY id_Remito desc'
        ultRemito = 'SELECT MAX(NroRemito) from Remitos'
        cur.execute(ultRemito)
        resultado = cur.fetchone()
        if len(resultado) < 1:
            ultimo = 0
        else:
            ultimo = resultado[0]
        return ultimo

    def encontrarItemRemito(id):
        sqlbusqueda = 'SELECT * FROM Remitos WHERE id_Remito = ' + str(id)
        cur.execute(sqlbusqueda)
        Resultado = cur.fetchall()

        if len(Resultado) > 0:
            for ind in Resultado:
                RemitoTupla = []
                for i in range(1, len(ind)):
                    RemitoTupla.append(ind[i])
                RemitoEncontrado = Remitos.Remitos(tuple(RemitoTupla))

        return RemitoEncontrado

    ###FUNCIONES DE CARGA DE ITEMS Y RemitoS
    def agregarArticulo():
        proveedores_combo.config(state='disabled')

        idRemito = buscarultimoRemito() + 1
        idProveedor = buscarProveedorPorRazonSocial()  # (buscar id_proveedor) de la opcion que haya seleccionado el proveedor
        idArticulo = buscarArticuloPorNombre()  # (buscar id del articulo seleccionado
        if cantidadVar.get() < 1:
            messagebox.showwarning(f'Carga de Remito', f'Debe ingresar una Cantidad superior a 0.')
            RemitosVent.focus()
            cantidad_input.select_range(0, tk.END)
            cantidad_input.focus()
        else:
            cantidad = cantidadVar.get()


            Seguir = True
            if len(listaDelRemitos) < 1:
                Seguir = True
            else:
                for item in listaDelRemitos:
                    if item[3] == idArticulo:
                        messagebox.showwarning(f'Carga de Remito', f'El item ya ha sido cargado.\n')
                        RemitosVent.focus()
                        articuloElegidoVar.set('')
                        articulos_combo.current(0)
                        articulos_combo.focus()
                        Seguir = False
            if Seguir:
                articuloRemito = [idRemito, FechaActual, idProveedor, idArticulo, cantidad, estado, 0, 0, 'Nuevo']
                itemMostrar = (articuloElegidoVar.get(), cantidadVar.get())  # lista de tuplas

                listaDelRemitos.append(articuloRemito)  # lista de listas

                if len(listaDeItemsRemito) > 0:  # lista de items
                    listaDeItemsRemito.append(itemMostrar)
                    VentanaGrilla.grillaFrame('Agregar', Remitos_columnasItems, lenRemitosItems,
                                              [(articuloElegidoVar.get(), cantidadVar.get(),), ], frameItemsRemito)
                else:
                    listaDeItemsRemito.append(itemMostrar)
                    VentanaGrilla.grillaFrame('Nuevo', Remitos_columnasItems, lenRemitosItems,
                                              [(articuloElegidoVar.get(), cantidadVar.get(),), ], frameItemsRemito)
                # articuloElegidoVar.set('')
                articulos_combo.current(0)
                articulos_combo.focus()
            else:
                RemitosVent.focus()
                # articuloElegidoVar.set('')
                articulos_combo.focus()

    def finalizarRemito():
        if messagebox.askquestion(f'Remito al Proveedor {proveedorVar.get()}',
                                  f'Desea finalizar el Remito con los items'
                                  f'cargados?') == 'yes':
            if len(listaDelRemitos) > 0:
                for reg in listaDelRemitos:
                    articuloAcargar = Remitos.Remitos(reg)
                    articuloAcargar.altaRemitos()

            if messagebox.askquestion(f'Remito al Proveedor {proveedorVar.get()}', f'Carga de Remito EXITOSA\n'
                                                                                   f'\n'
                                                                                   f'Desea cargar un Nuevo Remito?') == 'yes':
                RemitosVent.destroy()
                menuRemitos('Alta')
            else:
                RemitosVent.destroy()

        else:
            messagebox.showwarning(f'Remito al Proveedor {proveedorVar.get()}', 'Remito CANCELADO')
            RemitosVent.destroy()

    def modificarRemito():
        pedEncontrado = encontrarRemito()
        if len(pedEncontrado) > 1:
            pedEncontrado.modificarRemitos(idRemito_combo.get())
            # encontarArt = buscarArticulo()
            ArtEncontrado = Articulos.Articulos(tuple(encontarArt))
            ArtEncontrado.aumentarStock(cantidadVar.get())
            dbPk.commit()
            messagebox.showinfo('MODIFICACION RemitoS', 'Registro Modificado')

        limpiarvar()
        limpiarCampos()

    def buscarArticulo(id):
        buscaart = 'SELECT * FROM articulos WHERE id_articulo = ' + str(id)
        cur.execute(buscaart)
        resultado = cur.fetchall()
        for ind in resultado:
            articulo = []
            for i in range(1, len(ind)):
                articulo.append(ind[i])

            articuloEncontradoPorId = Articulos.Articulos(tuple(articulo))
            articuloEncontradoPorId._idArticulos = id
        return articuloEncontradoPorId

    # def listarcombo(tabla, campo):
    #     if tabla.upper() == 'RemitoS':
    #         if campo != '':
    #             buscarcombo = 'SELECT * FROM ' + tabla + ' GROUP BY ' + campo
    #     else:
    #         buscarcombo = 'SELECT * FROM ' + tabla
    #     cur.execute(buscarcombo)
    #     resultado = cur.fetchall()
    #     listadelcombo = []
    #     if len(resultado) < 0:
    #         messagebox.showwarning(f'LISTADO DE {tabla.upper()}',
    #                                f'No tiene ningun dato cargado en la tabla {tabla.upper()}')
    #         RemitosVent.focus()
    #     else:
    #         for ind in resultado:
    #             if tabla.upper() == 'PROVEEDORES':
    #                 listadelcombo.append(ind[2])
    #
    #             elif tabla.upper() == 'ARTICULOS':
    #                 listadelcombo.append(ind[2])
    #
    #             elif tabla.upper() == 'RemitoS':
    #                 listadelcombo.append(ind[1])
    #
    #     return listadelcombo

    def eliminarRemito():

        RemitoElim = encontrarRemito()
        if messagebox.askquestion('Eliminar Registro', f'Esta seguro de dar de baja al Remito?\n '
                                                       f'Numero: {RemitoElim.idRemito} \n'
                                                       f'Proveedor: {proveedores_combo.get()}') == 'yes':
            RemitoElim.borrarRemitos(RemitoElim.idRemito)
            dbPk.commit()

        else:
            messagebox.showwarning('Eliminar Registro', f'No se ha eliminado el registro')
        del RemitoElim
        limpiarvar()
        RemitosVent.destroy()

    # VENTANA REMITOS
    RemitosVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idRemitoVarsVent = RemitosVent.winfo_id()
    RemitosVent.title('Tech-Hard - Remitos de Proveedores')  # pone titulo a la ventana principal
    RemitosVent.geometry('600x700')  # Tamaño en pixcel de la ventana
    RemitosVent.iconbitmap('imagenHT.ico')  # icono
    RemitosVent.minsize(600, 700)
    RemitosVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar

    framecampoRemito = tk.Frame(RemitosVent)
    # framecampoRemito.pack(fill='both')
    # framecampoRemito.config(bg='lightblue')
    framecampoRemito.config(width=600, height=400)
    framecampoRemito.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoRemito.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoRemito.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoRemito.pack(anchor=SE) # lo ubica abajo a la derecha
    framecampoRemito.pack(fill='x')  # ancho como el padre
    framecampoRemito.pack(fill='y')  # alto igual que el padre
    framecampoRemito.pack(fill='both')  # ambas opciones
    framecampoRemito.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    # idcliente = tk.IntVar()
    def config_label(mi_label, fila):
        espaciado_labels = {'column': 50, 'sticky': 'e', 'padx': 10, 'pady': 10}
        # color_labels ={'bg':color_fondo, 'fg':color_letra,'font':fuente}
        mi_label.grid(row=fila, **espaciado_labels)
        # mi_label.config(**color_labels)

    idRemitoVar = tk.IntVar()
    fechaVar = tkinter.StringVar()
    cantidadVar = tk.IntVar()
    proveedorVar = tk.StringVar()
    articuloElegidoVar = tk.StringVar()
    remitoVar = tk.IntVar()
    subtotalVar = tk.DoubleVar()
    costoVar = tk.DoubleVar()

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
#### label/entry/botones
    numeroRemito_label = tk.Label(framecampoRemito, text='Numero Remito')
    config_label(numeroRemito_label,3)
    numeroRemito_input = tk.Entry(framecampoRemito, textvariable=remitoVar, width=40, justify=tk.RIGHT)
    numeroRemito_input.grid(row=3, column=51, padx=10, pady=10, sticky='w')
    numeroRemito_input.config(state='normal')
    numeroRemito_input.bind('<Return>',remitoNumeroEvento)

    fecha_label = tk.Label(framecampoRemito, text='fecha')
    config_label(fecha_label, 4)
    fecha_input = tk.Entry(framecampoRemito, textvariable=fechaVar, width=20, justify=tk.RIGHT)
    fecha_input.grid(row=4, column=51, padx=10, pady=10, sticky='w')
    Fechahoystr = f'{FechaActual.year}-{FechaActual.month}-{FechaActual.day}'
    fechaVar.set(Fechahoystr)
    fecha_input.config(state='disabled')

    proveedores_label = tk.Label(framecampoRemito, text='Proveedor')
    config_label(proveedores_label, 5)
    proveedores = listarcombo('Proveedores', '')
    proveedores_combo = ttk.Combobox(framecampoRemito, state='readonly', textvariable=proveedorVar, width=40,
                                     values=proveedores)  # ya que solo puede seleccionar los proveedores
    proveedores_combo.grid(row=5, column=51, padx=10, pady=10, sticky='w')
    proveedores_combo.current(0)
    proveedores_combo.bind('<<ComboboxSelected>>', elegirProveedor)

    articulos_label = tk.Label(framecampoRemito, text='Articulo')
    config_label(articulos_label, 6)
    articulos = listarcombo('Articulos', '')
    articulos_combo = ttk.Combobox(framecampoRemito, state='readonly', textvariable=articuloElegidoVar, width=40,
                                   values=articulos)  # ya que solo puede seleccionar los proveedores
    articulos_combo.grid(row=6, column=51, padx=10, pady=10, sticky='w')
    if len(articulos) > 0:
        articulos_combo.current(0)

    cantidad_label = tk.Label(framecampoRemito, text='Cantidad')
    config_label(cantidad_label, 7)
    cantidad_input = tk.Entry(framecampoRemito, textvariable=cantidadVar, width=20, justify=tk.RIGHT)
    cantidad_input.grid(row=7, column=51, padx=10, pady=10, sticky='w')
    cantidad_input.bind('<Return>', cargarItemEnterCantidad)

    # estado_label = tk.Label(framecampoRemito, text='Estado')
    # config_label(estado_label, 8)
    # estado_combo = ttk.Combobox(framecampoRemito, state='readonly', width=30,
    #                             values=['PENDIENTE', 'COMPLETADO'])  # ya que solo puede seleccionar los proveedores
    # estado_combo.grid(row=8, column=51, padx=10, pady=10, sticky='w')
    # estado_combo.current(0)
    # estado_combo.config(state='disabled')

    costo_label = tk.Label(framecampoRemito, text='Costo')
    config_label(costo_label, 8)
    costo_input = tk.Entry(framecampoRemito, textvariable=costoVar, width=20, justify=tk.RIGHT)
    costo_input.grid(row=8, column=51, padx=10, pady=10, sticky='w')

    subtotal_label = tk.Label(framecampoRemito, text='Subtotal Remito')
    config_label(subtotal_label, 10)
    subtotal_input = tk.Entry(framecampoRemito, textvariable=subtotalVar, width=30, justify=tk.RIGHT)
    subtotal_input.grid(row=10, column=51, padx=10, pady=10, sticky='w')
    subtotal_input.config(state='disabled')

####frame grilla
    frameItemsRemito = tk.Frame(RemitosVent)
    frameItemsRemito.config(width=600, height=150)
    frameItemsRemito.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    frameItemsRemito.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    frameItemsRemito.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoRemito.pack(anchor=SE) # lo ubica abajo a la derecha
    frameItemsRemito.pack(fill='x')  # ancho como el padre
    frameItemsRemito.pack(fill='y')  # alto igual que el padre
    frameItemsRemito.pack(fill='both')  # ambas opciones
    frameItemsRemito.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    # VentanaGrilla.Scrollbar_Example(RemitosVent)

    # FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesRemito = tk.Frame(RemitosVent)
    framebotonesRemito.pack()

    boton_Alta = tk.Button(framebotonesRemito, text='Nuevo Remito')
    boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)

    boton_CargarArticulo = tk.Button(framebotonesRemito, text='Cargar Articulo', command=agregarArticulo)
    boton_CargarArticulo.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_FinalizarRemito = tk.Button(framebotonesRemito, text='Finalizar Remito', command=finalizarRemito)
    boton_FinalizarRemito.grid(row=0, column=3, padx=5, pady=10, ipadx=7)

    # boton_Buscar = tk.Button(framebotonesRemito, text='Buscar Pendientes')
    # boton_Buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesRemito, text='Actualizar', command=modificarRemito)
    boton_Actualizar.grid(row=0, column=4, padx=5, pady=10, ipadx=7)

    boton_Eliminar = tk.Button(framebotonesRemito, text='Eliminar', command=eliminarRemito)
    boton_Eliminar.grid(row=0, column=5, padx=5, pady=10, ipadx=7)

    if opcion == 'Alta':
        listaDeItemsRemito = []
        listaDelRemitos = []
        # idRemito_combo.config(state='disabled')
        fecha_input.config(state='disabled')

        # boton_buscarProveedor.config(state='normal')
        # boton_buscarArticulo.config(state='disabled')
        deshabilitarbotones('disabled')
        componenteshabilitarRemito('disabled')
        limpiarCampos()

        articulos_combo.config(state='disabled')

        numeroRemito_input.focus()

    elif opcion == 'Baja':
        listaDeItemsRemito = []
        listaDelRemitos = []
        articulosDelRemitoNombre = []
        listarcombo('Remitos', 'nroRemito')
        # boton_BuscaridRemito.config(state='normal')
        fecha_input.config(state='disabled')
        # boton_buscarProveedor.config(state='disabled')
        # boton_buscarArticulo.config(state='disabled')
        deshabilitarbotones('disabled')
        componenteshabilitarRemito('disabled')
        limpiarCampos()
        idRemito_combo.config(state='normal')
        boton_Eliminar.config(state='normal')
        idRemito_combo.focus()

    elif opcion == 'Modificacion':
        listarcombo('Remitos', 'id_Remito')
        idRemito_combo.config(state='normal')
        # boton_BuscaridRemito.config(state='normal')
        idRemito_combo.focus()

        fecha_input.config(state='disabled')
        # boton_buscarProveedor.config(state='disabled')
        # boton_buscarArticulo.config(state='disabled')
        deshabilitarbotones('disabled')
        componenteshabilitarRemito('disabled')
        limpiarCampos()
        boton_Actualizar.config(state='normal')