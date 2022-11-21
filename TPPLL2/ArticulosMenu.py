#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from os import curdir
from tkinter import messagebox
from tkinter import ttk
import Proveedores
import Articulos
import StockMenu
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

# Proveedores_Campos = ('id_Proveedor', 'CUIT', 'RazonSocial', 'Titular','Direccion','Mail','Id_Iva')
Articulos_Campos = ('id_Articulo','CodigoBarras','Nombre','id_Rubro','CostoUnitario','PrecioFinal','id_Proveedor',
                    'UltimoPrecio','Stock_Minimo','Stock_Maximo','Cant_Stock')

# ---- MENU ARTICULOS
def menuArticulos(opcion):  # opcionmenu seria alta, muestrotodo en blanco y habilito el boton alta

    def limpiarvar():
        codigoBarrasVar.set(0)
        nombreVar.set('')
        idRubrosVar.set('')
        ProveedoresVar.set('')
        costoVar.set(0)
        precioFinaVar.set(0)
        ultimoPrecioVar.set(0)

    def componenteshabilitar(valor): #Valores 'disabled' o 'normal'
        codigoBarras_input.config(state=valor)
        nombre_input.config(state=valor)
        idRubros_combo.config(state=valor)
        proveedores_combo.config(state=valor)
        costo_input.config(state=valor)
        precioFinal_input.config(state=valor)
        ultimoPrecio_input.config(state=valor)


    def deshabilitarbotones(valor):
        boton_Alta.config(state=valor)
        boton_Buscar.config(state=valor)
        boton_Actualizar.config(state=valor)
        boton_Eliminar.config(state=valor)
        boton_Stock.config(state=valor)

    def limpiarCampos():
        codigoBarras_input.delete(0,tk.END)
        codigoBarras_input.select_range(0,tk.END)
        codigoBarras_input.focus()
        nombre_input.delete(0,tk.END)
        idRubros_combo.current(0)
        proveedores_combo.current(0)
        costo_input.delete(0,tk.END)
        precioFinal_input.delete(0,tk.END)
        ultimoPrecio_input.delete(0,tk.END)


    def llenarcampos(articulo):

        nombreVar.set(articulo.nombre)
        # Rubro = listarcombo('Rubros','Detalle') # 0=detalle, 1=idRubro
        asignarComboporId('RUBROS',idRubros_combo,articulo.idRubro)
        asignarComboporId('PROVEEDORES',proveedores_combo,articulo.idProveedor)
        costoVar.set(articulo.costoUnit)
        precioFinaVar.set(articulo.precioFinal)
        ultimoPrecioVar.set(articulo.ultPrecio)


####EVENTOS
    def buscarCodigoBarrasEnter(event):
        buscarCodigoBarras()

    def buscarNombreEnter(event):
        BuscarNombre()

    def buscarRubro(event):
        BuscarPorRubro()

    def buscarProveedor(event):
        BuscarPorProveddor()

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

    def ValidarRazonSocial(VentanaPadre, componente):
        while True:
            try:
                validacion = True
                varingresada = str(componente.get())

                if len(varingresada) < 2 or varingresada == '':
                    messagebox.showerror('Validacion Campo', f'Debe ingresar Nombre Valido')
                    componente.select_range(0, tk.END)
                    componente.focus()
                    VentanaPadre.focus()
                    validacion = False
                else:
                    espacio = 0
                    for i in varingresada:
                        if i == ' ':
                            espacio = 1
                            break
                    if espacio == 0:
                        validacion = True
                    else:
                        validacion = True

            except:
                messagebox.showerror('Validacion Campo', f'Debe ingresar un Campo Valido')
                componente.delete(0, tk.END)
                componente.select_range(0, tk.END)
                componente.focus()
                VentanaPadre.focus()
                validacion = False

            finally:
                return validacion



