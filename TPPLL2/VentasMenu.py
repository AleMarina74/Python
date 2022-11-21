#!/usr/bin/env python
# _*_ coding: utf-8 _*_
import tkinter

import Articulos
import Cliente
import VentanaGrilla
import Ventas
import mariadb
import datetime
import FuncionesMenu
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Pedidos

dbPk = mariadb.connect(
    host='127.0.0.1',
    user='root',
    password='root',
    database='Pk',
    autocommit=True
)
cur = dbPk.cursor()

VentasEncabezado_Campos = ('Nro_Factura','Fecha','Tipo_Factura','id_Cliente','Total')
CamposIntEncabezado = (0, 3)
CamposFloatEncabezado = (4,)
CamposCharEncabezado = (2,)
CamposDateEncabezado = (1,)

VentasItems_Campos = ('idItem', 'Nro_Factura','id_Articulo','Detalle','Cantidad','Precio_Unitario','Subtotal')

CamposIntItems = (0, 1, 2, 4)
CamposFloatItems = (5, 6)
CamposCharItems = (3,)

FechaActual = datetime.date.today()
FechaHoy = datetime.date.today().strftime('%d-%m-%Y')
Factura_items = ('NombreArticulo', 'Cantidad','Precio Unitario','Subtotal')
lenFacturaItems = (40, 10,18,15)


# ---- MENU PEDIDOS
def menuVentas(opcion):
    # def limpiarvar():
    #     pass
    #
    #
    # def deshabilitarbotones(valor):
    #     boton_CargarArticulo.config(state=valor)
    #     boton_FinalizarPedido.config(state=valor)
    #     boton_Actualizar.config(state=valor)
    #     boton_Eliminar.config(state=valor)
    #
    # def nuevoPedido():
    #     limpiarvar()
    #     limpiarCampos()
    #     ultimoPed = buscarultimopedido()
    #     nuevoPedido = ultimoPed + 1
    #     valores = tk.Listbox(idPedido_combo["values"])
    #     idPedido_combo["values"] = values + [nuevoPedido]
    #     idPedido_combo.set(nuevoPedido)

    def buscarsitiva(id):
        buscarid = 'SELECT * FROM situacioniva WHERE id_Iva = ' + str(id)
        cur.execute(buscarid)
        Resultado = cur.fetchall()
        if len(Resultado) > 0:
            for ind in Resultado:
                situacion = ind[1]
            return situacion

###EVENTOS
    def elegirTipoFactura(tipo):
        ultimonro = buscarUltimaFacturaTipo(tipo)
        if ultimonro == 0:
            nroFacturaVar.set(1)
        else:
            nroActual = ultimonro + 1
            nroFacturaVar.set(nroActual)
        tipoFactura_combo.config(state='disabled')
        cliente_input.focus()

    def ingresaCliente(event):
        if clienteVar.get() == '':
            clienteVar.set(0)
        encontrarCliente=buscarCliente(clienteVar.get())
        dniCliente = encontrarCliente.dni
        clienteVar.set(dniCliente)
        buscarsitiva(encontrarCliente.id_situacionIva)
        situacion = buscarsitiva(encontrarCliente.id_situacionIva)

        if situacion.upper() == 'CONSUMIDOR FINAL':
            tipoFacturaVar.set(1)
            elegirTipoFactura('B')
            tipoFactura_combo.current(1)
        else:
            tipoFacturaVar.set(0)
            elegirTipoFactura('A')
            tipoFactura_combo.current(0)
        situacionIvaVar.set(situacion)
        cliente_input.config(state='disabled')
        articulos_combo.config(state='normal')
        articulos_combo.focus()
        articulos_combo.current(0)

    def seleccionarArticulo(event):
        cantidad_input.config(state='normal')
        cantidad_input.delete(0,tk.END)
        cantidad_input.focus()

    def cantidadIngresada(event):
        agregarArticulo()
        boton_FinalizarPedido.config(state='normal')

