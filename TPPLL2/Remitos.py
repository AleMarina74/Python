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
    database = 'Pk',
    autocommit=True
)
cur = dbPk.cursor()

Remitos_Campos = ('id_Remito','Fecha','nro_Remito','id_Proveedor','id_Articulo','cantidad','costo','Total_Remito')
CamposInt = (0,2,3,4,5)
CamposFloat = (6,7)
CamposChar = ()
CamposDate = (1,)
FechaActual = datetime.date.today()
comboConsultasRemitos = ('id_Pedido','Fecha','id_Proveedor','id_Articulo','estado','nro_Remito')

class Remitos:
    def __init__(self,tupla):
        self._idPedido = tupla[0]
        self._fecha = tupla[1]
        self._remito = tupla[2]
        self._idProveedor = tupla[3]
        self._idArticulo = tupla[4]
        self._cantidad = tupla[5]
        self._costo = tupla[6]
        self._totalRemito = tupla[7]

    @property
    def idPedido(self):
        return self._idPedido

    @idPedido.setter
    def idPedido(self, idPed):
        self._idPedido = idPed

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor

    @property
    def idProveedor(self):
        return self._idProveedor

    @idProveedor.setter
    def idProveedor(self, valor):
        self._idProveedor = valor

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
    def remito(self):
        return self._remito

    @remito.setter
    def remito(self, valor):
        self._remito = valor

    @property
    def costo(self):
        return self._costo

    @costo.setter
    def costo(self, valor):
        self._costo = valor

    @property
    def totalRemito(self):
        return self._totalRemito

    @totalRemito.setter
    def totalRemito(self, valor):
        self._totalRemito = valor


    def altaRemitos(self):
        Campos = Remitos_Campos[0]
        Valores = '%s'
        for i in range(1,len(Remitos_Campos)):
            Campos = Campos + ',' + Remitos_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO Remitos (' + Campos + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarRemitos()
        cur.execute(sqlAlta,valAlta)


#ver el tema de consultas pendientes correccion
    def consultarRemitos(self, campo, valor): # comboConsultasRemitos = ('id_Pedido','Fecha','id_Proveedor','id_Articulo','estado','nro_Remito')
        for i in range(0,len(comboConsultasRemitos)):
            if campo == comboConsultasRemitos[i]:
                if i == 1:
                    sqlConsulta = 'SELECT * FROM Remitos WHERE ' + str(comboConsultasRemitos[i])+ ' = \"' + str(valor) + '\"'

                elif i == 0 or i == 2 or i == 3 or i == 5:
                    sqlConsulta = 'SELECT * FROM Remitos WHERE ' + str(comboConsultasRemitos[i]) + ' = ' + str(valor)

                else:
                    sqlConsulta = 'SELECT * FROM Remitos WHERE ' + str(
                        comboConsultasRemitos[i]) + ' LIKE \"%' + valor + '%\"'  #

            else:
                messagebox.showwarning('Validacion',f'No se ha elegido un campo valido de busqueda {campo}')
                break

        cur.execute(sqlConsulta)
        Resultado = cur.fetchall()
        return Resultado

    def modificarRemitos(self,valor):
        CliAux = self.mostrarRemitos()
        sqlModifica = 'UPDATE remitos SET '
        for i in range(4, len(Remitos_Campos)):
            if i == len(Remitos_Campos)-1:
                sqlModifica = sqlModifica + Remitos_Campos[i] + ' = \"'+ str(CliAux[i+1]) + '\"'
            elif FuncionesMenu.buscarindice(CamposInt, i):
                sqlModifica = sqlModifica + Remitos_Campos[i] + ' = ' + str(CliAux[i+1]) + ', '
            elif FuncionesMenu.buscarindice(CamposFloat,i):
                sqlModifica = sqlModifica + Remitos_Campos[i] + ' = ' + str(CliAux[i+1]) + ', '
            elif FuncionesMenu.buscarindice(CamposDate,i):
                # fecha = CliAux[i-1].year + '-' + CliAux[i-1].month + '-' + CliAux[i+1].day
                sqlModifica =  sqlModifica + Remitos_Campos[i] + ' = \"' + str(CliAux[i+1]) + '\", '
            else:
                sqlModifica =  sqlModifica + Remitos_Campos[i] + ' = \"' + CliAux[i+1] + '\", '

        sqlModifica = sqlModifica + ' WHERE id_Remito = ' + str(valor)
        cur.execute(sqlModifica)
        dbPk.commit()

    def mostrarRemitos(self):
        return self.idPedido, self.fecha, self.remito, self.idProveedor, self.idArticulo, self.cantidad, self.costo, self.totalRemito,

    def borrarRemitos(self,valor):
        sqlElimina = 'DELETE FROM Remitos WHERE id_Remito = ' + str(valor)
        cur.execute(sqlElimina)
        dbPk.commit()

if __name__ == '__main__':
    instruccion = 'SELECT * FROM Remitos WHERE id_pedido = 1'
    cur.execute(instruccion)
    Resultado = cur.fetchall()
    if len(Resultado) > 0:
        for ind in Resultado:
            pedido = []
            for index in range(0,len(ind)):
                pedido.append(ind[index])
            pedidocampos = tuple(pedido)
            pedidoencontrado = Remitos(pedidocampos)
            pedidoencontrado.modificarRemitos(1)
    else:
        print('no existe el pedido')
        messagebox.showwarning('Advertencia','No existe el pedido Solicitado')
                # ntrado = Remitos(ind[0], ind[1], ind[2], ind[3], ind[4])