#####FUNCIONES
    def buscarUltimoArticulo():
        # ultpedido = 'SELECT * FROM pedidos ORDER BY id_Pedido desc'
        ultpedido = 'SELECT MAX(id_Pedido) from articulos'
        cur.execute(ultpedido)
        resultado = cur.fetchone()
        if len(resultado) < 1:
            ultimo = 0
        else:
            ultimo = resultado[0]
        return ultimo

    def buscarRubroDetalle():
        rubroabuscar = 'SELECT id_rubro FROM rubros WHERE detalle=\"'+ idRubros_combo.get()+'\"'
        cur.execute(rubroabuscar)
        resultado = cur.fetchall()
        for ind in resultado:
            idrubro= ind[0]
        return idrubro

    def asignarComboporId(tabla,componente,dato):
        combodatos = listarcombo(tabla,'Id')
        datos = combodatos[0]
        idDato = combodatos[1]
        indice = idDato.index(dato)
        componente.current(indice)





#####FUNCIONES DE BOTONES
    def buscarProveedorPorRazonSocial():
        proveedorabuscar = 'SELECT id_proveedor FROM proveedores WHERE RazonSocial=\"'+ proveedores_combo.get()+'\"'
        cur.execute(proveedorabuscar)
        resultado = cur.fetchall()
        for ind in resultado:
            idprov= ind[0]
        return idprov

    def buscarCodigoBarras():
        if ValidarNumero(ArticulosVent,codigoBarras_input):
            buscaCodigo = codigoBarrasVar.get()

            if buscaCodigo == 0 or buscaCodigo > 99999999999999999999:
                messagebox.showerror('Verificacion de Datos', 'Debe ingresar un valor valido de CODIGO DE BARRAS')
                ArticulosVent.focus()
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
                    if opcion == 'Baja':
                        llenarcampos(ArticuloEncontrado)
                        boton_Eliminar.config(state='normal')
                        boton_Eliminar.focus()
                        del Resultado
                    elif opcion == 'Alta':
                        messagebox.showwarning('Advertencia',f'El Articulo ya existe {ArticuloEncontrado.nombre}')
                        limpiarvar()
                        limpiarCampos()
                        codigoBarras_input.delete(0,tk.END)
                        codigoBarras_input.focus()
                        del Resultado
                    elif opcion == 'Modificacion':
                        llenarcampos(ArticuloEncontrado)
                        boton_Actualizar.config(state='normal')
                        componenteshabilitar('normal')
                        # selecentradas()
                        nombre_input.focus()
                        del Resultado
                    elif opcion == 'BuscarCodigoBarras':
                        llenarcampos(ArticuloEncontrado)

                        codigoBarras_input.select_range(0, tk.END)
                        codigoBarras_input.focus()

                elif len(Resultado) < 1:
                    if opcion == 'Alta':
                        componenteshabilitar('normal')
                        codigoBarras_input.config(state='disabled')
                        boton_Alta.config(state='normal')
                        nombre_input.focus()
                        del Resultado
                    else:
                        # opcion == 'Baja' or opcion == 'Modificacion' or opcion == 'buscarCodigoBarras' or opcion == 'BuscarNombre' :
                        messagebox.showwarning('Advertencia', f'No existe el Articulo Solicitado\n con el Codigo de Barras: {buscaCodigo}')
                        del Resultado
                        ArticulosVent.focus()
                        limpiarCampos()
                        limpiarvar()
                        codigoBarras_input.delete(0, tk.END)
                        codigoBarras_input.select_range(0, tk.END)
                        codigoBarras_input.focus()



        else:
            del Resultado
            ArticulosVent.focus()
            codigoBarras_input.delete(0, tk.END)
            codigoBarras_input.select_range(0, tk.END)
            codigoBarras_input.focus()

    def listarcombo(tabla, campo):
        buscarcombo = 'SELECT * FROM ' + tabla
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
                if tabla.upper() == 'PROVEEDORES':
                    listadelcombo.append(ind[2])
                    id_campo.append(ind[0])

                elif tabla.upper() == 'RUBROS':
                    listadelcombo.append(ind[1])
                    id_campo.append(ind[0])

        return listadelcombo,id_campo

    def enontrarArticulo():
        sqlbusqueda = 'SELECT * FROM articulos WHERE CodigoBarras = ' + str(codigoBarrasVar.get())
        cur.execute(sqlbusqueda)
        Resultado = cur.fetchall()

        if len(Resultado) == 1:
            for ind in Resultado:
                protupla = []
                for i in range(1, len(ind)):
                    protupla.append(ind[i])
                articuloEncontrado = Articulos.Articulos(tuple(protupla))
        else:
            articuloEncontrado = 0

        return articuloEncontrado

    def altaArticulo():
        articuloEcontrar = enontrarArticulo()
        if articuloEcontrar == 0:
            codigoBarras_input.config(state='disabled')
            validacion = False
            if ValidarRazonSocial(ArticulosVent,nombre_input):
                nombre_input.config(state='disabled')
                nombre_input.config(bg='snow')
                nombreArticulo = nombreVar.get().upper()

                idRubro = buscarRubroDetalle()
                costo = costoVar.get()
                preciofinal = precioFinal_input.get()
                idProveedor = buscarProveedorPorRazonSocial()
                ultimoPrecio = ultimoPrecio_input.get()

                ArticuloAlta = [codigoBarrasVar.get(),nombreArticulo,idRubro,costo,preciofinal,idProveedor,ultimoPrecio]

                if messagebox.askquestion(f'Alta Articulos',f'Desea ingresar el Stock Inicial del Articulo {nombreArticulo}?') == 'yes':
                    #ejecutar stock inicial del menu Stock
                    StockMenu.menuStock('StockInicial')
                else:
                    for i in range(0,3):
                        ArticuloAlta.append(0)

                if messagebox.askquestion(f'Alta Articulos',f'Esta seguro de CARGAR el Articulo {nombreArticulo} con los siguientes datos?\n'
                                                            f'\n'
                                                            f'Codigo de Barras: {codigoBarrasVar.get()}\n'
                                                            f'Rubro: {idRubrosVar.get()}\n'
                                                            f'Proveedor: {ProveedoresVar.get()}\n') == 'yes':

                    ArticuloAlta = Articulos.Articulos(list(ArticuloAlta))
                    ArticuloAlta.altaArticulo()
                    dbPk.commit()
                    messagebox.showinfo(f'Alta Articulo {nombreArticulo}', f'La carga del articulo {nombreArticulo} ha sido EXITOSA')
                    del ArticuloAlta
                    limpiarvar()
                    limpiarCampos()

                else:
                    messagebox.showwarning(f'Alta Articulo {nombreArticulo}', f'La carga del articulo {nombreArticulo} ha sido CANCELADA')

                if messagebox.askquestion(f'Alta Articulos',f'Desea cargar un nuevo Articulo?') == 'yes':  
                    limpiarvar()
                    limpiarCampos()
                    componenteshabilitar('disabled')
                    codigoBarras_input.config(state='normal')
                    codigoBarras_input.delete(0,tk.END)
                    codigoBarras_input.select_range(0, tk.END)
                    ArticulosVent.focus()
                else:
                    ArticulosVent.destroy()
            else:
                nombre_input.config(bg='lemon chiffon')
                nombre_input.focus()
        else:
            if messagebox.askquestion(f'Alta Articulos',f'El Codigo de Barras ya existe en la base para el Articulo:\n'
                                                        f'Articulo: {articuloEcontrar.nombre}\n'
                                                        f'\n'
                                                        f'Desea cargar un nuevo Articulo?') == 'yes':
                limpiarvar()
                limpiarCampos()
                componenteshabilitar('disabled')
                codigoBarras_input.config(state='normal')
                codigoBarras_input.delete(0, tk.END)
                codigoBarras_input.select_range(0, tk.END)
                ArticulosVent.focus()
            else:
                ArticulosVent.destroy()

    def eliminarArticulo():
        articuloeliminar = enontrarArticulo()
        if messagebox.askquestion('Eliminar Articulo',f'Esta seguro de dar de baja el Articulo?\n '
                                                      f'Nombre: {articuloeliminar.nombre}') == 'yes':
            articuloeliminar.buscarId()
            idEliminar = articuloeliminar.idArticulos
            messagebox.showinfo('Eliminar Articulo',f'El articulo {articuloeliminar.nombre} se ha ELIMINADO con EXITO')
            articuloeliminar.borrarArticulos(idEliminar)
            dbPk.commit()
        else:
            messagebox.showwarning('Eliminar Articulo', f'Se ha CANCELADO la baja del articulo {articuloeliminar.nombre}')
        del articuloeliminar
        limpiarvar()
        limpiarCampos()
        codigoBarras_input.select_range(0, tk.END)
        ArticulosVent.destroy()

    def actualizarArticulos():
        articuloOriginal = enontrarArticulo()
        if ValidarRazonSocial(ArticulosVent, nombre_input):
            nombre_input.config(state='disabled')
            nombre_input.config(bg='snow')
            nombreArticulo = nombreVar.get().upper()

            idRubro = buscarRubroDetalle()
            costo = costoVar.get()
            preciofinal = precioFinal_input.get()
            idProveedor = buscarProveedorPorRazonSocial()
            ultimoPrecio = ultimoPrecio_input.get()

            articuloModificado = [codigoBarrasVar.get(), nombreArticulo, idRubro, costo, preciofinal, idProveedor,
                            ultimoPrecio,articuloOriginal.ultPrecio,articuloOriginal.stock,articuloOriginal.precioFinal]

            if messagebox.askquestion(f'Modificar Articulo {articuloOriginal.nombre}', f'Esta seguro de Modificar el Articulo?\n '
                                                           f'Nombre Anterior: {articuloOriginal.nombre}   Nombre Actualizar: {nombreVar.get()}\n') == 'yes':
                articuloOriginal.buscarId()
                idActualizar = articuloOriginal.idArticulos
                articuloActualizar = Articulos.Articulos(tuple(articuloModificado))
                # articuloActualizar.idArticulos = idActualizar
                messagebox.showinfo(f'Modificar Articulo {articuloActualizar.nombre}', f'El articulo {articuloActualizar.nombre} se ha MODIFICADO con EXITO')
                articuloActualizar.modificaArticulo(idActualizar)
                dbPk.commit()
                del articuloOriginal
                del articuloActualizar
            else:
                messagebox.showwarning(f'Modificar Articulo {articuloActualizar.nombre}',
                                       f'Se ha CANCELADO la modificacion del articulo {articuloActualizar.nombre}')

        if messagebox.askquestion(f'Modificacion de Articulos','Desea Modificar otro articulo?')== 'yes':
            componenteshabilitar('disabled')
            deshabilitarbotones('disabled')
            boton_Buscar.config(state='normal')
            limpiarvar()
            limpiarCampos()
            codigoBarras_input.config(state='normal')
            codigoBarras_input.select_range(0, tk.END)
        else:
            ArticulosVent.destroy()

    def BuscarNombre():
        tabla = 'articulos'

        Articulos_Campos = (
        'id_Articulo', 'CodigoBarras', 'Nombre', 'id_Rubro', 'CostoUnitario', 'PrecioFinal', 'id_Proveedor',
        'UltimoPrecio', 'Stock_Minimo',
        'Stock_Maximo', 'Stock')

        sqlConsulta = 'SELECT a.id_Articulo, a.CodigoBarras, a.Nombre, b.Detalle, a.CostoUnitario, a.PrecioFinal, ' \
                 'c.RazonSocial, a.ultimoPrecio, a.Stock_Minimo, a.Stock_Maximo, a.Stock FROM ' + tabla + \
                 ' a INNER JOIN rubros b ON b.id_Rubro=a.id_Rubro INNER JOIN proveedores c ON a.id_Proveedor=c.id_Proveedor ' \
                 'WHERE a.Nombre LIKE \"%' + nombreVar.get() + '%\"'
        cur.execute(sqlConsulta)
        resultado = cur.fetchall()

        if len(resultado) < 1:
            messagebox.showwarning('Atencion', 'No se Articulos con el Nombre ingresos.')
            ArticulosVent.focus()
            nombre_input.delete(0,tk.END)
            nombre_input.select_range(0,tk.END)
            nombre_input.focus()
        else:
            Articulos_AnchoCampo = (10, 20, 40, 30, 15, 13, 40, 14, 14, 14, 7)
            tablaNombre = VentanaGrilla.GrillaTabla(tabla,Articulos_Campos,Articulos_AnchoCampo, sqlConsulta)
            tablaNombre.mainloop()

    def BuscarPorRubro():
        id = buscarRubroDetalle()
        tabla = 'articulos'

        Articulos_Campos = (
        'id_Articulo', 'CodigoBarras', 'Nombre', 'id_Rubro', 'CostoUnitario', 'PrecioFinal', 'id_Proveedor',
        'UltimoPrecio', 'Stock_Minimo',
        'Stock_Maximo', 'Stock')

        sqlConsulta = 'SELECT a.id_Articulo, a.CodigoBarras, a.Nombre, b.Detalle, a.CostoUnitario, a.PrecioFinal, ' \
                 'c.RazonSocial, a.ultimoPrecio, a.Stock_Minimo, a.Stock_Maximo, a.Stock FROM ' + tabla + \
                 ' a INNER JOIN rubros b ON b.id_Rubro=a.id_Rubro INNER JOIN proveedores c ON a.id_Proveedor=c.id_Proveedor ' \
                 'WHERE a.id_rubro =' + str(id)
        cur.execute(sqlConsulta)
        resultado = cur.fetchall()

        if len(resultado)< 1:
            messagebox.showwarning('Atencion', 'No se encontraron Articulos en el Rubro Seleccionado.')
            ArticulosVent.focus()
            idRubros_combo.current(0)
            idRubros_combo.focus()
        else:
            Articulos_AnchoCampo = (10, 20, 40, 30, 15, 13, 40, 14, 14, 14, 7)
            tablaNombre = VentanaGrilla.GrillaTabla(tabla,Articulos_Campos,Articulos_AnchoCampo, sqlConsulta)
            tablaNombre.mainloop()

    def BuscarPorProveddor():
        id = buscarProveedorPorRazonSocial()
        tabla = 'articulos'

        Articulos_Campos = (
        'id_Articulo', 'CodigoBarras', 'Nombre', 'id_Rubro', 'CostoUnitario', 'PrecioFinal', 'id_Proveedor',
        'UltimoPrecio', 'Stock_Minimo',
        'Stock_Maximo', 'Stock')

        sqlConsulta = 'SELECT a.id_Articulo, a.CodigoBarras, a.Nombre, b.Detalle, a.CostoUnitario, a.PrecioFinal, ' \
                 'c.RazonSocial, a.ultimoPrecio, a.Stock_Minimo, a.Stock_Maximo, a.Stock FROM ' + tabla + \
                 ' a INNER JOIN rubros b ON b.id_Rubro=a.id_Rubro INNER JOIN proveedores c ON a.id_Proveedor=c.id_Proveedor ' \
                 'WHERE a.id_Proveedor =' + str(id)
        cur.execute(sqlConsulta)
        resultado = cur.fetchall()

        if len(resultado)< 1:
            messagebox.showwarning('Atencion', 'No se encontraron Articulos del Proveedor Seleccionado.')
            ArticulosVent.focus()
            proveedores_combo.current(0)
            proveedores_combo.focus()
        else:
            Articulos_AnchoCampo = (10, 20, 40, 30, 15, 13, 40, 14, 14, 14, 7)
            tablaNombre = VentanaGrilla.GrillaTabla(tabla,Articulos_Campos,Articulos_AnchoCampo, sqlConsulta)
            tablaNombre.mainloop()

