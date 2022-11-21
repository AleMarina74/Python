#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from os import curdir
from tkinter import messagebox
from tkinter import ttk
import Proveedores
import TelProveedores
import TelProveedoresMenu
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

Proveedores_Campos = ('id_Proveedor', 'CUIT', 'RazonSocial', 'telefono','Direccion','Mail','Id_Iva')
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}\w[.]+\w{2,3}$'
regex2 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

CUITVar = 0
razonSocialVar = ''
telefonoVar = ''
direccionVar = ''
mailVar = ''
id_iva = 0

def listarIdIva():
    global Situacion
    global idsituacion

    listariva = 'SELECT * FROM situacioniva'
    cur.execute(listariva)
    Resultado = cur.fetchall()
    if len(Resultado) > 0:
        Situacion = []
        idsituacion = []
        for ind in Resultado:
            Situacion.append(ind[1])
            idsituacion.append(ind[0])
        return Situacion
    else:
        messagebox.showerror('Error en la base', 'No se ha cargado ningun item en la base')

def buscarsitiva(id):
    buscarid = 'SELECT * FROM situacioniva WHERE id_Iva = '+str(id)
    cur.execute(buscarid)
    Resultado = cur.fetchall()
    if len(Resultado) > 0:
        for ind in Resultado:
            situacion = ind[1]
        return situacion

# def listarRubro():
#     global Rubro
#     global idRubro
#
#     listarrubros = 'SELECT * FROM rubros'
#     cur.execute(listarrubros)
#     Resultado = cur.fetchall()
#     if len(Resultado) > 0:
#         Rubro = []
#         idRubro = []
#         for ind in Resultado:
#             Rubro.append(ind[1])
#             idRubro.append(ind[0])
#         return Rubro
#     else:
#         messagebox.showerror('Error en la base', 'No se ha cargado ningun item en la base de Rubros')

# def buscarRubrodesdeId(id):
#     buscarid = 'SELECT * FROM rubros WHERE id_Rubro = '+str(id)
#     cur.execute(buscarid)
#     Resultado = cur.fetchall()
#     if len(Resultado) > 0:
#         for ind in Resultado:
#             Rubro = ind[1]
#         return Rubro

# ---- MENU CLIENTES
def menuProveedores(opcion):  # opcionmenu seria alta, muestrotodo en blanco y habilito el boton alta

    def limpiarvar():
        CUITVar.set(0)
        razonSocialVar.set('')
        telefonoVar.set('')
        direccionVar.set('')
        mailVar.set('')

    def componenteshabilitar(valor): #Valores 'disabled' o 'normal'

        razonSocial_input.config(state=valor)
        telefono_combo.config(state=valor)
        direccion_input.config(state=valor)
        mail_input.config(state=valor)
        # telefono_combo.config(state=valor)
        idiva_combo.config(state=valor)

    def deshabilitarbotones(valor):
        boton_Alta.config(state=valor)
        boton_Buscar.config(state=valor)
        boton_Actualizar.config(state=valor)
        boton_Eliminar.config(state=valor)

    def limpiarCampos():
        cuit_input.delete(0,tk.END)
        cuit_input.select_range(0,tk.END)
        cuit_input.focus()

        razonSocial_input.delete(0,tk.END)
        telefono_combo.delete(0,tk.END)
        direccion_input.delete(0,tk.END)
        mail_input.delete(0,tk.END)
        idiva_combo.set('Responsable Inscripto')

    def llenarcampos(proveedor):
        razonSocialVar.set(proveedor.nombre)
        # telefonoVar.set(proveedor.telefono)
        direccionVar.set(proveedor.direccion)
        mailVar.set(proveedor.mail)
        idiva_combo.set(buscarsitiva(proveedor.idIva))

    def selecentradas():
        razonSocial_input.delete(0, tk.END)
        telefono_combo.delete(0, tk.END)
        direccion_input.delete(0, tk.END)
        mail_input.delete(0, tk.END)
