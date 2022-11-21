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
import Pedidos


dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit=True
)
cur = dbPk.cursor()

Pedidos_Campos = ('Fecha','id_Proveedor','id_Articulo','cantidad','estado','nro_Remito','Total_Remito','Motivo') #'id_Pedido', autoincremental
CamposInt = (1,2,3,5)
CamposFloat = (6,)
CamposChar = (4,7)
CamposDate = (0,)
FechaActual = datetime.date.today()
FechaHoy = datetime.date.today().strftime('%d-%m-%Y')
Pedidos_columnasItems = ('NombreArticulo','Cantidad')
lenPedidosItems = (50,10)

# ---- MENU PEDIDOS
def menuPedidos(opcion):
    def limpiarvar():
        idPedidoVar.set(0)
        fechaVar.set(FechaActual)
        cantidadVar.set(0)
        remitoVar.set(0)
        subtotalVar.set(0)
        motivoVar.set('')

    def componenteshabilitarRemito(valor):  # Valores 'disabled' o 'normal'
        if valor == 'normal' and opcion == 'Remitos':
            estado_combo.current(1)
        else:
            estado_combo.config(state=valor)
        boton_Actualizar.config(state=valor)
        numeroRemito_input.config(state=valor)
        cantidad_input.config(state=valor)
        motivo_input.config(state=valor)


    def deshabilitarbotones(valor):
        boton_Alta.config(state=valor)
        boton_CargarArticulo.config(state=valor)
        boton_FinalizarPedido.config(state=valor)
        # boton_Buscar.config(state=valor)
        boton_Actualizar.config(state=valor)
        boton_Eliminar.config(state=valor)


    def limpiarCampos():
        cantidad_input.delete(0, tk.END)

        fecha_input.delete(0, tk.END)

        numeroRemito_input.delete(0, tk.END)
        subtotal_input.delete(0, tk.END)
        motivo_input.delete(0, tk.END)

    def nuevoPedido():
        limpiarvar()
        limpiarCampos()
        ultimoPed= buscarultimopedido()
        nuevoPedido = ultimoPed + 1
        valores = tk.Listbox(idPedido_combo["values"])
        idPedido_combo["values"] = values + [nuevoPedido]
        idPedido_combo.set(nuevoPedido)

