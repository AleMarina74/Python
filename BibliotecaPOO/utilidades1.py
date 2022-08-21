#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import os

def limpiarPantalla():
    sisOper = os.name
    if sisOper =='posix': # si fuera unix
        os.system('clear')
    elif sisOper == 'ce' or sisOper == 'dos' or sisOper == 'nt':
        os.system('cls')
        print("\033[1;35m" + "Gestion de biblioteca \n".center(165, ' '))
        print('\033[0;37m' + "")

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

#Menues
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

#ValidacionDatos
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