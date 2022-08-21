#!/usr/bin/env python
# _*_ coding: utf-8 _*_

from utilidades1 import *
import mariadb
from cliente import *
from Libro import *

# dbbiblioteca = mariadb.connect(
#             host="127.0.0.1",
#             user="root",
#             password="root",    # no le puse pass a mi base por el momento
#             autocommit=True
#         )
# cur = dbbiblioteca.cursor()
# cur.execute("CREATE DATABASE bibliotecaAle")
# cur = dbbiblioteca.cursor()
# cur.execute("CREATE TABLE Libros (USBN INT PRIMARY KEY, Titulo VARCHAR(255), Autor VARCHAR(255), estado VARCHAR(255), dni INT)")
# dbbiblioteca.commit()
# cur.execute("CREATE TABLE clientes (dni INT PRIMARY KEY, nombre VARCHAR(255), telefono INT, domicilio VARCHAR(255), estado VARCHAR(1), ISBN INT)")
#  dbbiblioteca.commit()
# sql = "INSERT INTO clientes (dni, nombre, telefono, domicilio, estado, ISBN) VALUES (%s, %s, %s, %s, %s, %s)"
# val = [
#     (24155337, 'Alejandra Marina Magis', 1149921315, 'AV TRIUNVIRATO 4355 5C', 'P', 9781569319727),
#     (12345678, 'Ahilen Rocio Kesternich', 1132065365, 'TRONADOR 2563', 'P', 9789870400691),
#     (22365415, 'Cesar Kesternich', 1149921999, 'PACHECO DE MELO 2635 LOCAL', 'D',0),
#     (20696890, 'David Omar Kesternich', 1149920199, 'PACHECO DE MELO 2635 LOCAL', 'D',0),
#     (98765432, 'Camila Lit', 1234567890, 'PASEO COLON 123 PB B', 'D',0),
#     (00000000, 'Cosme Luar Fulanito', 1111111111, 'CORDOBA 123', 'D',0),
#     (11111111, 'Paula Florencia Cloe', 2222222222, 'PASEO COLON 987 PB 3', 'D',0)
# ]
# cur.executemany(sql, val)
# dbbiblioteca.commit()
# print(cur.rowcount, "Fueron insertados en tabla Clientes.")
# cur = dbbiblioteca.cursor()
# sql = "INSERT INTO Libros (USBN, Titulo, Autor, estado, dni) VALUES (%s, %s, %s, %s, %s)"
# val = [
#     (9786123032166,'FRIDA KAHLO','Frida Kahlo','D',0),
#     (9786123032562,'LO MEJOR DE CONDORITO','Alberto Briceo','D',0),
#     (9786124013737,'MAFALDA LO MEJOR','Quino Caloi','D',0),
#     (9781569319727,'BANANA FISH','Akimi Yoshida','P',24155337),
#     (9789875733169,'EL ROCK DE LA PRINCESA','Cecilia Pisos','D',0),
#     (9789875450745,'LA FAMILIA LOPEZ','Margarita Maine','D',0),
#     (9789875450783,'ARRIBA EL TELON','Beatriz Ferro','D',0),
#     (9789875454118,'DOMINO','Cecilia Pisos','D',0),
#     (9789501303339,'ANTOLOGIA LITERIAIA','Silvana Daszuk','D',0),
#     (9788431678494,'ERASE UNA VEZ DON QUIJOTE','Miguel De Cervantes','D',0),
#     (9789500710022,'BREVE ANTOLOGIA DE CIENCIA FICCION','Arthur Clarke','D',0),
#     (9789500835572,'DOS AÑOS DE VACACIONES','Julio Verne','D',0),
#     (9789500707213,'BRUJAS DE POCO TRABAJO','Silvia Schujer','D',0),
#     (9781451690316,'FAHRENHEIT 451','Ray Bradbury','D',0),
#     (978184168509,'EXCALIBUR','Jenny Dooley','D',0),
#     (9780330337489,'THE SECRET OF PLATFORM 13','Eva Ibbotson','D',0),
#     (9780261102354,'THE FELLOWSHIP OF THE RING','Jrr Tolkien','D',0),
#     (9780553593716,'GAME OF THRONES','Geroge Martin','D',0),
#     (9789875450820,'TORRE DE PAPEL','Adela Basch','D',0),
#     (9789500824088,'ELIJE TU PROPIA AVENTURA - EL SECRETO DE LOS DELFINES','Edward Packard','D',0),
#     (9789505119257,'NADIE TE CREERIA','Luis Maria Pescetti','D',0),
#     (9789871343188,'CONFESIONES DE UN VAMPIRO','Liliana Cinetto','D',0),
#     (9789870400691,'FRIN','Luis Maria Pescetti','P',12345678),
#     (9781402726651,'OLIVER TWIST','Charles Dickens','D',0),
#     (9789876283472,'YO ROBOT','Isaac Asimov','D',0),
#     (9789875664074,'CARRETERA MALDITA','Stephen King','D',0),
#     (1231231231,'MIENTRAS ESCRIBO','STEPHEN KING','D',0),
#     (9500403528,'CEMENTERIO DE MASCOTAS','stephen king','D',0)
# ]
# cur.executemany(sql, val)
# dbbiblioteca.commit()
# print(cur.rowcount, "Fueron insertados en tabla Peliculas.")