###EVENTOS
    def elegirProveedor(event):
        articulosprov = listarArticulosPorProveedor()
        articuloElegidoVar.set('')
        articulos_combo['values'] = articulosprov

        if len(articulosprov) > 0:
            articulos_combo.current(0)

        cantidad_input.config(state='normal')
        boton_CargarArticulo.config(state='normal')
        boton_FinalizarPedido.config(state='normal')
        articulos_combo.config(state='normal')

        articulos_combo.focus()

    def elegirNroPedido(event):
        pedidosEncontrados = buscarItemsPedidos()
        if len(pedidosEncontrados) > 0:
            for item in pedidosEncontrados:
                articuloEncontradoEleccion = buscarArticulo(item[4])
                itemMostrar = (articuloEncontradoEleccion.nombre,item[5])
                listaDeItemsPedido.append(itemMostrar)
                listaDelPedidos.append(item)
                articulosDelPedidoNombre.append(articuloEncontradoEleccion.nombre)
            registroAux = listaDelPedidos[0]
            idProveedor = registroAux[3]
            proveedor = buscarProveedorPorId(idProveedor)
            proveedorVar.set(proveedor)
            VentanaGrilla.grillaFrame('Cargar',Pedidos_columnasItems,lenPedidosItems,listaDeItemsPedido,frameItemsPedido)
            proveedores_combo['values'] = proveedor
            proveedores_combo.config(state='disabled')
            articulos_combo['values'] = articulosDelPedidoNombre
            articulos_combo.current(0)
            articulos_combo.focus()

    def cargarItemEnterCantidad(event):
        if cantidadVar.get() == 0:
            for item in listaDelPedidos:
                if item[3] == idArticulo:
                    messagebox.showwarning(f'Carga de Pedido',f'El item ya ha sido cargado.')
                    PedidosVent.focus()
                    #despues preguntaria si quiere eliminar el item
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
        proveedorabuscar = 'SELECT id_proveedor FROM proveedores WHERE RazonSocial=\"'+ proveedorVar.get() +'\"'
        cur.execute(proveedorabuscar)
        resultado = cur.fetchall()
        for ind in resultado:
            idprov= ind[0]
        return idprov

    def buscarProveedorPorId(id):
        proveedorBuscado = 'SELECT * FROM proveedores WHERE id_Proveedor='+str(id)
        cur.execute(proveedorBuscado)
        resultado = cur.fetchall()
        for ind in resultado:
            nomresultado = ind[2]
        return nomresultado


    def listarcombo(tabla, campo):
        if tabla.upper() == 'PEDIDOS':
            if campo != '':
                buscarcombo = 'SELECT * FROM ' + tabla + ' GROUP BY ' + campo
        elif campo !='':
            idprovencontrado = buscarProveedorPorRazonSocial()
            buscarcombo = 'SELECT * FROM ' + tabla + ' WHERE id_Proveedor = ' + idprovencontrado
        else:
            buscarcombo = 'SELECT * FROM ' + tabla
        cur.execute(buscarcombo)
        resultado = cur.fetchall()
        listadelcombo = []
        id_campo =[]
        if len(resultado) < 0:
            messagebox.showwarning(f'LISTADO DE {tabla.upper()}',
                                   f'No tiene ningun dato cargado en la tabla {tabla.upper()}')
            PedidosVent.focus()
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

                elif tabla.upper() == 'PEDIDOS':
                    listadelcombo.append(ind[1])
                    id_campo.append(ind[0])

        return listadelcombo

    def pedidosPendientes():
        pedidosPendientes = 'Select * From pedidos WHERE estado = \" PENDIENTE \" GROUP BY id_Proveedor'
        cur.execute(pedidosPendientes)
        resultadoPedidosPendientes = cur.fetchall()
        if len(resultadoPedidosPendientes) < 1:
            messagebox.showwarning('PEDIDOS PENDIENTES', f'No hay pedidos PENDIENTES')
            PedidosVent.destroy()
        else:

            idPedidoLista= []
            for reg in resultadoPedidosPendientes:
                idPedidoLista.append(reg[0])

            listaPedidoSet = set(idPedidoLista)
            listaPedido = list(listaPedidoSet)
            idPedido_combo['values'] = listaPedido
            idPedido_combo.current(0)
            return resultadoPedidosPendientes

    def buscarItemsPedidos():
        pedidoBusca = 'SELECT * FROM pedidos WHERE nroPedido = '+ str(idPedido_combo.get())
        cur.execute(pedidoBusca)
        resultado = cur.fetchall()
        if len(resultado) < 1:
            resultado = []
        return resultado

    def cargarRetmito():
        pedidosPendientes = pedidosPendientes()

    def buscarProveedor():
        if opcion == 'Alta':
            articulosprov = listarArticulosPorProveedor()
            articulos_combo[values] = ttk.Combobox(framecampoPed, state='readonly', width=40,
                                           values=articulosprov)  # ya que solo puede seleccionar los proveedores
            articulos_combo.grid(row=6, column=51, padx=10, pady=10, sticky='w')
            if len(articulos) > 0:
                if len(articulosprov) >0 :
                    articulos_combo.current(0)
                articulos_combo.focus()
                cantidad_input.config(state='normal')
                boton_CargarArticulo.config(state='normal')
                boton_FinalizarPedido.config(state='normal')

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
                    selProveedor.append((ind[0],ind[2]))
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

    def buscarultimopedido():
        # ultpedido = 'SELECT * FROM pedidos ORDER BY id_Pedido desc'
        ultpedido = 'SELECT MAX(NroPedido) from pedidos'
        cur.execute(ultpedido)
        resultado = cur.fetchone()
        if len(resultado) < 1:
            ultimo = 0
        else:
            ultimo = resultado[0]
        return ultimo


    def encontrarItemPedido(id):
        sqlbusqueda = 'SELECT * FROM pedidos WHERE id_pedido = ' + str(id)
        cur.execute(sqlbusqueda)
        Resultado = cur.fetchall()

        if len(Resultado) > 0:
            for ind in Resultado:
                pedidoTupla = []
                for i in range(1, len(ind)):
                    pedidoTupla.append(ind[i])
                pedidoEncontrado = Pedidos.Pedidos(tuple(pedidoTupla))

        return pedidoEncontrado

