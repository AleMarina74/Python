#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

def crear_base(Archivo):
    if not os.path.isfile(Archivo):
        RutaDirectorio = RutaTrabajo()
        ArchivoCrear =  Archivo
        if not os.path.isfile(ArchivoCrear):
            wArchivo = open(ArchivoCrear, 'w', encoding="utf-8")
            wArchivo.close()
    return None

def ExisteArchivo(Archivo):
    if not os.path.isfile(Archivo):
        RutaDirectorio = RutaTrabajo()
        Archivofinal = RutaDirectorio + Archivo
    else:
        Archivofinal = Archivo

    return Archivofinal

def RutaTrabajo():
    while True:
        try:
            Directorios = str(input('Ingrese la Ruta de Trabajo: '))
        except ValueError:
            print(f'La Ruta de directorios ingresada es incorrecta, vuelva a cargarla')
        else:
            sisOper = os.name
            Directorio = ''
            if sisOper == 'posix':  # si fuera unix
                posicion = 0
                for caracter in Directorios:
                    if posicion == 0:
                        if caracter.isalpha():
                            Directorio = caracter.upper()
                        else:
                            print(f'El caracter ingresado no es valido, vuelva a cargar la Ruta. Debe empezar con una letra indicando Unidad de Disco')
                    elif posicion == 1:
                        if caracter != ':':
                            print(f'El caracter ingresado no es valido, vuelva a cargar la Ruta. Deberia ser (:) ')
                        else:
                            Directorio = Directorio + caracter
                    elif posicion > 1 and posicion < len(Directorios):
                        if caracter == '\\':
                            Directorio = Directorio + '/'
                        else:
                            Directorio = Directorio + caracter.upper()
                    elif posicion == (len(Directorios)-1):
                        if caracter.isalpha():
                            Directorio = Directorio + '/'
                    else:
                        Directorio = Directorio + caracter.upper()
                break
            elif sisOper == 'ce' or sisOper == 'dos' or sisOper == 'nt':
                posicion = 0
                for caracter in Directorios:
                    if posicion == 0:
                        if caracter.isalpha():
                            Directorio = caracter.upper()
                            cantes = caracter.upper()
                        else:
                            print(f'El caracter ingresado no es valido, vuelva a cargar la Ruta. Debe empezar con una letra indicando Unidad de Disco')
                    elif posicion == 1:
                        if caracter != ':':
                            print(f'El caracter ingresado no es valido, vuelva a cargar la Ruta. Deberia ser (:) ')
                        else:
                            Directorio = Directorio + caracter
                            cantes = caracter.upper()
                    elif posicion > 1 and posicion < (len(Directorios)-1):
                        if caracter == '\\':
                            Directorio = Directorio + '\\'
                            cantes = caracter.upper()
                        elif caracter == '/':
                            Directorio = Directorio + '\\'
                            cantes = '\\'
                        else:
                            Directorio = Directorio + caracter.upper()
                            cantes = caracter.upper()
                    elif posicion == (len(Directorios)):
                        if caracter.isalpha():
                            Directorio = Directorio + caracter.upper() + '\\'
                        elif caracter == '\\':
                            Directorio = Directorio + caracter.upper()
                    else:
                        Directorio = Directorio + caracter.upper()
                    posicion += 1
                if Directorio[:-1] != '\\':
                    Directorio = Directorio + '\\'
                break
    return Directorio

def limpiarPantalla():
    sisOper = os.name
    if sisOper =='posix': # si fuera unix
        os.system('clear')
    elif sisOper == 'ce' or sisOper == 'dos' or sisOper == 'nt':
        os.system('cls')
        print("\033[1;35m" + "Gestion de biblioteca \n".center(165, ' '))
        print('\033[0;37m' + "")

def menu_principal():
    while True:
        try:
            limpiarPantalla()
            print(" 0 - Consulta de disponibilidad \n", "1 - Prestamos de libro \n", "2 - Gestion de cliente \n", "3 - Gestion de libros \n", "4 - Salir \n")
            OpcionMenu = int(input('Elija una Opcion del Menu Principal: '))
        except ValueError:
            print(f'Debe elegir una opcion Valida Numerica entre 0 y 4')
            os.system('Pause')
        else:
            if OpcionMenu >= 0 and OpcionMenu <= 4:
                break
            else:
                print(f'Debe elegir una opcion Valida Numerica entre 0 y 4. Ud ingreso {OpcionMenu}')
                os.system('Pause')
    return OpcionMenu

def CambioColor(Tipo,Color):
    Estilo = ['Normal','Negrita','Debil','Cursiva','Subrayadao','Inverso','Oculto','Tachado']
    Colores = {
        'Negro':'30',
        'Rojo':'31',
        'Verde':'32',
        'Amarillo':'33',
        'Azul':'34',
        'Morado':'35',
        'Cian':'36',
        'Blanco':'37'}
    indice = 0
    while indice < len(Estilo):
        if Tipo == Estilo[indice]:
            indiceEstilo = indice
            break
        else:
            indice += 1
    nroColor = Colores.get(Color)

    strColor = '\033[' + str(indiceEstilo) + ';' + nroColor + 'm'

    return strColor

def sub_menu_prestamos():
    while True:
        try:
            limpiarPantalla()
            print("\033[1;36m"+"Prestamo de libros \n")
            print('\033[0;37m' + "")
            print("0 - Consulta de titulos disponibles")
            print("1 - Registrar préstamo de libros/actualización de estado")
            print("2 - Registro de devoluciones/actualización de estado")
            print('3 - Volver al Menu Principal \n')
            OpcionMenu = int(input('Elija una Opcion del Menu Principal: '))
        except ValueError:
            print(f'Debe elegir una opcion Valida Numerica entre 0 y 3')
            os.system('Pause')
        else:
            if OpcionMenu >= 0 and OpcionMenu <= 3:
                break
            else:
                print(f'Debe elegir una opcion Valida Numerica entre 0 y 3. Ud ingreso {OpcionMenu}')
                os.system('Pause')
    return OpcionMenu

def sub_menuCliLi(SubMenu): # Libro o Cliente
    while True:
        try:
            limpiarPantalla()
            print(f"\033[1;34m Gestion de {SubMenu} \n")
            print('\033[0;37m' + "")
            print(f"0 - Alta de {SubMenu}")
            if SubMenu == 'Cliente':
                print(f"1 - Consulta de estado de {SubMenu}")
            else:
                print(f'1 - Consulta de {SubMenu}')
            print(f"2 - Modificacion de {SubMenu}")
            print(f"3 - Eliminación de {SubMenu}")
            print(f'4 - Volver al Menu Principal \n')

            OpcionMenu = int(input(f'Elija una Opcion del Menu {SubMenu}: '))
        except ValueError:
            print(f'Debe elegir una opcion Valida Numerica entre 0 y 4')
            os.system('Pause')
        else:
            if OpcionMenu >= 0 and OpcionMenu <= 4:
                break
            else:
                print(f'Debe elegir una opcion Valida Numerica entre 0 y 4. Ud ingreso {OpcionMenu}')
                os.system('Pause')
    return OpcionMenu

