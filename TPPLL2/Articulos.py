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

Articulos_Campos = ('CodigoBarras','Nombre','id_Rubro','CostoUnitario','PrecioFinal','id_Proveedor','UltimoPrecio','Stock','Stock_Minimo','Stock_Maximo')
CamposInt = (0, 2,5,7,8,9)
CamposFloat = (3,4,6)
CamposChar = (1)

class Articulos:
    def __init__(self,tupla):
        self._codigoBarras = tupla[0]
        self._nombre = tupla[1]
        self._idRubro = tupla[2]
        self._costoUnit = tupla[3]
        self._precioFinal = tupla[4]
        self._idProveedor = tupla[5]
        self._ultPrecio = tupla[6]
        self._stock = tupla[7]
        self._stockMin = tupla[8]
        self._stockMax = tupla[9]


    @property
    def idArticulos(self):
        return self._idArticulos

    @idArticulos.setter
    def idArticulos(self, idArt):
        self._idArticulos = idArt

    @property
    def codigoBarras(self):
        return self._codigoBarras

    @codigoBarras.setter
    def codigoBarras(self, Valor):
        self._codigoBarras = Valor

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, Valor):
        self._nombre = Valor

    @property
    def idRubro(self):
        return self._idRubro

    @idRubro.setter
    def idRubro(self, Valor):
        self._idRubro = Valor

    @property
    def costoUnit(self):
        return self._costoUnit

    @costoUnit.setter
    def costoUnit(self, Valor):
        self._costoUnit = Valor

    @property
    def precioFinal(self):
        return self._precioFinal

    @precioFinal.setter
    def precioFinal(self, Valor):
        self._precioFinal = Valor

    @property
    def idProveedor(self):
        return self._idProveedor

    @idProveedor.setter
    def idProveedor(self, Valor):
        self._idProveedor = Valor

    @property
    def ultPrecio(self):
        return self._ultPrecio

    @ultPrecio.setter
    def ultPrecio(self, Valor):
        self._ultPrecio = Valor

    @property
    def stockMin(self):
        return self._stockMin

    @stockMin.setter
    def stockMin(self, Valor):
        self._stockMin = Valor

    @property
    def stockMax(self):
        return self._stockMax

    @stockMax.setter
    def stockMax(self, Valor):
        self._stockMax = Valor

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, Valor):
        self._stock = Valor

    def altaArticulo(self):
        Campos = Articulos_Campos[0]
        Valores = '%s'
        for i in range(1,len(Articulos_Campos)):
            Campos = Campos + ',' + Articulos_Campos[i]
            Valores = Valores + ', %s'

        sqlAlta = 'INSERT INTO articulos (' + Campos + ') VALUES (' + Valores + ')'
        valAlta = self.mostrarArticulos()
        cur.execute(sqlAlta,valAlta)
        dbPk.commit()

#ver el tema de consultas pendientes correccion
    def consultaArticulo(self, campo, valor):
        if campo == 'CODIGOBARRAS':
            sqlConsulta = 'SELECT * FROM articulos WHERE id_articulo = '+ str(valor)
            cur.execute(sqlConsulta)
        elif campo == Cliente_Campos[2]:
            sqlConsulta = 'SELECT * FROM articulos WHERE '+ str(Articulos_Campos[2]) + ' LIKE \"%' + valor + '%\"' #
            cur.execute(sqlConsulta)

        Resultado = cur.fetchall()
        return Resultado

    def modificaArticulo(self,valor):
        CliAux = self.mostrarArticulos()
        sqlModifica = 'UPDATE articulos SET '
        for i in range(0, len(Articulos_Campos)):
            if i == len(Articulos_Campos)-1:
                sqlModifica = sqlModifica + Articulos_Campos[i] + ' = '+ str(CliAux[i])
            elif i in CamposInt:
                sqlModifica = sqlModifica + Articulos_Campos[i] + ' = ' + str(CliAux[i]) + ', '
            elif i in CamposFloat:
                sqlModifica = sqlModifica + Articulos_Campos[i] + ' = ' + str(CliAux[i]) + ', '
            else:
                sqlModifica =  sqlModifica + Articulos_Campos[i] + ' = \"' + CliAux[i] + '\", '

        sqlModifica = sqlModifica + ' WHERE id_articulo = ' + str(valor)
        cur.execute(sqlModifica)
        dbPk.commit()

    def registroArticulo(self):
        datosArticulo = self.mostrarArticulos()



        return

    def mostrarArticulos(self):
        return self.codigoBarras,self.nombre,self.idRubro,self.costoUnit,self.precioFinal,self.idProveedor,self.ultPrecio,self.stock,self.stockMin,self.stockMax

    def buscarId(self):
        buscaidArticulo = 'SELECT id_articulo FROM articulos WHERE CodigoBarras='+str(self.codigoBarras)
        cur.execute(buscaidArticulo)
        resultado = cur.fetchone()
        for ind in resultado:
            self._idArticulos = ind

    def borrarArticulos(self,valor):
        sqlElimina = 'DELETE FROM articulos WHERE id_articulo = ' + str(valor)
        cur.execute(sqlElimina)
        dbPk.commit()

    def aumentarStock(self,valor):
        stockActual = self.stock
        self.stock = stockActual+valor
        sqlModifica = 'UPDATE articulos SET stock = ' + str(self.stock) +  ' WHERE id_articulo = ' + str(self.idArticulos)
        cur.execute(sqlModifica)
        dbPk.commit()

    def disminuirStock(self,valor):
        stockActual = self.stock
        self.stock= stockActual - valor
        sqlModifica = 'UPDATE articulos SET stock = ' + str(self.stock) + ' WHERE id_articulo = ' + str(self.idArticulos)
        cur.execute(sqlModifica)
        dbPk.commit()

