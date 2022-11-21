#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import mariadb
import datetime
import FuncionesMenu
import Articulos
from tkinter import messagebox

dbPk = mariadb.connect(
    host = '127.0.0.1',
    user = 'root',
    password = 'root',
    database = 'Pk'
)
cur = dbPk.cursor()

VentasEncabezado_Campos = ('id_Venta', 'Nro_Factura','Fecha','Tipo_Factura','DNI','Total')
#id_Venta es clave primaria autoincremental
CamposIntEncabezado = (0, 1, 3)
CamposFloatEncabezado = (4,)
CamposCharEncabezado = (2,)
CamposDateEncabezado = (1,)

VentasItems_Campos = ('idItem', 'id_Venta','id_Articulo','Detalle','Cantidad','Precio_Unitario','Subtotal')
#idItem es clave primaria y autoincrementable
CamposIntItems = (0, 1, 2, 4)
CamposFloatItems = (5, 6)
CamposCharItems = (3,)

FechaActual = datetime.date.today()
comboConsultasVentas = ('Nro_Factura','Fecha','Tipo_Factura','id_Cliente','Total','id_Articulo','Detalle','Cantidad','Precio_Unitario','Subtotal')

tuplaingresa= ('Nro_Factura','Fecha','Tipo_Factura','id_Cliente','Total','id_Articulo','Detalle','Cantidad','Precio_Unitario','Subtotal')
class Ventas:
    def __init__(self, tupla):
        self._factura = tupla[0]
        self._fecha = tupla[1]
        self._tipofactura = tupla[2]
        self._idCliente = tupla[3]
        self.total = tupla[4]
        self._idArticulo = tupla[5]
        self._detalle = tupla[6]
        self._cantidad= tupla[7]
        self._precioUnit = tupla[8]
        self._subtotal = tupla[9]
        self.IdItem = 0
        self._IdVenta = 0

    @property
    def IdVenta(self):
        return self._IdVenta

    @IdVenta.setter
    def IdVenta(self, idVenta):
        self._IdVenta = idVenta

    @property
    def factura(self):
        return self._factura

    @factura.setter
    def factura(self, idPed):
        self._factura = idPed

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = valor

    @property
    def tipofactura(self):
        return self._tipofactura

    @tipofactura.setter
    def tipofactura(self, valor):
        self._tipofactura = valor

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
    def idCliente(self):
        return self._idCliente

    @idCliente.setter
    def idCliente(self, valor):
        self._idCliente = valor

    @property
    def precioUnit(self):
        return self._precioUnit

    @precioUnit.setter
    def precioUnit(self, valor):
        self._precioUnit = valor

    @property
    def subtotal(self):
        return self._subtotal

    @subtotal.setter
    def subtotal(self, valor):
        self._subtotal = valor

    @property
    def detalle(self):
        return self._detalle

    @detalle.setter
    def detalle(self, valor):
        self._detalle = valor

    def altaVenta(self):
        #Encabezado
        Campos = VentasEncabezado_Campos[1]
        Valores = '%s'
        for i in range(2,len(VentasEncabezado_Campos)):
            Campos = Campos + ',' + VentasEncabezado_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO ventasencabezado (' + Campos + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarVentaEncabezado()
        cur.execute(sqlAlta,valAlta)
        dbPk.commit()
        IdVenta = cur.lastrowid
        self.idVenta = IdVenta

    def altaItems(self, valor):
        #items
        self.IdVenta = valor
        campoitem = VentasItems_Campos[1]
        Valores = '%s'
        for i in range(2,len(VentasItems_Campos)):
            campoitem = campoitem + ',' + VentasItems_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO ventasitems (' + campoitem + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarVentaItem()
        cur.execute(sqlAlta,valAlta)
        dbPk.commit()


    # ver el tema de consultas pendientes correccion
    def consultarVenta(self, campo,
                         valor):  # comboConsultasVentas = ('Nro_Factura','Fecha','Tipo_Factura','id_Cliente')
        for i in range(0, len(comboConsultasVentas)):
            if campo == comboConsultasVentas[i]:
                if i == 1:
                    sqlConsulta = 'SELECT * FROM ventas WHERE ' + str(comboConsultasVentas[i]) + ' = \"' + str(
                        valor) + '\"'

                elif i == 0 or i == 3:
                    sqlConsulta = 'SELECT * FROM ventas WHERE ' + str(comboConsultasVentas[i]) + ' = ' + str(
                        valor)

                else:
                    sqlConsulta = 'SELECT * FROM ventas WHERE ' + str(
                        comboConsultasVentas[i]) + ' LIKE \"%' + valor + '%\"'  #

            else:
                messagebox.showwarning('Validacion', f'No se ha elegido un campo valido de busqueda {campo}')
                break

        cur.execute(sqlConsulta)
        Resultado = cur.fetchall()
        return Resultado

    def modificarVentas(self,valor):
        CliAux = self.mostrarVenta()
        sqlModifica = 'UPDATE ventas SET '
        for i in range(0, len(Ventas_Campos)):
            if i == len(Ventas_Campos)-1:
                sqlModifica = sqlModifica + Ventas_Campos[i] + ' = '+ str(CliAux[i])
            elif FuncionesMenu.buscarindice(CamposInt, i):
                sqlModifica = sqlModifica + Ventas_Campos[i] + ' = ' + str(CliAux[i]) + ', '
            elif FuncionesMenu.buscarindice(CamposFloat,i):
                sqlModifica = sqlModifica + Ventas_Campos[i] + ' = ' + str(CliAux[i]) + ', '
            elif FuncionesMenu.buscarindice(CamposDate,i):
                # fecha = CliAux[i-1].year + '-' + CliAux[i-1].month + '-' + CliAux[i+1].day
                sqlModifica =  sqlModifica + Ventas_Campos[i] + ' = \"' + str(CliAux[i]) + '\", '
            else:
                sqlModifica =  sqlModifica + Ventas_Campos[i] + ' = \"' + CliAux[i] + '\", '

        sqlModifica = sqlModifica + ' WHERE Nro_Factura = ' + str(valor)
        cur.execute(sqlModifica)
        dbPk.commit()

    def mostrarVentaEncabezado(self):
        return self.factura, self.fecha, self.tipofactura, self.idCliente, self.total

    def mostrarVentaItem(self):
        return self.IdVenta, self.idArticulo, self.detalle, self.cantidad, self.precioUnit, self.subtotal

    def borrarVenta(self,valor):
        # no deberia poder borrar una venta, ya que anulo antes de hacer la venta
        sqlElimina = 'DELETE FROM ventasencabezado WHERE id_Venta = ' + str(valor)
        cur.execute(sqlElimina)
        dbPk.commit()
        sqlElimina = 'DELETE FROM ventasitems WHERE id_Venta = ' + str(valor)
        cur.execute(sqlElimina)
        dbPk.commit()