def IngresarDniTelefono(campo, Tipo, campoAnterior):
    while True:
        try:
            ingreso = str(input(f"Ingrese {campo}: "))
        except ValueError:
            print("Debe ingresar valores númericos")
        else:
            if Tipo == 'Modif' and ingreso == '':
                ingreso = campoAnterior
                break
            elif ingreso.isnumeric():
                if campo == 'DNI' and (len(ingreso) > 8 or len(ingreso) < 7):
                    print(f'El {campo} no es valido, Debe contener entre 7 y 8 caracteres sin el punto.')
                elif len(ingreso) == 7:
                    ingreso = '0' + ingreso
                    break
                else:
                    break
                if campo =='Telefono':
                    if (len(campo) > 10):
                        print(f'El telefono Ingresado no es correcto. Ingrese codigo de area sin el 0 y si es celular sin el 15')
                    elif Telefono == '':
                        print(f'Usted no ha ingresado Telefono.')
                        EstasSeguro = Confirmacion('Esta Seguro de no cargar Telefono?')
                        if EstasSeguro:
                            Telefono = ' '
                            break
                    else:
                        break
            else:
                print("Debe ingresar valores númericos")
    return ingreso

def IngresarNombre(Texto, Tipo, NombreAnterior): #lo vamos a usar para autor
    if NombreAnterior != ' ':
        NomAnterior = NombreAnterior.split(' ')
        longNomAnt = len(NomAnterior)
        if longNomAnt == 2:
            AntNombre = NomAnterior[0]
            AntApellido = NomAnterior[1]
        elif longNomAnt == 3:
            AntNombre = NomAnterior[0]
            AntNom2App = NomAnterior[1]
            AntApellido = NomAnterior[2]
        else:
            AntNombre = NomAnterior[0]
            AntNom2App = NomAnterior[1]
            AntApellido = NomAnterior[2]
            AntApellido2 = NomAnterior[3]

    while True:
        try:
            Nombre1 = str(input(f'Ingrese Primer Nombre del {Texto}: '))
        except ValueError:
            print(f'Debe ingresar un nombre valido. Usted ingreso: {Nombre1}')
        else:
            if Tipo == 'Modif' and Nombre1 == '':
                NombreCompleto = AntNombre + ' '
                break
            elif not Nombre1.isalpha() or Nombre1 == '' or len(Nombre1) < 2:
                print(f'Debe ingresar un nombre valido. Usted ingreso: {Nombre1}')
            else:
                Nombre1 = Nombre1.lower().capitalize()
                NombreCompleto = Nombre1 + ' '
                break
    while True:
        try:
            Nombre2 = input(f'Ingrese Segundo Nombre del {Texto}: ')
        except ValueError:
            print(f'Debe ingresar un nombre valido. Usted ingreso: {Nombre2}')
        else:
            if Tipo == 'Modif':
                if Nombre2 == '':
                    if longNomAnt == 2:
                        break
                    elif longNomAnt == 4:
                        if AntNom2App != '':
                            NombreCompleto = NombreCompleto + AntNom2App + ' '
                            break
                        else:
                            break
                    else:
                        if AntNom2App != '':
                            NombreCompleto = NombreCompleto + AntNom2App + ' '
                        break
                elif Nombre2 == ' ':
                    if longNomAnt == 2:
                        break
                    elif longNomAnt == 4:
                        NombreCompleto = NombreCompleto
                        break
                    else:
                        if Confirmacion(f'El {AntNom2App} es su Apellido? S/N'):
                            AntApellido2 = AntApellido
                            AntApellido = AntNom2App
                            NombreCompleto = NombreCompleto
                            break
                        else:
                            NombreCompleto = NombreCompleto
                            break
                else:
                    if longNomAnt == 2:
                        NombreCompleto = NombreCompleto + Nombre2.lower().capitalize() + ' '
                        break
                    elif longNomAnt == 4:
                        NombreCompleto = NombreCompleto + Nombre2.lower().capitalize() + ' '
                    else:
                        if Confirmacion(f'El {AntNom2App} es su Apellido? S/N'):
                            AntApellido2 = AntApellido
                            AntApellido = AntNom2App
                        else:
                            NombreCompleto = NombreCompleto + AntNom2App + ' '
                        break
            elif not Nombre2.isalpha() and Nombre2 != '':
                print(f'Debe ingresar un nombre valido. Usted ingreso: {Nombre2}')
            elif Nombre2 == '':
                print(f'Usted no ha ingresado segundo Nombre.')
                break
            else:
                Nombre2 = Nombre2.lower().capitalize()
                NombreCompleto = NombreCompleto + Nombre2 + ' '
                break
    while True:
        try:
            Apellido1 = input(f'Ingrese Primer Apellido del {Texto}: ')
        except ValueError:
            print(f'Debe ingresar un Apellido valido. Usted ingreso: {Apellido1}')
        else:
            if Tipo == 'Modif' and Apellido1 == '':
                NombreCompleto = NombreCompleto + AntApellido
                break
            elif not Apellido1.isalpha() or Apellido1 == '' or len(Apellido1) < 2:
                print(f'Debe ingresar un Apellido valido. Usted ingreso: {Apellido1}')
            else:
                Apellido1 = Apellido1.lower().capitalize()
                NombreCompleto = NombreCompleto + Apellido1
                break
    while True:
        try:
            Apellido2 = input(f'Ingrese Segundo Apellido del {Texto}: ')

        except ValueError:
            print(f'Debe ingresar un Apellido valido. Usted ingreso: {Apellido2}')
        else:
            if Tipo == 'Modif':
                if Apellido2 == '':
                    if longNomAnt == 2:
                        break
                    else:
                        if Apellido2 != '':
                            NombreCompleto = NombreCompleto + ' ' + AntApellido2
                        break
                elif Apellido2 == ' ':
                    if longNomAnt == 2:
                        break
                    else:
                        NombreCompleto = NombreCompleto
                        break
                else:
                    if longNomAnt == 2:
                        NombreCompleto = NombreCompleto + ' ' + Apellido2.lower().capitalize()
                        break
                    elif longNomAnt == 4:
                        NombreCompleto = NombreCompleto + Apellido2.lower().capitalize()
                        break
                    else:
                        break
            elif not Apellido2.isalpha() and Apellido2 != '':
                print(f'Debe ingresar un Apellido valido. Usted ingreso: {Apellido2}')
            elif Apellido2 == '':
                print(f'Usted no ha ingresado segundo Apellido.')
                break
            else:
                Apellido2 = Apellido2.lower().capitalize()
                NombreCompleto = NombreCompleto + ' ' + Apellido2
                break

    return NombreCompleto

def IngresarTitulo(Texto, Tipo, TextoAnterior):
    while True:
        try:
            Titulo = input(f'{Texto}: ')
        except ValueError:
            print(f'Debe ingresar un Titulo Valido.')
        else:
            if Tipo == 'Modif' and Titulo == '':
                Titulo = TextoAnterior
                break
            elif Titulo == ' ' or Titulo == '':
                print(f'Debe ingresar algun contenido de Titulo')
            elif len(Titulo) > 70:
                print(f'El titulo {Titulo} es muy largo, debe acortar el mismo.')
            else:
                Titulo = Titulo.upper()
                break
            Titulo = Titulo.upper()
    return Titulo

def IngresarAutor(Texto, Tipo, TextoAnterior):
    while True:
        try:
            Autor = input(f'{Texto}: ')
        except ValueError:
            print(f'Debe ingresar un Autor Valido.')
        else:
            if Tipo == 'Modif' and Autor == '':
                Autor = TextoAnterior.upper()
                break
            elif Autor == ' ' or Autor == '':
                print(f'Debe ingresar algun contenido de Autor')
            elif len(Autor) > 15:
                print(f'El Autor {Autor} es muy largo, debe acortar el mismo.')
            else:
                Autor = Autor.upper()
                break
            Autor = Autor.upper()
    return Autor