####VALIDACIONES
    def ValidarNumero(VentanaPadre, componente):
        while True:
            try:
                validacion = True
                varingresada = int(componente.get())

            except:
                messagebox.showerror('Validacion Campo',f'Debe ingresar un valor entero Valido')
                componente.delete(0, tk.END)
                componente.select_range(0, tk.END)
                componente.focus()
                VentanaPadre.focus()
                validacion = False

            finally:
                return validacion


#     def elegirProveedor(event):
#         articulosprov = listarArticulosPorProveedor()
#         articuloElegidoVar.set('')
#         articulos_combo = ttk.Combobox(framecampoVentas, state='readonly', textvariable=articuloElegidoVar,
#                                        values=articulosprov)  # ya que solo puede seleccionar los proveedores
#         articulos_combo.grid(row=6, column=51, padx=10, pady=10)
#         if len(articulosprov) > 0:
#             articulos_combo.current(0)
#
#         cantidad_input.config(state='normal')
#         boton_CargarArticulo.config(state='normal')
#         boton_FinalizarPedido.config(state='normal')
#         articulos_combo.config(state='normal')
#         articulos_combo.current(0)
#         articulos_combo.focus()
#
#     def elegirNroPedido(event):
#         pedidosEncontrados = buscarItemsPedidos()
#         if len(pedidosEncontrados) > 0:
#             for item in pedidosEncontrados:
#                 articuloEncontradoEleccion = buscarArticulo(item[4])
#                 itemMostrar = (articuloEncontradoEleccion.nombre, item[5])
#                 listaDeItemsPedido.append(itemMostrar)
#                 listaDeFactura.append(item)
#                 articulosDelPedidoNombre.append(articuloEncontradoEleccion.nombre)
#             registroAux = listaDeFactura[0]
#             idProveedor = registroAux[3]
#             proveedor = buscarProveedorPorId(idProveedor)
#             proveedorVar.set(proveedor)
#             VentanaGrilla.grillaFrame('Cargar', Pedidos_columnasItems, lenPedidosItems, listaDeItemsPedido,
#                                       frameItemsFactura)
#             tipoFactura_combo['values'] = proveedor
#             tipoFactura_combo.config(state='disabled')
#             articulos_combo['values'] = articulosDelPedidoNombre
#             articulos_combo.current(0)
#             articulos_combo.focus()
#
#     def asignarComboporId(tabla, campo, componente, dato):
#         combodatos = listarcombo(tabla, campo)
#         datos = combodatos[0]
#         idDato = combodatos[1]
#         indice = idDato.index(dato)
#         componente.current(indice)
#
###FUNCIONES DE BUSQUEDA DE DATOS
    def buscarCliente(valor): #Devuelve el dni clave primaria
        if ValidarNumero(VentasVent, cliente_input):
            clienteBuscado = 'SELECT * FROM clientes WHERE DNI=' + str(valor)
            cur.execute(clienteBuscado)
            resultado = cur.fetchall()
            if len(resultado) < 1:
                messagebox.showwarning(f'Carga Cliente', 'No se encuentra el cliente en nuestra base de datos')
                VentasVent.focus()
                cliente_input.delete(0, tk.END)
                cliente_input.focus()
            else:
                for ind in resultado:
                    if ind == None:
                        messagebox.showwarning(f'Carga Cliente', 'No se encuentra el cliente en nuestra base de datos')
                        VentasVent.focus()
                        cliente_input.delete(0, tk.END)
                        cliente_input.focus()
                    else:
                        clienteEncontrado = Cliente.Cliente(tuple(ind))

        else:
            clienteBuscado = 'SELECT * FROM clientes WHERE NombreApellido = \"' + valor + '\"'
            cur.execute(clienteBuscado)
            resultado = cur.fetchone()
            if len(resultado) < 1:
                messagebox.showwarning(f'Carga Cliente','No se encuentra el cliente en nuestra base de datos')
                VentasVent.focus()
                cliente_input.delete(0,tk.END)
                cliente_input.focus()
            else:

                for ind in resultado:
                    if ind == None:
                        messagebox.showwarning(f'Carga Cliente', 'No se encuentra el cliente en nuestra base de datos')
                        VentasVent.focus()
                        cliente_input.delete(0, tk.END)
                        cliente_input.focus()
                    else:
                        clienteEncontrado = Cliente.Cliente(tuple(ind))
        return clienteEncontrado

    def listarcombo(tabla, campo):
        if tabla.upper() == 'PEDIDOS':
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
            VentasVent.focus()
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

    def buscarArticulo(valor):
        articuloBuscado = 'SELECT * FROM articulos WHERE id_articulo = ' + str(valor)
        cur.execute(articuloBuscado)
        resultado = cur.fetchall()
        if len(resultado) > 0:
            for ind in resultado:
                aux =[]
                for i in range(1,len(ind)):
                    aux.append(ind[i])
                articuloEcontrado = Articulos.Articulos(aux)
                articuloEcontrado.idArticulos = ind[0]


        return articuloEcontrado
