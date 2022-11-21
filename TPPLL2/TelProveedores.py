#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import mariadb

dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk'
)
cur = dbPk.cursor()
TelProveedores_Campos = ('CUIT','Telefono','Area','Contacto')
CamposInt = (0)

class TelProveedores:
    def __init__(self,CUIT, telefono, area, contacto):
        self._CUIT = CUIT
        self._telefono = telefono
        self._area = area
        self._contacto = contacto
        self._idTel = 0

    @property
    def idTel(self):
        return self._idTel

    @idTel.setter
    def idTel(self,id):
        self._idTel = id

    @property
    def CUIT(self):
        return self._CUIT

    @CUIT.setter
    def CUIT(self, cuit):
        self._CUIT = cuit

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        self._telefono = telefono

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, areas):
        self._area = areas

    @property
    def contacto(self):
        return self._contacto

    @contacto.setter
    def contacto(self, contact):
        self._contacto = contact

    def altaTelefono(self):
        Campos = TelProveedores_Campos[0]
        Valores = '%s'
        for i in range(1,len(TelProveedores_Campos)):
            Campos = Campos + ',' + TelProveedores_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO telproveedores (' + Campos + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarTelefono()
        cur.execute(sqlAlta,valAlta)
        dbPk.commit()

    def consultaTelefono(self, campo, valor):
        if campo == TelProveedores_Campos[0]:
            sqlConsulta = 'SELECT * FROM telproveedores WHERE ' + campo + ' = '+str(valor)
            cur.execute(sqlConsulta)
            Resultado = cur.fetchall()
        else:
            print('No se puede buscar por otro campo')
            Resultado = []
        return Resultado

    def modificaTelefono(self,id):
        CliAux = self.mostrarTelefono()
        sqlModifica = 'UPDATE telproveedores SET '
        for i in range(0, len(TelProveedores_Campos)):
            if i == len(TelProveedores_Campos)-1:
                sqlModifica = sqlModifica + TelProveedores_Campos[i] + ' = \"'+ str(CliAux[i]) + '\"'
            elif i == 0:
                sqlModifica = sqlModifica + TelProveedores_Campos[i] + ' = ' + str(CliAux[i]) + ', '
            else:
                sqlModifica =  sqlModifica + TelProveedores_Campos[i] + ' = \"' + CliAux[i] + '\", '

        sqlModifica = sqlModifica + ' WHERE id_Telefono = ' + str(id)
        cur.execute(sqlModifica)
        dbPk.commit()

    def mostrarTelefono(self):
        return self.CUIT, self.telefono, self.area, self.contacto

    def encontrarTelefono(self):
        return self.idTel, self.CUIT, self.telefono, self.area, self.contacto

    def encontrarId(self,cuit,telefono):
        sqlEncontrarId = 'SELECT id_telefono FROM telproveedores WHERE CUIT='+str(cuit)+' AND Telefono = \"' + str(telefono) + '\"'
        cur.execute(sqlEncontrarId)
        resultado = cur.fetchone()
        if len(resultado) > 0:
            for ind in resultado:
                return ind[0]
        else:
            return -1

    def borrarUnTelefono(self,id):
        sqlElimina = 'DELETE FROM telproveedores WHERE id_Telefono = ' + str(id)
        cur.execute(sqlElimina)
        dbPk.commit()

    def borrarTodosTelefonos(self,cuit):
        sqlEliminar = 'DELETE FROM telproveedores WHERE CUIT = '+str(cuit)
        cur.execute(sqlEliminar)
        dbPk.commit()

if __name__ == '__main__':
    tel = TelProveedores(1,'1149921999','','CESAR')
    tel2 = TelProveedores(1,'1149921315','Administracion','Alejandra')
    tel3 = TelProveedores(2,'1149920199','','David')

    tel.altaTelefono()
    tel2.altaTelefono()
    tel3.altaTelefono()

    tel1 = TelProveedores(1,'1149921999','Gerente','Cesar')
    tel1.modificaTelefono(1,'1149921999')

    print(tel.consultaTelefono('id_Proveedor', 1))
    print(tel1.consultaTelefono('id_Proveedor',2))

    tel.borrarTelefono(1,'1149921999')
    print(tel.consultaTelefono('id_Proveedor', 1))

