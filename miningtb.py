# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:40:40 2019 - Wed May 22 14:27:00 2019

@author: Javier A. Cuartas Micieces

Data-visualizer is a personal project to work as a simple data visualizer and 
database builder written in python (v3.7-Anaconda). It is not open for 
contributions at the moment but please, feel free to share any comments, 
questions or suggestions through javiercuartasmicieces@hotmail.com

    Copyright (C) 2019  Javier Alejandro Cuartas Micieces

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published 
    by the Free Software Foundation, version 3.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

@author: pc1pc1
"""
import json
import csv
import sqlite3 as sq
import os
from tkinter import *

#Introducir la combinación de variables columna como en el ejemplo a continuación
#con un número secuencial al comienzo del nombre de la columna resultante en la
#tabla de minado para localizarla en la misma.

class variables:
    def __init__(self, dr):
        try:
            with open(dr+"config.json") as ty:
                tp=json.load(ty)
            conn=sq.connect("seguimientobd.db")
            c=conn.cursor()
            namedef="miningtb.csv"
            if os.path.exists(namedef):
                os.remove(namedef)
            
            self.name1="Global1"#Fill with name of column and input parameters
            self.values1=dict()
            self.vars1=["Dominio1","Dominio2"]
            
            self.name2="Date1"#Fill with name of column and input parameters
            self.values2=dict()
            self.vars2=["Date"]
            
            for els in range(0,len(self.vars1)):
                state="SELECT "+self.vars1[els]+" FROM '"+tp["Tables"][tp["Columns"][self.vars1[els]][1]+1]+"' WHERE ID_0 = 1"
                c.execute(state)
                r=c.fetchall()
                self.values1[self.vars1[els]]=r
            
            for els in range(0,len(self.vars2)):
                state="SELECT "+self.vars2[els]+" FROM '"+tp["Tables"][tp["Columns"][self.vars2[els]][1]+1]+"' WHERE ID_0 = 1"
                c.execute(state)
                r=c.fetchall()
                self.values2[self.vars2[els]]=r
            
            with open(namedef,'a',newline='') as filedata:
                info = csv.writer(filedata, delimiter=';')
                info.writerow([self.name1,self.name2])
                for i in list(range(0,len(r))):
                    info.writerow([self.values1[self.vars1[0]][i][0]+self.values1[self.vars1[1]][i][0], self.values2[self.vars2[0]][i][0]])#Fill with formula
            conn.close()
        except:
            messagebox.showerror("Error al cargar gráficas", "Información incorrecta en la base de datos.")
        