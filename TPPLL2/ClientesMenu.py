#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import Cliente
import mariadb
import VentanaGrilla
import re


dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit=True
)
cur = dbPk.cursor()

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}\w+[.]\w{2,3}$'
regex2 = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

dniVar = 0
nombreapellidoVar = ''
direccionVar = ''
telefonoVar = ''
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

# ---- MENU CLIENTES
def menuClientes(opcion):  # opcionmenu seria alta, muestrotodo en blanco y habilito el boton alta

    def limpiarvar():
        dniVar.set(0)
        nombreapellidoVar.set('')
        direccionVar.set('')
        telefonoVar.set('')
        mailVar.set('')

    def componenteshabilitar(valor): #Valores 'disabled' o 'normal'

        nombre_input.config(state=valor)
        direccion_input.config(state=valor)
        mail_input.config(state=valor)
        telefono_input.config(state=valor)
        idiva_combo.config(state=valor)

    def deshabilitarbotones(valor):
        boton_Alta.config(state=valor)
        boton_Buscar.config(state=valor)
        boton_Actualizar.config(state=valor)
        boton_Eliminar.config(state=valor)

    def limpiarCampos():
        dni_input.delete(0,tk.END)
        dni_input.select_range(0,tk.END)
        dni_input.focus()

        nombre_input.delete(0,tk.END)
        direccion_input.delete(0,tk.END)
        telefono_input.delete(0,tk.END)
        mail_input.delete(0,tk.END)
        idiva_combo.set('Consumidor Final')

    def llenarcampos(cliente):
        nombreapellidoVar.set(cliente.nombre)
        direccionVar.set(cliente.domicilio)
        telefonoVar.set(cliente.celular)
        mailVar.set(cliente.mail)
        idiva_combo.set(buscarsitiva(cliente.id_situacionIva))

    def selecentradas():
        nombre_input.select_range(0, tk.END)
        direccion_input.select_range(0,tk.END)
        telefono_input.select_range(0,tk.END)
        mail_input.select_range(0,tk.END)
