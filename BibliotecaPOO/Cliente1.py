#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import mariadb

dbbiblioteca = mariadb.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database = "bibliotecaAle"
)
curCliente = dbbiblioteca.cursor()

class Cliente:
    def __init__(self, dni, nombre, cel, dom, prestado, ISBN):
        self._dni = dni
        self._nombre = nombre
        self._celular = cel
        self._domicilio = dom
        self.prestado = prestado
        self.ISBN = ISBN

    @property
    def dni(self):
        return self._dni

    @dni.setter
    def dni(self, Dni):
        self._dni = Dni

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, Nombre):
        self._nombre = Nombre

    @property
    def celular(self):
        return self._celular

    @celular.setter
    def celular(self, Cel):
        self._celular = Cel

    @property
    def domicilio(self):
        return self._domicilio

    @domicilio.setter
    def domicilio(self, Domicilio):
        self._domicilio = Domicilio

    def imprimirCliente(self):
        print(f'\033[0;37m Nombre: \033[1;37m {self._nombre}')
        print(f'\033[0;37m Telefono: \033[1;37m {self._celular}')
        print(f'\033[0;37m Domicilio: \033[1;37m {self._domicilio}')
        if self.prestado == 'D':
            print(f'\033[0;37m Estado: \033[1;32m DISPONIBLE')
            print(f'\033[0;37m')
        else:
            print(f'\033[0;37m Estado: \033[1;31m NO DISPONIBLE')
            print(f'\033[0;37m')

    def alta(self):
        return int(self._dni),self._nombre,int(self._celular),self._domicilio,self.prestado, self.ISBN