####EVENTOS
    def buscarCUITEvento(event):
        buscarCUIT()

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
                    messagebox.showerror('Validacion Campo', f'Debe ingresar un valor Razon Social Valido')
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
                        # messagebox.showerror('Validacion Campo', f'Debe ingresar una Razon Social')
                        # componente.select_range(0, tk.END)
                        # componente.focus()
                        # VentanaPadre.focus()
                        validacion = True
                    else:
                        validacion = True

            except:
                messagebox.showerror('Validacion Campo',f'Debe ingresar un Campo Valido')
                componente.delete(0, tk.END)
                componente.select_range(0, tk.END)
                componente.focus()
                VentanaPadre.focus()
                validacion = False

            finally:
                return validacion

    def ValidarDireccion(VentanaPadre,componente):
        while True:
            try:
                validacion = True
                varingresada = str(componente.get())

                if len(varingresada) < 2  or varingresada == '':
                    messagebox.showerror('Validacion Campo', f'Debe ingresar un Domicilio Valido\n No acepta caracteres especiales @,*,º\n Vuelva a ingresarlo correctamente.')
                    componente.select_range(0, tk.END)
                    componente.focus()
                    VentanaPadre.focus()
                    validacion = False
                else:
                    espacio = 0
                    for i in varingresada:
                        if i == ' ':
                            espacio = 1
                    if espacio == 0:
                        messagebox.showerror('Validacion Campo', f'Debe ingresar un Domicilio Valido\n No acepta caracteres especiales @,*,º\n Vuelva a ingresarlo correctamente.')
                        componente.select_range(0, tk.END)
                        componente.focus()
                        VentanaPadre.focus()
                        validacion = False
                    else:
                        validacion = True

            except:
                messagebox.showerror('Validacion Campo',f'Debe ingresar una direccion Valido')
                componente.delete(0, tk.END)
                componente.select_range(0, tk.END)
                componente.focus()
                VentanaPadre.focus()
                validacion = False

            finally:
                return validacion

    def ValidarTelefono(VentanaPadre,componente):
        while True:
            try:
                validacion = True
                varingresada = componente.get()

                if varingresada == '':
                    validacion = True
                else:
                    varingresada = int(varingresada)

                    if varingresada < 0 or varingresada > 9999999999:
                        messagebox.showerror('Validacion Campo', f'Debe ingresar un valor numerico de Telefono Valido')
                        componente.delete(0, tk.END)
                        componente.select_range(0, tk.END)
                        componente.focus()
                        VentanaPadre.focus()
                        validacion = False
                    else:
                        validacion = True

            except:
                messagebox.showerror('Validacion Campo', f'Debe ingresar un valor numerico Valido')
                componente.delete(0, tk.END)
                componente.select_range(0, tk.END)
                componente.focus()
                VentanaPadre.focus()
                validacion = False

            finally:
                return validacion


    def ValidarMail(VentanaPadre,componente):
        while True:
            try:
                varingresada = str(componente.get())

                if re.search(regex, varingresada) or re.search(regex2, varingresada):
                    validacion = True
                else:
                    messagebox.showwarning('Validacion Campo', f'Debe ingresar un valor de email Valido')
                    componente.delete(0, tk.END)
                    componente.select_range(0, tk.END)
                    componente.focus()
                    VentanaPadre.focus()
                    validacion = False

            except:
                messagebox.showerror('Validacion Campo', f'Debe ingresar un valor de email Valido')
                componente.delete(0, tk.END)
                componente.select_range(0, tk.END)
                componente.focus()
                VentanaPadre.focus()
                validacion = False

            finally:
                return validacion

### FUNCIONES
    def llenarComboTelefonos():
        TelefonosProveedor = buscarTelefonos()
        telefono_combo['values'] = tuple(TelefonosProveedor)
        if len(TelefonosProveedor)>0:
            telefono_combo.current(0)

    def agregarTelefono():
        ValidarTelefono(ProveedorVent,telefono_combo)
        TelProveedoresMenu.menuTelefonos(CUITVar.get(),telefonoVar.get())

    def buscarTelefonos():
        sqlbuscaTel = 'SELECT * FROM telproveedores WHERE CUIT=' + str(CUITVar.get())
        cur.execute(sqlbuscaTel)
        Resultado = cur.fetchall()
        TelProveedor = []

        if len(Resultado) >0:
            for ind in Resultado:
                TelProveedor.append(ind[2])

        return TelProveedor

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
                ProveedorVent.focus()
                limpiarvar()
                limpiarCampos()
                cuit_input.select_range(0, tk.END)
            else:
                ProveedorVent.destroy()

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