###EVENTOS
    def DNIenter(event):
        buscarDni()

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

    def ValidarNombre(VentanaPadre, componente):
        while True:
            try:
                validacion = True
                varingresada = str(componente.get())

                if len(varingresada) < 2 or varingresada == '':
                    messagebox.showerror('Validacion Campo', f'Debe ingresar un valor Nombre y Apellido Valido')
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
                        messagebox.showerror('Validacion Campo', f'Debe ingresar un Nombre y un Apellido')
                        componente.select_range(0, tk.END)
                        componente.focus()
                        VentanaPadre.focus()
                        validacion = False
                    else:
                        validacion = True

            except:
                messagebox.showerror('Validacion Campo',f'Debe ingresar un Valido')
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
                varingresada = int(componente.get())

                if varingresada <0 or varingresada > 9999999999:
                    messagebox.showerror('Validacion Campo', f'Debe ingresar un valor numerico Valido')
                    componente.delete(0, tk.END)
                    componente.select_range(0, tk.END)
                    componente.focus()
                    VentanaPadre.focus()
                    validacion = False

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

                if re.search(regex, varingresada) or re.search(regex2,varingresada):
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

    #####FUNCIONES DE BOTONES
    def ActualizarCliente():
        dni_input.config(state='disabled')
        # boton_Buscardni.config(state='disabled')
        validacion = False
        CliAlta = [dniVar.get()]
        while validacion == False:
            if ValidarNombre(ClienteVent, nombre_input):
                nombre_input.config(state='disabled')
                nombreap = nombreapellidoVar.get().upper()
                CliAlta.append(nombreap)
                if ValidarDireccion(ClienteVent, direccion_input):
                    direccion_input.config(state='disabled')
                    dire = direccionVar.get().upper()
                    CliAlta.append(dire)
                    if ValidarTelefono(ClienteVent, telefono_input):
                        telefono_input.config(state='disabled')
                        CliAlta.append(telefonoVar.get())
                        if ValidarMail(ClienteVent, mail_input):
                            mailingreso = mailVar.get().lower()
                            CliAlta.append(mailingreso)
                            idiva = idiva_combo.current() + 1
                            CliAlta.append(idiva)
                            ClienteAlta = Cliente.Cliente(CliAlta)
                            ClienteAlta.modificaCliente(dniVar.get())
                            dbPk.commit()
                            del ClienteAlta
                            limpiarvar()
                            # print(dniVar.get())
                            validacion = True
                        else:
                            mail_input.select_range(0, tk.END)
                            mail_input.focus()
                            ClienteVent.focus()
                            break
                    else:
                        telefono_input.select_range(0, tk.END)
                        telefono_input.focus()
                        ClienteVent.focus()
                        break
                else:
                    direccion_input.select_range(0, tk.END)
                    direccion_input.focus()
                    ClienteVent.focus()
                    break
            else:
                nombre_input.select_range(0, tk.END)
                nombre_input.focus()
                ClienteVent.focus()
                break
        else:
            limpiarCampos()
            dni_input.delete(0, tk.END)
            dni_input.select_range(0, tk.END)
            ClienteVent.destroy()

    def buscarDni():

        if ValidarNumero(ClienteVent,dni_input):
            dnibuscar = dniVar.get()

            if dnibuscar == 0 or dnibuscar > 99999999:
                messagebox.showerror('Verificacion de Datos', 'Debe ingresar un numero valido de DNI')
                ClienteVent.focus()
                dni_input.delete(0,tk.END)
                dni_input.select_range(0,tk.END)
                dni_input.focus()
            else:
                sqlbusqueda='SELECT * FROM clientes WHERE DNI = ' +str(dnibuscar)
                cur.execute(sqlbusqueda)
                Resultado = cur.fetchall()

                if len(Resultado) > 0:
                    clitupla = []
                    for ind in Resultado:
                        for i in range(0,len(ind)):
                            clitupla.append(ind[i])
                        clienteEncontrado = Cliente.Cliente(tuple(clitupla))
                    if opcion == 'Baja':
                        llenarcampos(clienteEncontrado)
                        boton_Eliminar.config(state='normal')
                        boton_Eliminar.focus()
                        del Resultado
                    elif opcion == 'Alta':
                        messagebox.showwarning('Advertencia',f'El Cliente ya existe {clienteEncontrado.dni}')
                        limpiarvar()
                        limpiarCampos()
                        dni_input.focus()
                        del Resultado
                    elif opcion == 'Modificacion':
                        llenarcampos(clienteEncontrado)
                        boton_Actualizar.config(state='normal')
                        componenteshabilitar('normal')
                        selecentradas()
                        nombre_input.focus()
                        del Resultado
                    elif opcion == 'BuscarDni':
                        llenarcampos(clienteEncontrado)
                        dni_input.select_range(0, tk.END)
                        dni_input.focus()
                        # boton_Buscardni.focus()

                elif len(Resultado) < 1:
                    if opcion == 'Baja' or opcion == 'Modificacion' or opcion == 'BucarDni' or opcion == 'BuscarNombre':
                        messagebox.showwarning('Advertencia', f'No existe el cliente Solicitado\n con el DNI: {dnibuscar}')
                        del Resultado
                        dni_input.select_range(0, tk.END)
                        dni_input.focus()
                        ClienteVent.focus()
                        limpiarCampos()
                        limpiarvar()

                    else: # permito ingresar los datos
                        componenteshabilitar('normal')
                        dni_input.config(state='disabled')
                        boton_Alta.config(state='normal')
                        nombre_input.focus()
                        del Resultado
        else:
            ClienteVent.focus()
            dni_input.delete(0, tk.END)
            dni_input.select_range(0, tk.END)
            dni_input.focus()

    def BuscarNombre():
        tabla = 'clientes'

        sqlConsulta = 'SELECT a.dni, a.nombreapellido, a.direccion, a.telefono, a.mail, b.Situacion FROM ' \
                      'clientes a INNER JOIN situacioniva b ON a.Id_Iva = b.Id_Iva WHERE a.NombreApellido ' \
                      'LIKE \"%' + nombreapellidoVar.get() + '%\"' #
        cur.execute(sqlConsulta)
        resultado = cur.fetchall()

        if len(resultado) < 1:
            messagebox.showwarning('Atencion', 'No se encontro el dato en la base, revise que este correcto.')
            ClienteVent.focus()
            nombre_input.delete(0,tk.END)
            nombre_input.select_range(0,tk.END)
            nombre_input.focus()
        else:
            Cliente_Campos = ('DNI', 'NombreApellido', 'Direccion', 'Telefono', 'Mail', 'CondicionIva')
            Cliente_AnchoCampo = (10, 60, 60, 20, 40, 30)
            tablaNombre = VentanaGrilla.GrillaTabla(tabla,Cliente_Campos,Cliente_AnchoCampo, sqlConsulta)
            tablaNombre.mainloop()


    def encontrarcliente():
        sqlbusqueda = 'SELECT * FROM clientes WHERE DNI = ' + str(dniVar.get())
        cur.execute(sqlbusqueda)
        Resultado = cur.fetchall()

        if len(Resultado) == 1:
            for ind in Resultado:
                clitupla = []
                for i in range(0, len(ind)):
                    clitupla.append(ind[i])
                clienteEncontrado = Cliente.Cliente(tuple(clitupla))

        return clienteEncontrado

    def altaCliente():

        dni_input.config(state='disabled')
        # boton_Buscardni.config(state='disabled')
        validacion = False
        CliAlta = [dniVar.get()]
        while validacion == False:
            if ValidarNombre(ClienteVent,nombre_input):
                nombre_input.config(state='disabled')
                nombreap = nombreapellidoVar.get().upper()
                CliAlta.append(nombreap)
                if ValidarDireccion(ClienteVent,direccion_input):
                    direccion_input.config(state='disabled')
                    dire = direccionVar.get().upper()
                    CliAlta.append(dire)
                    if ValidarTelefono(ClienteVent,telefono_input):
                        telefono_input.config(state='disabled')
                        CliAlta.append(telefonoVar.get())
                        if ValidarMail(ClienteVent, mail_input):
                            mailingreso = mailVar.get().lower()
                            CliAlta.append(mailingreso)
                            idiva = idiva_combo.current() + 1
                            CliAlta.append(idiva)
                            ClienteAlta = Cliente.Cliente(CliAlta)
                            ClienteAlta.altaCliente()
                            dbPk.commit()
                            del ClienteAlta
                            limpiarvar()
                            # print(dniVar.get())
                            validacion = True
                        else:
                            mail_input.select_range(0,tk.END)
                            mail_input.focus()
                            ClienteVent.focus()
                            break
                    else:
                        telefono_input.select_range(0,tk.END)
                        telefono_input.focus()
                        ClienteVent.focus()
                        break
                else:
                    direccion_input.select_range(0,tk.END)
                    direccion_input.focus()
                    ClienteVent.focus()
                    break
            else:
                nombre_input.select_range(0,tk.END)
                nombre_input.focus()
                ClienteVent.focus()
                break
        else:
            limpiarCampos()
            dni_input.delete(0,tk.END)
            dni_input.select_range(0, tk.END)
            ClienteVent.destroy()



    def eliminarCliente():
        clielim = encontrarcliente()
        if messagebox.askquestion('Eliminar Registro',f'Esta seguro de dar de baja al cliente?\n '
                                                   f'DNI: {clielim.dni} \n'
                                                   f'Nombre y Apellido: {clielim.nombre}') == 'yes':
            clielim.borrarCliente(clielim.dni)
            dbPk.commit()

        else:
            messagebox.showwarning('Eliminar Registro', f'No se ha eliminado el registro')
        del clielim
        limpiarvar()
        limpiarCampos()
        dni_input.select_range(0, tk.END)
        ClienteVent.destroy()


    # si es baja, permito cargar nro dni busca y
    ClienteVent = tk.Toplevel()  # creo ventana que dependa del raiz si cierro el raiz se cierran todas las ventanas
    idClienteVent = ClienteVent.winfo_id()
    ClienteVent.title('Tech-Hard - Clientes')  # pone titulo a la ventana principal
    ClienteVent.geometry('500x400')  # Tamaño en pixcel de la ventana
    ClienteVent.iconbitmap('imagenHT.ico')  # icono
    ClienteVent.minsize(500, 400)
    ClienteVent.resizable(0, 0)  # size ancho, alto 0 no se agranda, 1 se puede agrandar
    # Cliente.config(bd=25)
    # Cliente.config(relief='sunken')

    Cliente_Campos = ('id_Cliente', 'DNI', 'NombreApellido', 'Direccion', 'Telefono', 'Mail', 'Id_Iva')
    CamposInt = (0, 1, 6)

    framecampoCli = tk.Frame(ClienteVent)
    # framecampoCli.pack(fill='both')
    # framecampoCli.config(bg='lightblue')
    framecampoCli.config(width=500, height=400)
    framecampoCli.config(cursor='')  # Tipo de cursor si es pirate es (arrow defecto)
    framecampoCli.config(relief='groove')  # relieve hundido tenemos
    # FLAT = plano RAISED=aumento SUNKEN = hundido GROOVE = ranura RIDGE = cresta
    framecampoCli.config(bd=25)  # tamano del borde en pixeles
    # framcampoCli.pack(side=RIGHT) # lo ubica a la derecha
    # framecampoCli.pack(anchor=SE) # lo ubica abajo a la derecha
    framecampoCli.pack(fill='x')  # ancho como el padre
    framecampoCli.pack(fill='y')  # alto igual que el padre
    framecampoCli.pack(fill='both')  # ambas opciones
    framecampoCli.pack(fill='both', expand=1)  # expandirese para ocupar el espacio

    # idcliente = tk.IntVar()
    def config_label(mi_label, fila):
        espaciado_labels = {'column': 50, 'sticky': 'e', 'padx': 10, 'pady': 10}
        # color_labels ={'bg':color_fondo, 'fg':color_letra,'font':fuente}
        mi_label.grid(row=fila, **espaciado_labels)
        # mi_label.config(**color_labels)

    dniVar = tk.IntVar()
    nombreapellidoVar = tk.StringVar()
    direccionVar = tk.StringVar()
    telefonoVar = tk.StringVar()
    mailVar = tk.StringVar()

    '''
    entero = IntVar()  # Declara variable de tipo entera
    flotante = DoubleVar()  # Declara variable de tipo flotante
    cadena = StringVar()  # Declara variable de tipo cadena
    booleano = BooleanVar()  # Declara variable de tipo booleana
    '''