###FUNCIONES DE CARGA DE ITEMS Y PEDIDOS
    def agregarArticulo():
        proveedores_combo.config(state='disabled')

        idPedido = buscarultimopedido()+1
        idProveedor = buscarProveedorPorRazonSocial() #(buscar id_proveedor) de la opcion que haya seleccionado el proveedor
        idArticulo = buscarArticuloPorNombre() #(buscar id del articulo seleccionado
        if cantidadVar.get() < 1:
            messagebox.showwarning(f'Carga de Pedido', f'Debe ingresar una Cantidad superior a 0.')
            PedidosVent.focus()
            cantidad_input.select_range(0,tk.END)
            cantidad_input.focus()
        else:
            cantidad = cantidadVar.get()
            estado = estado_combo.get() #'PENDIENTE'

            Seguir = True
            if len(listaDelPedidos) < 1:
                Seguir = True
            else:
                for item in listaDelPedidos:
                    if item[3] == idArticulo:
                        messagebox.showwarning(f'Carga de Pedido',f'El item ya ha sido cargado.\n')
                        PedidosVent.focus()
                        articuloElegidoVar.set('')
                        articulos_combo.current(0)
                        articulos_combo.focus()
                        Seguir = False
            if Seguir:
                articuloPedido = [idPedido,FechaActual,idProveedor,idArticulo,cantidad,estado,0,0,'Nuevo']
                itemMostrar = (articuloElegidoVar.get(), cantidadVar.get())  # lista de tuplas

                listaDelPedidos.append(articuloPedido) # lista de listas

                if len(listaDeItemsPedido) > 0: #lista de items
                    listaDeItemsPedido.append(itemMostrar)
                    VentanaGrilla.grillaFrame('Agregar', Pedidos_columnasItems, lenPedidosItems,
                                              [(articuloElegidoVar.get(), cantidadVar.get(),),], frameItemsPedido)
                else:
                    listaDeItemsPedido.append(itemMostrar)
                    VentanaGrilla.grillaFrame('Nuevo', Pedidos_columnasItems, lenPedidosItems,
                                              [(articuloElegidoVar.get(), cantidadVar.get(),),], frameItemsPedido)
                # articuloElegidoVar.set('')
                articulos_combo.current(0)
                articulos_combo.focus()
            else:
                PedidosVent.focus()
                # articuloElegidoVar.set('')
                articulos_combo.focus()

    def finalizarPedido():
        if messagebox.askquestion(f'Pedido al Proveedor {proveedorVar.get()}',f'Desea finalizar el pedido con los items'
                                                                              f'cargados?') == 'yes':
            if len(listaDelPedidos) > 0:
                for reg in listaDelPedidos:
                    articuloAcargar = Pedidos.Pedidos(reg)
                    articuloAcargar.altaPedidos()

            if messagebox.askquestion(f'Pedido al Proveedor {proveedorVar.get()}',f'Carga de Pedido EXITOSA\n'
                                                                                  f'\n'
                                                                                  f'Desea cargar un Nuevo Pedido?') == 'yes':
                PedidosVent.destroy()
                menuPedidos('Alta')
            else:
                PedidosVent.destroy()

        else:
            messagebox.showwarning(f'Pedido al Proveedor {proveedorVar.get()}','Pedido CANCELADO')
            PedidosVent.destroy()



    def modificarPedido():
        pedEncontrado = encontrarPedido()
        if len(pedEncontrado) > 1:
            pedEncontrado.modificarPedidos(idPedido_combo.get())
            # encontarArt = buscarArticulo()
            ArtEncontrado = Articulos.Articulos(tuple(encontarArt))
            ArtEncontrado.aumentarStock(cantidadVar.get())
            dbPk.commit()
            messagebox.showinfo('MODIFICACION PEDIDOS', 'Registro Modificado')

        limpiarvar()
        limpiarCampos()

    def buscarArticulo(id):
        buscaart = 'SELECT * FROM articulos WHERE id_articulo = '+ str(id)
        cur.execute(buscaart)
        resultado = cur.fetchall()
        for ind in resultado:
            articulo = []
            for i in range(1,len(ind)):
                articulo.append(ind[i])

            articuloEncontradoPorId = Articulos.Articulos(tuple(articulo))
            articuloEncontradoPorId._idArticulos = id
        return articuloEncontradoPorId


    # def listarcombo(tabla, campo):
    #     if tabla.upper() == 'PEDIDOS':
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
    #         PedidosVent.focus()
    #     else:
    #         for ind in resultado:
    #             if tabla.upper() == 'PROVEEDORES':
    #                 listadelcombo.append(ind[2])
    #
    #             elif tabla.upper() == 'ARTICULOS':
    #                 listadelcombo.append(ind[2])
    #
    #             elif tabla.upper() == 'PEDIDOS':
    #                 listadelcombo.append(ind[1])
    #
    #     return listadelcombo



    def eliminarPedido():

        pedidoElim = encontrarPedido()
        if messagebox.askquestion('Eliminar Registro', f'Esta seguro de dar de baja al Pedido?\n '
                                                       f'Numero: {pedidoElim.idPedido} \n'
                                                       f'Proveedor: {proveedores_combo.get()}') == 'yes':
            pedidoElim.borrarPedidos(pedidoElim.idPedido)
            dbPk.commit()

        else:
            messagebox.showwarning('Eliminar Registro', f'No se ha eliminado el registro')
        del pedidoElim
        limpiarvar()
        PedidosVent.destroy()