#####FUNCIONES DE BOTONES
    def buscarCUIT():

        if ValidarNumero(ProveedorVent,cuit_input):
            buscacuit = CUITVar.get()

            if buscacuit < 1 or buscacuit > 99999999999:
                messagebox.showerror('Verificacion de Datos', 'Debe ingresar un numero valido de CUIT')
                ProveedorVent.focus()
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
                            llenarcampos(proveedorEncontrado)
                            TelProveedorEncontrado = buscarTelefonos()
                            if len(TelProveedorEncontrado) > 0:
                                llenarComboTelefonos()
                            else:
                                telefono_combo.config(state='disabled')
                                telefono_combo['values']=('Sin_Telefonos')
                                telefono_combo.current(0)
                            boton_Eliminar.config(state='normal')
                            boton_Eliminar.focus()
                            del Resultado
                        elif opcion == 'Alta':
                            messagebox.showwarning('Advertencia',f'El Proveedor ya existe {proveedorEncontrado.cuit}')
                            limpiarvar()
                            limpiarCampos()
                            cuit_input.select_range(0, tk.END)
                            cuit_input.focus()
                            del Resultado
                        elif opcion == 'Modificacion':
                            llenarcampos(proveedorEncontrado)
                            TelProveedorEncontrado = buscarTelefonos()
                            if len(TelProveedorEncontrado) > 0:
                                llenarComboTelefonos()
                            else:
                                telefono_combo.config(state='disabled')

                            boton_Actualizar.config(state='normal')
                            componenteshabilitar('normal')
                            telefono_combo.config(state='readonly')
                            boton_Buscartelefono.config(state='normal',text='Modificar')

                            razonSocial_input.focus()

                        elif opcion == 'BuscarCUIT':
                            llenarcampos(proveedorEncontrado)
                            cuit_input.select_range(0, tk.END)
                            cuit_input.focus()


                    elif len(Resultado) < 1:
                        if opcion == 'Baja' or opcion == 'Modificacion' or opcion == 'BuscarCUIT' or opcion == 'BuscarNombre':
                            messagebox.showwarning('Advertencia', f'No existe el Proveedor Solicitado\n con el CUIT: {buscacuit}')
                            del Resultado
                            ProveedorVent.focus()
                            limpiarCampos()
                            limpiarvar()

                        else: # permito ingresar los datos
                            componenteshabilitar('normal')
                            cuit_input.config(state='disabled')
                            telefono_combo.config(state='normal')
                            boton_Buscartelefono.config(state='normal')
                            boton_Alta.config(state='normal')
                            razonSocial_input.focus()
                            del Resultado
                else:
                    if messagebox.askquestion('Validacion',f'El numero ingresado no es un CUIT Valido\n'
                                                           f'\n'
                                                           f'Desea ingresar otro Nro de CUIT?') == 'yes':
                        ProveedorVent.focus()
                        cuit_input.delete(0, tk.END)
                        cuit_input.select_range(0, tk.END)
                        cuit_input.focus()
                    else:
                        ProveedorVent.destroy()


        else:
            del Resultado
            ProveedorVent.focus()
            cuit_input.delete(0, tk.END)
            cuit_input.select_range(0, tk.END)
            cuit_input.focus()

    def altaProveedor():
        cuit_input.config(state='disabled')
        boton_BuscarCuit.config(state='disabled')
        validacion = False
        proveedorAlta = [CUITVar.get()]
        telefonoagregar = [CUITVar.get()]
        # while validacion == False:
        if ValidarRazonSocial(ProveedorVent,razonSocial_input):
            razonSocial_input.config(bg='snow')
            razonSocial_input.config(state='disabled')
            nombreap = razonSocialVar.get().upper()
            proveedorAlta.append(nombreap)
            if ValidarTelefono(ProveedorVent,telefono_combo):
                telefono_combo.config(background='snow')
                telefono_combo.config(state='disabled')
                telefono = telefonoVar.get()
                telefonoagregar.append(telefono)
                if ValidarDireccion(ProveedorVent,direccion_input):
                    direccion_input.config(bg='snow')
                    direccion_input.config(state='disabled')
                    dire = direccionVar.get().upper()
                    proveedorAlta.append(dire)
                    if ValidarMail(ProveedorVent, mail_input):
                        mail_input.config(bg='snow')
                        mailingreso = mailVar.get().lower()
                        proveedorAlta.append(mailingreso)
                        idiva = idiva_combo.current() + 1
                        proveedorAlta.append(idiva)
                        if messagebox.askquestion(f'Alta Proveedor CUIT Nº: {CUITVar.get()}',
                                                  f'Esta seguro de dar el Alta del Proveedor \n'
                                                  f'\n'
                                                  f'Razon Social: {razonSocialVar.get()}\n'
                                                  f'Telefono: {telefonoVar.get()}\n'
                                                  f'Domicilio: {direccionVar.get()}\n'
                                                  f'mail: {mailVar.get()}\n'
                                                  f'Situacion frente al IVA:{idiva_combo.get()}?') == 'yes':
                            provAlta = Proveedores.Proveedores(tuple(proveedorAlta))
                            provAlta.altaProveedor()
                            dbPk.commit()

                            busquedaTelefono = buscarTelefono(telefonoVar.get())
                            if busquedaTelefono == 0:
                                if telefonoVar.get() != '':
                                    telfonoAlta = TelProveedores.TelProveedores(CUITVar.get(),telefonoVar.get(),'','')
                                    telfonoAlta.altaTelefono()
                                    dbPk.commit()

                            del provAlta
                            limpiarvar()
                            cuit_input.select_range(0, tk.END)
                            validacion = True
                            messagebox.showinfo(f'Alta Proveedor CUIT Nº: {CUITVar.get()}', 'Alta de Proveedor Exitosa')
                        else:
                            busquedaTelefono = buscarTelefono(telefonoVar.get())
                            if busquedaTelefono != 0:
                                busquedaTelefono.borrarUnTelefono(busquedaTelefono.idTel)
                            messagebox.showwarning(f'Alta Proveedor CUIT Nº: {CUITVar.get()}','No se ha registrado el Alta')
                            ProveedorVent.destroy()
                    else:
                        mail_input.config(bg='lemon chiffon')
                        mail_input.select_range(0,tk.END)
                        mail_input.focus()
                        ProveedorVent.focus()

                else:
                    direccion_input.config(bg='lemon chiffon')
                    direccion_input.select_range(0,tk.END)
                    direccion_input.focus()
                    ProveedorVent.focus()

            else:
                telefono_combo.config(background='lemon chiffon')
                telefono_combo.select_range(0,tk.END)
                telefono_combo.focus()
                ProveedorVent.focus()

        else:
            razonSocial_input.config(bg='lemon chiffon')
            razonSocial_input.select_range(0,tk.END)
            razonSocial_input.focus()
            ProveedorVent.focus()


    def eliminarProveedor():
        provelim = encontrarProveedor()
        if messagebox.askquestion('Eliminar Registro',f'Esta seguro de dar de baja al Proveedor?\n '
                                                   f'CUIT: {provelim.cuit} \n'
                                                   f'Razon Social: {provelim.nombre}') == 'yes':
            provelim.borrarProveedor(provelim.cuit)
            dbPk.commit()
            TelefonosProveedor = buscarTelefonos()

            if len(TelefonosProveedor) > 0:
                sqlelimtel = 'DELETE FROM telproveedores WHERE CUIT='+str(CUITVar.get())
                cur.execute(sqlelimtel)
                dbPk.commit()
                if messagebox.askquestion('Eliminar Registros',f'Se han eliminado los telefonos del Proveedor\n'
                                                               f'CUIT: {provelim.cuit} \n'
                                                               f'Razon Social: {provelim.nombre} \n'
                                                               f'\n'
                                                               f'Registro del proveedor eliminado con exito.\n'
                                                               f'\n'
                                                               f'Desea eliminar otro Proveedor?') == 'yes':
                    del provelim
                    limpiarvar()
                    limpiarCampos()
                    cuit_input.select_range(0, tk.END)
                    ProveedorVent.focus()
                else:
                    del provelim
                    ProveedorVent.destroy()
            else:
                if messagebox.askquestion('Eliminar Registros',f'No existen telefonos del Proveedor\n'
                                                               f'CUIT: {provelim.cuit} \n'
                                                               f'Razon Social: {provelim.nombre} \n'
                                                               f'\n'
                                                               f'Registro del proveedor eliminado con exito.\n'
                                                               f'\n'
                                                               f'Desea eliminar otro Proveedor?') == 'yes':
                    del provelim
                    limpiarvar()
                    limpiarCampos()
                    cuit_input.select_range(0, tk.END)
                    ProveedorVent.focus()
                else:
                    del provelim
                    ProveedorVent.destroy()

        else:
            if messagebox.askquestion('Eliminar Registros', f'No se ha eliminado el registro\n'
                                                            f'\n'
                                                            f'Desea eliminar otro Proveedor?') =='yes':
                del provelim
                limpiarvar()
                limpiarCampos()
                cuit_input.select_range(0, tk.END)
                ProveedorVent.focus()
            else:
                del provelim
                ProveedorVent.destroy()


