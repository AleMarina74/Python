#!/usr/bin/env python
# _*_ coding: utf-8 _*_

# 6. Crear una clase llamada Persona. Sus atributos son: nombre, edad y DNI. Construya los 
# siguientes métodos para la clase:
# • Un constructor, donde los datos pueden estar vacíos.
# • Los setters y getters para cada uno de los atributos. Hay que validar las entradas de 
# datos.
# • mostrar(): Muestra los datos de la persona.
# • es_mayor_de_edad(): Devuelve un valor lógico indicando si es mayor de edad.


class Persona:
    def __init__(self, nombre='', edad=0, dni=''):
        self._nombre = nombre
        self._edad = edad
        self._dni = dni
    
    @property
    def nombre(self):
        while True:
            try:
                if self._nombre == '':
                    nombre_nuevo = str(input(f'Ingrese Nombre: '))
                else:
                    break

            except ValueError:
                print(f'Debe ingresar un nombre valido. Usted ingreso: {nombre_nuevo}')

            else:
                if not nombre_nuevo.isalpha() or nombre_nuevo == '' or len(nombre_nuevo) < 2:
                    print(f'Debe ingresar un nombre valido. Usted ingreso: {nombre_nuevo}')
                else:
                    self._nombre = nombre_nuevo.lower().capitalize()
                    break
        return self._nombre
    
    @nombre.setter
    def nombre(self, nombre_nuevo):
        self._nombre = nombre_nuevo

    @property
    def edad(self):
        while True:
            try:
                if self._edad < 1:
                    cargar_edad = int(input('Ingrese la edad:'))
                else:
                    break

            except ValueError:
                print("Debe ingresar valores númericos")

            else:
                if cargar_edad < 1:
                    print(f'Debe ingresar edad valida mayor a 0')
                else:
                    self._edad = cargar_edad
                    break

        return self._edad
    
    @edad.setter
    def edad(self, edad_nueva):
        self._edad = edad_nueva
    
    @property
    def dni(self):
        while True:
            try:
                if self._dni == '' or len(self._dni) < 7:
                    cargar_dni = str(input(f"Ingrese DNI: "))

            except ValueError:
                print("Debe ingresar valores númericos")

            else:
                if cargar_dni.isnumeric():
                    if len(cargar_dni) > 8 or len(cargar_dni) < 7:
                        print(f'El DNI no es valido, Debe contener entre 7 y 8 numeros sin el punto.')
                    elif len(cargar_dni) == 7:
                        self._dni = '0' + cargar_dni
                        break
                    else:
                        self._dni = cargar_dni
                        break
        return self._dni
    
    @dni.setter
    def dni(self, nuevo_dni):
        self._dni = nuevo_dni

    def mostrar(self):
        return f'Nombre = {self.nombre}, Edad = {self.edad}, DNI = {self.dni}'
    
    def es_mayor_de_edad(self):
        if self.edad >17:
            mayorEdad = True
        else:
            mayorEdad = False
        return mayorEdad

  

# 7. Crea una clase llamada Cuenta que tendrá los siguientes atributos: titular (que es una 
# persona) y cantidad (puede tener decimales). El titular será obligatorio y la cantidad es 
# opcional. Crear los siguientes métodos para la clase:
# • Un constructor, donde los datos pueden estar vacíos.
# • Los setters y getters para cada uno de los atributos. El atributo no se puede modificar 
# directamente, sólo ingresando o retirando dinero.
# • mostrar(): Muestra los datos de la cuenta.
# • ingresar(cantidad): se ingresa una cantidad a la cuenta, si la cantidad introducida es 
# negativa, no se hará nada.
# • retirar(cantidad): se retira una cantidad a la cuenta. La cuenta puede estar en números 
# rojos.

class Cuenta(Persona):
    def __init__(self, nombre, edad, dni, cantidad=0):
        super().__init__(nombre,edad,dni)
        self._cantidad = cantidad
        
    @property
    def cantidad(self):
        return self._cantidad
    
    @cantidad.setter
    def cantidad(self, importe):
        self._cantidad = importe
    
    def mostrar(self):
        return f'Nombre = {self._nombre}, Edad = {self._edad}, DNI = {self._dni}, Saldo = {self.cantidad}'
    
    def ingresar(self, cantidad):
        if cantidad > 0:
            self._cantidad += cantidad
        

    def retirar(self, cantidad):
        if cantidad > 0:
            self._cantidad -= cantidad




# 8. Vamos a definir ahora una “Cuenta Joven”, para ello vamos a crear una nueva clase 
# CuantaJoven que deriva de la clase creada en el punto 7. Cuando se crea esta nueva clase, 
# además del titular y la cantidad se debe guardar una bonificación que estará expresada en 
# tanto por ciento. Crear los siguientes métodos para la clase:
# • Un constructor.
# • Los setters y getters para el nuevo atributo.
# • En esta ocasión los titulares de este tipo de cuenta tienen que ser mayor de edad, por lo 
# tanto hay que crear un método es_titular_valido() que devuelve verdadero si el titular es 
# mayor de edad pero menor de 25 años y falso en caso contrario.
# • Además, la retirada de dinero sólo se podrá hacer si el titular es válido.
# • El método mostrar() debe devolver el mensaje de “Cuenta Joven” y la bonificación de la 
# cuenta

class CuentaJoven(Cuenta):
    def __init__(self,nombre,edad,dni,cantidad,bonificacion):
        super().__init__(nombre,edad,dni,cantidad)
        self._bonificacion = bonificacion
    
    @property
    def bonificacion(self):
        return self._bonificacion
    
    @bonificacion.setter
    def bonificacion(self, importe):
        self._bonificacion = importe
    
    def es_titular_valido(self):
        if self.es_mayor_de_edad and self.edad < 25:
            es_valido = True
        else:
            es_valido = False
        return es_valido
    
    def retirar(self, importe):
        if self.es_titular_valido:
            self._cantidad -= importe
        else:
            print('No puede retirar dinero porque no es titular de la cuenta')

    def mostrar(self):
        return f'Cuenta Joven, su bonificacion es {self._bonificacion} %'

cuenta = CuentaJoven('ale', 22 ,'45155337',2000,3.5)
print(cuenta.mostrar())
cuenta.ingresar(2000)
print(cuenta.mostrar())
cuenta.ingresar(-2000)
print(cuenta.mostrar())
cuenta.retirar(1000.50)
print(cuenta.mostrar())