#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk

import FuncionesMenu
import ClientesMenu
import ProveedoresMenu
import PedidosMenu
import ArticulosMenu
import StockMenu
import TelProveedoresMenu
import VentanaGrilla
import VentasMenu
import menuRemitos
import EstadisticasStock
from FuncionesMenu import *
from os import curdir
import datetime
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

raiz = tk.Tk() #creo ventana principal
raiz.title('Tech-Hard') #pone titulo a la ventana principal
# raiz.geometry('800x600') #Tamaño en pixcel de la ventana
raiz.iconbitmap('imagenHT.ico') #icono
raiz.minsize(800,600)
raiz.resizable(1,1) # size ancho, alto 0 no se agranda, 1 se puede agrandar

PruebaFrame = tk.Frame()
PruebaFrame.pack(fill='both')
# side= 'left' 'rigth' 'top' 'bottom' anclado a la izquierda si es resizable el raiz
 # posicionar combinado con side
 # fill rellena 'x' en el eje 'y' para este eje tengo que poner expand='True' 'both' 'none'
# PruebaFrame.config(bg='red')
PruebaFrame.config(width='800', height='600')
PruebaFrame.config(bd=35)
# PruebaFrame.config(relief='sunken')
PruebaFrame.config(cursor='hand2') # 'pirate' forma de calabera

miImagen = tk.PhotoImage(file='colores_tkinter.png')

imagen = tk.Label(PruebaFrame,image=miImagen) #png y gif
imagen.place(x=800,y=600)

#INTERFAZ GRAFICA
# imagen_Fondo = tk.PhotoImage(file='colores_tkinter.png')
# background = tk.Label(image=imagen_Fondo, text='Imagen de fondo')
# background.place(x=5, y=5)

barramenu = tk.Menu(raiz) #creo la barra de menu
raiz.config(menu = barramenu) #indico a la ventana principal que ubique el menu

FechaActual = datetime.date.today()
FechaHoy = datetime.date.today().strftime('%d-%m-%Y')
Fechahoystr = f'{FechaActual.year}-{FechaActual.month}-{FechaActual.day}'

#FUNCIONES
#Salir
def salir():
    rta = messagebox.askquestion('Confirme','Desea salir de la aplicacion?')
    if rta == 'yes':
        # dbPk.close()
        raiz.destroy()

#CLIENTES
def menuClienteAlta():
    ClientesMenu.menuClientes('Alta')

def menuClienteBaja():
    ClientesMenu.menuClientes('Baja')

def menuClienteModificacion():
    ClientesMenu.menuClientes('Modificacion')

def menuClienteBuscaDni():
    ClientesMenu.menuClientes('BuscarDni')

def menuClientesBuscaNombre():
    ClientesMenu.menuClientes('BuscarNombre')

def menuClientesBuscar():
    tabla = 'clientes'
    Cliente_Campos = ('DNI', 'NombreApellido', 'Direccion', 'Telefono', 'Mail', 'CondicionIva')
    Cliente_AnchoCampo = (10,60,60,20,40,30)
    sqlbus = 'SELECT a.dni, a.nombreapellido as Nombre_Apellido, a.direccion, a.telefono, a.mail, b.Situacion as Condicion_Iva FROM ' +  tabla + ' a INNER JOIN situacioniva b on a.Id_Iva=b.id_Iva WHERE a.dni > 0'
    tablas = VentanaGrilla.GrillaTabla(tabla, Cliente_Campos, Cliente_AnchoCampo, sqlbus)
    tablas.mainloop()


#PROVEEDORES
def menuProveedorAlta():
    ProveedoresMenu.menuProveedores('Alta')

def menuProveedorBaja():
    ProveedoresMenu.menuProveedores('Baja')

def menuProveedoresModificacion():
    ProveedoresMenu.menuProveedores('Modificacion')

def menuProveedorBuscarCUIT():
    ProveedoresMenu.menuProveedores('BuscarCUIT')