###VENTANA PROVEEDORES
    ProveedorVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    # idClienteVent = ClienteVent.winfo_id()
    ProveedorVent.title('Tech-Hard - Proveedores')  # pone titulo a la ventana principal
    ProveedorVent.geometry('600x400')  # Tamaño en pixcel de la ventana
    ProveedorVent.iconbitmap('imagenHT.ico')  # icono
    ProveedorVent.minsize(600, 400)
    ProveedorVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar
    # Cliente.config(bd=25)
    # Cliente.config(relief='sunken')

    Proveedores_Campos = ('id_Proveedor', 'CUIT', 'RazonSocial', 'telefono','Direccion','Mail','Id_Iva')
    CamposInt = (0, 1, 6)

    framecampoProv = tk.Frame(ProveedorVent)
    # framecampoCli.pack(fill='both')
    # framecampoCli.config(bg='lightblue')
    framecampoProv.config(width=600, height=400)
    framecampoProv.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoProv.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoProv.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoCli.pack(anchor=SE) # lo ubica abajo a la derecha
    framecampoProv.pack(fill='x')  # ancho como el padre
    framecampoProv.pack(fill='y')  # alto igual que el padre
    framecampoProv.pack(fill='both')  # ambas opciones
    framecampoProv.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    # idcliente = tk.IntVar()
    def config_label(mi_label, fila):
        espaciado_labels = {'column': 50, 'sticky': 'e', 'padx': 10, 'pady': 10}
        # color_labels ={'bg':color_fondo, 'fg':color_letra,'font':fuente}
        mi_label.grid(row=fila, **espaciado_labels)
        # mi_label.config(**color_labels)

    CUITVar = tk.IntVar()
    razonSocialVar = tk.StringVar()
    direccionVar = tk.StringVar()
    telefonoVar = tk.StringVar()
    mailVar = tk.StringVar()

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
    # label/entry/botones

    cuit_label = tk.Label(framecampoProv, text='CUIT')
    config_label(cuit_label, 3)

    cuit_input = tk.Entry(framecampoProv, width=11 ,justify=tk.RIGHT, textvariable=CUITVar)
    cuit_input.grid(row=3, column=51, padx=10, pady=10, sticky='w')
    cuit_input.delete(0, tk.END)
    cuit_input.select_range(0, tk.END)
    cuit_input.focus()
    cuit_input.bind('<Return>',buscarCUITEvento)

    # boton_BuscarCuit = tk.Button(framecampoProv, text='Buscar', command=buscarCUIT)
    # boton_BuscarCuit.grid(row=3, column=100, padx=5, pady=10, ipadx=7)
    # # dni_input.insert(tk.END,'')

    nombre_label = tk.Label(framecampoProv, text='Razon Social')
    config_label(nombre_label, 4)

    razonSocial_input = tk.Entry(framecampoProv, width=40, textvariable=razonSocialVar)
    razonSocial_input.grid(row=4, column=51, padx=10, pady=10, sticky='w')

    boton_Buscarnom = tk.Button(framecampoProv, text='Buscar')
    boton_Buscarnom.grid(row=4, column=100, padx=5, pady=10, ipadx=7)

    telefono_label = tk.Label(framecampoProv, text='Telefonos')
    config_label(telefono_label, 5)

    telefono_combo = ttk.Combobox(framecampoProv, width=20, textvariable=telefonoVar)
    telefono_combo.grid(row=5, column=51, padx=10, pady=10,sticky='w')

    boton_Buscartelefono = tk.Button(framecampoProv, text='Agregar Telefono',command=agregarTelefono)
    boton_Buscartelefono.grid(row=5, column=100, padx=5, pady=10, ipadx=7)

    direccion_label = tk.Label(framecampoProv, text='Direccion')
    config_label(direccion_label, 6)
    direccion_input = tk.Entry(framecampoProv, width=40, textvariable=direccionVar)
    direccion_input.grid(row=6, column=51, padx=10, pady=10, sticky='w')

    # telefono_combo = tk.Entry(framecampoProv, textvariable=telefonoVar)
    # telefono_combo.grid(row=6, column=51, padx=10, pady=10)
    # telefono_label = tk.Label(framecampoCli, text='Telefono')
    # config_label(telefono_label, 6)


    mail_input = tk.Entry(framecampoProv, width=40, textvariable=mailVar)
    mail_input.grid(row=7, column=51, padx=10, pady=10,sticky='w')

    mail_label = tk.Label(framecampoProv, text='Mail')
    config_label(mail_label, 7)

    ivasit = listarIdIva()
    idiva_combo = ttk.Combobox(framecampoProv, state='readonly',
                               values=ivasit)  # ya que solo puede seleccionar los tipos de iva
    idiva_combo.grid(row=8, column=51, padx=10, pady=10,sticky='w')
    idiva_combo.set('Responsable Inscripto')
    # print(idiva_combo.current())

    idiva_label = tk.Label(framecampoProv, text='Situacion frente al Iva')
    config_label(idiva_label, 8)



# FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesProv = tk.Frame(ProveedorVent)
    framebotonesProv.pack()

    boton_Alta = tk.Button(framebotonesProv, text='Alta', command=altaProveedor)
    boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)

    boton_Buscar = tk.Button(framebotonesProv, text='Buscar')
    boton_Buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesProv, text='Actualizar')
    boton_Actualizar.grid(row=0, column=3, padx=5, pady=10, ipadx=7)

    boton_Eliminar = tk.Button(framebotonesProv, text='Eliminar', command=eliminarProveedor)
    boton_Eliminar.grid(row=0, column=4, padx=5, pady=10, ipadx=7)

    if opcion == 'Alta':
        componenteshabilitar('disabled')

        boton_Buscarnom.config(state='disabled')
        boton_Buscartelefono.config(state='disabled')
        deshabilitarbotones('disabled')
        limpiarCampos()
        cuit_input.select_range(0, tk.END)
        cuit_input.focus()

    elif opcion == 'Baja':
        componenteshabilitar('disabled')
        boton_Buscartelefono.config(state='disabled')
        boton_Buscarnom.config(state='disabled')
        deshabilitarbotones('disabled')
        limpiarCampos()
        cuit_input.select_range(0, tk.END)
        cuit_input.focus()

    elif opcion == 'Modificacion':
        componenteshabilitar('disabled')
        boton_Buscartelefono.config(state='disabled')
        boton_Buscarnom.config(state='disabled')
        deshabilitarbotones('disabled')
        limpiarCampos()
        cuit_input.select_range(0, tk.END)
        cuit_input.focus()

    elif opcion == 'BuscarDni':
        componenteshabilitar('disabled')

        boton_Buscarnom.config(state='disabled')
        deshabilitarbotones('disabled')
        limpiarCampos()
        cuit_input.select_range(0, tk.END)
        cuit_input.focus()

    elif opcion == 'BuscarNombre':
        componenteshabilitar('disabled')


        deshabilitarbotones('disabled')
        limpiarCampos()
        cuit_input.select_range(0, tk.END)
        cuit_input.focus()