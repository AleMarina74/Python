#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from os import curdir
from tkinter import messagebox
from tkinter import ttk
import Proveedores
import TelProveedores
import mariadb
import PkUtilidades

import re


dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit=True
)
cur = dbPk.cursor()


TelProveedores_Campos = ('CUIT','Telefono','Area','Contacto')
CamposInt = (0)

def menuTelefonos(cuit,tel):

    def limpiarvar():
        CUITVar.set(0)
        telefonoVar.set('')
        telefonosVar.set('')
        areaVar.set('')
        contactoVar.set('')

    def deshabilitarbotones(valor):
        boton_Alta.config(state=valor)
        # boton_Buscar.config(state=valor)
        boton_Actualizar.config(state=valor)
        boton_Eliminar.config(state=valor)

    def limpiarCampos():
        telefono_input.delete(0,tk.END)
        telefonos_combo.delete(0,tk.END)
        area_input.delete(0,tk.END)
        contacto_input.delete(0,tk.END)


###VALIDACIONES
    def Validartelefono(VentanaPadre, componente):
        while True:
            try:
                validacion = True
                varingresada = str(componente.get())

                if len(varingresada) < 2:
                    messagebox.showerror('Validacion Campo', f'Debe ingresar un telefono Valido')
                    componente.select_range(0, tk.END)
                    componente.focus()
                    VentanaPadre.focus()
                    validacion = False
                elif varingresada == '':
                    validacion = True
                else:
                    espacio = 0
                    for i in varingresada:
                        if i == ' ':
                            espacio = 1
                            break
                    if espacio == 0:
                        validacion = True
                    else:
                        messagebox.showerror('Validacion Campo', f'No debe haber espacios en el numero de telefono')
                        telefonoVar.set(telefonosVar.get().strip())
                        componente.select_range(0, tk.END)
                        componente.focus()
                        VentanaPadre.focus()
                        validacion = False

            except:
                messagebox.showerror('Validacion Campo',f'Debe ingresar un Campo Valido')
                componente.delete(0, tk.END)
                componente.select_range(0, tk.END)
                componente.focus()
                VentanaPadre.focus()
                validacion = False

            finally:
                return validacion
    