def menuProveedoresBuscar():
    tabla = 'proveedores'
    Proveedores_Campos = ('id_Proveedor', 'CUIT', 'RazonSocial','Direccion','Mail','CondicionIva')
    Proveedores_AnchoCampo = (12, 13, 60, 60, 40, 30)
    sqlbus = 'SELECT a.id_Proveedor, a.CUIT, a.RazonSocial, a.Direccion, a.Mail, b.situacion FROM '+ tabla +' a INNER JOIN situacioniva b on a.Id_Iva=b.id_Iva'
    tablas = VentanaGrilla.GrillaTabla(tabla, Proveedores_Campos,Proveedores_AnchoCampo,sqlbus)
    tablas.mainloop()

def cargarTelefono():
    TelProveedoresMenu.menuTelefonos(0,'Alta')

def eliminarTelefono():
    TelProveedoresMenu.menuTelefonos(0,'Baja')

def modificarTelefono():
    TelProveedoresMenu.menuTelefonos(0,'Modificacion')


#PEDIDOS
def nuevoPedido():
    PedidosMenu.menuPedidos('Alta')

def eliminarPedido():
    PedidosMenu.menuPedidos('Baja')

def modificarPedido():
    PedidosMenu.menuPedidos('Modificar')

def consultaPedidoNumero():
    PedidosMenu.menuPedidos('Buscar')

def menuPedidosBuscarTodos():
    tabla = 'pedidos'
    Pedidos_Campos = (
    'id_Pedido','Nro_Pedid' ,'Fecha', 'Proveedor', 'Articulo', 'Cantidad', 'Estado', 'Nro_Remito', 'Total_Remito',
    'Motivo')  # 'id_Pedido', autoincremental
    Pedidos_AnchoCampo = (10, 10, 12, 60, 60, 10, 20, 20, 10)
    sqlbus = 'SELECT a.id_Pedido, a.NroPedido, a.Fecha, b.RazonSocial, c.Nombre, a.cantidad, a.estado, a.nro_Remito, a.Total_Remito, a.Motivo FROM '+ tabla +' a INNER JOIN proveedores b ON b.id_Proveedor=a.id_Proveedor INNER JOIN articulos c ON a.id_Articulo=c.id_Articulo'
    tablas = VentanaGrilla.GrillaTabla(tabla, Pedidos_Campos, Pedidos_AnchoCampo, sqlbus)
    tablas.mainloop()


#ARTICULOS
def menuArticuloAlta():
    ArticulosMenu.menuArticulos('Alta')

def menuArticuloBaja():
    ArticulosMenu.menuArticulos('Baja')

def menuArticuloModificacion():
    ArticulosMenu.menuArticulos('Modificacion')

# def menuArticuloBuscarId():
#     ArticulosMenu.menuArticulos('BuscarID')

def menuArticuloBuscarCodigoBarras():
    ArticulosMenu.menuArticulos('BuscarCodigoBarras')

def menuArtiuloBuscarNombre():
    ArticulosMenu.menuArticulos('BuscarNombre')

def menuArticuloBuscarRubro():
    ArticulosMenu.menuArticulos('BuscarRubro')

def menuArticuloBuscarProveedor():
    ArticulosMenu.menuArticulos('BuscarProveedor')

def menuArticuloBuscar():
    tabla = 'articulos'
    Articulos_Campos = ('id_Articulo','CodigoBarras','Nombre','id_Rubro','CostoUnitario','PrecioFinal','id_Proveedor','UltimoPrecio','Stock_Minimo',
                        'Stock_Maximo','Stock')
    Articulos_AnchoCampo = (10, 20, 40, 30, 15, 13, 40, 14, 14, 14, 7)
    sqlbus = 'SELECT a.id_Articulo, a.CodigoBarras, a.Nombre, b.Detalle, a.CostoUnitario, a.PrecioFinal, c.RazonSocial, a.ultimoPrecio, a.Stock_Minimo, a.Stock_Maximo, a.Stock FROM ' + tabla + ' a INNER JOIN rubros b ON b.id_Rubro=a.id_Rubro INNER JOIN proveedores c ON a.id_Proveedor=c.id_Proveedor'
    tablas = VentanaGrilla.GrillaTabla(tabla, Articulos_Campos,Articulos_AnchoCampo, sqlbus)
    tablas.mainloop()

#PEDIDOS
def stockInicial():
    StockMenu.menuStock('StockInicial')

def stockCarga():
    StockMenu.menuStock('Carga')

def stockBaja():
    StockMenu.menuStock('Baja')