#
#     # def listarArticulos():
#     #     listArticulo = 'SELECT * FROM articulos'
#     #     cur.execute(listArticulo)
#     #     resultado = cur.fetchall()
#     #     selArticulos = []
#     #     if len(resultado) > 0:
#     #         for ind in resultado:
#     #             selArticulos.append((ind[0],ind[2]))
#     #     return selArticulos
#
    def buscarArticuloPorNombre():
        articulobuscar = 'SELECT * FROM articulos WHERE nombre=\"' + articulos_combo.get() + '\"'
        cur.execute(articulobuscar)
        resultado = cur.fetchall()
        for ind in resultado:
            aux = []
            id = ind[0]
            for campo in range(1,len(ind)):
                aux.append(ind[campo])
            articuloEncontrado = Articulos.Articulos(tuple(aux))
            articuloEncontrado.idArticulos = id
        return articuloEncontrado

    def buscarUltimaFacturaTipo(tipo):
        # ultFactura = 'SELECT * FROM ventasencabezado  WHERE tipo_Factura = \"'+ tipo + '\" ORDER BY nro_factura desc'
        ultFactura = 'SELECT MAX(Nro_Factura) from ventasencabezado WHERE tipo_Factura = \"'+ tipo + '\"'
        cur.execute(ultFactura)
        resultado = cur.fetchone()
        if len(resultado) < 1:
            ultimo = 0
        else:
            for reg in resultado:
                if reg == None:
                    ultimo = 0
                else:
                    ultimo = reg
        return ultimo
