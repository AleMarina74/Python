#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import mariadb
from tkinter import messagebox

dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk',
    autocommit = True
)
cur = dbPk.cursor()


Cliente_Campos = ('DNI', 'NombreApellido', 'Direccion', 'Telefono', 'Mail', 'Id_Iva')
CamposInt = (1, 3, 5)

class Cliente:
    def __init__(self, tupla):
        self._dni = tupla[0]
        self._nombre = tupla[1]
        self._celular = tupla[3]
        self._domicilio = tupla[2]
        self._mail = tupla[4]
        self.id_situacionIva = tupla[5]

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

    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self, mails):
        self._mail = mails

    def altaCliente(self):

        Campos = Cliente_Campos[0]
        Valores = '%s'
        for i in range(1,len(Cliente_Campos)):
            Campos = Campos + ',' + Cliente_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO clientes (' + Campos + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarCliente()
        cur.execute(sqlAlta,valAlta)
        if messagebox.askquestion('Alta Resgistro', f'Esta seguro dar de alta al Cliente\n'
                                                    f'DNI: {self.dni}\n'
                                                    f'Nombre: {self.nombre}') == 'yes':
            dbPk.commit()

            messagebox.showinfo("STATUS", "Registro agregado")
        else:
            messagebox.showinfo('STATUS','No se ha cargado el registro en la base')

    def consultaCliente(self, campo, valor):

        if campo == 'DNI':
            sqlConsulta = 'SELECT * FROM Clientes WHERE DNI = '+str(valor)
            cur.execute(sqlConsulta)
        elif campo == Cliente_Campos[1]:
            sqlConsulta = 'SELECT * FROM clientes WHERE '+ str(Cliente_Campos[2]) + ' LIKE \"%' + valor + '%\"' #
            cur.execute(sqlConsulta)

        Resultado = cur.fetchall()
        # dbPk.close()
        return Resultado

    def modificaCliente(self,valor):
        CliAux = self.mostrarCliente()
        sqlModifica = 'UPDATE clientes SET '
        for i in range(1, len(Cliente_Campos)):
            if i == 5:
                sqlModifica = sqlModifica + Cliente_Campos[i] + ' = '+ str(CliAux[i])
            elif i == 0 or i == 3:
                sqlModifica = sqlModifica + Cliente_Campos[i] + ' = ' + str(CliAux[i]) + ', '
            else:
                sqlModifica =  sqlModifica + Cliente_Campos[i] + ' = \"' + CliAux[i] + '\", '

        sqlModifica = sqlModifica + ' WHERE DNI = ' + str(valor)
        cur.execute(sqlModifica)
        dbPk.commit()

    def mostrarCliente(self):
        return self.dni,self.nombre,self.domicilio,self.celular,str(self.mail),self.id_situacionIva

    def borrarCliente(self,valor):

        sqlElimina = 'DELETE FROM Clientes WHERE DNI = ' + str(valor)
        cur.execute(sqlElimina)
        dbPk.commit()


if __name__ == '__main__':
    # Cliente_Campos = ('id_Cliente', 'DNI', 'NombreApellido', 'Direccion', 'Telefono', 'Mail', 'Id_Iva')
    # Campos = Cliente_Campos[0]
    # Valores = '%s'
    # for i in range(1, len(Cliente_Campos)):
    #     Campos = Campos + ',' + Cliente_Campos[i]
    #     Valores = Valores + ', %s'
    # print(Campos)
    # print(Valores)
    tupla=(1111,'prueba','MELO 2635','12456789','prueba@gmail.com',2)

    Cli = Cliente(tupla)
    Cli.altaCliente()
    print(Cli.mostrarCliente())
    consultaprueba = Cli.consultaCliente(25,25)
    print(consultanombre)
    print(consultadni)
    print(Cli.mostrarCliente())
    Cli.borrarCliente(1111)