####Funciones de Botones
    
    def buscarCUIT():

        if Validartelefono(TelProveedorVent,cuit_input):
            buscacuit = CUITVar.get()

            if buscacuit < 1 or buscacuit > 99999999999:
                messagebox.showerror('Verificacion de Datos', 'Debe ingresar un numero valido de CUIT')
                TelProveedorVent.focus()
                cuit_input.delete(0,tk.END)
                cuit_input.select_range(0,tk.END)
                cuit_input.focus()
            else:
                if PkUtilidades.validador_cuit(buscacuit):
                    sqlbusqueda='SELECT * FROM proveedores WHERE CUIT = ' +str(buscacuit)
                    cur.execute(sqlbusqueda)
                    Resultado = cur.fetchall()

                    if len(Resultado) > 0:
                        protupla = []
                        for ind in Resultado:
                            for i in range(1,len(ind)):
                                protupla.append(ind[i])
                            proveedorEncontrado = Proveedores.Proveedores(tuple(protupla))
                        if opcion == 'Baja':
                            TelProveedorEncontrado = buscarTelefonos()
                            if len(TelProveedorEncontrado[0]) > 0:
                                llenarComboTelefonos()
                                telefonos_combo.config(state='readonly')
                                telefonos_combo.current(0)

                                boton_Eliminar.config(state='normal')
                                boton_Eliminar.focus()
                                del Resultado
                            else:
                                telefono_combos['values']=('Sin_Telefonos')
                                messagebox.showwarning('Telefonos Proveedor',f'El Proveedor con CUIT {proveedorEncontrado.cuit}\n'
                                                                             f'no posee telefonos en la base.\n'
                                                                             f'\n'
                                                                             f'NO SE PUEDEN ELIMINAR TELEFONOS DEL PROVEEDOR')
                                TelProveedorVent.destroy()

                        elif opcion == 'Alta':
                            TelProveedorEncontrado = buscarTelefonos()
                            if len(TelProveedorEncontrado) > 0:
                                llenarComboTelefonos()
                            boton_Alta.config(state='normal')
                            telefonos_combo.config(state='readonly')
                            if TelProveedorEncontrado != 0:
                                telefonos_combo.current(0)
                            telefono_input.focus()
                            del Resultado

                        elif opcion == 'Modificacion':
                            TelProveedorEncontrado = buscarTelefonos()
                            if len(TelProveedorEncontrado) > 0:
                                llenarComboTelefonos()
                                telefonos_combo.config(state='readonly')
                                telefonos_combo.current(0)
                                areaVar.set(TelProveedorEncontrado[1][0])
                                contactoVar.set(TelProveedorEncontrado[2][0])
                                telefonoVar.set(telefonosVar.get())
                            else:
                                telefonos_combo['values'] = ('Sin_Telefonos')

                            boton_Actualizar.config(state='normal')
                            telefono_input.config(state='normal')
                            area_input.config(state='normal')
                            contacto_input.config(state='normal')

                    else:
                        messagebox.showwarning('Telefonos Proveedor',f'El CUIT ingresado del proveedor no se encuentra en nuestra base de datos\n'
                                                                        f'Corrobore los datos o de de alta al Proveedor')
                        TelProveedorVent.destroy()
                else:
                    if messagebox.askquestion('Validacion',f'El numero ingresado no es un CUIT Valido\n'
                                                           f'\n'
                                                           f'Desea ingresar otro Nro de CUIT?') == 'yes':
                        TelProveedorVent.focus()
                        cuit_input.delete(0, tk.END)
                        cuit_input.select_range(0, tk.END)
                        cuit_input.focus()
                    else:
                        TelProveedorVent.destroy()


        else:
            del Resultado
            TelProveedorVent.focus()
            cuit_input.delete(0, tk.END)
            cuit_input.select_range(0, tk.END)
            cuit_input.focus()

    def encontrarProveedor():
        if PkUtilidades.validador_cuit(CUITVar.get()):

            sqlbusqueda = 'SELECT * FROM proveedores WHERE CUIT = ' + str(CUITVar.get())
            cur.execute(sqlbusqueda)
            Resultado = cur.fetchall()

            if len(Resultado) == 1:
                for ind in Resultado:
                    protupla = []
                    for i in range(1, len(ind)):
                        protupla.append(ind[i])
                    proveedorEncontrado = Proveedores.Proveedores(tuple(protupla))

            return proveedorEncontrado
        else:
            if messagebox.askquestion('Validacion', f'El numero de cuit ingresado no es valido\n'
                                                    f'\n'
                                                    f'Desea ingresar otro Nro. de CUIT?') == 'yes':
                TelProveedorVent.focus()
                limpiarvar()
                limpiarCampos()
                cuit_input.select_range(0, tk.END)
            else:
                TelProveedorVent.destroy()

    def seleccionTelefono(event):
        buscarTel = buscarTelefono(telefonosVar.get())

        telProveedorseleccion = buscarTelefonos()
        indice = telefonos_combo.current()
        telefonoVar.set(telefonosVar.get())
        areaseleccionada = telProveedorseleccion[1][indice]
        contactoSeleccionado = telProveedorseleccion[2][indice]

        # buscarTel._idTel= telProveedorseleccion[3][indice]
        areaVar.set(areaseleccionada)
        contactoVar.set(contactoSeleccionado)


    def buscarTelefono(telefono):
        sqlbuscaTel = 'SELECT * FROM telproveedores WHERE CUIT=' + str(CUITVar.get()) + ' AND Telefono = \"'+str(telefono)+'\"'
        cur.execute(sqlbuscaTel)
        Resultado = cur.fetchall()

        if len(Resultado) == 1:
            for ind in Resultado:
                telProveedorEncontrado = TelProveedores.TelProveedores(ind[1],ind[2],ind[3],ind[4])
                telProveedorEncontrado._idTel = ind[0]
        else:
            telProveedorEncontrado = 0

        return telProveedorEncontrado

    def buscarTelefonos():
        sqlbuscaTel = 'SELECT * FROM telproveedores WHERE CUIT=' + str(CUITVar.get())
        cur.execute(sqlbuscaTel)
        Resultado = cur.fetchall()
        indiceTelProveedor=[]
        TelProveedor = []
        AreaProveedor =[]
        ContactoProveedor =[]

        if len(Resultado) >0:
            for ind in Resultado:
                indiceTelProveedor.append(ind[0])
                TelProveedor.append(ind[2])
                AreaProveedor.append(ind[3])
                ContactoProveedor.append(ind[4])

        return TelProveedor,AreaProveedor,ContactoProveedor, indiceTelProveedor

    def llenarComboTelefonos():
        TelefonosProveedor = buscarTelefonos()
        if len(TelefonosProveedor[0])>0:
            telefonos_combo['values'] = tuple(TelefonosProveedor[0])

    def altaTelefono():
        if Validartelefono(TelProveedorVent,telefono_input):
            buscarTelefono = buscarTelefono(telefonoVar.get()) #busco si existe en la base

            if buscarTelefono == 0: #hago el alta del telefono
                telAlta = TelProveedores.TelProveedores(CUITVar.get(),telefonoVar.get(),areaVar.get(),contactoVar.get())
                if messagebox.askquestion(f'Alta de Telefono del Proveedor CUIT Nº {CUITVar.get()}',
                                          f'Esta seguro que desea Cargar el Telefono: {telefonoVar.get()}?') == 'yes':
                    telAlta.altaTelefono()
                    dbPk.commit()
                    if messagebox.askquestion(f'Alta de Telefono del Proveedor CUIT Nº {CUITVar.get()}',
                                              f'Desea cargar otro Telefono del mismo Proveedor?') == 'yes':
                        TelProveedorVent.focus()
                        cuitaux = CUITVar.get()
                        limpiarvar()
                        CUITVar.set(cuitaux)
                        llenarComboTelefonos()
                        telefonos_combo.current(0)
                        telefonos_combo.config(state='readonly')
                        telefono_input.focus()

            else:
                if messagebox.askquestion(f'Telefonos del CUIT Nº: {CUITVar.get()}',f'El telefono ingresado ya se encuentra en el Proveedor\n'
                                                                                    f'\n'
                                                                                    f'Desea Ingresar Otro Telefono del mismo Proveedor?') == 'yes':
                    TelProveedorVent.focus()
                    CUITVar.set(cuit)
                else:
                    TelProveedorVent.destroy()

    def actualizarTelefono():
        if Validartelefono(TelProveedorVent,telefono_input):
            buscarTel = buscarTelefono(telefonoVar.get())
            if buscarTel != 0:
                telNuevo = TelProveedores.TelProveedores(CUITVar.get(),telefonoVar.get(),areaVar.get(),contactoVar.get())
                telNuevo._idTel = buscarTel._idTel
                if messagebox.askquestion(f'Telefonos Proveedor CUIT Nº: {CUITVar.get()}',f'Esta seguro de modificar el siguiente telefono del Proveedor?\n'
                                                                                          f'\n'
                                                                                          f'Telefono Anterior: {buscarTel.telefono}    Telefono Nuevo: {telNuevo.telefono}\n'
                                                                                          f'\n'
                                                                                          f'Area Anterior: {buscarTel.area}    Area Nueva: {telNuevo.area}\n'
                                                                                          f'\n'
                                                                                          f'Contacto Anterior: {buscarTel.contacto}    Contacto Nuevo: {telNuevo.contacto}') == 'yes':
                    telNuevo.modificaTelefono(telNuevo.idTel)
                    messagebox.showinfo(f'Telefonos Proveedor CUIT Nº: {CUITVar.get()}','Registro actualizado con exito')
                    dbPk.commit()
                else:
                    messagebox.showinfo(f'Telefonos Proveedor CUIT Nº: {CUITVar.get()}', 'No se ha actualizado el registro del telefono del Proveedor.')
                    TelProveedorVent.focus()
                    telefono_input.delete(0,tk.END)
                    telefono_input.focus()
            else:
                if messagebox.askquestion(f'Telefonos Proveedor CUIT Nº: {CUITVar.get()}', 'No se puede actualizar el telefono del Proveedor\n'
                                                                                           'El mismo no esta registrado en la base\n'
                                                                                           '\n'
                                                                                           'Desea dar Cargar el nuevo Telefono?') == 'yes':
                    altaTelefono()
                else:
                    TelProveedorVent.destroy()
        if messagebox.askquestion(f'Telefono Proveedor CUIT Nº: {CUITVar.get()}', 'Desea modificar otro telefono del Proveedor?') == 'yes':
            dbPk.commit()
            limpiarvar()
            CUITVar.set(telNuevo.CUIT)
            llenarComboTelefonos()
            TelProveedorVent.focus()
            telefono_input.delete(0, tk.END)
            telefono_input.focus()
        else:
            TelProveedorVent.destroy()



    def eliminarTelefono():
        buscarTel = buscarTelefono(telefonosVar.get())
        buscarTel.borrarUnTelefono(buscarTel.idTel)
        dbPk.commit()