#### label/entry/botones
    dni_label = tk.Label(framecampoCli, text='DNI')
    config_label(dni_label, 3)

    dni_input = tk.Entry(framecampoCli, width=8, justify=tk.RIGHT, textvariable=dniVar)
    dni_input.grid(row=3, column=51, padx=10, pady=10, sticky='w')
    dni_input.delete(0, tk.END)
    dni_input.select_range(0, tk.END)
    dni_input.focus()
    dni_input.bind('<Return>',DNIenter)

    # boton_Buscardni = tk.Button(framecampoCli, text='Buscar', command=buscarDni)
    # boton_Buscardni.grid(row=3, column=100, padx=5, pady=10, ipadx=7)
    # dni_input.insert(tk.END,'')

    nombre_label = tk.Label(framecampoCli, text='Nombre y Apellido')
    config_label(nombre_label, 4)
    nombre_input = tk.Entry(framecampoCli, width=30, textvariable=nombreapellidoVar)
    nombre_input.grid(row=4, column=51, padx=10, pady=10,sticky='w')
    # boton_Buscarnom = tk.Button(framecampoCli, text='Buscar',command=BuscarNombre)
    # boton_Buscarnom.grid(row=4, column=100, padx=5, pady=10, ipadx=7)

    direccion_label = tk.Label(framecampoCli, text='Direccion')
    config_label(direccion_label, 5)
    direccion_input = tk.Entry(framecampoCli, width=30 ,textvariable=direccionVar)
    direccion_input.grid(row=5, column=51, padx=10, pady=10, sticky='w')

    telefono_label = tk.Label(framecampoCli, text='Telefono')
    config_label(telefono_label, 6)
    telefono_input = tk.Entry(framecampoCli, textvariable=telefonoVar)
    telefono_input.grid(row=6, column=51, padx=10, pady=10,sticky='w')


    mail_label = tk.Label(framecampoCli, text='Mail')
    config_label(mail_label, 7)
    mail_input = tk.Entry(framecampoCli, textvariable=mailVar)
    mail_input.grid(row=7, column=51, padx=10, pady=10, sticky='w')

    idiva_label = tk.Label(framecampoCli, text='Situacion frente al Iva')
    config_label(idiva_label, 8)
    ivasit = listarIdIva()
    idiva_combo = ttk.Combobox(framecampoCli, state='readonly',
                               values=ivasit)  # ya que solo puede seleccionar los tipos de iva
    idiva_combo.grid(row=8, column=51, padx=10, pady=10, sticky='w')
    idiva_combo.set('Consumidor Final')