dbbiblioteca = mariadb.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database = "bibliotecaAle"
)

cur = dbbiblioteca.cursor()



def consulta_libros():
    sqlConsulta = 'SELECT * FROM Libros'
    cur.execute(sqlConsulta)
    resultado = cur.fetchall()
    campos = ['ISBN', 'TITULO', 'AUTOR']
    print(f'{CambioColor(Negrita, Blanco)}| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} | {CambioColor(Negrita, Amarillo)}')
    print(f'='.center(130, '='))
    CambioColor(Normal,Blanco)
    maxPantalla = 0
    for ind in resultado:
        if maxPantalla < 21:
            print(f'{CambioColor(Normal,Blanco)}| {ind[0]:^13} || {ind[1]:^55} || {ind[2]:^50} |')
            maxPantalla += 1
            Continuar = True
        else:
            print(" ")
            Continuar = Confirmacion('Presione S para continuar con la lista o N para salir al menu Principal')
            if Continuar:
                limpiarPantalla()
                print(f'{CambioColor(Normal, Blanco)}| {campos[0]:^13} || {campos[1]:^55} || {campos[2]:^50} |{CambioColor(Normal, Amarillo)}')
                print(f'='.center(130, '='))
                maxPantalla = 0
            else:
                limpiarPantalla()
                break
    if Continuar:
        print(f'{CambioColor(Negrita, Amarillo)}')
        print(f' Fin de Libros de la Biblioteca '.center(130, '▲'))
        print(CambioColor(Normal, Blanco))
        if Confirmacion('Presione S para volver al menu Principal'):
            Opcion = menu_principal()
        else:
            Opcion = menu_principal()
    else:
        Opcion = menu_principal()
    return Opcion