###VENTANA TELEFONOS PROVEEDOR
    TelProveedorVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idClienteVent = ClienteVent.winfo_id()
    TelProveedorVent.title('Tech-Hard - Telefonos de Proveedores')  # pone titulo a la ventana principal
    TelProveedorVent.geometry('600x400')  # Tamaño en pixcel de la ventana
    TelProveedorVent.iconbitmap('imagenHT.ico')  # icono
    TelProveedorVent.minsize(600, 400)
    TelProveedorVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar

####Frame Telefonos del proveedor
    framecampoTelProveedor = tk.Frame(TelProveedorVent)
    framecampoTelProveedor.config(width=600, height=400)
    framecampoTelProveedor.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoTelProveedor.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoTelProveedor.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoCli.pack(anchor=SE) # lo ubica abajo a la derecha
    framecampoTelProveedor.pack(fill='x')  # ancho como el padre
    framecampoTelProveedor.pack(fill='y')  # alto igual que el padre
    # framecampoTelProveedor.pack(fill='both')  # ambas opciones
    framecampoTelProveedor.pack(fill='both', expand=1)  # expandirese para ocupar el espacio


    def config_label(mi_label, fila):
        espaciado_labels = {'column': 50, 'sticky': 'e', 'padx': 10, 'pady': 10}
        mi_label.grid(row=fila, **espaciado_labels)