####VENTANA ARTICULOS
    ArticulosVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idClienteVent = ClienteVent.winfo_id()
    ArticulosVent.title('Tech-Hard - Articulos')  # pone titulo a la ventana principal
    ArticulosVent.geometry('500x400')  # Tamaño en pixcel de la ventana
    ArticulosVent.iconbitmap('imagenHT.ico')  # icono
    ArticulosVent.minsize(500, 400)
    ArticulosVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar

    framecampoArticulos = tk.Frame(ArticulosVent)
    framecampoArticulos.config(width=500, height=400)
    framecampoArticulos.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoArticulos.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoArticulos.config(bd=25)  # tamano del borde en pixeles
    framecampoArticulos.pack(fill='x')  # ancho como el padre
    framecampoArticulos.pack(fill='y')  # alto igual que el padre
    framecampoArticulos.pack(fill='both')  # ambas opciones
    framecampoArticulos.pack(fill='both', expand=1)  # expandirese para ocupar el espacio


    def config_label(mi_label, fila):
        espaciado_labels = {'column': 50, 'sticky': 'e', 'padx': 10, 'pady': 10}
        # color_labels ={'bg':color_fondo, 'fg':color_letra,'font':fuente}
        mi_label.grid(row=fila, **espaciado_labels)
        # mi_label.config(**color_labels)

    codigoBarrasVar = tk.IntVar()
    nombreVar = tk.StringVar()
    idRubrosVar = tk.StringVar()
    ProveedoresVar = tk.StringVar()
    costoVar = tk.DoubleVar()
    precioFinaVar = tk.DoubleVar()
    ultimoPrecioVar = tk.DoubleVar()
    # stockVar = tk.IntVar()
    # stockMinVar = tk.IntVar()
    # stockMaxVar = tk.IntVar()

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
    # label/entry/botones

    codigoBarras_label = tk.Label(framecampoArticulos, text='Codigo de Barras')
    config_label(codigoBarras_label, 3)

    codigoBarras_input = tk.Entry(framecampoArticulos, width=20, justify=tk.RIGHT, textvariable=codigoBarrasVar)
    codigoBarras_input.grid(row=3, column=51, padx=10, pady=10,sticky='w')
    codigoBarras_input.delete(0, tk.END)
    codigoBarras_input.select_range(0, tk.END)
    codigoBarras_input.focus()
    codigoBarras_input.bind('<Return>',buscarCodigoBarrasEnter) #crear funcion evento


    nombre_label = tk.Label(framecampoArticulos, text='Nombre')
    config_label(nombre_label, 4)
    nombre_input = tk.Entry(framecampoArticulos, width=40, textvariable=nombreVar)
    nombre_input.grid(row=4, column=51, padx=10, pady=10, sticky='w')


    idRubro_label = tk.Label(framecampoArticulos, text='Rubro')
    config_label(idRubro_label, 5)
    idRubro = listarcombo('Rubros', 'Detalle')
    idRubros_combo = ttk.Combobox(framecampoArticulos, width=40, state='readonly', textvariable=idRubrosVar,
                                     values=idRubro[0])  # ya que solo puede seleccionar los rubros
    idRubros_combo.grid(row=5, column=51, padx=10, pady=10, sticky='w')
    idRubros_combo.current(0)


    proveedores_label = tk.Label(framecampoArticulos, text='Proveedor')
    config_label(proveedores_label, 6)
    proveedores = listarcombo('Proveedores', 'RazonSocial')
    proveedores_combo = ttk.Combobox(framecampoArticulos, width=40, state='readonly', textvariable=ProveedoresVar,
                                     values=proveedores[0])  # ya que solo puede seleccionar los proveedores
    proveedores_combo.grid(row=6, column=51, padx=10, pady=10, sticky='w')
    proveedores_combo.current(0)

    costo_label = tk.Label(framecampoArticulos, text='Costo')
    config_label(costo_label, 7)
    costo_input = tk.Entry(framecampoArticulos, width=20, textvariable=costoVar)
    costo_input.grid(row=7, column=51, padx=10, pady=10, sticky='w')

    precioFinal_label = tk.Label(framecampoArticulos, text='Precio Final')
    config_label(precioFinal_label, 8)
    precioFinal_input = tk.Entry(framecampoArticulos, width=20, textvariable=precioFinaVar)
    precioFinal_input.grid(row=8, column=51, padx=10, pady=10, sticky='w')

    ultimoPrecio_label = tk.Label(framecampoArticulos, text='Ultimo Precio')
    config_label(ultimoPrecio_label, 9)
    ultimoPrecio_input = tk.Entry(framecampoArticulos, width=20, textvariable=ultimoPrecioVar)
    ultimoPrecio_input.grid(row=9, column=51, padx=10, pady=10, sticky='w')
    

# FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesArticulos = tk.Frame(ArticulosVent)
    framebotonesArticulos.pack()

    boton_Alta = tk.Button(framebotonesArticulos, text='Alta', command=altaArticulo)
    boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)

    boton_Buscar = tk.Button(framebotonesArticulos, text='Buscar', command=buscarCodigoBarras)
    boton_Buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesArticulos, text='Actualizar', command=actualizarArticulos)
    boton_Actualizar.grid(row=0, column=3, padx=5, pady=10, ipadx=7)

    boton_Eliminar = tk.Button(framebotonesArticulos, text='Eliminar', command=eliminarArticulo)
    boton_Eliminar.grid(row=0, column=4, padx=5, pady=10, ipadx=7)

    boton_Stock = tk.Button(framebotonesArticulos, text='Stock')
    boton_Stock.grid(row=0, column=5, padx=5, pady=10, ipadx=7)

    if opcion == 'Alta':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
        codigoBarras_input.config(state='normal')
        codigoBarras_input.select_range(0, tk.END)
        codigoBarras_input.focus()

    elif opcion == 'Baja':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
        codigoBarras_input.config(state='normal')
        codigoBarras_input.select_range(0, tk.END)
        codigoBarras_input.focus()

    elif opcion == 'Modificacion':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        limpiarCampos()
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

    elif opcion == 'BuscarProveedor':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal',command=BuscarPorProveddor) # cambiar comman para buscar por proveedor armar funcion
        proveedores_combo.bind('<<ComboboxSelected>>', buscarProveedor)
        limpiarCampos()
        proveedores_combo.config(state='normal')
        proveedores_combo.select_range(0, tk.END)
        proveedores_combo.current(0)
        proveedores_combo.focus()

    elif opcion == 'BuscarNombre':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal', command=BuscarNombre) # cambiar comman para buscar por nombre armar funcion
        nombre_input.bind('<Return>',buscarNombreEnter)
        limpiarCampos()
        nombre_input.config(state='normal')
        nombre_input.select_range(0, tk.END)
        nombre_input.focus()

    elif opcion == 'BuscarRubro':
        componenteshabilitar('disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal', command=BuscarPorRubro) # cambiar comman para buscar por rubro armar funcion
        idRubros_combo.bind('<<ComboboxSelected>>',buscarRubro)
        limpiarCampos()
        idRubros_combo.config(state='normal')
        idRubros_combo.select_range(0, tk.END)
        idRubros_combo.current(0)
        idRubros_combo.focus()