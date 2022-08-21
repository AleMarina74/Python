#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import mariadb

dbbiblioteca = mariadb.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database = "bibliotecaAle"
)
cur = dbbiblioteca.cursor()

class Libro:
    def __init__(self,ISBN,Titulo,Autor,estado,dni):
        self._ISBN = ISBN
        self._Titulo = Titulo
        self._Autor = Autor
        self.estado =  estado
        self.dni = dni

    @property
    def ISBN(self):
        return self._ISBN

    @ISBN.setter
    def ISBN(self, isbn):
        self._ISBN = isbn

    @property
    def Titulo(self):
        return self._Titulo

    @Titulo.setter
    def Titulo(self, tit):
        self._Titulo = tit

    @property
    def Autor(self):
        return self._Autor

    @Autor.setter
    def Autor(self, Aut):
        self._Autor = Aut

    def imprimirLibro(self):
        print('')
        print(f'Titulo: \033[1;37m {self._Titulo}')
        print(f'\033[0;37m Autor: \033[1;37m {self._Autor}')
        print(f'\033[0;37m ISBN: \033[1;37m {self._ISBN}')
        if self.estado == 'D':
            print(f'\033[0;37m')
            print(f'Estado: \033[1;32m DISPONIBLE')
            print(f'\033[0;37m')
        else:
            print(f'\033[0;37m')
            print(f'Estado: \033[1;31m NO DISPONIBLE')
            print(f'\033[0;37m')

    def alta(self):
        return int(self._ISBN),self._Titulo,self._Autor,self.estado, self.dni





if __name__ == '__main__':
    libro1 = Libro
    libro1.consulta_libro()
