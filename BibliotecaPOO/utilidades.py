#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import os
import mariadb


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