#!/usr/bin/env python
# _*_ coding: utf-8 _*_


class Cliente:
    def __init__(self):
        self._dni = IngresarDniTelefono('DNI', 'Alta',' ')
        self._nombre = IngresarNombre('Cliente','Alta',' ')
        self._celular = IngresarDniTelefono('Telefono', 'Alta',' ')
        self._domicilio = IngresarDireccion('Modif')
        self.prestado = False
        self.ISBN = ''

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