def stockActualizar():
    StockMenu.menuStock('Modificacion')

def stockPorArticulo():
    StockMenu.menuStock('BuscarNombre')

def stockPorCodigo():
    StockMenu.menuStock('BuscarCodigoBarras')

def stockConsulta():
    tabla = 'articulos'
    Articulos_Campos = ('id_Articulo','CodigoBarras','Nombre','Stock_Minimo',
                        'Stock_Maximo','Stock')
    Articulos_AnchoCampo = (10, 20, 40, 14, 14, 7)
    sqlbus = 'SELECT id_Articulo, CodigoBarras, Nombre, Stock_Minimo, Stock_Maximo, Stock FROM ' \
             + tabla
    cur.execute(sqlbus)
    resultado = cur.fetchall()
    if len(resultado) > 0:
        tablas = VentanaGrilla.GrillaTabla(tabla, Articulos_Campos,Articulos_AnchoCampo, sqlbus)
        tablas.mainloop()
    else:
        messagebox.showwarning('Tabla Articulos','La base de Articulos esta vacia.')

def stockEstadisticaVendidos():
    EstadisticasStock.EstadisticaGrafico('Vendidos','1.png')

def stockEstadisticaMenosVendidos():
    EstadisticasStock.EstadisticaGrafico('Menos','2.png')

def stockEstadisticaTodos():
    EstadisticasStock.EstadisticaGrafico('Todos','3.png')

#REMITO
def CargarRemito():
    menuRemitos.menuRemitos('Alta')


#VENTAS
def menuNuevaVenta():
    VentasMenu.menuVentas('Alta')

def menuAnularVenta():
    VentasMenu.menuVentas('Baja')

def menuModificarVenta():
    VentasMenu.menuVentas('Modificar')

def menuVentasDia():
    tabla = 'VentasEncabezado'
    VentasEncabezado_Campos = ('Nro_Factura', 'Fecha', 'Tipo_Factura', 'id_Cliente', 'Total')
    CamposIntEncabezado = (0, 3)
    CamposFloatEncabezado = (4,)
    CamposCharEncabezado = (2,)
    CamposDateEncabezado = (1,)

    VentasItems_Campos = ('idItem', 'Nro_Factura', 'id_Articulo', 'Detalle', 'Cantidad', 'Precio_Unitario', 'Subtotal')

    CamposIntItems = (0, 1, 2, 4)
    CamposFloatItems = (5, 6)
    CamposCharItems = (3,)

    FechaActual = datetime.date.today()
    FechaHoy = datetime.date.today().strftime('%d-%m-%Y')
    camposAMostrar = ('NroFactura','Cliente','TotalFactura')
    anchoCampos=(15,30,15)

    sqlbus = 'SELECT a.Nro_factura, b.NombreApellido, a.Total FROM ' + tabla +' a INNER JOIN clientes b ON b.DNI=a.DNI WHERE a.fecha=\"' + Fechahoystr + '\"'
    cur.execute(sqlbus)
    resultado = cur.fetchall()
    if len(resultado) > 0:
        tablas = VentanaGrilla.GrillaTabla(tabla, camposAMostrar, anchoCampos, sqlbus)
        tablas.mainloop()
    else:
        messagebox.showwarning('Tabla Ventas del Dia', 'No hubo ventas en el Dia de la fecha.\n')


####VENTANA MENUES PRINCIPAL

####### Menu Cliente

clientesmenu = tk.Menu(barramenu, tearoff=0)

clientesmenu.add_command(label = 'Alta de Cliente', command=menuClienteAlta)
clientesmenu.add_command(label = 'Baja de Cliente', command=menuClienteBaja)
clientesmenu.add_command(label = 'Modificacion de Cliente', command=menuClienteModificacion)

#Submenu Consulta Clientes
consultaclientemenu = tk.Menu(barramenu, tearoff=0)

consultaclientemenu.add_command(label= ' Por... DNI', command=menuClienteBuscaDni)
consultaclientemenu.add_command(label= ' Por... Nombre', command=menuClientesBuscaNombre)
consultaclientemenu.add_separator()
consultaclientemenu.add_command(label= 'Todos los Clientes', command=menuClientesBuscar)

clientesmenu.add_cascade(label = 'Consultas de Clientes',menu=consultaclientemenu)

