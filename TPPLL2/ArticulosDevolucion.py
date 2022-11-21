#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import mariadb
import datetime
import FuncionesMenu
from tkinter import messagebox

dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk'
)
cur = dbPk.cursor()

Art_Devolver_Campos = ('id_Articulo','Fecha','Cantidad','Estado','Motivo', 'Descripcion')
CamposInt = (0,2)
CamposFloat = ()
CamposChar = (3,4,5)
CamposDate = (1,)
FechaActual = datetime.date.today()
comboConsultasArticulosDevol = ('id_Articulo','Fecha','Estado','Motivo')

class ArticulosDevolucion:
    def __init__(self, tupla):
        self._idDevolucion = 0
        self._idArticulo = tupla[0]
        self._fecha = tupla[1]
        self._catindad = tupla[2]
        self._estado = tupla[3]
        self._motivo = tupla[4]
        self._descripcion = tupla[5]

    @property
    def idDevolucion(self):
        return self._idDevolucion

    @idDevolucion.setter
    def idDevolucion(self, valor):
        self._idDevolucion = valor

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor

    @property
    def idArticulo(self):
        return self._idArticulo

    @idArticulo.setter
    def idArticulo(self, valor):
        self._idArticulo = valor

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        self._cantidad = valor

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        self._estado = valor

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = valor

    @property
    def motivo(self):
        return self._motivo

    @motivo.setter
    def motivo(self, valor):
        self._motivo = valor

    def buscarId(self):
        buscaidDevolucion = 'SELECT id_devolucion FROM artdevolver WHERE id_Articulo ='+str(self.idArticulo) +\
                            ' AND Fecha = ' +str(self.fecha) + ' AND Motivo = \"' + self.motivo + '\"'
        cur.execute(buscaidDevolucion)
        resultado = cur.fetchone()
        for ind in resultado:
            self._idArticulos = ind

    def CargarDevolucionArticulo(self):
        Campos = ArticulosDevolucion[0]
        Valores = '%s'
        for i in range(1,len(Art_Devolver_Campos)):
            Campos = Campos + ',' + Art_Devolver_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO artdevolver (' + Campos + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarDevolucion()
        cur.execute(sqlAlta,valAlta)
        dbPk.commit()

    def modificarDevolucion(self,valor):
        CliAux = self.mostrarDevolucion()
        sqlModifica = 'UPDATE artdevolver SET '
        for i in range(0, len(Ventas_Campos)):
            if i == len(Ventas_Campos)-1:
                sqlModifica = sqlModifica + Ventas_Campos[i] + ' = \"'+ str(CliAux[i])+'\"'
            elif FuncionesMenu.buscarindice(CamposInt, i):
                sqlModifica = sqlModifica + Ventas_Campos[i] + ' = ' + str(CliAux[i]) + ', '
            elif FuncionesMenu.buscarindice(CamposFloat,i):
                sqlModifica = sqlModifica + Ventas_Campos[i] + ' = ' + str(CliAux[i]) + ', '
            elif FuncionesMenu.buscarindice(CamposDate,i):
                # fecha = CliAux[i-1].year + '-' + CliAux[i-1].month + '-' + CliAux[i+1].day
                sqlModifica =  sqlModifica + Ventas_Campos[i] + ' = \"' + str(CliAux[i]) + '\", '
            else:
                sqlModifica =  sqlModifica + Ventas_Campos[i] + ' = \"' + CliAux[i] + '\", '

        sqlModifica = sqlModifica + ' WHERE id_devolucion = ' + str(valor)
        cur.execute(sqlModifica)
        dbPk.commit()

    def mostrarDevolucion(self):
        return self.idArticulo, self.fecha, self.cantidad, self.estado, self.motivo, self._descripcion

    def borrarDevolucion(self,valor,valor2):
        sqlElimina = 'DELETE FROM artdevolver WHERE id_devolucion = ' + str(valor)
        cur.execute(sqlElimina)
        dbPk.commit()