####VARIABLES
    CUITVar = tk.IntVar()
    telefonoVar = tk.StringVar()
    telefonosVar = tk.StringVar()
    areaVar = tk.StringVar()
    contactoVar = tk.StringVar()

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
##### label/entry/botones

    cuit_label = tk.Label(framecampoTelProveedor, text='CUIT')
    config_label(cuit_label, 3)

    cuit_input = tk.Entry(framecampoTelProveedor, width=11 ,justify=tk.RIGHT, textvariable=CUITVar)
    cuit_input.grid(row=3, column=51, padx=10, pady=10, sticky='w')
    cuit_input.delete(0, tk.END)
    cuit_input.select_range(0, tk.END)
    cuit_input.focus()

    boton_BuscarCuit = tk.Button(framecampoTelProveedor, text='Buscar', command=buscarCUIT)
    boton_BuscarCuit.grid(row=3, column=100, padx=5, pady=10, ipadx=7)


    telefono_label = tk.Label(framecampoTelProveedor, text='Telefono')
    config_label(telefono_label, 4)

    telefono_input = tk.Entry(framecampoTelProveedor, width=20, textvariable=telefonoVar)
    telefono_input.grid(row=4, column=51, padx=10, pady=10, sticky='w')

    telefonos_label = tk.Label(framecampoTelProveedor, text='Telefonos')
    config_label(telefonos_label, 5)

    telefonos_combo = ttk.Combobox(framecampoTelProveedor, width=20, textvariable=telefonosVar)
    telefonos_combo.grid(row=5, column=51, padx=10, pady=10,sticky='w')
    telefonos_combo.bind('<<ComboboxSelected>>',seleccionTelefono)

    # boton_Buscartelefono = tk.Button(framecampoTelProveedor, text='Agregar Telefono',command=agregarTelefono)
    # boton_Buscartelefono.grid(row=5, column=100, padx=5, pady=10, ipadx=7)

    area_label = tk.Label(framecampoTelProveedor, text='Area')
    config_label(area_label, 6)

    area_input = tk.Entry(framecampoTelProveedor, width=40, textvariable=areaVar)
    area_input.grid(row=6, column=51, padx=10, pady=10, sticky='w')

    contacto_label = tk.Label(framecampoTelProveedor, text='Contacto')
    config_label(contacto_label, 7)

    contacto_input = tk.Entry(framecampoTelProveedor, width=40, textvariable=contactoVar)
    contacto_input.grid(row=7, column=51, padx=10, pady=10,sticky='w')


# FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesProv = tk.Frame(TelProveedorVent)
    framebotonesProv.pack()

    boton_Alta = tk.Button(framebotonesProv, text='Alta', command=altaTelefono)
    boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)

    # boton_Buscar = tk.Button(framebotonesProv, text='Buscar')
    # boton_Buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesProv, text='Actualizar', command=actualizarTelefono)
    boton_Actualizar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Eliminar = tk.Button(framebotonesProv, text='Eliminar', command=eliminarTelefono)
    boton_Eliminar.grid(row=0, column=3, padx=5, pady=10, ipadx=7)


    if cuit != 0:
        CUITVar.set(cuit)

        if tel == '':
            opcion = 'Alta'
            telefonoVar.set(tel)

            cuit_input.config(state='disabled')
            boton_BuscarCuit.config(state='disabled')

            llenarComboTelefonos()
            telefonos_combo.config(state='normal')


            deshabilitarbotones('disabled')
            boton_Alta.config(state='normal')

            area_input.delete(0,tk.END)
            contacto_input.delete(0,tk.END)

            telefono_input.select_range(0, tk.END)
            telefono_input.focus()

        else:
            telefonoVar.set(tel)


            cuit_input.config(state='disabled')
            boton_BuscarCuit.config(state='disabled')

            llenarComboTelefonos()


            buscarTel = buscarTelefono(tel)
            if buscarTel == 0:
                opcion = 'Alta'
                telefonos_combo.current(0)
            else:
                opcion = 'Modificacion'
                telefonosVar.set(tel)
                telefonos_combo.set(tel)
                areaVar.set(buscarTel.area)
                contactoVar.set(buscarTel.contacto)

            deshabilitarbotones('disabled')
            boton_Actualizar.config(state='normal')

            telefonos_combo.config(state='readonly')

            area_input.select_range(0, tk.END)
            area_input.focus()

    else:
        opcion = tel
        if opcion == 'Alta':
            deshabilitarbotones('disabled')
            cuit_input.config(state='normal')
            cuit_input.delete(0,tk.END)
            boton_BuscarCuit.config(state='normal')
            telefonoVar.set('')
            limpiarCampos()
            cuit_input.select_range(0, tk.END)
            cuit_input.focus()

        elif opcion == 'Baja':
            deshabilitarbotones('disabled')
            cuit_input.config(state='normal')
            cuit_input.delete(0, tk.END)
            boton_BuscarCuit.config(state='normal')
            telefonoVar.set('')
            limpiarCampos()
            cuit_input.select_range(0, tk.END)
            cuit_input.focus()

        elif opcion == 'Modificacion':
            deshabilitarbotones('disabled')
            cuit_input.config(state='normal')
            cuit_input.delete(0, tk.END)
            boton_BuscarCuit.config(state='normal')
            telefonoVar.set('')
            limpiarCampos()
            cuit_input.select_range(0, tk.END)
            cuit_input.focus()

        # elif opcion == 'Buscar':
        #     deshabilitarbotones('disabled')
        #     cuit_input.config(state='normal')
        #     cuit_input.delete(0, tk.END)
        #     boton_BuscarCuit.config(state='normal')
        #     telefonoVar.set('')
        #     limpiarCampos()
        #     cuit_input.select_range(0, tk.END)
        #     cuit_input.focus()