#
#     def encontrarItemPedido(id):
#         sqlbusqueda = 'SELECT * FROM pedidos WHERE id_pedido = ' + str(id)
#         cur.execute(sqlbusqueda)
#         Resultado = cur.fetchall()
#
#         if len(Resultado) > 0:
#             for ind in Resultado:
#                 pedidoTupla = []
#                 for i in range(1, len(ind)):
#                     pedidoTupla.append(ind[i])
#                 pedidoEncontrado = Pedidos.Pedidos(tuple(pedidoTupla))
#
#         return pedidoEncontrado
#
###FUNCIONES DE CARGA DE ITEMS Y PEDIDOS
    def agregarArticulo():
        tipoFactura_combo.config(state='disabled')
        factura = nroFacturaVar.get()
        tipoFactura = tipoFacturaVar.get()
        clienteDNI = clienteVar.get()
        articuloBuscar = buscarArticuloPorNombre()
        idArticulo = articuloBuscar.idArticulos  # (buscar id del articulo seleccionado
        detalle = articuloBuscar.nombre
        detalleVar.set(detalle)
        if cantidadVar.get() < 1:
            messagebox.showwarning(f'Carga de Pedido', f'Debe ingresar una Cantidad superior a 0.')
            VentasVent.focus()
            cantidad_input.select_range(0, tk.END)
            cantidad_input.focus()
        else:
            cantidad = cantidadVar.get()

            Seguir = True
            if len(listaDeFactura) < 1:
                Seguir = True
            else:
                for item in listaDeFactura:
                    if item[5] == idArticulo:
                        messagebox.showwarning(f'Carga de Articulo a la Venta', f'El item ya ha sido cargado.\n')
                        VentasVent.focus()
                        articuloElegidoVar.set('')
                        articulos_combo.focus()
                        articulos_combo.current(0)
                        Seguir = False
            if Seguir:
                precioUnitario = articuloBuscar.precioFinal
                subtotal = precioUnitario * cantidad
                subtotalGeneral = totalVar.get() + subtotal
                totalVar.set(subtotalGeneral)

                itemVenta = [factura, FechaActual,tipoFactura,clienteDNI,totalVar.get(),idArticulo, detalle, cantidad, precioUnitario, subtotal]
                itemMostrar = (articuloElegidoVar.get(), cantidadVar.get(), precioUnitario, subtotal)  # lista de tuplas

                listaDeFactura.append(itemVenta)  # lista de listas

                if len(listadeItemsFactura) > 0:  # lista de items
                    listadeItemsFactura.append(itemMostrar)
                    VentanaGrilla.grillaFrame('Agregar', Factura_items, lenFacturaItems,
                                              [(articuloElegidoVar.get(), cantidadVar.get(),precioUnitario, subtotal,), ], frameItemsFactura)
                else:
                    listadeItemsFactura.append(itemMostrar)
                    VentanaGrilla.grillaFrame('Nuevo', Factura_items, lenFacturaItems,
                                              [(articuloElegidoVar.get(), cantidadVar.get(),precioUnitario, subtotal,), ], frameItemsFactura)

                articuloElegidoVar.set('')
                articulos_combo.current(0)
                articulos_combo.focus()
            else:
                VentasVent.focus()
                articuloElegidoVar.set('')
                articulos_combo.current(0)
                articulos_combo.focus()

    def finalizarVenta():
        if messagebox.askquestion(f'Venta del Cliente {clienteVar.get()}',
                                  f'Desea finalizar la Venta con los items'
                                  f'cargados?') == 'yes':
            if len(listaDeFactura) > 0:
                ultimoRegistro = listaDeFactura[-1]
                # aux = []
                # for i in range(1,len(ultimoRegistro)):
                #     aux.append(ultimoRegistro[i])
                # itemCargaEncabezado = Ventas.Ventas(tuple(aux))
                itemCargaEncabezado = Ventas.Ventas(tuple(ultimoRegistro))
                itemCargaEncabezado.altaVenta()
                id_Venta = itemCargaEncabezado.idVenta

                for reg in listaDeFactura:
                    itemFacturaCarga = Ventas.Ventas(tuple(reg))
                    itemFacturaCarga.idVenta = id_Venta
                    itemFacturaCarga.altaItems(id_Venta)
                    idArticulo = itemFacturaCarga.idArticulo
                    encontrarArticulo = buscarArticulo(idArticulo)
                    encontrarArticulo.idArticulos = itemFacturaCarga.idArticulo
                    encontrarArticulo.disminuirStock(itemFacturaCarga.cantidad)


            if messagebox.askquestion(f'Ventas', f'Carga de Venta EXITOSA\n'
                                               f'\n'
                                               f'Desea generar uns Nueva Venta?') == 'yes':
                VentasVent.destroy()
                menuVentas('Alta')
            else:
                VentasVent.destroy()
        else:
            messagebox.showwarning('Ventas','Venta CANCELADA')
            VentasVent.destroy()