#Menu Proveedores / Telefono Proveedor / pedidos
proveedoresmenu = tk.Menu(barramenu, tearoff=0)

proveedoresmenu.add_command(label = 'Alta de Proveedor', command=menuProveedorAlta)
proveedoresmenu.add_command(label = 'Baja de Proveedor', command=menuProveedorBaja )
proveedoresmenu.add_command(label = 'Modificacion de Proveedor', command=menuProveedoresModificacion)
proveedoresmenu.add_separator()

#Submenu Consulta Proveedores
consultaprovmenu = tk.Menu(barramenu, tearoff=0)

consultaprovmenu.add_command(label= 'Por... CUIT', command=menuProveedorBuscarCUIT)
# # consultaprovmenu.add_command(label= 'Por... Razon Social')
# # consultaprovmenu.add_command(label= 'Por... Dirección')
# # consultaprovmenu.add_command(label= 'Por... Contacto')
# # consultaprovmenu.add_command(label= 'Por... Rubro')
# consultaprovmenu.add_separator()
consultaprovmenu.add_command(label= 'Todos los Proovedores', command=menuProveedoresBuscar)

proveedoresmenu.add_cascade(label = 'Consultas de Proveedores',menu=consultaprovmenu)
proveedoresmenu.add_separator()


#Submenu Telefonos Proveedores
telproveedor = tk.Menu(barramenu,tearoff=0)

telproveedor.add_command(label= 'Cargar Telefono', command=cargarTelefono)
telproveedor.add_command(label= 'Borrar Telefono', command=eliminarTelefono)
telproveedor.add_command(label= 'Modificar Telefono', command=modificarTelefono)

proveedoresmenu.add_cascade(label= 'Telefonos Proveedor', menu=telproveedor)


#SubMenu Pedidos
pedidosproveedor = tk.Menu(barramenu, tearoff=0)

pedidosproveedor.add_command(label= 'Nuevo Pedido', command=nuevoPedido)
pedidosproveedor.add_command(label= 'Eliminar Pedido', command=eliminarPedido)
pedidosproveedor.add_command(label= 'Modificar Pedido', command=modificarPedido)


#Submenu Consultas Pedidos
consultapedidomenu = tk.Menu(barramenu, tearoff=0)

consultapedidomenu.add_command(label= 'Por... Numero',command=consultaPedidoNumero)
consultapedidomenu.add_command(label= 'Por... Fecha')
consultapedidomenu.add_command(label= 'Por... Proveedor')
consultapedidomenu.add_command(label= 'Por... Articulo')
consultapedidomenu.add_command(label= 'Por... Estado')
consultapedidomenu.add_command(label= 'Por... Nº Remito')
consultapedidomenu.add_separator()
consultapedidomenu.add_command(label='Listar Pedidos',command=menuPedidosBuscarTodos)

# pedidosproveedor.add_cascade(label= 'Pedidos', menu=pedidosproveedor)

pedidosproveedor.add_cascade(label= 'Consultar Pedido', menu= consultapedidomenu)

pedidosproveedor.add_separator()
pedidosproveedor.add_command(label= 'Cargar Remito', command=CargarRemito)

#Menu Articulos / Articulos a Devolver
articulosmenu = tk.Menu(barramenu,tearoff=0)

articulosmenu.add_command(label= 'Alta de Articulo', command=menuArticuloAlta)
articulosmenu.add_command(label= 'Baja de Articulo', command=menuArticuloBaja)
articulosmenu.add_command(label= 'Modificar Articulo',command=menuArticuloModificacion)
articulosmenu.add_separator()

#Submenu Consulta Articulo
consultaarticulomenu = tk.Menu(barramenu, tearoff=0)

consultaarticulomenu.add_command(label= 'Por... Codigo de Barras',command=menuArticuloBuscarCodigoBarras)
consultaarticulomenu.add_command(label= 'Por... Nombre', command=menuArtiuloBuscarNombre)
consultaarticulomenu.add_command(label= 'Por... Rubro', command=menuArticuloBuscarRubro)
consultaarticulomenu.add_command(label= 'Por... Proveedor', command=menuArticuloBuscarProveedor)
consultaarticulomenu.add_separator()
consultaarticulomenu.add_command(label= 'Todos los Articulos', command=menuArticuloBuscar)