#VENTANA PEDIDOS
    PedidosVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idPedidoVarsVent = PedidosVent.winfo_id()
    PedidosVent.title('Tech-Hard - Pedidos a Proveedores')  # pone titulo a la ventana principal
    PedidosVent.geometry('600x700')  # Tamaño en pixcel de la ventana
    PedidosVent.iconbitmap('imagenHT.ico')  # icono
    PedidosVent.minsize(600, 700)
    PedidosVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar


    Pedidos_Campos = (
    'id_Pedido', 'Fecha', 'id_Proveedor', 'id_Articulo', 'cantidad', 'estado', 'nro_Remito', 'Total_Remito',
    'Motivo')  # 'id_Pedido', autoincremental
    CamposInt = (0, 2, 3, 4, 6)
    CamposFloat = (7,)
    CamposChar = (5, 8)
    CamposDate = (1,)
    FechaActual = datetime.date.today()
    comboConsultasPedidos = ('id_Pedido', 'Fecha', 'id_Proveedor', 'id_Articulo', 'estado', 'nro_Remito')

    framecampoPed = tk.Frame(PedidosVent)
    # framecampoPed.pack(fill='both')
    # framecampoPed.config(bg='lightblue')
    framecampoPed.config(width=600, height=400)
    framecampoPed.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoPed.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoPed.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoPed.pack(anchor=SE) # lo ubica abajo a la derecha
    framecampoPed.pack(fill='x')  # ancho como el padre
    framecampoPed.pack(fill='y')  # alto igual que el padre
    framecampoPed.pack(fill='both')  # ambas opciones
    framecampoPed.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    # idcliente = tk.IntVar()
    def config_label(mi_label, fila):
        espaciado_labels = {'column': 50, 'sticky': 'e', 'padx': 10, 'pady': 10}
        # color_labels ={'bg':color_fondo, 'fg':color_letra,'font':fuente}
        mi_label.grid(row=fila, **espaciado_labels)
        # mi_label.config(**color_labels)

    idPedidoVar = tk.IntVar()
    fechaVar = tkinter.StringVar()
    cantidadVar = tk.IntVar()
    proveedorVar = tk.StringVar()
    articuloElegidoVar = tk.StringVar()
    remitoVar = tk.IntVar()
    subtotalVar = tk.DoubleVar()
    motivoVar = tk.StringVar()

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
    # label/entry/botones
    idPedido_label = tk.Label(framecampoPed, text='Pedido N')
    config_label(idPedido_label, 3)

    # idPedido_input = tk.Entry(framecampoPed, width=8, justify=tk.RIGHT, textvariable=idPedidoVar)
    # idPedido_input.grid(row=3, column=51, padx=10, pady=10)
    # idPedido_input.config(state='disabled')

    pedidos = listarcombo('Pedidos', 'nroPedido')
    idPedido_combo = ttk.Combobox(framecampoPed, state='readonly', width=30, justify=tk.RIGHT,
                                     values=pedidos)  # ya que solo puede seleccionar los proveedores
    idPedido_combo.grid(row=3, column=51, padx=10, pady=10,sticky='w')
    idPedido_combo.current(0)
    idPedido_combo.config(state='disabled')
    idPedido_combo.bind('<<ComboboxSelected>>', elegirNroPedido)


    fecha_label = tk.Label(framecampoPed, text='fecha')
    config_label(fecha_label, 4)
    fecha_input = tk.Entry(framecampoPed, textvariable=fechaVar, width=20, justify=tk.RIGHT)
    fecha_input.grid(row=4, column=51, padx=10, pady=10, sticky='w')
    Fechahoystr = f'{FechaActual.year}-{FechaActual.month}-{FechaActual.day}'
    fechaVar.set(Fechahoystr)
    fecha_input.config(state='disabled')


    proveedores_label = tk.Label(framecampoPed,text='Proveedor')
    config_label(proveedores_label,5)
    proveedores = listarcombo('Proveedores','')
    proveedores_combo = ttk.Combobox(framecampoPed, state='readonly', textvariable=proveedorVar, width=40,
                               values=proveedores)  # ya que solo puede seleccionar los proveedores
    proveedores_combo.grid(row=5, column=51, padx=10, pady=10, sticky='w')
    proveedores_combo.current(0)
    proveedores_combo.bind('<<ComboboxSelected>>', elegirProveedor)


    articulos_label = tk.Label(framecampoPed, text='Articulo')
    config_label(articulos_label, 6)
    articulos = listarcombo('Articulos', '')
    articulos_combo = ttk.Combobox(framecampoPed, state='readonly', textvariable=articuloElegidoVar, width=40,
                                     values=articulos)  # ya que solo puede seleccionar los proveedores
    articulos_combo.grid(row=6, column=51, padx=10, pady=10, sticky='w')
    if len(articulos) > 0:
        articulos_combo.current(0)


    cantidad_label = tk.Label(framecampoPed, text='Cantidad')
    config_label(cantidad_label, 7)
    cantidad_input = tk.Entry(framecampoPed, textvariable=cantidadVar, width=20, justify=tk.RIGHT)
    cantidad_input.grid(row=7, column=51, padx=10, pady=10,sticky='w')
    cantidad_input.bind('<Return>', cargarItemEnterCantidad)

    estado_label = tk.Label(framecampoPed, text='Estado')
    config_label(estado_label, 8)
    estado_combo = ttk.Combobox(framecampoPed, state='readonly', width=30,
                                     values=['PENDIENTE','COMPLETADO'])  # ya que solo puede seleccionar los proveedores
    estado_combo.grid(row=8, column=51, padx=10, pady=10, sticky='w')
    estado_combo.current(0)
    estado_combo.config(state='disabled')


    numeroRemito_label = tk.Label(framecampoPed, text='Numero Remito')
    config_label(numeroRemito_label, 9)
    numeroRemito_input = tk.Entry(framecampoPed, textvariable=remitoVar, width=40, justify=tk.RIGHT)
    numeroRemito_input.grid(row=9, column=51, padx=10, pady=10, sticky='w')
    numeroRemito_input.config(state='disabled')


    subtotal_label = tk.Label(framecampoPed, text='Subtotal Remito')
    config_label(subtotal_label, 10)
    subtotal_input = tk.Entry(framecampoPed, textvariable=subtotalVar, width=30, justify=tk.RIGHT)
    subtotal_input.grid(row=10, column=51, padx=10, pady=10, sticky='w')
    subtotal_input.config(state='disabled')

    motivo_label = tk.Label(framecampoPed, text='Cantidad Entregada')
    config_label(motivo_label, 11)
    motivo_input = tk.Entry(framecampoPed, textvariable=motivoVar, width=40)
    motivo_input.grid(row=11, column=51, padx=10, pady=10, sticky='w')
    motivo_input.config(state='disabled')

