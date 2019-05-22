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

"""

import csv
import os
import matplotlib.pyplot as plt

class gp:
    def __init__(self):
        if os.path.exists('image1.png'):
            os.remove('image1.png')
        gdata=list()
        if os.path.exists('miningtb.csv'):
            with open("miningtb.csv") as cv:
                k=csv.reader(cv, delimiter=';')
                for el in k:
                    gdata.append(el)
            plt.title("Evolución")
            plt.ylabel("Severidad")
            plt.xlabel("Año")
            g=list()
            for t in range(0,len(gdata[0])):
                r=list()
                for s in range(0,len(gdata)):
                    r.append(gdata[s][t])
                g.append(r)
            plt.plot(g[1], g[0])
        plt.savefig('image1.png',bbox_inches='tight')
        plt.close()