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

Pedidos_Campos = ('NroPedido', 'Fecha','id_Proveedor','id_Articulo','cantidad','estado','nro_Remito','Total_Remito','Motivo') #'id_Pedido', autoincremental
CamposInt = (0,2,3,4,6)
CamposFloat = (7,)
CamposChar = (5,8)
CamposDate = (1,)
FechaActual = datetime.date.today()
comboConsultasPedidos = ('id_Pedido','Fecha','id_Proveedor','id_Articulo','estado','nro_Remito')

class Pedidos:
    def __init__(self,tupla):
        self._idPedido = tupla[0]
        self._fecha = tupla[1]
        self._idProveedor = tupla[2]
        self._idArticulo = tupla[3]
        self._cantidad = tupla[4]
        self._estado = tupla[5]
        self._remito = tupla[6]
        self._totalRemito = tupla[7]
        self._motivo = tupla[8]

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
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        self._estado = valor

    @property
    def remito(self):
        return self._remito

    @remito.setter
    def remito(self, valor):
        self._remito = valor

    @property
    def totalRemito(self):
        return self._totalRemito

    @totalRemito.setter
    def totalRemito(self, valor):
        self._totalRemito = valor

    @property
    def motivo(self):
        return self._motivo

    @motivo.setter
    def motivo(self, valor):
        self._motivo = valor

    def altaPedidos(self):
        Campos = Pedidos_Campos[0]
        Valores = '%s'
        for i in range(1,len(Pedidos_Campos)):
            Campos = Campos + ',' + Pedidos_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO pedidos (' + Campos + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarPedidos()
        cur.execute(sqlAlta,valAlta)


#ver el tema de consultas pendientes correccion
    def consultarPedidos(self, campo, valor): # comboConsultasPedidos = ('id_Pedido','Fecha','id_Proveedor','id_Articulo','estado','nro_Remito')
        for i in range(0,len(comboConsultasPedidos)):
            if campo == comboConsultasPedidos[i]:
                if i == 1:
                    sqlConsulta = 'SELECT * FROM pedidos WHERE ' + str(comboConsultasPedidos[i])+ ' = \"' + str(valor) + '\"'

                elif i == 0 or i == 2 or i == 3 or i == 5:
                    sqlConsulta = 'SELECT * FROM pedidos WHERE ' + str(comboConsultasPedidos[i]) + ' = ' + str(valor)

                else:
                    sqlConsulta = 'SELECT * FROM pedidos WHERE ' + str(
                        comboConsultasPedidos[i]) + ' LIKE \"%' + valor + '%\"'  #

            else:
                messagebox.showwarning('Validacion',f'No se ha elegido un campo valido de busqueda {campo}')
                break

        cur.execute(sqlConsulta)
        Resultado = cur.fetchall()
        return Resultado

    def modificarPedidos(self,valor):
        CliAux = self.mostrarPedidos()
        sqlModifica = 'UPDATE pedidos SET '
        for i in range(4, len(Pedidos_Campos)):
            if i == len(Pedidos_Campos)-1:
                sqlModifica = sqlModifica + Pedidos_Campos[i] + ' = \"'+ str(CliAux[i+1]) + '\"'
            elif FuncionesMenu.buscarindice(CamposInt, i):
                sqlModifica = sqlModifica + Pedidos_Campos[i] + ' = ' + str(CliAux[i+1]) + ', '
            elif FuncionesMenu.buscarindice(CamposFloat,i):
                sqlModifica = sqlModifica + Pedidos_Campos[i] + ' = ' + str(CliAux[i+1]) + ', '
            elif FuncionesMenu.buscarindice(CamposDate,i):
                # fecha = CliAux[i-1].year + '-' + CliAux[i-1].month + '-' + CliAux[i+1].day
                sqlModifica =  sqlModifica + Pedidos_Campos[i] + ' = \"' + str(CliAux[i+1]) + '\", '
            else:
                sqlModifica =  sqlModifica + Pedidos_Campos[i] + ' = \"' + CliAux[i+1] + '\", '

        sqlModifica = sqlModifica + ' WHERE id_Pedido = ' + str(valor)
        cur.execute(sqlModifica)
        dbPk.commit()

    def mostrarPedidos(self):
        return self.idPedido, self.fecha, self.idProveedor, self.idArticulo, self.cantidad, self.estado, self.remito, self.totalRemito, self.motivo

    def borrarPedidos(self,valor):
        sqlElimina = 'DELETE FROM pedidos WHERE id_pedido = ' + str(valor)
        cur.execute(sqlElimina)
        dbPk.commit()

if __name__ == '__main__':
    instruccion = 'SELECT * FROM pedidos WHERE id_pedido = 1'
    cur.execute(instruccion)
    Resultado = cur.fetchall()
    if len(Resultado) > 0:
        for ind in Resultado:
            pedido = []
            for index in range(0,len(ind)):
                pedido.append(ind[index])
            pedidocampos = tuple(pedido)
            pedidoencontrado = Pedidos(pedidocampos)
            pedidoencontrado.modificarPedidos(1)
    else:
        print('no existe el pedido')
        messagebox.showwarning('Advertencia','No existe el pedido Solicitado')
                # ntrado = Pedidos(ind[0], ind[1], ind[2], ind[3], ind[4])