####frame grilla
    frameItemsPedido = tk.Frame(PedidosVent)
    frameItemsPedido.config(width=600, height=150)
    frameItemsPedido.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    frameItemsPedido.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    frameItemsPedido.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoPed.pack(anchor=SE) # lo ubica abajo a la derecha
    frameItemsPedido.pack(fill='x')  # ancho como el padre
    frameItemsPedido.pack(fill='y')  # alto igual que el padre
    frameItemsPedido.pack(fill='both')  # ambas opciones
    frameItemsPedido.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    # VentanaGrilla.Scrollbar_Example(PedidosVent)

# FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesPedido = tk.Frame(PedidosVent)
    framebotonesPedido.pack()

    boton_Alta = tk.Button(framebotonesPedido, text='Nuevo Pedido')
    boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)
    
    boton_CargarArticulo = tk.Button(framebotonesPedido, text='Cargar Articulo', command=agregarArticulo)
    boton_CargarArticulo.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_FinalizarPedido = tk.Button(framebotonesPedido, text='Finalizar Pedido', command=finalizarPedido)
    boton_FinalizarPedido.grid(row=0, column=3, padx=5, pady=10, ipadx=7)

    # boton_Buscar = tk.Button(framebotonesPedido, text='Buscar Pendientes')
    # boton_Buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesPedido, text='Actualizar',command=modificarPedido)
    boton_Actualizar.grid(row=0, column=4, padx=5, pady=10, ipadx=7)


    boton_Eliminar = tk.Button(framebotonesPedido, text='Eliminar', command=eliminarPedido)
    boton_Eliminar.grid(row=0, column=5, padx=5, pady=10, ipadx=7)

    if opcion == 'Alta':
        listaDeItemsPedido = []
        listaDelPedidos = []
        idPedido_combo.config(state='disabled')
        fecha_input.config(state='disabled')

        # boton_buscarProveedor.config(state='normal')
        # boton_buscarArticulo.config(state='disabled')
        deshabilitarbotones('disabled')
        componenteshabilitarRemito('disabled')
        limpiarCampos()
        articulos_combo.config(state='disabled')
        proveedores_combo.focus()

    elif opcion == 'Baja':
        listaDeItemsPedido = []
        listaDelPedidos = []
        articulosDelPedidoNombre = []
        listarcombo('Pedidos','nroPedido')
        # boton_BuscaridPedido.config(state='normal')
        fecha_input.config(state='disabled')
        # boton_buscarProveedor.config(state='disabled')
        # boton_buscarArticulo.config(state='disabled')
        deshabilitarbotones('disabled')
        componenteshabilitarRemito('disabled')
        limpiarCampos()
        idPedido_combo.config(state='normal')
        boton_Eliminar.config(state='normal')
        idPedido_combo.focus()

    elif opcion == 'Modificacion':
        listarcombo('Pedidos','id_pedido')
        idPedido_combo.config(state='normal')
        # boton_BuscaridPedido.config(state='normal')
        idPedido_combo.focus()

        fecha_input.config(state='disabled')
        # boton_buscarProveedor.config(state='disabled')
        # boton_buscarArticulo.config(state='disabled')
        deshabilitarbotones('disabled')
        componenteshabilitarRemito('disabled')
        limpiarCampos()
        boton_Actualizar.config(state='normal')