if __name__ == '__main__':

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
        if Opcion == 0: # Consulta de Libros
            limpiarPantalla()
            print(CambioColor(Negrita, Amarillo))
            print(f' Libros de la Biblioteca '.center(130, '▼'))
            print(CambioColor(Normal, Blanco))
            Opcion = consulta_libros()

        elif Opcion == 1: #Menu Prestamo de Libro
            OpcionPrestamo = sub_menu_prestamos()
            if OpcionPrestamo == 0: #Disponibilidad de Libro por Titulo
                limpiarPantalla()

                print('\033[1:36m')
                print('Consulta Disponibilidad de Libro por Titulo\n')
                print('\033[0;37m')
                TituloConsultar = IngresarTitulo('Cual es el Titulo del Libro a consultar?','Consulta',' ')
                sqlLibro = 'SELECT * FROM Libros WHERE Titulo = \'' + TituloConsultar.upper() + '\''
                cur.execute(sqlLibro)
                Resultado = cur.fetchall()
                if len(Resultado) > 0:
                    for ind in Resultado:
                        libroEncontrado = Libro(ind[0],ind[1],ind[2],ind[3],ind[4])
                        libroEncontrado.imprimirLibro()
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Prestamos')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        Opcion = 1
                else:
                    print(f'\033[0;37m')
                    print(f'El titulo ingresado no existe \033[1;37m {TituloConsultar}')
                    print(CambioColor(Normal, Blanco))
                    if Confirmacion('Desea buscar otro titulo S/N?'):
                        Opcion = 1
                    else:
                        limpiarPantalla()
                        Opcion = menu_principal()


            elif OpcionPrestamo == 1: #  Resgistrar Prestamo de Libro
                limpiarPantalla()
                print("\033[1;36m" + "Prestamo de libros \n")
                print('\033[0;37m' + "")
                print(f'\033[0;36m Carga de Prestamo')
                print(f'\033[0;37m ')
                ClientePrestamo = IngresarDniTelefono('DNI', 'Consulta', ' ')
                sqlCliente = 'SELECT * FROM clientes WHERE DNI = '+ ClientePrestamo
                cur.execute(sqlCliente)
                Resultado = cur.fetchall()
                if len(Resultado) > 0:
                    for ind in Resultado:
                        ClienteEncontrado = Cliente(ind[0],ind[1],ind[2],ind[3],ind[4],ind[5])
                        ClienteEncontrado.imprimirCliente()
                    if ClienteEncontrado.prestado == 'D':
                        ISBNPrestamo = IngresarDniTelefono('Ingrese el ISBN del libro a Prestar', 'Prestamo', ' ')
                        sqlLibro = 'SELECT * FROM Libros WHERE USBN = ' + ISBNPrestamo
                        curlibro = dbbiblioteca.cursor()
                        curlibro.execute(sqlLibro)
                        Resultado = curlibro.fetchall()
                        if len(Resultado) > 0:
                            for ind in Resultado:
                                libroEncontrado = Libro(ind[0], ind[1], ind[2], ind[3], ind[4])
                            print(f' \033[0;33m')
                            print(f'El ISBN ingresado corresponde al TITULO: \033[1;33m {libroEncontrado.Titulo}')
                            print(f' \033[0;37m')

                            if libroEncontrado.estado == 'D': #Registra el prestamo
                                libroEncontrado.estado = 'P'
                                libroEncontrado.dni = ClienteEncontrado.dni
                                sqllibrop = 'UPDATE libros SET estado = \'' + libroEncontrado.estado + '\', DNI = '+ str(libroEncontrado.dni) + ' WHERE USBN = ' + ISBNPrestamo
                                print(sqlLibro)
                                curlibro.execute(sqllibrop)


                                ClienteEncontrado.prestado = 'P'
                                ClienteEncontrado.ISBN = libroEncontrado.ISBN
                                sqlclientep = 'UPDATE clientes SET estado = \'' + ClienteEncontrado.prestado + '\', ISBN = '+ str(ClienteEncontrado.ISBN) + ' WHERE dni = ' + ClientePrestamo
                                curcliente = dbbiblioteca.cursor()
                                curcliente.execute(sqlclientep)
                                dbbiblioteca.commit()
                                print(curlibro.rowcount, " registros modificados Libros")
                                curlibro.close()
                                print(curcliente.rowcount, " registros modificados Clientes")
                                curcliente.close()
                                print(f'Usted modifico el siguiente registro de Cliente')
                                sql = "SELECT * FROM clientes WHERE dni = " + ClientePrestamo
                                cur.execute(sql)
                                Resultado = cur.fetchall()
                                for ind in Resultado:
                                    ClienteEncontrado = Cliente(ind[0], ind[1], ind[2], ind[3], ind[4], ind[5])
                                    ClienteEncontrado.imprimirCliente()

                            else:
                                print(f'\033[0;37m')
                                print(f'El libro {CambioColor(Negrita, Amarillo)} {libroEncontrado.Titulo} \033[0;37m no se encuentra disponible, elija otro libro. \n')
                                Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Prestamos')
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
                        sqlLibro = 'SELECT * FROM Libros WHERE USBN = ' + str(ClienteEncontrado.ISBN)
                        cur.execute(sqlLibro)
                        Resultado = cur.fetchall()
                        if len(Resultado) > 0:
                            for ind in Resultado:
                                libroEncontrado = Libro(ind[0], ind[1], ind[2], ind[3], ind[4])
                            print(f'')
                            print(f'Usted no ha devuelto el libro: \033[1;33m {libroEncontrado.Titulo}')
                            print(f'\033[0;37m')
                            Continuar = Confirmacion(
                                'Presione S para volver al menu Principal o N para volver al menu de Prestamos')
                            if Continuar:
                                limpiarPantalla()
                                Opcion = menu_principal()
                            else:
                                Opcion = 1
                        else:
                            print('Hay incosistencias en la base de datos, chequee los datos')

                else:
                    print('')
                    print(f'El DNI \033[1;37m {ClientePrestamo} \033[0;37m no existe, cargue alta de cliente.')
                    Continuar = Confirmacion('Desea cargar ahora el alta de Cliente S/N?')
                    if Continuar:
                        Opcion = 2
                    else:
                        limpiarPantalla()
                        Opcion = menu_principal()

            elif OpcionPrestamo == 2: #Devolucion de Libro
                limpiarPantalla()
                print("\033[1;36m" + "Prestamo de libros \n")
                print('\033[0;37m' + "")
                print(f'\033[0;36m Devolucion de Libro en Prestamo')
                print(f'\033[0;37m')
                ClientePrestamo = IngresarDniTelefono('DNI', 'Devolucion', ' ')
                sqlCliente = 'SELECT * FROM clientes WHERE DNI = ' + ClientePrestamo
                cur.execute(sqlCliente)
                Resultado = cur.fetchall()
                if len(Resultado) > 0:
                    for ind in Resultado:
                        ClienteEncontrado = Cliente(ind[0], ind[1], ind[2], ind[3], ind[4], ind[5])
                        ClienteEncontrado.imprimirCliente()
                    if ClienteEncontrado.prestado == 'D':
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
                        print(f'\033[0;37m')
                        print(f'\033[1;37m Usted esta devolviendo el libro:')
                        print(f'\033[0;37m')
                        sqllibrop = 'SELECT * FROM Libros WHERE USBN = ' + str(ClienteEncontrado.ISBN)
                        curlibro = dbbiblioteca.cursor()
                        curlibro.execute(sqllibrop)
                        Resultado = curlibro.fetchall()
                        if len(Resultado) > 0:
                            for ind in Resultado:
                                libroEncontrado = Libro(ind[0], ind[1], ind[2], ind[3], ind[4])
                            print(f'\033[0;37m Nombre del libro: {CambioColor(Negrita, Amarillo)} {libroEncontrado.Titulo}')
                            print(f'\033[0;37m')
                            if libroEncontrado.estado == 'P':
                                libroEncontrado.estado = 'D'
                                libroEncontrado.dni = 0
                                sqllibrop = 'UPDATE libros SET estado = \'' + libroEncontrado.estado + '\', DNI = ' + str(libroEncontrado.dni) + ' WHERE USBN = ' + str(libroEncontrado.ISBN)
                                curlibro.execute(sqllibrop)

                                ClienteEncontrado.prestado = 'D'
                                ClienteEncontrado.ISBN = 0
                                sqlclientep = 'UPDATE clientes SET estado = \'' + ClienteEncontrado.prestado + '\', ISBN = ' + str(ClienteEncontrado.ISBN) + ' WHERE dni = ' + ClientePrestamo
                                curcliente = dbbiblioteca.cursor()
                                curcliente.execute(sqlclientep)

                                if Confirmacion(f'Esta seguro que desea devolver el libro {CambioColor(Negrita, Amarillo)} {libroEncontrado.Titulo} {CambioColor(Normal, Blanco)}?'):
                                    dbbiblioteca.commit()
                                    print(curlibro.rowcount, " registros modificados Libros")
                                    curlibro.close()
                                    print(curcliente.rowcount, " registros modificados Clientes")
                                    curcliente.close()
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
                                    print(f' {CambioColor(Negrita, Verde)}')
                                    print(f'No se han modificado los registros.')
                                    print(f'\033[0;37m')
                                    if Confirmacion('Presione S para volver al menu Princial o N para volver al Menu de Prestamos'):
                                        limpiarPantalla()
                                        Opcion = menu_principal()
                                    else:
                                        limpiarPantalla()
                                        Opcion = 1

                            else:
                                print(f'El Titulo de libro \033[1;37m {TituloPrestamo} \033[0;37m no se encuentra en la base.')
                                Opcion = menu_principal()

                else:
                    print(f'\033[0;31mEl DNI {CambioColor(Negrita, Amarillo)}{ClientePrestamo} {CambioColor(Normal, Blanco)}no existe, cargue alta de cliente. \n')
                    print(f'\033[0;37m')
                    if Confirmacion('Presione S para volver al menu Princial o N para volver al Menu de Prestamos'):
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 1
            else:
                Opcion = menu_principal()

        elif Opcion == 2: #Gestion de Clientes
            OpcionCliente = sub_menuCliLi('Cliente')

            if OpcionCliente == 0: #Alta de Cliente
                limpiarPantalla()
                print("\033[1;36m" + "Gestion de Clientes \n")
                print('\033[0;37m' + "")
                print(f'\033[0;36m Alta de Cliente')
                print(f'\033[0;37m ')
                ClienteDni = IngresarDniTelefono('DNI', 'Alta', ' ')
                sqlClienteB = 'SELECT * FROM Clientes WHERE dni = '+str(ClienteDni)
                cur.execute(sqlClienteB)
                Resultado = cur.fetchall()
                if len(Resultado) > 0:
                    for ind in Resultado:
                        ClienteEncontrado = Cliente(ind[0],ind[1],ind[2],ind[3],ind[4],ind[5])
                        print(f'El DNI ingresado corresponde al Cliente: {ind[1]}')
                        ClienteEncontrado.imprimirCliente()
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 2

                else:
                    print(' ')
                    ClienteNombre = IngresarNombre('Cliente', 'Alta', ' ')
                    ClienteTelefono = IngresarDniTelefono('Telefono', 'Alta', ' ')
                    ClienteDireccion = IngresarDireccion('Modif')
                    ClienteNuevo = Cliente(ClienteDni,ClienteNombre,ClienteTelefono,ClienteDireccion,'D',0)
                    sqlClienteN = 'INSERT INTO clientes (dni,nombre,telefono,domicilio,estado,ISBN) VALUES (%s, %s, %s, %s, %s, %s)'
                    valClienteN = ClienteNuevo.alta()
                    cur.execute(sqlClienteN,valClienteN)
                    dbbiblioteca.commit()

                    print(f'Registro de Cliente cargado.')
                    ClienteNuevo.imprimirCliente()
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 2

            elif OpcionCliente == 1: #Consulta estado Cliente
                limpiarPantalla()
                print("\033[1;36m" + "Gestion de Clientes \n")
                print('\033[0;37m' + "")
                print(f'\033[0;36m Consulta Estado de Cliente')
                print(f'\033[0;37m ')

                ClienteDni = IngresarDniTelefono('DNI', 'Consulta', ' ')
                sqlClienteB = 'SELECT * FROM Clientes WHERE dni = ' + str(ClienteDni)
                cur.execute(sqlClienteB)
                Resultado = cur.fetchall()
                if len(Resultado) > 0:
                    for ind in Resultado:
                        ClienteEncontrado = Cliente(ind[0], ind[1], ind[2], ind[3], ind[4], ind[5])
                        ClienteEncontrado.imprimirCliente()
                    if ClienteEncontrado.prestado == 'P':
                        sqlLibro = 'SELECT * FROM Libros WHERE USBN = ' + str(ClienteEncontrado.ISBN)
                        cur.execute(sqlLibro)
                        Resultado = cur.fetchall()
                        if len(Resultado) > 0:
                            for ind in Resultado:
                                libroEncontrado = Libro(ind[0], ind[1], ind[2], ind[3], ind[4])
                            print(f'')
                            print(f'Usted no ha devuelto el libro: \033[1;33m {libroEncontrado.Titulo}')
                            print(f'\033[0;37m')
                            Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Clientes')
                            if Continuar:
                                limpiarPantalla()
                                Opcion = menu_principal()
                            else:
                                Opcion = 2
                    else:
                        Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Clientes')
                        if Continuar:
                            limpiarPantalla()
                            Opcion = menu_principal()
                        else:
                            Opcion = 2

                else:
                    print(f'\033[0;34m')
                    print(f'El DNI {ClienteDni} no existe en la base de Datos. \n')
                    print(f' {CambioColor(Normal, Blanco)}')
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 2


            elif OpcionCliente == 2: #Modificacion de Cliente
                limpiarPantalla()
                print("\033[1;36m" + "Gestion de Clientes \n")
                print('\033[0;37m' + "")
                print(f'\033[0;36m Modificacion de Cliente')
                print(f'\033[0;37m ')

                ClienteDni = IngresarDniTelefono('DNI', 'Consulta', ' ')
                sqlClienteB = 'SELECT * FROM Clientes WHERE dni = ' + str(ClienteDni)
                cur.execute(sqlClienteB)
                Resultado = cur.fetchall()
                if len(Resultado) > 0:
                    for ind in Resultado:
                        ClienteEncontrado = Cliente(ind[0], ind[1], ind[2], ind[3], ind[4], ind[5])
                        ClienteEncontrado.imprimirCliente()
                    modNombre = IngresarNombre('Cliente', 'Modif', ind[1])
                    modTelefono = IngresarDniTelefono('Telefono', 'Modif', ind[2])
                    modDomicilio = IngresarTitulo('Domicilio Cliente', 'Modif', ind[3])
                    ClienteEncontrado._nombre = modNombre
                    ClienteEncontrado._celular = modTelefono
                    ClienteEncontrado._domicilio = modDomicilio
                    sqlClienteModif = 'UPDATE Clientes SET nombre = \'' + ClienteEncontrado._nombre + '\'' + ', telefono = ' + str(ClienteEncontrado._celular) + ', domicilio = \'' + ClienteEncontrado._domicilio + '\' WHERE dni = ' + str(ClienteEncontrado._dni)
                    cur.execute(sqlClienteModif)
                    dbbiblioteca.commit()
                    print(cur.rowcount, " registros modificado del Cliente")

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
                    print(f' {CambioColor(Normal, Blanco)}')
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 2

            elif OpcionCliente == 3: #Baja de Cliente
                limpiarPantalla()
                print("\033[1;36m" + "Gestion de Clientes \n")
                print('\033[0;37m' + "")
                print(f'\033[0;36m Baja de Cliente')
                print(f'\033[0;37m ')

                ClienteDni = IngresarDniTelefono('DNI', 'Baja', ' ')
                sqlClienteB = 'SELECT * FROM Clientes WHERE dni = ' + str(ClienteDni)
                cur.execute(sqlClienteB)
                Resultado = cur.fetchall()
                if len(Resultado) > 0:
                    for ind in Resultado:
                        ClienteEncontrado = Cliente(ind[0], ind[1], ind[2], ind[3], ind[4], ind[5])
                        ClienteEncontrado.imprimirCliente()

                    if ClienteEncontrado.prestado == 'P':
                        print(f' {CambioColor(Normal, Amarillo)}')
                        print(f'No puede darse de baja hasta no devolver el libro que tiene en Cliente')
                        print(f' {CambioColor(Normal, Blanco)}')
                        sqlLibro = 'SELECT * FROM Libros WHERE USBN = ' + str(ClienteEncontrado.ISBN)
                        cur.execute(sqlLibro)
                        Resultado = cur.fetchall()
                        if len(Resultado) > 0:
                            for ind in Resultado:
                                libroEncontrado = Libro(ind[0], ind[1], ind[2], ind[3], ind[4])
                            print(f'')
                            print(f'Usted no ha devuelto el libro: \033[1;33m {libroEncontrado.Titulo}')
                            print(f'\033[0;37m')
                            Continuar = Confirmacion(
                                'Presione S para volver al menu Principal o N para volver al menu de Clientes')
                            if Continuar:
                                limpiarPantalla()
                                Opcion = menu_principal()
                            else:
                                Opcion = 2
                    else:
                        Seguro = Confirmacion('Esta seguro de dar de baja el Cliente. S/N?')
                        if Seguro:
                            sqlClienteBorrar = 'DELETE FROM Clientes WHERE dni = ' + str(ClienteEncontrado._dni)
                            cur.execute(sqlClienteBorrar)
                            dbbiblioteca.commit()
                            print(f' {CambioColor(Normal, Rojo)}\n')
                            print(f'El Cliente {CambioColor(Negrita, Rojo)} {ClienteEncontrado._nombre} {CambioColor(Normal, Rojo)}ha sido eliminado de la Base de Datos')
                            print(f'{CambioColor(Normal, Blanco)} ')
                            print(cur.rowcount, " registros eliminado del Cliente")
                        else:
                            print(f' {CambioColor(Normal, Azul)}')
                            print(f'El Cliente {CambioColor(Negrita, Azul)} {ClienteEncontrado._nombre} {CambioColor(Normal, Azul)}No ha sido eliminado de la Base de Datos')
                            print(f' {CambioColor(Normal, Blanco)}')
                            Opcion = 2

                else:
                    print(f' {CambioColor(Normal, Rojo)}')
                    print(f'El DNI {CambioColor(Negrita, Rojo)} {ClienteDni} {CambioColor(Normal, Rojo)} no existe en la base de Datos. \n')
                    print(f' {CambioColor(Normal, Blanco)}')
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Clientes')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 2

            else:
                Opcion = menu_principal()

        elif Opcion == 3: #Menu Libros
            OpcionLibro = sub_menuCliLi('Libro')

            if OpcionLibro == 0: #Alta de Libros
                limpiarPantalla()
                print(f' {CambioColor(Negrita, Azul)} Gestion de Libros \n')
                print(f' {CambioColor(Normal, Azul)} Alta de Libros \n')
                print(f'{CambioColor(Normal, Blanco)}')
                LibroISBN = IngresarDniTelefono('ISBN', 'Alta', ' ')
                sqlLibro = 'SELECT * FROM Libros WHERE USBN = ' + str(LibroISBN)
                cur.execute(sqlLibro)
                Resultado = cur.fetchall()
                if len(Resultado) > 0:
                    for ind in Resultado:
                        libroEncontrado = Libro(ind[0], ind[1], ind[2], ind[3], ind[4])
                        libroEncontrado.imprimirLibro()
                    print(f' \033[0;33m')
                    print(f'El ISBN ingresado corresponde al TITULO: \033[1;33m {libroEncontrado.Titulo}')
                    print(f' \033[0;37m')
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Libros')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3
                else:
                    LibroTitulo = IngresarTitulo('Ingrese el Titulo del Libro', 'Consulta', ' ')
                    LibroAutor = IngresarNombre('Autor', 'Alta', ' ')
                    LibroNuevo = Libro(LibroISBN,LibroTitulo,LibroAutor,'D',0)
                    sqlLibroNuevo = 'INSERT INTO Libros (USBN,titulo,autor,estado,dni) VALUES (%s, %s, %s, %s, %s)'
                    valLibroN = LibroNuevo.alta()
                    cur.execute(sqlLibroNuevo, valLibroN)
                    dbbiblioteca.commit()
                    print(f'Registro de Libro cargado.')
                    LibroNuevo.imprimirLibro()
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Libros')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3

            elif OpcionLibro == 1: #Disponibilidad de Libro
                limpiarPantalla()
                print(f' {CambioColor(Negrita, Azul)} Gestion de Libros \n')
                print(f' {CambioColor(Normal, Azul)} Consulta Disponibilidad de Libro \n')
                print(f'{CambioColor(Normal, Blanco)}')
                if Confirmacion('Desea Consultar por Titulo S/N?'):
                    TituloConsultar = IngresarTitulo('Cual es el Titulo del Libro que desea Consultar o palabra clave?',
                                                     'Consulta', ' ')
                    sqlBuscaLibro = 'SELECT * FROM Libros WHERE titulo = \'' + TituloConsultar + '\''
                    cur.execute(sqlBuscaLibro)
                    Resultado = cur.fetchall()

                    Titulo = 'Titulo'
                    Titulos = 'Titulos'
                    Busca = True
                elif Confirmacion('Desea Consultar por Autor S/N?'):
                    TituloConsultar = IngresarTitulo('Cual es el Nombre o Apellido del Autor a Consultar?', 'Consulta',
                                                     ' ')
                    TituloConsultar = TituloConsultar.capitalize()
                    sqlBuscaLibro = 'SELECT * FROM Libros WHERE autor = \'' + TituloConsultar + '\''
                    cur.execute(sqlBuscaLibro)
                    Resultado = cur.fetchall()

                    Titulo = 'Autor'
                    Titulos = 'Autores'
                    Busca = True
                else:
                    limpiarPantalla()
                    Busca = False
                if Busca:
                    if len(Resultado) < 1:
                        print(f' {CambioColor(Normal, Cian)}')
                        print(f'El {Titulo} ingresado no existe \033[1;36m {TituloConsultar}')
                        print('\033[0;37m')
                        if Titulo == 'Autor':
                            sqllibroLike = 'SELECT * FROM Libros WHERE autor LIKE \'%' + TituloConsultar + '%\''
                            cur.execute(sqllibroLike)
                            ResultadoL = cur.fetchall()
                        else:
                            sqllibroLike = 'SELECT * FROM Libros WHERE titulo LIKE \'%' + TituloConsultar + '%\''
                            cur.execute(sqllibroLike)
                            ResultadoL = cur.fetchall()
                        if len(ResultadoL) < 1:
                            print(f'No Existen {Titulos} que contienen la Clave {TituloConsultar}')
                            if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                                Opcion = menu_principal()
                            else:
                                Opcion = 3
                        else:
                            print(f' {CambioColor(Negrita, Azul)}')
                            print(f' Los {Titulos} que contienen la Clave {TituloConsultar} son:'.center(130, '▼'))
                            print(f' {CambioColor(Normal, Blanco)}')
                            maxPantalla = 0
                            campos = ['ISBN', 'TITULO', 'AUTOR']
                            print(f'| {CambioColor(Negrita, Azul)}{campos[0]:^13} {CambioColor(Normal, Azul)}||{CambioColor(Negrita, Azul)} {campos[1]:^55} {CambioColor(Normal, Azul)}||{CambioColor(Negrita, Azul)} {campos[2]:^52} {CambioColor(Normal, Azul)}|')
                            print(f'='.center(130, '='))
                            print(f' {CambioColor(Normal, Blanco)}')
                            for ind in ResultadoL:
                                print(f'| {ind[0]:^13} || {ind[1]:^55} || {ind[2]:^52} |')
                                print(f' {CambioColor(Normal, Blanco)}')
                                if maxPantalla < 21:
                                    maxPantalla += 1
                                    Continuar = True
                                else:
                                    print(' ')
                                    Continuar = Confirmacion('Presione S para continuar con la lista o N para salir al menu Libros')
                                    if Continuar:
                                        limpiarPantalla()
                                        campos = ['ISBN', 'TITULO', 'AUTOR']
                                        print(f'| {CambioColor(Negrita, Azul)}{campos[0]:^13} {CambioColor(Normal, Azul)}||{CambioColor(Negrita, Azul)} {campos[1]:^55} {CambioColor(Normal, Azul)}||{CambioColor(Negrita, Azul)} {campos[2]:^52} {CambioColor(Normal, Azul)}|')
                                        print(f'='.center(130, '='))
                                        print(f' {CambioColor(Normal, Blanco)}')
                                        maxPantalla = 0
                                    else:
                                        limpiarPantalla()
                                        Opcion = 3
                                        break
                            if Continuar:
                                print(f' {CambioColor(Negrita, Azul)}')
                                print(f' Fin de {Titulos} con la clave {TituloConsultar} '.center(130, '▲'))
                                print(f' {CambioColor(Normal, Blanco)}')
                                if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                                    Opcion = menu_principal()
                                else:
                                    Opcion = 3
                    elif len(Resultado) > 1:
                        print(f' {CambioColor(Negrita, Azul)}')
                        print(f' Los {Titulos} que contienen la Clave {TituloConsultar} son:'.center(130, '▼'))
                        print(f' {CambioColor(Normal, Blanco)}')
                        maxPantalla = 0
                        for ind in Resultado:
                            campos = ['ISBN', 'TITULO', 'AUTOR']
                            print(
                                f'| {CambioColor(Negrita, Azul)}{ind[0]:^13} {CambioColor(Normal, Azul)}||{CambioColor(Negrita, Azul)} {ind[1]:^55} {CambioColor(Normal, Azul)}||{CambioColor(Negrita, Azul)} {ind[2]:^52} {CambioColor(Normal, Azul)}|')
                            print(f' ')
                            print(f'='.center(130, '='))
                            print(f' {CambioColor(Normal, Blanco)}')
                            if maxPantalla < 21:
                                maxPantalla += 1
                                Continuar = True
                            else:
                                print(' ')
                                Continuar = Confirmacion('Presione S para continuar con la lista o N para salir al menu Libros')
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
                            print(f' {CambioColor(Negrita, Azul)}')
                            print(f' Fin de {Titulos} con la clave {TituloConsultar} '.center(130, '▲'))
                            print(f' {CambioColor(Normal, Blanco)}')
                            if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                                Opcion = menu_principal()
                            else:
                                Opcion = 3
                    else:
                        for ind in Resultado:
                            LibroEncontrado = Libro(ind[0],ind[1], ind[2], ind[3] ,ind[4])
                            LibroEncontrado.imprimirLibro()
                        if Confirmacion(
                                'Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                            limpiarPantalla()
                            Opcion = menu_principal()
                        else:
                            limpiarPantalla()
                            Opcion = 3

                else:
                    print(f' {CambioColor(Negrita, Amarillo)}')
                    print(f'Ud. no eligio ninguno de los dos tipos de Busqueda (Libro o Autor)')
                    print(f' {CambioColor(Normal, Blanco)}')
                    if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3

            elif OpcionLibro == 2: #Modificacion de Libros
                limpiarPantalla()
                print(f' {CambioColor(Negrita, Azul)} Gestion de Libros \n')
                print(f' {CambioColor(Normal, Azul)} Modificacion de Libros \n')
                print(f'{CambioColor(Normal, Blanco)}')
                TituloConsultar = IngresarTitulo('Cual es el Titulo del Libro que desea Modificar?', 'Consulta', ' ')
                sqllibroBuscar = 'SELECT * FROM Libros WHERE titulo = \''+TituloConsultar+'\''
                cur.execute(sqllibroBuscar)
                Resultado = cur.fetchall()
                if len(Resultado) < 1:
                    print('\033[1;36m')
                    print(f'El titulo ingresado no existe {TituloConsultar}')
                    print('\033[0;37m')
                    print(' ')
                    if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3
                else:
                    for ind in Resultado:
                        LibroEncontrado = Libro(ind[0], ind[1], ind[2] , ind[3], ind[4])
                        LibroEncontrado.imprimirLibro()

                    modTitulo = IngresarTitulo('Nuevo Titulo', 'Modif', libroEncontrado._Titulo)
                    modAutor = IngresarAutor('Ingresar Autor', 'Modif', libroEncontrado._Autor)
                    LibroISBN = IngresarAutor('Ingresar ISBN', 'Modif', libroEncontrado._ISBN)
                    libroEncontrado._Titulo = modTitulo
                    libroEncontrado._Autor = modAutor

                    sqlLibroM = 'UPDATE Libros SET USBN = ' + str(LibroISBN) + ', titulo = \'' + libroEncontrado._titulo + '\'' + ', autor = \'' + libroEncontrado._Autor + '\' WHERE USBN = ' + libroEncontrado._ISBN
                    cur.execute(sqlLibroM)
                    dbbiblioteca.commit()
                    print(cur.rowcount, 'Registro modificado de Libro')
                    Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Libros')
                    if Continuar:
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3


            elif OpcionLibro == 3: # Eliminacion de Libro
                limpiarPantalla()
                print(f' {CambioColor(Negrita, Azul)} Gestion de Libros \n')
                print(f' {CambioColor(Normal, Azul)} Eliminacion de Libros \n')
                print(f'{CambioColor(Normal, Blanco)}')
                TituloConsultar = IngresarTitulo('Cual es el Titulo del Libro que desea Eliminar?',
                                                 'Consulta', ' ')
                sqllibroBuscar = 'SELECT * FROM Libros WHERE titulo = \'' + TituloConsultar + '\''
                cur.execute(sqllibroBuscar)
                Resultado = cur.fetchall()
                if len(Resultado) < 1:
                    print('\033[1;36m')
                    print(f'El titulo ingresado no existe {TituloConsultar}')
                    print('\033[0;37m')
                    print(' ')
                    if Confirmacion('Presione S para volver al menu Principal N para volver al Menu Gestion de Libros'):
                        limpiarPantalla()
                        Opcion = menu_principal()
                    else:
                        limpiarPantalla()
                        Opcion = 3
                else:
                    for ind in Resultado:
                        LibroEncontrado = Libro(ind[0], ind[1], ind[2], ind[3], ind[4])
                        LibroEncontrado.imprimirLibro()
                    if LibroEncontrado.estado == 'D':
                        Continuar = Confirmacion('Esta seguro de Eliminar el Libro?')
                        if Continuar:
                            sqlLibroE = 'DELETE FROM Libros WHERE USBN = ' + str(LibroEncontrado._ISBN)
                            cur.execute(sqlLibroE)
                            dbbiblioteca.commit()
                            print(cur.rowcount, 'Registro elimando de Libros')
                            Continuar = Confirmacion('Presione S para volver al menu Principal o N para volver al menu de Gestion de Libros')
                            if Continuar:
                                limpiarPantalla()
                                Opcion = menu_principal()
                            else:
                                limpiarPantalla()
                                Opcion = 3

                        else:
                            Opcion = 3
                    else:
                        print(f' {CambioColor(Normal, Amarillo)}')
                        print(f'No puede dar de baja el Libro hasta no sea devuelto por el cliente que lo tiene en Prestamo')
                        print(f' {CambioColor(Normal, Blanco)}')
                        sqlClienteB = 'SELECT * FROM Clientes WHERE dni = ' + str(LibroEncontrado.dni)
                        cur.execute(sqlClienteB)
                        ResultadoC = cur.fetchall()
                        if len(ResultadoC) > 0 :
                            for ind in ResultadoC:
                                ClienteEncontrado = Cliente(ind[0], ind[1],  ind[2], ind[3], ind[4], ind[5])
                            print(f'')
                            print(f'El cliente que posee el libro es: \033[1;33m {ClienteEncontrado._nombre}')
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
    print(f' Gracias por utilizar nuestro Sistema de Biblioteca '.center(130, '*'))
    print('\033[0;37m' + "")
