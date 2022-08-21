#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import os
import mariadb

bibliotecaDB = mariadb.connect(
    host="127.0.0.1",
    user="root",
    password="root",  # no le puse pass a mi base por el momento
    autocommit=True
)
curbiblio = bibliotecaDB.cursor()
sql = 'CREATE DATABASE ' + 'bibliotecaAle'
curbiblio.execute(sql)