def IngresarDireccion(Tipo):
    while True:
        try:
            print('Domicilio:')
            Calle = input('Ingrese la Calle: ')
        except ValueError:
            print(f'Debe ingresar un Calle Valido.')
        else:
            if Tipo == 'Modif' and Calle == '':
                break
            elif Calle == ' ' or Calle == '':
                print(f'Debe ingresar algun contenido de Calle')
            else:
                DomicilioCompleto = Calle
                break
    while True:
        try:
            Numero = int(input('Ingrese Numero: '))
        except ValueError:
            print(f'Debe ser un numero valido mayor a 0. Usted ingreso {Numero}')
        else:
            if Tipo == 'Modif' and Calle == '':
                break
            if Numero <= 0 or Numero > 99999:
                print(f'Debe ser un numero valido mayor a 0. Usted ingreso {Numero}')
            else:
                Altura = str(Numero)
                DomicilioCompleto = DomicilioCompleto + ' ' + Altura
                break
    while True:
        try:
            Depto = input('Ingrese Departamento: ')
        except ValueError:
            print(f'Debe ingresar un Departamento Valido.')
        else:
            if Tipo == 'Modif' and Calle == '':
                break
            if Depto != ' ' or Depto != '':
                DomicilioCompleto = DomicilioCompleto.upper() + ' ' + Depto.upper()
                break
    return DomicilioCompleto

def Confirmacion(Texto):
    while True:
        try:
            EstaSeguro = str(input(f'{Texto}: '))
        except ValueError:
            print(f'Debe ingresar un Valor valido. Usted ingreso: {EstaSeguro}')
        else:
            if EstaSeguro.upper() == 'S' or EstaSeguro.upper() == 'N':
                if EstaSeguro.upper() == 'S':
                    Confirma = True
                else:
                    Confirma = False
                break
            else:
                print(f'Debe ingresar S o N. Usted ingreso: {EstaSeguro}')
    return Confirma

def nvoRegistro(Archivo,ingresarRegistro):
    with open(Archivo,'a', encoding="utf-8") as aArchivo:
        aArchivo.write(ingresarRegistro)
        print(f'Se ha dado de alta el nuevo registro con los datos ingresados')
    return None

def modificaRegistro(Archivo,indice,RegistroModificado):
    with open(Archivo,'r+', encoding="utf-8") as rArchivo:
        lineas = rArchivo.readlines()
        lineas[indice] = RegistroModificado
        rArchivo.close()
        with open(Archivo, 'w', encoding="utf-8") as wArchivo:
            for renglon in range(0,len(lineas)):
                wArchivo.write(lineas[renglon])
            wArchivo.close()
    print(f' {CambioColor(Negrita,Amarillo)}')
    print(f'Se ha modificado el registro {Archivo}')
    print(f'\033[0;37m')

def eliminarRegistro(Archivo,indice):
    with open(Archivo,'r+', encoding="utf-8") as rArchivo:
        lineas = rArchivo.readlines()
        del(lineas[indice])
        rArchivo.close()
        with open(Archivo, 'w', encoding="utf-8") as wArchivo:
            for renglon in range(0,len(lineas)):
                wArchivo.write(lineas[renglon])
            wArchivo.close()
    print(f'\033[1;37m')
    print(f'Se ha Eliminado el registro {Archivo}')
    print(f'\033[0;37m')

def BuscoRegistro(Archivo,Busqueda,Indice):
    with open(Archivo, 'r', encoding="utf-8") as rArchivo:
        Contenido = rArchivo.readlines()
        if len(Contenido) != 0:
            largo = len(Contenido)
            Registros = []
            RegistrosClave =[]
            if Busqueda == 'D':
                CantRegistros = 0
                for linea in Contenido:
                    renglon = linea.split(',')
                    if renglon[Indice] == Busqueda:
                        Registros.append(linea)
                        CantRegistros +=1
                if CantRegistros == 0:
                    Indice = CantRegistros
                    Resultado = 'N'
                else:
                    Indice = Busqueda
                    Resultado = 'S'
                rArchivo.close()
            else:
                Registro = 0
                for indice in range(0, largo):
                    if Busqueda in Contenido[indice]:  # veo que el nombre este en el registro
                        Renglon = Contenido[indice].split(',')
                        if Busqueda == Renglon[Indice]:
                            Registro += 1
                            Registros.append(Contenido[indice])
                            Indice = indice
                        elif Busqueda in Renglon[Indice]:
                            RegistrosClave.append(Contenido[indice])
                if Registro == 0:  # no hallo registros
                    Resultado = 'N'
                else:
                    Resultado = 'S'
        else:
            Resultado = 'E'
    return Resultado, Indice, Registros, RegistrosClave

#Parte principal del programa


archiClientes = ExisteArchivo('Clientes.txt')  #'C:\\Alejandra\\Algoritmos\\TpBiblioteca\\Clientes.txt'
archiLibros = ExisteArchivo('Libros.txt') #'C:\\Alejandra\\Algoritmos\\TpBiblioteca\\Libros.txt'

crear_base(archiClientes)
crear_base(archiLibros)

Negrita = 'Negrita'
Normal = 'Normal'
Negro = 'Negro'
Rojo = 'Rojo'
Verde = 'Verde'
Blanco = 'Blanco'
Cian = 'Cian'
Amarillo = 'Amarillo'
Azul = 'Azul'
Morado = 'Morado'