# FRAME BOTONES -> FUNCIONES CRUD (Create, read, update, delete)
    framebotonesCli = tk.Frame(ClienteVent)
    framebotonesCli.pack()

    boton_Alta = tk.Button(framebotonesCli, text='Alta', command=altaCliente)
    boton_Alta.grid(row=0, column=1, padx=5, pady=10, ipadx=7)

    boton_Buscar = tk.Button(framebotonesCli, text='Buscar')
    boton_Buscar.grid(row=0, column=2, padx=5, pady=10, ipadx=7)

    boton_Actualizar = tk.Button(framebotonesCli, text='Actualizar', command=ActualizarCliente)
    boton_Actualizar.grid(row=0, column=3, padx=5, pady=10, ipadx=7)

    boton_Eliminar = tk.Button(framebotonesCli, text='Eliminar', command=eliminarCliente)
    boton_Eliminar.grid(row=0, column=4, padx=5, pady=10, ipadx=7)


    if opcion == 'Alta':
        componenteshabilitar('disabled')

        # boton_Buscarnom.config(state='disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        boton_Buscar.config(command=buscarDni)

        limpiarCampos()
        dni_input.focus()

    elif opcion == 'Baja':
        componenteshabilitar('disabled')
        # boton_Buscarnom.config(state='disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        boton_Buscar.config(command=buscarDni)
        limpiarCampos()
        dni_input.focus()

    elif opcion == 'Modificacion':
        componenteshabilitar('disabled')
        # boton_Buscarnom.config(state='disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        boton_Buscar.config(command=buscarDni)
        limpiarCampos()
        dni_input.select_range(0, tk.END)
        dni_input.focus()

    elif opcion == 'BuscarDni':
        componenteshabilitar('disabled')

        # boton_Buscarnom.config(state='disabled')
        deshabilitarbotones('disabled')
        boton_Buscar.config(state='normal')
        boton_Buscar.config(command=buscarDni)
        limpiarCampos()
        dni_input.select_range(0, tk.END)
        dni_input.focus()

    elif opcion == 'BuscarNombre':
        componenteshabilitar('disabled')
        dni_input.config(state='disabled')
        deshabilitarbotones('disabled')
        # boton_Buscarnom.config(state='normal')
        limpiarCampos()
        nombre_input.config(state='normal')
        nombre_input.select_range(0, tk.END)
        nombre_input.focus()
        boton_Buscar.config(state='normal', command=BuscarNombre)

