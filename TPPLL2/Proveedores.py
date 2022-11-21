#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import mariadb

dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit=True
)
cur = dbPk.cursor()
Proveedores_Campos = ('id_Proveedor', 'CUIT', 'RazonSocial','Direccion','Mail','Id_Iva')
CamposInt = (0,1,5)

class Proveedores:
    def __init__(self, tupla):
        self._cuit = tupla[0]
        self._nombre = tupla[1]
        self._direccion = tupla[2]
        self._mail = tupla[3]
        self.idIva = tupla[4]

    @property
    def cuit(self):
        return self._cuit

    @cuit.setter
    def cuit(self, cuit):
        self._cuit = cuit

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, razonsocial):
        self._nombre = razonsocial

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, dir):
        self._direccion = dir

    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self, mails):
        self._mail = mails

    def altaProveedor(self):
        Campos = Proveedores_Campos[1]
        Valores = '%s'
        for i in range(2,len(Proveedores_Campos)):
            Campos = Campos + ',' + Proveedores_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO proveedores (' + Campos + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarProveedor()
        cur.execute(sqlAlta,valAlta)
        dbPk.commit()

    def consultaProveedor(self, campo, valor):
        if campo == Proveedores_Campos[1]:
            sqlConsulta = 'SELECT * FROM proveedores WHERE CUIT = ' + str(valor)
            cur.execute(sqlConsulta)
        elif campo == Proveedores_Campos[2]:
            sqlConsulta = 'SELECT * FROM proveedores WHERE '+ str(Proveedores_Campos[2]) + ' LIKE \"%' + valor + '%\"' #
            cur.execute(sqlConsulta)
        elif campo == Proveedores_Campos[3]:
            sqlConsulta = 'SELECT * FROM proveedores WHERE ' + str(
                Proveedores_Campos[3]) + ' LIKE \"%' + valor + '%\"'  #
            cur.execute(sqlConsulta)

        Resultado = cur.fetchall()
        return Resultado

    def modificaProveedor(self,valor):
        CliAux = self.mostrarProveedor()
        sqlModifica = 'UPDATE proveedores SET '
        for i in range(1, len(Proveedores_Campos)):
            if i == 5:
                sqlModifica = sqlModifica + Proveedores_Campos[i] + ' = '+ str(CliAux[i-1])
            elif i == 1:
                sqlModifica = sqlModifica + Proveedores_Campos[i] + ' = ' + str(CliAux[i-1]) + ', '
            else:
                sqlModifica =  sqlModifica + Proveedores_Campos[i] + ' = \"' + CliAux[i-1] + '\", '

        sqlModifica = sqlModifica + ' WHERE CUIT = ' + str(valor)
        cur.execute(sqlModifica)
        dbPk.commit()

    def mostrarProveedor(self):
        return self.cuit, self.nombre, self.direccion, self.mail, self.idIva

    def borrarProveedor(self,valor):
        sqlElimina = 'DELETE FROM proveedores WHERE CUIT = ' + str(valor)
        cur.execute(sqlElimina)
        dbPk.commit()