# VENTANA VENTAS
    VentasVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idPedidoVarsVent = VentasVent.winfo_id()
    VentasVent.title('Tech-Hard - Ventas')  # pone titulo a la ventana principal
    VentasVent.geometry('600x700')  # Tamaño en pixcel de la ventana
    VentasVent.iconbitmap('imagenHT.ico')  # icono
    VentasVent.minsize(600, 700)
    VentasVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar

    FechaActual = datetime.date.today()

    framecampoVentas = tk.Frame(VentasVent)
    # framecampoVentas.pack(fill='both')
    # framecampoVentas.config(bg='lightblue')
    framecampoVentas.config(width=600, height=350)
    framecampoVentas.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoVentas.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoVentas.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoVentas.pack(anchor=SE) # lo ubica abajo a la derecha
    framecampoVentas.pack(fill='x')  # ancho como el padre
    framecampoVentas.pack(fill='y')  # alto igual que el padre
    framecampoVentas.pack(fill='both')  # ambas opciones
    framecampoVentas.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    # idcliente = tk.IntVar()
    def config_label(mi_label, fila):
        espaciado_labels = {'column': 50, 'sticky': 'e', 'padx': 10, 'pady': 10}
        # color_labels ={'bg':color_fondo, 'fg':color_letra,'font':fuente}
        mi_label.grid(row=fila, **espaciado_labels)
        # mi_label.config(**color_labels)

    nroFacturaVar = tk.IntVar()
    fechaVar = tk.StringVar()
    tipoFacturaVar = tk.StringVar()
    clienteVar = tk.StringVar()
    situacionIvaVar = tk.StringVar()
    totalVar = tk.DoubleVar()
    articuloElegidoVar = tk.StringVar()
    cantidadVar = tk.IntVar()
    subTotalVar = tk.DoubleVar()
    detalleVar = tk.StringVar()

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
    # label/entry/botones
    nroFactura_label = tk.Label(framecampoVentas, text='Factura Nº')
    config_label(nroFactura_label, 3)

    nroFactura_input = tk.Entry(framecampoVentas, width=12, justify=tk.RIGHT, textvariable=nroFacturaVar)
    nroFactura_input.grid(row=3, column=51, padx=10, pady=10, sticky='w')
    nroFactura_input.config(state='disabled')

    fecha_label = tk.Label(framecampoVentas, text='fecha')
    config_label(fecha_label, 4)
    fecha_input = tk.Entry(framecampoVentas, textvariable=fechaVar, width=20, justify=tk.RIGHT)
    fecha_input.grid(row=4, column=51, padx=10, pady=10, sticky='w')
    Fechahoystr = f'{FechaActual.year}-{FechaActual.month}-{FechaActual.day}'
    fechaVar.set(Fechahoystr)
    fecha_input.config(state='disabled')

    tipoFactura_label = tk.Label(framecampoVentas, text='Tipo Factura')
    config_label(tipoFactura_label, 5)
    tipoFacturas = ('A','B')
    tipoFactura_combo = ttk.Combobox(framecampoVentas, state='readonly', textvariable=tipoFacturaVar, width=5,
                                     values=tipoFacturas)  # ya que solo puede seleccionar los proveedores
    tipoFactura_combo.grid(row=5, column=51, padx=10, pady=10, sticky='w')
    tipoFactura_combo.current(0)
    tipoFactura_combo.bind('<<ComboboxSelected>>')

    cliente_label = tk.Label(framecampoVentas, text='Cliente')
    config_label(cliente_label,6)
    cliente_input = tk.Entry(framecampoVentas, textvariable=clienteVar, width=40)
    cliente_input.grid(row=6, column=51, padx=10, pady=10, sticky='w')
    cliente_input.bind('<Return>',ingresaCliente)

    situacionIva_label = tk.Label(framecampoVentas, text='Situacion Iva')
    config_label(situacionIva_label,7)
    situacionIva_input = tk.Entry(framecampoVentas, textvariable=situacionIvaVar, width=30)
    situacionIva_input.grid(row=7, column=51, padx=10, pady=10, sticky='w')
    situacionIva_input.config(state='disabled')

    articulos_label = tk.Label(framecampoVentas, text='Articulo')
    config_label(articulos_label, 8)
    articulos = listarcombo('Articulos', '')
    articulos_combo = ttk.Combobox(framecampoVentas, state='readonly', textvariable=articuloElegidoVar, width=40,
                                   values=articulos)  # ya que solo puede seleccionar los proveedores
    articulos_combo.grid(row=8, column=51, padx=10, pady=10, sticky='w')
    if len(articulos) > 0:
        articulos_combo.current(0)
    articulos_combo.bind('<<ComboboxSelected>>',seleccionarArticulo)

    cantidad_label = tk.Label(framecampoVentas, text='Cantidad')
    config_label(cantidad_label, 9)
    cantidad_input = tk.Entry(framecampoVentas, textvariable=cantidadVar, width=20, justify=tk.RIGHT)
    cantidad_input.grid(row=9, column=51, padx=10, pady=10, sticky='w')
    cantidad_input.bind('<Return>',cantidadIngresada)

    subtotal_label = tk.Label(framecampoVentas, text='Total')
    config_label(subtotal_label, 10)
    subtotal_input = tk.Entry(framecampoVentas, textvariable=totalVar, width=30, justify=tk.RIGHT)
    subtotal_input.grid(row=10, column=51, padx=10, pady=10, sticky='w')
    subtotal_input.config(state='disabled')