Opcion = menu_principal()
while Opcion != 4:
    if Opcion == 0:
        limpiarPantalla()
        print(CambioColor(Negrita, Amarillo))
        print(f' Libros Disponibles '.center(130, '▼'))
        print(CambioColor(Normal,Blanco))
        BusquedaD = BuscoRegistro('Libros.txt','D',3)
        RegistrosD = BusquedaD[2]
        LongitudD = len(RegistrosD)
        TipoBusqueda = BusquedaD[1]
        if TipoBusqueda == 'D':
            if LongitudD > 0:
                maxPantalla = 0
                campos = ['ISBN','TITULO','AUTOR']
                print(f'{CambioColor(Negrita,Blanco)}| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} | {CambioColor(Negrita,Amarillo)}')
                print(f'='.center(130,'='))
                CambioColor(Normal,Blanco)
                for registro in RegistrosD:
                    RegImpr = registro.split(',')
                    if maxPantalla < 21:
                        print(f'{CambioColor(Normal,Blanco)}| {RegImpr[0]:^13} || {RegImpr[1]:55s} || {RegImpr[2]:50s} |')
                        maxPantalla +=1
                        Continuar = True
                    else:
                        print(" ")
                        Continuar = Confirmacion('Presione S para continuar con la lista o N para salir al menu Principal')
                        if Continuar:
                            limpiarPantalla()
                            print(f'{CambioColor(Normal,Blanco)}| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} |{CambioColor(Normal,Amarillo)}')
                            print(f'='.center(130, '='))
                            maxPantalla = 0
                        else:
                            limpiarPantalla()
                            break
                if Continuar:
                    print(f'{CambioColor(Negrita,Amarillo)}')
                    print(f' Fin de Libros disponibles '.center(130,'▲'))
                    print(CambioColor(Normal,Blanco))
                    if Confirmacion('Presione S para volver al menu Principal'):
                        Opcion = menu_principal()
                    else:
                        Opcion = menu_principal()
                else:
                    Opcion = menu_principal()

    elif Opcion == 1:
        OpcionPrestamo = sub_menu_prestamos()
        if OpcionPrestamo == 0:
            limpiarPantalla()

            print('\033[1:36m')
            print('Consulta Disponibilidad de Libro por Titulo\n')
            print('\033[0;37m')
            TituloConsultar = IngresarTitulo('Cual es el Titulo del Libro a consultar?','Consulta',' ')
            OpcionTitulo = BuscoRegistro('Libros.txt', TituloConsultar, 1)
            if OpcionTitulo[0] == 'E' or OpcionTitulo[0] == 'N':
                print(f'\033[0;37m')
                print(f'El titulo ingresado no existe \033[1;37m {TituloConsultar}')
                print(CambioColor(Normal,Blanco))
                if Confirmacion('Desea buscar otro titulo S/N?'):
                    Opcion = 1
                else:
                    limpiarPantalla()
                    Opcion = menu_principal()
            else:
                renglon = OpcionTitulo[2]
                registro = renglon[0].split(',')
                print('')
                print(f'Autor: \033[1;37m {registro[2]}')
                print(f'\033[0;37m ISBN: \033[1;37m {registro[0]}')
                if registro[3] == 'D':
                    print(f'\033[0;37m')
                    print(f'Estado: \033[1;32m DISPONIBLE')
                    print(f'\033[0;37m')
                else:
                    print(f'\033[0;37m')
                    print(f'Estado: \033[1;31m NO DISPONIBLE')
                    print(f'\033[0;37m')
                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Prestamos')
                if Continuar:
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    Opcion = 1
        elif OpcionPrestamo == 1:
            limpiarPantalla()
            print("\033[1;36m" + "Prestamo de libros \n")
            print('\033[0;37m' + "")
            print(f'\033[0;36m Carga de Prestamo')
            print(f'\033[0;37m ')
            ClientePrestamo = IngresarDniTelefono('DNI','Consulta',' ')
            BusquedaCliente = BuscoRegistro('Clientes.txt', ClientePrestamo, 0)
            if BusquedaCliente != 'E':
                IndiceBusqueda = BusquedaCliente[1]
                if BusquedaCliente[0] == 'S':
                    with open('Clientes.txt', 'r+', encoding="utf-8") as rwClientes:
                        lineas = rwClientes.readlines()
                        renglon = lineas[IndiceBusqueda].split(',')
                        print(f'\033[0;37m Nombre: \033[1;37m {renglon[1]}')
                        print(f'\033[0;37m Telefono: \033[1;37m {renglon[2]}')
                        print(f'\033[0;37m Domicilio: \033[1;37m {renglon[3]}')
                        if renglon[4] == 'D':
                            print(f'\033[0;37m Estado: \033[1;32m DISPONIBLE')
                            print(f'\033[0;37m')
                            ISBNPrestamo = IngresarDniTelefono('Ingrese el ISBN del libro a Prestar','Prestamo',' ')
                            ExisteISBN = BuscoRegistro('Libros.txt', ISBNPrestamo, 0)
                            if ExisteISBN[0] != 'E':
                                IndiceLibro = ExisteISBN[1]
                                if ExisteISBN[0] == 'S':
                                    RegistroISBN = ExisteISBN[2]
                                    RegistroISBN = RegistroISBN[0][:-2].split(',')
                                    print(f' \033[0;33m')
                                    print(f'El ISBN ingresado corresponde al TITULO: \033[1;33m {RegistroISBN[1]}')
                                    print(f' \033[0;37m')
                                    with open('Libros.txt', 'r+', encoding="utf-8") as rwLibros:
                                        lineasLibros = rwLibros.readlines()
                                        renglonLibro = lineasLibros[IndiceLibro].split(',')
                                        if renglonLibro[3] == 'D' or renglonLibro[3] == 'E' or renglonLibro[3] == ' ' or \
                                                renglonLibro[3] == '':
                                            registroLibro = renglonLibro[0] + ',' + renglonLibro[1] + ',' + renglonLibro[
                                                2] + ',P,' + renglon[0] + ' \n'
                                            registroCliente = renglon[0] + ',' + renglon[1] + ',' + renglon[2] + ',' + \
                                                            renglon[3] + ',P,' + renglonLibro[0] + ' \n'
                                            modificaRegistro('Clientes.txt', IndiceBusqueda, registroCliente)
                                            modificaRegistro('Libros.txt', IndiceLibro, registroLibro)
                                            Continuar = Confirmacion(
                                                'Presione S para volver al menu Principal o N para volver al menu de Prestamos')
                                            if Continuar:
                                                Opcion = menu_principal()
                                            else:
                                                Opcion = 1
                                        else:
                                            print(f'\033[0;37m')
                                            print(f'El libro {CambioColor(Negrita, Amarillo)} {renglonLibro[1]} \033[0;37m no se encuentra disponible, elija otro libro. \n')
                                            Continuar = Confirmacion(
                                                'Presione S para volver al menu Principal o N para volver al menu de Prestamos')
                                            if Continuar:
                                                limpiarPantalla()
                                                Opcion = menu_principal()
                                            else:
                                                Opcion = 1
                                else:
                                    print(f'\033[1;37m El Titulo de libro ingresado no se encuentra en nuestra base de datos.')
                                    print(f'\033[0;37m')
                                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver ir al Menu de Alta de Libros')
                                    if Continuar:
                                        limpiarPantalla()
                                        Opcion = menu_principal()
                                    else:
                                        Opcion = 1
                            else:
                                print(f'\033[1;37m El ISBN de libro {ISBNPrestamo} no se encuentra en la base.')
                                print(f'\033[0;37m')
                                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver ir al Menu de Prestamo de Libros')
                                if Continuar:
                                    limpiarPantalla()
                                    Opcion = menu_principal()
                                else:
                                    Opcion = 1
                        else:
                            print(f'\033[0;37m Estado: \033[1;31m NO DISPONIBLE')
                            print(f'\033[0;37m')
                            BuscarPrestado = BuscoRegistro('Libros.txt', renglon[5][:-2], 0)
                            with open('libros.txt', 'r', encoding="utf-8") as rLibros:
                                lineasLibros = rLibros.readlines()
                                renglonLibro = lineasLibros[BuscarPrestado[1]].split(',')
                                print(f'')
                                print(f'Usted no ha devuelto el libro: \033[1;33m {renglonLibro[1]}')
                                print(f'\033[0;37m')
                                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Prestamos')
                                if Continuar:
                                    limpiarPantalla()
                                    Opcion = menu_principal()
                                else:
                                    Opcion = 1
                else:
                    print('')
                    print(f'El DNI \033[1;37m {ClientePrestamo} \033[0;37m no existe, cargue alta de cliente.')
                    Continuar = Confirmacion('Desea cargar ahora el alta de Cliente S/N?')
                    if Continuar:
                        Opcion = 2
                    else:
                        limpiarPantalla()
                        Opcion = menu_principal()
            else:
                print(f'\033[1;32m La Base de Clientes esta vacia, verifique que ha sucedido.')
                Opcion = menu_principal()
        elif OpcionPrestamo == 2: #Devolucion de Prestamo
            limpiarPantalla()
            print("\033[1;36m" + "Prestamo de libros \n")
            print('\033[0;37m' + "")
            print(f'\033[0;36m Devolucion de Libro en Prestamo')
            print(f'\033[0;37m')
            ClientePrestamo = IngresarDniTelefono('DNI','Devolucion',' ')
            BusquedaCliente = BuscoRegistro('Clientes.txt', ClientePrestamo, 0)
            if BusquedaCliente != 'E':
                IndiceBusqueda = BusquedaCliente[1]
                if BusquedaCliente[0] == 'S':
                    with open('Clientes.txt', 'r+', encoding="utf-8") as rwClientes:
                        lineas = rwClientes.readlines()
                        renglon = lineas[IndiceBusqueda].split(',')
                        print(f'\033[1;37m Datos del Cliente:\n')
                        print(f'\033[0;37m Dni Nº: \033[1;37m {renglon[0]}')
                        print(f'\033[0;37m Nombre Completo: \033[1;37m {renglon[1]}')
                        print(f'\033[0;37m Domicilio: \033[1;37m {renglon[2]}')
                        print(f'\033[0;37m Telefono: \033[1;37m {renglon[3]}')
                        if renglon[4] == 'D':
                            print(f'\033[0;37m')
                            print(f'\033[1;32m Usted no tiene ningun libro en prestamo. Puede solicitar un Prestamos de Libro')
                            print(f'\033[0;37m')
                            if Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Prestamos.'):
                                limpiarPantalla()
                                Opcion = menu_principal()
                            else:
                                limpiarPantalla()
                                Opcion = 1
                        else:
                            TituloPrestamo = renglon[5][:-2]
                            print(f'\033[0;37m')
                            print(f'\033[1;37m Usted esta devolviendo el libro:')
                            print(f'\033[0;37m')
                            BusquedaLibro = BuscoRegistro('Libros.txt', TituloPrestamo, 0)
                            if BusquedaLibro[0] != 'E':
                                IndiceLibro = BusquedaLibro[1]
                                if BusquedaLibro[0] == 'S':
                                    with open('Libros.txt', 'r+', encoding="utf-8") as rwLibros:
                                        lineasLibros = rwLibros.readlines()
                                        renglonLibro = lineasLibros[IndiceLibro].split(',')
                                        if renglonLibro[3] == 'P':
                                            registroLibro = renglonLibro[0] + ',' + renglonLibro[1] + ',' + \
                                                            renglonLibro[2] + ',D,' + ' \n'
                                            registroCliente = renglon[0] + ',' + renglon[1] + ',' + renglon[2] + ',' + \
                                                              renglon[3] + ',D,' + ' \n'

                                            print(f'\033[0;37m Nombre del libro: {CambioColor(Negrita,Amarillo)} {renglonLibro[1]}')
                                            print(f'\033[0;37m')
                                            if Confirmacion(f'Esta seguro que desea devolver el libro {CambioColor(Negrita,Amarillo)} {renglonLibro[1]} {CambioColor(Normal,Blanco)}?'):
                                                modificaRegistro('Clientes.txt', IndiceBusqueda, registroCliente)
                                                modificaRegistro('Libros.txt', IndiceLibro, registroLibro)
                                                print(f'\033[1;33m')
                                                print('Registros Modificados, se ha devuelto el libro correctamente.')
                                                print(f'\033[0;37m')
                                                Volver = Confirmacion('Presione S para volver al menu Princial o N para volver al Menu de Prestamos')
                                                if Volver:
                                                    limpiarPantalla()
                                                    Opcion = menu_principal()
                                                else:
                                                    limpiarPantalla()
                                                    Opcion = 1
                                            else:
                                                print(f' {CambioColor(Negrita,Verde)}')
                                                print(f'No se han modificado los registros.')
                                                print(f'\033[0;37m')
                                                if Confirmacion('Presione S para volver al menu Princial o N para volver al Menu de Prestamos'):
                                                    limpiarPantalla()
                                                    Opcion = menu_principal()
                                                else:
                                                    limpiarPantalla()
                                                    Opcion = 1
                                        else:
                                            limpiarPantalla()
                                            Opcion = menu_principal()
                                else:
                                    print(f'El Titulo de libro \033[1;37m {TituloPrestamo} \033[0;37m no se encuentra en la base.')
                                    Opcion = menu_principal()
                            else:
                                print(f'\033[0;32mEl cliente {ClientePrestamo} no tiene Libros prestados')
                                print(CambioColor(Normal,Blanco))
                                if Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Prestamos.'):
                                    limpiarPantalla()
                                    Opcion = menu_principal()
                                else:
                                    limpiarPantalla()
                                    Opcion = 1
                else:
                    print(f'\033[0;31mEl DNI {CambioColor(Negrita,Amarillo)}{ClientePrestamo} {CambioColor(Normal,Blanco)}no existe, cargue alta de cliente. \n')
                    print(f'\033[0;37m')
                    Continuar = Confirmacion('Desea cargar ahora el alta de Cliente?')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = 2
                    else:
                        limpiarPantalla()
                        Opcion = menu_principal()
            else:
                print(f'\033[1;32m La Base de Clientes esta vacia, verifique que ha sucedido.')
                print(CambioColor(Normal,Blanco))
                Opcion = menu_principal()
        else:
            limpiarPantalla()
            Opcion = menu_principal()

    elif Opcion == 2:
        OpcionCliente = sub_menuCliLi('Cliente')

        if OpcionCliente == 0:
            limpiarPantalla()
            print("\033[1;36m" + "Gestion de Clientes \n")
            print('\033[0;37m' + "")
            print(f'\033[0;36m Alta de Cliente')
            print(f'\033[0;37m ')
            ClienteDni = IngresarDniTelefono('DNI', 'Alta',' ')
            ExisteDNI = BuscoRegistro('Clientes.txt', ClienteDni, 0)
            if ExisteDNI[0] == 'S':
                BuscarNombre = BuscoRegistro('Clientes.txt', ClienteDni, 0)
                Registro = BuscarNombre[2]
                Registro = Registro[0][:-2].split(',')
                print(f'El DNI ingresado corresponde al Cliente: {Registro[1]}')
                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                if Continuar:
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    limpiarPantalla()
                    Opcion = 2
            else:
                print(' ')
                ClienteNombre = IngresarNombre('Cliente','Alta',' ')
                ClienteTelefono = IngresarDniTelefono('Telefono', 'Alta',' ')
                ClienteDireccion = IngresarDireccion('Modif')
                CargaCliente = ClienteDni + ',' + ClienteNombre + ',' + ClienteTelefono + ',' + ClienteDireccion.upper() + ',D, \n'
                nvoRegistro('Clientes.txt',CargaCliente)
                print(f'Registro de Cliente cargado.')
                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                if Continuar:
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    limpiarPantalla()
                    Opcion = 2

        elif OpcionCliente == 1:
            limpiarPantalla()
            print("\033[1;36m" + "Gestion de Clientes \n")
            print('\033[0;37m' + "")
            print(f'\033[0;36m Consulta Estado de Cliente')
            print(f'\033[0;37m ')

            ClienteDni = IngresarDniTelefono('DNI', 'Consulta',' ')
            BusquedaCliente = BuscoRegistro('Clientes.txt', ClienteDni, 0)
            if BusquedaCliente[0] != 'E':
                IndiceBusqueda = BusquedaCliente[1]
                if BusquedaCliente[0] == 'S':
                    with open('Clientes.txt', 'r+', encoding="utf-8") as rwClientes:
                        lineas = rwClientes.readlines()
                        renglon = lineas[IndiceBusqueda].split(',')
                        print(f' ')
                        print(f'\033[0;37m Nombre: \033[1;37m {renglon[1]}')
                        print(f'\033[0;37m Telefono: \033[1;37m {renglon[2]}')
                        print(f'\033[0;37m Domicilio: \033[1;37m {renglon[3]} \n')
                        if renglon[4] == 'D' or renglon[4] == 'E' or renglon[4] == ' ' or renglon[4] == '':
                            print(f'\033[0;37m Estado: \033[1;32m DISPONIBLE')
                            print(f'\033[0;37m')
                        else:
                            print(f'\033[0;37m Estado: \033[1;31m NO DISPONIBLE')
                            print(f'\033[0;37m')
                            BuscarPrestado = BuscoRegistro('Libros.txt', renglon[5][:-2], 0)
                            with open('libros.txt', 'r', encoding="utf-8") as rLibros:
                                lineasLibros = rLibros.readlines()
                                renglonLibro = lineasLibros[BuscarPrestado[1]].split(',')
                                print(f'')
                                print(f'Usted no ha devuelto el libro: \033[1;33m {renglonLibro[1]}')
                                print(f'\033[0;37m')
                        Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                        if Continuar:
                            limpiarPantalla()
                            Opcion = menu_principal()
                        else:
                            limpiarPantalla()
                            Opcion = 2
                else:
                    print(f'\033[0;34m')
                    print(f'El DNI {ClienteDni} no existe en la base de Datos. \n')
                    print(f' {CambioColor(Normal,Blanco)}')
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 2
            else:
                print(f' {CambioColor(Negrita,Rojo)}')
                print(f'No existe en la base de Datos. \n')
                print(f' {CambioColor(Normal,Blanco)}')
                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                if Continuar:
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    limpiarPantalla()
                    Opcion = 2

        elif OpcionCliente == 2:
            limpiarPantalla()
            print("\033[1;36m" + "Gestion de Clientes \n")
            print('\033[0;37m' + "")
            print(f'\033[0;36m Modificacion de Cliente')
            print(f'\033[0;37m ')

            ClienteDni = IngresarDniTelefono('DNI', 'Consulta',' ')
            BusquedaCliente = BuscoRegistro('Clientes.txt', ClienteDni, 0)
            if BusquedaCliente[0] != 'E':
                IndiceBusqueda = BusquedaCliente[1]
                if BusquedaCliente[0] == 'S':
                    with open('Clientes.txt', 'r+', encoding="utf-8") as rwClientes:
                        lineas = rwClientes.readlines()
                        renglon = lineas[IndiceBusqueda].split(',')
                        print(f'\033[0;37m Nombre: \033[1;37m {renglon[1]}')
                        print(f'\033[0;37m Telefono: \033[1;37m {renglon[2]}')
                        print(f'\033[0;37m Domicilio: \033[1;37m {renglon[3]}')
                        if renglon[4] == 'D':
                            print(f'\033[0;37m Estado: \033[1;32m DISPONIBLE')
                            print(f'\033[0;37m')
                        else:
                            print(f'\033[0;37m Estado: \033[1;31m NO DISPONIBLE')
                            print(f'\033[0;37m')
                        modNombre = IngresarNombre('Cliente', 'Modif',renglon[1])
                        modTelefono = IngresarDniTelefono('Telefono', 'Modif', renglon[2])
                        modDomicilio = IngresarTitulo('Domicilio Cliente','Modif',renglon[3])
                        if renglon[4] == 'D':
                            RegistroMod = ClienteDni + ',' + modNombre + ',' + modTelefono + ',' + modDomicilio + ',' + renglon[4] + ', \n'
                        else:
                            RegistroMod = ClienteDni + ',' + modNombre + ',' + modTelefono + ',' + modDomicilio + ',' + renglon[4] + ',' + renglon[5][:-2] + ' \n'

                        modificaRegistro('Clientes.txt', BusquedaCliente[1], RegistroMod)

                        Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                        if Continuar:
                            limpiarPantalla()
                            Opcion = menu_principal()
                        else:
                            limpiarPantalla()
                            Opcion = 2
                else:
                    print(f' {CambioColor(Normal,Rojo)}')
                    print(f'El DNI {CambioColor(Negrita,Rojo)} {ClienteDNI} {CambioColor(Normal,Rojo)} no existe en la base de Datos. \n')
                    print(f' {CambioColor(Normal,Blanco)}')
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 2
            else:
                print(f' {CambioColor(Negrita,Rojo)}')
                print(f'No existe en la base de Datos. \n')
                print(f' {CambioColor(Normal,Blanco)}')
                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                if Continuar:
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    limpiarPantalla()
                    Opcion = 2

        elif OpcionCliente == 3:
            limpiarPantalla()
            print("\033[1;36m" + "Gestion de Clientes \n")
            print('\033[0;37m' + "")
            print(f'\033[0;36m Baja de Cliente')
            print(f'\033[0;37m ')

            ClienteDni = IngresarDniTelefono('DNI', 'Baja', ' ')
            BusquedaCliente = BuscoRegistro('Clientes.txt', ClienteDni, 0)
            if BusquedaCliente[0] != 'E':
                IndiceBusqueda = BusquedaCliente[1]
                if BusquedaCliente[0] == 'S':
                    with open('Clientes.txt', 'r+', encoding="utf-8") as rwClientes:
                        lineas = rwClientes.readlines()
                        renglon = lineas[IndiceBusqueda].split(',')
                        print(f'\033[0;37m Nombre: \033[1;37m {renglon[1]}')
                        print(f'\033[0;37m Telefono: \033[1;37m {renglon[2]}')
                        print(f'\033[0;37m Domicilio: \033[1;37m {renglon[3]}')
                        if renglon[4] == 'D':
                            print(f'\033[0;37m Estado: \033[1;32m DISPONIBLE')
                            print(f'\033[0;37m')

                        else:
                            print(f'\033[0;37m Estado: \033[1;31m NO DISPONIBLE')
                            print(f'\033[0;37m')
                        if renglon[4] == 'D':
                            Seguro = Confirmacion('Esta seguro de dar de baja el Cliente. S/N?')
                            if Seguro:
                                eliminarRegistro('Clientes.txt', BusquedaCliente[1])
                                print(f' {CambioColor(Normal, Rojo)}\n')
                                print(f'El Cliente {CambioColor(Negrita,Rojo)} {renglon[1]} {CambioColor(Normal,Rojo)}ha sido eliminado de la Base de Datos')
                                print(f'{CambioColor(Normal,Blanco)} ')
                            else:
                                print(f' {CambioColor(Normal,Azul)}')
                                print(f'El Cliente {CambioColor(Negrita,Azul)} {renglon[1]} {CambioColor(Normal,Azul)}No ha sido eliminado de la Base de Datos')
                                print(f' {CambioColor(Normal,Blanco)}')
                                Opcion = 2
                        else:
                            print(f' {CambioColor(Normal, Amarillo)}')
                            print(f'No puede darse de baja hasta no devolver el libro que tiene en Prestamo')
                            print(f' {CambioColor(Normal,Blanco)}')
                            BuscarPrestado = BuscoRegistro('Libros.txt', renglon[5][:-2], 0)
                            with open('libros.txt', 'r', encoding="utf-8") as rLibros:
                                lineasLibros = rLibros.readlines()
                                renglonLibro = lineasLibros[BuscarPrestado[1]].split(',')
                                print(f'')
                                print(f'Usted no ha devuelto el libro: \033[1;33m {renglonLibro[1]}')
                                print(f'\033[0;37m')
                        Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                        if Continuar:
                            limpiarPantalla()
                            Opcion = menu_principal()
                        else:
                            limpiarPantalla()
                            Opcion = 2
                else:
                    print(f' {CambioColor(Normal,Rojo)}')
                    print(f'El DNI {CambioColor(Negrita,Rojo)} {ClienteDni} {CambioColor(Normal,Rojo)} no existe en la base de Datos. \n')
                    print(f' {CambioColor(Normal,Blanco)}')
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 2
            else:
                print(f' {CambioColor(Normal,Rojo)}')
                print(f'No existe en la base de Datos. \n')
                print(f' {CambioColor(Normal,Blanco)}')
                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                if Continuar:
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    limpiarPantalla()
                    Opcion = 2

        else:
            Opcion = menu_principal()

    elif Opcion == 3:
        OpcionLibro = sub_menuCliLi('Libro')

        if OpcionLibro == 0:
            limpiarPantalla()
            print(f' {CambioColor(Negrita,Azul)} Gestion de Libros \n')
            print(f' {CambioColor(Normal,Azul)} Alta de Libros \n')
            print(f'{CambioColor(Normal,Blanco)}')
            LibroISBN = IngresarDniTelefono('ISBN', 'Alta',' ')
            ExisteISBN = BuscoRegistro('Libros.txt',LibroISBN,0)
            if ExisteISBN[0] == 'S':
                RegistroISBN = ExisteISBN[2]
                RegistroISBN = RegistroISBN[0][:-2].split(',')
                print(f' \033[0;33m')
                print(f'El ISBN ingresado corresponde al TITULO: \033[1;33m {RegistroISBN[1]}')
                print(f' \033[0;37m')
                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Libros')
                if Continuar:
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    limpiarPantalla()
                    Opcion = 3
            else:
                LibroTitulo = IngresarTitulo('Ingrese el Titulo del Libro','Consulta',' ')
                LibroAutor = IngresarNombre('Autor','Alta',' ')
                CargaLibro = LibroISBN + ',' + LibroTitulo + ',' + LibroAutor + ',D, \n'
                nvoRegistro('Libros.txt', CargaLibro)
                print(f' {CambioColor(Negrita,Amarillo)}')
                print(f'Registro de libro cargado.')
                print(f' {CambioColor(Normal,Blanco)}')
                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Libros')
                if Continuar:
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    limpiarPantalla()
                    Opcion = 3

        elif OpcionLibro == 1:
            limpiarPantalla()
            print(f' {CambioColor(Negrita, Azul)} Gestion de Libros \n')
            print(f' {CambioColor(Normal, Azul)} Consulta Disponibilidad de Libros \n')
            print(f'{CambioColor(Normal, Blanco)}')
            if Confirmacion('Desea Consultar por Titulo S/N?'):
                TituloConsultar = IngresarTitulo('Cual es el Titulo del Libro que desea Consultar o palabra clave?', 'Consulta', ' ')
                OpcionTitulo = BuscoRegistro('Libros.txt', TituloConsultar, 1)
                Titulo = 'Titulo'
                Titulos = 'Titulos'
                Busca = True
            elif Confirmacion('Desea Consultar por Autor S/N?'):
                TituloConsultar = IngresarTitulo('Cual es el Nombre o Apellido del Autor a Consultar?','Consulta',' ')
                TituloConsultar = TituloConsultar.capitalize()
                OpcionTitulo = BuscoRegistro('Libros.txt', TituloConsultar, 2)
                Titulo = 'Autor'
                Titulos = 'Autores'
                Busca = True
            else:
                limpiarPantalla()
                Busca = False
            if Busca:
                if OpcionTitulo[0] == 'E' or OpcionTitulo[0] == 'N':
                    print(f' {CambioColor(Normal,Cian)}')
                    print(f'El {Titulo} ingresado no existe \033[1;36m {TituloConsultar}')
                    print('\033[0;37m')
                    if len(OpcionTitulo[3]) > 0:
                        print(f' {CambioColor(Negrita, Azul)}')
                        print(f' Los {Titulos} que contienen la Clave {TituloConsultar} son:'.center(130, '▼'))
                        print(f' {CambioColor(Normal,Blanco)}')
                        RegistrosD = OpcionTitulo[3]
                        LongitudD = len(RegistrosD)
                        if LongitudD > 0:
                            maxPantalla = 0
                            campos = ['ISBN', 'TITULO', 'AUTOR']
                            print(f'| {CambioColor(Negrita,Azul)}{campos[0]:^13} {CambioColor(Normal,Azul)}||{CambioColor(Negrita,Azul)} {campos[1]:^55} {CambioColor(Normal,Azul)}||{CambioColor(Negrita,Azul)} {campos[2]:^52} {CambioColor(Normal,Azul)}|')
                            print(f' ')
                            print(f'='.center(130, '='))
                            print(f' {CambioColor(Normal,Blanco)}')
                            for registro in RegistrosD:
                                RegImpr = registro.split(',')
                                if maxPantalla < 21:
                                    print(f'| {RegImpr[0]:^13} || {RegImpr[1]:55s} || {RegImpr[2]:50s} |')
                                    maxPantalla += 1
                                    Continuar = True
                                else:
                                    print(' ')
                                    Continuar = Confirmacion('Presione S para continuar con la lista o N para salir al menu Clientes')
                                    if Continuar:
                                        limpiarPantalla()
                                        print(f'| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} |')
                                        print(f'='.center(130, '='))
                                        maxPantalla = 0
                                    else:
                                        limpiarPantalla()
                                        Opcion = 3
                                        break
                            if Continuar:
                                print(f' {CambioColor(Negrita,Azul)}')
                                print(f' Fin de {Titulos} con la clave {TituloConsultar} '.center(130, '▲'))
                                print(f' {CambioColor(Normal,Blanco)}')
                                if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                                    Opcion = menu_principal()
                                else:
                                    Opcion = 3
                        else:
                            Opcion = 3
                    else:
                        print(f' {CambioColor(Normal,Blanco)}')
                        if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                            limpiarPantalla()
                            Opcion = menu_principal()
                        else:
                            limpiarPantalla()
                            Opcion = 3
                else:
                    renglon = OpcionTitulo[2]
                    renglon = renglon[0].split(',')
                    print(f' ')
                    print(f'Autor: {CambioColor(Negrita,Blanco)} {renglon[2]} {CambioColor(Normal,Blanco)}')
                    print(f'ISBN: {CambioColor(Negrita,Blanco)} {renglon[0]} {CambioColor(Normal,Blanco)}')
                    print(f' ')
                    if renglon[3] == 'D':
                        print(f'Estado: {CambioColor(Negrita,Verde)} DISPONIBLE {CambioColor(Normal,Blanco)}')
                    else:
                        print(f'Estado: {CambioColor(Negrita,Rojo)} NO DISPONIBLE {CambioColor(Normal,Blanco)}')
                        BuscarClientePrestamo = BuscoRegistro('Clientes.txt', renglon[4][:-2], 0)
                        with open('Clientes.txt', 'r', encoding="utf-8") as rClientes:
                            lineasClientes = rClientes.readlines()
                            renglonCliente = lineasClientes[BuscarClientePrestamo[1]].split(',')
                            print(f'')
                            print(f'El cliente que posee el libro es: \033[1;33m {renglonCliente[1]}')
                            print(f'\033[0;37m')
                    print(f' ')
                    if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3
            else:
                print(f' {CambioColor(Negrita,Amarillo)}')
                print(f'Ud. no eligio ninguno de los dos tipos de Busqueda (Libro o Autor)')
                print(f' {CambioColor(Normal,Blanco)}')
                if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                    limpiarPantalla()
                    Opcion = menu_principal()
                else:
                    limpiarPantalla()
                    Opcion = 3
        elif OpcionLibro == 2:
            limpiarPantalla()
            print(f' {CambioColor(Negrita, Azul)} Gestion de Libros \n')
            print(f' {CambioColor(Normal, Azul)} Modificacion de Libros \n')
            print(f'{CambioColor(Normal, Blanco)}')
            TituloConsultar = IngresarTitulo('Cual es el Titulo del Libro que desea Modificar?','Consulta',' ')
            OpcionTitulo = BuscoRegistro('Libros.txt', TituloConsultar, 1)
            if OpcionTitulo[0] == 'E' or OpcionTitulo[0] == 'N':
                print('\033[1;36m')
                print(f'El titulo ingresado no existe {TituloConsultar}')
                print('\033[0;37m')
                if len(OpcionTitulo[3]) > 0:
                    print(f'Los Titulos que contienen la Clave {TituloConsultar} son:'.center(130, '▼'))
                    print(f' ')
                    RegistrosD = OpcionTitulo[3]
                    LongitudD = len(RegistrosD)
                    if LongitudD > 0:
                        maxPantalla = 0
                        campos = ['ISBN', 'TITULO', 'AUTOR']
                        print(f'| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} |')
                        print(f'='.center(130, '='))
                        for registro in RegistrosD:
                            RegImpr = registro.split(',')
                            if maxPantalla < 21:
                                print(f'| {RegImpr[0]:^13} || {RegImpr[1]:55s} || {RegImpr[2]:50s} |')
                                maxPantalla += 1
                                Continuar = True
                            else:
                                print(' ')
                                Continuar = Confirmacion('Presione S para continuar con la lista o N para salir al menu Clientes')
                                if Continuar:
                                    limpiarPantalla()
                                    print(f'| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} |')
                                    print(f'='.center(130, '='))
                                    maxPantalla = 0
                                else:
                                    limpiarPantalla()
                                    Opcion = 2
                                    break
                        if Continuar:
                            print(f'Fin de Libros con la clave {TituloConsultar}'.center(130, '▲'))
                            if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                                limpiarPantalla()
                                Opcion = menu_principal()
                            else:
                                limpiarPantalla()
                                Opcion = 3
                    else:
                        limpiarPantalla()
                        Opcion = 3
                else:
                    print(' ')
                    if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3

            else:
                with open('Libros.txt', 'r+', encoding="utf-8") as rwLibros:
                    lineas = rwLibros.readlines()
                    renglon = OpcionTitulo[2]
                    renglon = renglon[0].split(',')

                    print(' ')
                    print(f'\033[0;37m ISBN: \033[1;37m {renglon[0]}')
                    print(f'\033[0;37m Titulo: \033[1;37m {renglon[1]}')
                    print(f'\033[0;37m Autor: \033[1;37m {renglon[2]}')

                    if renglon[4] == 'D':
                        print(f'\033[0;37m Estado: \033[1;32m DISPONIBLE')
                        print(f'\033[0;37m')
                    else:
                        print(f'\033[0;37m Estado: \033[1;31m NO DISPONIBLE')
                        print(f'\033[0;37m')

                    modTitulo = IngresarTitulo('Nuevo Titulo', 'Modif', renglon[1])
                    modAutor = IngresarAutor('Ingresar Autor', 'Modif', renglon[2])
                    LibroISBN = IngresarAutor('Ingresar ISBN', 'Modif', renglon[0])

                    if renglon[3] == 'D':
                        RegistroMod = LibroISBN + ',' + modTitulo + ',' + modAutor + ','  + renglon[3] + ', \n'
                    else:
                        RegistroMod = LibroISBN + ',' + modTitulo + ',' + modAutor + ',' + renglon[3] + ',' + renglon[4][:-2] + ' \n'

                    modificaRegistro('Libros.txt', OpcionTitulo[1], RegistroMod)

                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Libros')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3
        elif OpcionLibro == 3:
            limpiarPantalla()
            print(f' {CambioColor(Negrita, Azul)} Gestion de Libros \n')
            print(f' {CambioColor(Normal, Azul)} Eliminacion de Libros \n')
            print(f'{CambioColor(Normal, Blanco)}')
            TituloConsultar = IngresarTitulo('Cual es el Titulo del Libro que desea Eliminar o palabra clave?','Consulta', ' ')
            OpcionTitulo = BuscoRegistro('Libros.txt', TituloConsultar, 1)
            if OpcionTitulo[0] == 'E' or OpcionTitulo[0] == 'N':
                print('\033[1;36m')
                print(f'El titulo ingresado no existe {TituloConsultar}')
                print('\033[0;37m')
                if len(OpcionTitulo[3]) > 0:
                    print(f'Los Titulos que contienen la Clave {TituloConsultar} son:'.center(130, '▼'))
                    print(f' ')
                    RegistrosD = OpcionTitulo[3]
                    LongitudD = len(RegistrosD)
                    if LongitudD > 0:
                        maxPantalla = 0
                        campos = ['ISBN', 'TITULO', 'AUTOR']
                        print(f'| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} |')
                        print(f'='.center(130, '='))
                        for registro in RegistrosD:
                            RegImpr = registro.split(',')
                            if maxPantalla < 21:
                                print(f'| {RegImpr[0]:^13} || {RegImpr[1]:55s} || {RegImpr[2]:50s} |')
                                maxPantalla += 1
                                Continuar = True
                            else:
                                print(' ')
                                Continuar = Confirmacion(
                                    'Presione S para continuar con la lista o N para salir al menu Clientes')
                                if Continuar:
                                    limpiarPantalla()
                                    print(f'| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} |')
                                    print(f'='.center(130, '='))
                                    maxPantalla = 0
                                else:
                                    limpiarPantalla()
                                    Opcion = 2
                                    break
                        if Continuar:

                            print(f'Fin de Libros con la clave {TituloConsultar}'.center(130, '▲'))
                            if Confirmacion(
                                    'Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                                Opcion = menu_principal()
                            else:
                                Opcion = 3
                    else:
                        Opcion = 3
                else:
                    print(' ')
                    if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                        Opcion = menu_principal()
                    else:
                        Opcion = 3

            else:
                renglon = OpcionTitulo[2]
                renglon = renglon[0].split(',')
                print(f' {CambioColor(Normal,Blanco)}')
                print(f'Autor: {CambioColor(Negrita, Blanco)} {renglon[2]} {CambioColor(Normal,Blanco)}')
                print(f'ISBN: {CambioColor(Negrita, Blanco)} {renglon[0]}{CambioColor(Normal,Blanco)} \n')
                if renglon[3] == 'D':
                    print(f'Estado: {CambioColor(Negrita,Verde)} DISPONIBLE')
                    print(f' {CambioColor(Normal,Blanco)}')
                else:
                    print(f'Estado: {CambioColor(Negrita,Rojo)} NO DISPONIBLE')
                    print(f' {CambioColor(Normal, Blanco)}')
                print(f'='.center(130, '='))
                if renglon[3] == 'D':
                    Continuar = Confirmacion('Esta seguro de Eliminar el Libro?')
                    if Continuar:
                        eliminarRegistro('Libros.txt',OpcionTitulo[1])
                    else:
                        Opcion = 3
                else:
                    print(f' {CambioColor(Normal, Amarillo)}')
                    print(f'No puede dar de baja el Libro hasta no sea devuelto por el cliente que lo tiene en Prestamo')
                    print(f' {CambioColor(Normal, Blanco)}')
                    BuscarClientePrestamo = BuscoRegistro('Clientes.txt', renglon[4][:-2], 0)
                    with open('Clientes.txt', 'r', encoding="utf-8") as rClientes:
                        lineasClientes = rClientes.readlines()
                        renglonCliente = lineasClientes[BuscarClientePrestamo[1]].split(',')
                        print(f'')
                        print(f'El cliente que posee el libro es: \033[1;33m {renglonCliente[1]}')
                        print(f'\033[0;37m')
                if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                    Opcion = menu_principal()
                else:
                    Opcion = 3
        else:
            Opcion = menu_principal()

    else:
        break

print('\033[0;35m' + ' ')
print(f' Gracias por utilizar nuestro Sistema de Biblioteca '.center(130,'*'))
print('\033[0;37m' + "")