articulosmenu.add_cascade(label= 'Consultar Articulos', menu= consultaarticulomenu)

#Submenu Devolver Articulo


#menu control de Stock
controlstockmenu = tk.Menu(barramenu,tearoff=0)

controlstockmenu.add_command(label= 'Stock Inicial', command=stockInicial)
controlstockmenu.add_command(label= 'Carga Stock', command=stockCarga)
controlstockmenu.add_command(label= 'Baja Stock por arqueo', command=stockBaja)
controlstockmenu.add_command(label= 'Modificacion de Stock', command=stockActualizar)
controlstockmenu.add_separator()

#Submenu ConsultasStock
consultaStock = tk.Menu(barramenu,tearoff=0)

consultaStock.add_command(label= '... por Articulo', command=stockPorArticulo)
consultaStock.add_command(label= '... por Codigo de Barras', command=stockPorCodigo)
consultaStock.add_separator()
consultaStock.add_command(label= '... Total general', command=stockConsulta)

controlstockmenu.add_cascade(label='Consultas Stock',menu=consultaStock)

controlstockmenu.add_separator()

#submenu Estadisticas
controlstockEstadistica = tk.Menu(barramenu,tearoff=0)

controlstockEstadistica.add_command(label='... los 10 mas vendidos',command=stockEstadisticaVendidos)
controlstockEstadistica.add_command(label='... los 10 menos vendidos',command=stockEstadisticaMenosVendidos)
controlstockEstadistica.add_command(label='... Porcentaje productos vendidos',command=stockEstadisticaTodos)
controlstockmenu.add_cascade(label='Estadísticas', menu=controlstockEstadistica)

#Menu Ventas
ventasmenu = tk.Menu(barramenu, tearoff=0)

ventasmenu.add_command(label = 'Nueva Venta', command=menuNuevaVenta)
# ventasmenu.add_command(label = 'Eliminar Venta', command=menuAnularVenta)
# ventasmenu.add_command(label = 'Modificar Venta', command=menuModificarVenta)
ventasmenu.add_separator()


#Submenu Consultas Ventas
consultarventas = tk.Menu(barramenu, tearoff=0)

# consultarventas.add_command(label= 'Por... Numero de Factura')
consultarventas.add_command(label= 'Del Dia',command=menuVentasDia)


ventasmenu.add_cascade(label= 'Consultas', menu=consultarventas)
#Herramientas Crear Rubro Situacion Iva




#Botones del submenu BBDD

#menu conexion base de datos
bbddmenu = tk.Menu(barramenu,tearoff=0)
bbddmenu.add_command(label = 'Conectar Base de Datos', command=conectar)

salirmenu = tk.Menu(barramenu, tearoff=0)
salirmenu.add_command(label = 'Salir', command= salir)

#Menu Ayuda y Acerca de
ayudamenu = tk.Menu(barramenu, tearoff=0)
ayudamenu.add_command(label = 'Licencia',
                      command = mostrar_licencia)
ayudamenu.add_separator() #agrego linea de separacion
ayudamenu.add_command(label = 'Acerca de...',
                      command = mostrar_acerca)



#Barra de menu principal
barramenu.add_cascade(label = 'Clientes', menu=clientesmenu)
barramenu.add_cascade(label = 'Proveedores', menu = proveedoresmenu)
barramenu.add_cascade(label = 'Articulos', menu=articulosmenu)
barramenu.add_cascade(label = 'Stock', menu=controlstockmenu)
barramenu.add_cascade(label = 'Pedidos a Proveedores', menu=pedidosproveedor)
barramenu.add_cascade(label = 'Ventas', menu=ventasmenu)
barramenu.add_cascade(label = 'Herramientas')
barramenu.add_cascade(label = 'BBDD',menu = bbddmenu)
barramenu.add_cascade(label = 'Acerca de ...', menu =ayudamenu)
barramenu.add_cascade(label = 'Salir',command=salir)

#FRAME DEL PIE
framecopy = ttk.Frame(raiz)
framecopy.pack(side=tk.BOTTOM)

copy_label = ttk.Label(framecopy, text = '(2022) por 4 Panas para Tech Hard')
copy_label.pack()

raiz.mainloop()