####FRAME GRILLA
    frameItemsFactura = tk.Frame(VentasVent)
    frameItemsFactura.config(width=600, height=250)
    frameItemsFactura.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    frameItemsFactura.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    frameItemsFactura.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoVentas.pack(anchor=SE) # lo ubica abajo a la derecha
    frameItemsFactura.pack(fill='x')  # ancho como el padre
    frameItemsFactura.pack(fill='y')  # alto igual que el padre
    frameItemsFactura.pack(fill='both')  # ambas opciones
    frameItemsFactura.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    # VentanaGrilla.Scrollbar_Example(VentasVent)

### FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesVenta = tk.Frame(VentasVent)
    framebotonesVenta.pack()

    # boton_Alta = tk.Button(framebotonesVenta, text='Nuevo Pedido')
    # boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)

    boton_CargarArticulo = tk.Button(framebotonesVenta, text='Cargar Articulo', command=agregarArticulo)
    boton_CargarArticulo.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_FinalizarPedido = tk.Button(framebotonesVenta, text='Finalizar Venta', command=finalizarVenta)
    boton_FinalizarPedido.grid(row=0, column=3, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesVenta, text='Actualizar')
    boton_Actualizar.grid(row=0, column=4, padx=5, pady=10, ipadx=7)

    boton_Eliminar = tk.Button(framebotonesVenta, text='Eliminar Item')
    boton_Eliminar.grid(row=0, column=5, padx=5, pady=10, ipadx=7)

    if opcion == 'Alta':
        listadeItemsFactura = []
        listaDeFactura = []
        boton_Eliminar.config(state='disabled')
        boton_Actualizar.config(state='disabled')
        boton_FinalizarPedido.config(state='disabled')
        boton_CargarArticulo.config(state='normal')
        nroFactura_input.config(state='disabled')
        tipoFactura_combo.config(state='disabled')

        fecha_input.config(state='disabled')
        articulos_combo.config(state='disabled')
        cantidad_input.config(state='disabled')
        cliente_input.focus()

    elif opcion == 'Baja':
        listaDeItemsPedido = []
        # listaDeFactura = []
        # articulosDelPedidoNombre = []
        # listarcombo('Pedidos', 'nroPedido')
        # # boton_BuscaridPedido.config(state='normal')
        # fecha_input.config(state='disabled')
        # # boton_buscarProveedor.config(state='disabled')
        # # boton_buscarArticulo.config(state='disabled')
        # deshabilitarbotones('disabled')
        # componenteshabilitarRemito('disabled')
        # limpiarCampos()
        # idPedido_combo.config(state='normal')
        # boton_Eliminar.config(state='normal')
        # idPedido_combo.focus()

    elif opcion == 'Modificacion':
        listarcombo('Pedidos', 'id_pedido')
        # idPedido_combo.config(state='normal')
        # # boton_BuscaridPedido.config(state='normal')
        # idPedido_combo.focus()
        #
        # fecha_input.config(state='disabled')
        # # boton_buscarProveedor.config(state='disabled')
        # # boton_buscarArticulo.config(state='disabled')
        # deshabilitarbotones('disabled')
        # componenteshabilitarRemito('disabled')
        # limpiarCampos()
        # boton_Actualizar.config(state='normal')




