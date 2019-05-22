# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 17:40:40 2019 - Wed May 22 14:27:00 2019

@author: Javier Alejandro Cuartas Micieces

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

from datetime import date
import json
import csv
import pandas as pd
import sqlite3 as sq
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess as sp
import importlib

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
os.chdir('..')

import datavisualizer.miningtb as miningtb
import datavisualizer.graphs as graphs
    
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)

class Db:
    def __init__(self):
        self.tablei=1
        self.delvariables=0
        
        self.conn=sq.connect("seguimientobd.db")
        self.c=self.conn.cursor()
        with open(dname+"\\config.json") as ty:
            self.tp=json.load(ty)
        os.chdir(self.tp["Path"])
        
    def __del__(self):
        self.conn.close()
        
    def reset_db(self):
        Db.export_csv(self,"todo","todo")
        for k in list(self.tp["Columns"].keys()):
            ls=["ID" in k,"Delete" in k,"Last_change" in k]
            if not any(ls):
                del self.tp["Columns"][k]
        with open("config.json",'w') as ty:
            json.dump(self.tp,ty)
        with open("config.json") as ty:
            self.tp=json.load(ty)
        for el in range(1,len(self.tp["Tables"])):
            Db.del_dbtable(self,self.tp["Tables"][el])
        Db.create_dbtables(self)
        Db.import_starter(self)
    
    def create_dbtables(self):
        for el in range(1,len(self.tp["Tables"])):
            Db.create_dbtable(self,el)

    def create_dbtable(self,el):
        for e in range(0,len(self.tp["Building"]["CreateTable"])):
            lind=list()
            for k in self.tp["Columns"].keys():
                lc=[self.tp["Columns"][k][1]+1==el,"ID_" in k]
                if all(lc):
                    lind.append(k)
            ls=list()
            for t in self.tp["Columns"].keys():
                if self.tp["Columns"][t][1]+1==el:
                    ls.append(t)
            if e==1:
                w=w+self.tp["Tables"][el]+self.tp["Building"]["CreateTable"][e]
            elif e==2:
                w=w+"ID"+str(el-1)+self.tp["Building"]["CreateTable"][e]+","
            elif e==3:
                s=0
                for k in ls:
                    if "ID_" in k:
                        w=w+"'"+k+"' "+self.tp["Columns"][k][0]+","
                        s=1
                    elif "ID" in k:
                        continue
                    else:
                        w=w+"'"+k+"' "+self.tp["Columns"][k][0]+","
                if s==1:
                    for r in range(0,len(lind)):
                        w=w+self.tp["Building"]["CreateTable"][e]+lind[r]+self.tp["Building"]["CreateTable"][e+1]+self.tp["Tables"][int(lind[r][3:])+1]+self.tp["Building"]["CreateTable"][e+2]+"ID"+lind[r][3:]+self.tp["Building"]["CreateTable"][e+3]+","
                w=w[:-1]
            else:
                if e==0:
                    w=self.tp["Building"]["CreateTable"][e]
                elif e==7:
                    w=w+self.tp["Building"]["CreateTable"][e]
        self.c.executescript(w)
        self.conn.commit()

    def del_dbtable(self,tablen):
        for k in range(0,len(self.tp["Building"]["Delete"])):
            if k==0:
                w=self.tp["Building"]["Delete"][k]
            elif k==len(self.tp["Building"]["Delete"])-1:
                w=w+tablen+self.tp["Building"]["Delete"][k]
            else:
                w=w+self.tp["Building"]["Delete"][k]
        self.c.executescript(w)
        self.conn.commit()
        
    def add_variables(self,name,tps,table,anull):
        state="ALTER TABLE "+self.tp["Tables"][table+1]+" ADD COLUMN '"+name+"' "+tps
        self.tp["Columns"][name]=[tps,table,anull]
        with open("config.json",'w') as ty:
            json.dump(self.tp,ty)
        with open("config.json") as ty:
            self.tp=json.load(ty)
        self.c.execute(state)
        self.conn.commit()

    def import_starter(self):
        self.newdata=list()
        with open(self.tp["Tables"][self.tablei]+".csv") as cv:
            k=csv.reader(cv, delimiter=';')
            for el in k:
                self.newdata.append(el)
        for cl in range(0,len(self.newdata[0])):
            if self.newdata[0][cl] not in self.tp["Columns"]:
                MainWindow.newcol(self,self.tp["Tables"][self.tablei],self.newdata[0][cl],cl)
        MainWindow.continue_button(self,self.tp["Tables"][self.tablei])

    def load_names(self,tablen):
        self.newdata=list()
        with open(tablen+".csv") as cv:
            k=csv.reader(cv, delimiter=';')
            for el in k:
                self.newdata.append(el)
        state="SELECT * FROM '"+tablen+"' LIMIT 1"
        self.c.execute(state)
        self.c.fetchall()
        self.bdih0=list()
        for i in list(range(0,len(self.c.description))):
            self.bdih0.append(self.c.description[i][0])

    def import_data(self,tablen):
        Db.load_names(self,tablen)
        unsort=0
        for j in list(range(0,len(self.newdata[0]))):
            if self.newdata[0][j] != self.bdih0[j]:
                if self.newdata[0][j] in self.tp["Columns"]:
                    messagebox.showerror("Error por columna desordenada en la base de datos", "Introducir primero todas las columnas correspondientes como "+self.newdata[0][j]+" en la base de datos y vigilar que en el archivo csv de entrada de datos, conserven el mismo orden que en la base de datos (se puede exportar la información existente para ser utilizada como referencia).")
                else:
                    messagebox.showerror("Error por columna inexistente en la base de datos", "Introducir antes de importar los datos, todas las columnas como "+self.newdata[0][j]+", en la base de datos.")
                unsort=1
                break

        if unsort !=1:
            for i in list(range(1,len(self.newdata))):
                state="SELECT ID"+str(self.tp["Tables"].index(tablen)-1)+" FROM '"+tablen+"'"
                self.c.execute(state)
                self.IDs=list()
                R=self.c.fetchall()
                for l in list(range(0,len(R))):
                    self.IDs.append(str(R[l][0]))
                new=1
                try:
                    if self.newdata[i][0] in self.IDs:
                        new=0
                        state="SELECT * FROM '"+tablen+"' WHERE "+self.newdata[0][0]+" = "+self.newdata[i][0]
                        self.c.execute(state)
                        self.bdi=self.c.fetchall()
                        
                        inpch=Db.inputandchanges(self, new,i)
                        if inpch[0]==-1:
                            Db.del_row(self,self.newdata[i][0],tablen)
                            continue
                        else:
                            if inpch[1]==1:
                                state="UPDATE '"+tablen+"' SET "+inpch[0]+" WHERE "+self.newdata[0][0]+" = "+self.newdata[i][0]
                                self.c.execute(state)
                                self.conn.commit()
                    else:
                        inpch=Db.inputandchanges(self, new,i)
                        if inpch[0]==-1:
                            continue
                        else:
                            state="INSERT INTO '"+tablen+"' VALUES "+inpch[0]
                            self.c.execute(state)
                            self.conn.commit()
                except:
                    messagebox.showerror("Error en importación", "Ocurrió un error al importar la fila con código "+self.newdata[i][0]+", aunque fue añadida en la base de datos. Exportar la información asociada y continuar si todo está correcto.")
                    inpch=Db.inputandchanges(self, new,i)
                    if inpch[0]==-1:
                        continue
                    else:
                        state="INSERT INTO '"+tablen+"' VALUES "+inpch[0]
                        self.c.execute(state)
                        self.conn.commit()
        
        if self.tablei<len(self.tp["Tables"])-1:
            if self.delvariables==0:
                MainWindow.continueimport_button(self,self.tp["Tables"][self.tablei])
        else:
            self.tablei=1

    def inputandchanges(self, new,i):
        change=0
        index1=0
        index2=0
        for es in range(0,len(self.newdata[0])):
            if 'Delete' in self.newdata[0][es]:
                index1=es
            if 'Last_change' in self.newdata[0][es]:
                index2=es
        if int(self.newdata[i][index1])==0:
            for j in list(range(0,len(self.newdata[0]))):
                if self.tp["Columns"][self.newdata[0][j]][0] in ['TEXT','DATE']:
                    w="'"+str(self.newdata[i][j])+"'"
                else:
                    w=str(self.newdata[i][j])
                if new==1:
                    self.newdata[i][index2]=str(date.today().strftime("%d/%m/%Y"))
                    if j==0:
                        row="("+w+","
                    elif j !=len(self.newdata[0])-1:
                        row=row+w+","
                    else:
                        row=row+w+")"
                else:
                    if self.newdata[i][j] != str(self.bdi[0][j]):
                        change=1
                        self.newdata[i][index2]=str(date.today().strftime("%d/%m/%Y"))
                    if j==0:
                        row=self.newdata[0][j]+"="+w+","
                    elif j !=len(self.newdata[0])-1:
                        row=row+self.newdata[0][j]+"="+w+","
                    else:
                        row=row+self.newdata[0][j]+"="+w
        else:
            row=-1
        return [row,change]
        
    def list_maincodes(self):
        try:
            state="SELECT ID0 FROM '"+self.tp['Tables'][1]+"'"
            self.c.execute(state)
            lr=list()
            r=self.c.fetchall()
            lr.append('_')
            lr.append('todo')
            for l in list(range(0,len(r))):
                lr.append(str(r[l][0]))
            return lr
        except:
            return ['___']
        
    def set_path(path):
        try:
            os.chdir(path)
            messagebox.showinfo("Cambio de ruta", "Ruta cambiada correctamente.")
        except:
            messagebox.showerror("Error por columna desordenada en la base de datos", "Introducir una ruta de archivos válida.")

    def export_csv(self,a,b):
        if a!='todo':
            if b=='todo':
                ar0="' WHERE ID0"+" = "+a
                ar1="' WHERE ID_0"+" = "+a
            elif b!="individuos":
                ar="' WHERE ID_0"+" = "+a
            else:
                ar="' WHERE ID"+str(self.tp["Tables"].index(b)-1)+" = "+a
        else:
            ar="'"
        lstate=list()
        lname=list()
        if b=='todo':
            if a=='todo':
                ar0=ar
                ar1=ar
            for el in range(1,len(self.tp["Tables"])):
                if el==1:
                    lstate.append("SELECT * FROM '"+self.tp["Tables"][el]+ar0)
                    lname.append(self.tp["Tables"][el])
                else:
                    try:
                        lstate.append("SELECT * FROM '"+self.tp["Tables"][el]+ar1)
                        lname.append(self.tp["Tables"][el])
                    except:
                        lstate.append("SELECT * FROM '"+self.tp["Tables"][el]+"'")
                        lname.append(self.tp["Tables"][el])
        else:
            lstate.append("SELECT * FROM '"+b+ar)
            lname.append(b)
        for j in range(1,len(lstate)+1):
            try:
                self.c.execute(lstate[j-1])
                r=self.c.fetchall()
                bdih0=list()
                name=lname[j-1]+"_exp.csv"
                namedef=Db.no_repeating_name(name, "_exp.csv")
                for i in list(range(0,len(self.c.description))):
                    bdih0.append(self.c.description[i][0])
                    
                with open(namedef,'a',newline='') as filedata:
                    info = csv.writer(filedata, delimiter=';')
                    info.writerow(bdih0)
                    for i in list(range(0,len(r))):
                        info.writerow(r[i])
            except:
                continue

    def delvar_export_csv(self,ntable,namecol,ending):
        lstate="SELECT * FROM '"+self.tp["Tables"][ntable]+"'"
        try:
            indexdelete=0
            self.c.execute(lstate)
            r=self.c.fetchall()
            bdih0=list()
            name=self.tp["Tables"][ntable]+ending
            namedef=Db.no_repeating_name(name,ending)
            for i in list(range(0,len(self.c.description))):
                if self.c.description[i][0]!=namecol:
                    bdih0.append(self.c.description[i][0])
                else:
                    indexdelete=i
                
            with open(namedef,'a',newline='') as filedata:
                info = csv.writer(filedata, delimiter=';')
                info.writerow(bdih0)
                nr=list()
                for i in list(range(0,len(r))):
                    ni=list()
                    for p in range(0,len(r[i])):
                        if p!=indexdelete:
                            ni.append(r[i][p])
                    nr.append(ni)
                    info.writerow(nr[i])
        except:
            messagebox.showerror("Error de eliminación", "Error al exportar registros durante la eliminación.")

    def no_repeating_name(name,term):
        for file in os.listdir(os.curdir):
            if name in file:
                name=name[:-4]+term
                name=Db.no_repeating_name(name,term)
                break
        return name
    
    def del_variables(self,name,ntable):
        self.delvariables=1
        files = [i for i in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),i)) and i.endswith(".csv")]
        ls=list()
        lt=list()
        for f in files:
            cond=[f[:-4] in self.tp["Tables"],f[:-4]!=self.tp["Tables"][ntable]]
            if all(cond):
                if f not in ls:
                    ls.append(f[:-4]+'_in1'+f[-4:])
                    lt.append(f)
                else:
                    rname=Db.no_repeating_name(f,'_p.csv')
                    ls.append(rname)
                    lt.append(f)
            elif f[:-4]!=self.tp["Tables"][ntable]:
                rname=Db.no_repeating_name(f,'_p.csv')
                ls.append(rname)
                lt.append(f)
        for s in range(0,len(ls)-1):
            os.rename(os.path.join(os.getcwd(),lt[s]), os.path.join(os.getcwd(),ls[s]))
        Db.delvar_export_csv(self,ntable,name,'_in2.csv')
        os.rename(os.path.join(os.getcwd(),self.tp["Tables"][ntable]+'.csv'), os.path.join(os.getcwd(),self.tp["Tables"][ntable]+'_bk.csv'))
        files = [i for i in os.listdir(os.getcwd()) if os.path.isfile(os.path.join(os.getcwd(),i))]
        for f in files:
            if any([all(['_p' not in f,'_in1' in f]),'_in2' in f]):
                s=f[:-8]+f[-4:]
                os.rename(os.path.join(os.getcwd(),f), os.path.join(os.getcwd(),s))
        del self.tp["Columns"][name]
        with open("config.json",'w') as ty:
            json.dump(self.tp,ty)
        with open("config.json") as ty:
            self.tp=json.load(ty)
        for el in range(1,len(self.tp["Tables"])):
            if ntable==el:
                Db.del_dbtable(self,self.tp["Tables"][el])
                Db.create_dbtable(self,ntable)
        Db.import_data(self,self.tp["Tables"][ntable])
        self.delvariables=0

    def ren_variable(self,name_orig,name_new,table):
        if len(self.bdih0)<=len(self.newdata[0]):
            Db.export_csv(self,"todo","todo")
            self.tp["Columns"][name_new]=self.tp["Columns"][name_orig]
            del self.tp["Columns"][name_orig]
            with open("config.json",'w') as ty:
                json.dump(self.tp,ty)
            with open("config.json") as ty:
                self.tp=json.load(ty)
            for el in range(1,len(self.tp["Tables"])):
                if table==self.tp["Tables"][el]:
                    Db.del_dbtable(self,self.tp["Tables"][el])
                    Db.create_dbtable(self,self.tp["Tables"].index(table))
            Db.import_data(self,table)
        else:
            messagebox.showerror("Error al renombrar", "Operación no permitida porque si se renombra la columna, habrá distinto número de columnas en el archivo importado que en la base de datos.")
        
    def del_row(self,ID,table):
        state="DELETE FROM '"+table+"' WHERE ID"+str(self.tp["Tables"].index(table)-1)+" = "+ID+";"
        self.c.execute(state)
        self.conn.commit()



class MainWindow:
    
    def __init__(self):
        self.db= Db()
        m=miningtb.variables(self.db.tp["Path"])
        gt=graphs.gp()
        self.fontsizeB='11'
        self.fontsizeT='12'
        
        self.root=Tk()
        self.root.geometry('800x600+300+100')
        self.root.title("Data-visualizer")
        self.root.resizable(0,0)
        #self.root.overrideredirect(1)
        self.style=ttk.Style()
        self.style.configure("TButton",font = ('Arial' , self.fontsizeB))
        self.style.configure("second.TButton",font = ('Arial' , self.fontsizeB), background='red',highlightcolor="green")
        
        self.frame_header=ttk.Frame()
        self.frame_header.pack()
        
        self.frame_folder=ttk.Frame()
        self.frame_folder.pack()
        
        self.frame_graphs=ttk.Frame(width=300,height=500)
        self.frame_graphs.pack()
        
        self.frame_codes=ttk.Frame()
        self.frame_codes.pack()
        
        self.frame_codes_body1=ttk.Frame()
        self.frame_codes_body1.pack()
        
        self.bottomf=ttk.Frame()
        self.bottomf.pack(side=RIGHT,padx=10)
        self.bottomh=ttk.Frame()
        self.bottomh.pack(side=LEFT,padx=10)
        self.bottomg=ttk.Frame()
        self.bottomg.pack(side=LEFT,padx=(230,10))
        
        self.lab1=ttk.Label(self.frame_header,text='Evolución',font = ('Arial' , 15)).grid(row=0,column=0,ipady=20)
        
        image = Image.open(self.db.tp["Path"]+"helpimg.png")
        photo1 = ImageTk.PhotoImage(image.resize((20,20),Image.ANTIALIAS))
        self.bth = Button(self.frame_folder,image=photo1,command=lambda: (MainWindow.helpw(self)))
        self.bth.pack(side=LEFT,padx=(0,10))
        
        image = Image.open(self.db.tp["Path"]+"about.png")
        photo2 = ImageTk.PhotoImage(image.resize((20,20),Image.ANTIALIAS))
        self.bta = Button(self.frame_folder,image=photo2,command=lambda: (sp.Popen(["notepad.exe", self.db.tp["Path"]+"/LICENSE.md"])))
        self.bta.pack(side=LEFT,padx=(0,10))

        self.clopts=['_']+self.db.tp["Tables"]

        def varlist(event):
            self.combo1=StringVar()
            lx=self.db.list_maincodes()
            self.combom1 = ttk.OptionMenu(self.frame_codes_body1, self.combo1,*lx)
            self.combom1.grid(row=3,column=2)
        
        self.bt1=ttk.Button(self.frame_folder,text="Ruta de trabajo", command=self.localization,style="TButton")
        self.bt1.pack(side=LEFT,padx=20)
        self.lab2=ttk.Label(self.frame_folder, text="Variables:",font = ('Arial' , self.fontsizeB))
        self.lab2.pack(side=LEFT,padx=10)
        self.bt3=ttk.Button(self.frame_folder,text="Eliminar", command=lambda: (self.delcol(), varlist),style="TButton")
        self.bt3.pack(side=LEFT,padx=10)
        self.lab2=ttk.Label(self.frame_folder, text="Constructos/Gráficas:",font = ('Arial' , self.fontsizeB))
        self.lab2.pack(side=LEFT,padx=10)
        self.bt4=ttk.Button(self.frame_folder,text="Editar", command=lambda:(self.constructs_menu()),style="TButton")
        self.bt4.pack(side=LEFT,padx=10)
        
        photo=PhotoImage(file='image1.png')
        label=Label(self.frame_graphs, width=850,height=400, image=photo)
        label.pack()

        self.lab3=ttk.Label(self.frame_codes,text='Input   ',font = ('Arial' , self.fontsizeT,'bold')).grid(row=2, column=0)
        self.bt5=ttk.Button(self.frame_codes,text="Importar", command=lambda: (self.db.import_starter(), varlist),style="TButton")
        self.bt5.grid(row=2,column=1)
        self.lab4=ttk.Label(self.frame_codes,font = ('Arial' , self.fontsizeT)).grid(row=2,column=2)

        self.lab5=ttk.Label(self.frame_codes_body1,text='Output   ',font = ('Arial' , self.fontsizeT,'bold')).grid(row=3,column=0)
        self.lab6=ttk.Label(self.frame_codes_body1,text="Código: ",font = ('Arial' , self.fontsizeB))
        self.lab6.grid(row=3,column=1)
        self.combo1=StringVar()
        self.combom1 = ttk.OptionMenu(self.frame_codes_body1, self.combo1,*self.db.list_maincodes())
        self.combom1.grid(row=3,column=2)

        self.lab7=ttk.Label(self.frame_codes_body1,text="Tabla: ",font = ('Arial' , self.fontsizeB))
        self.lab7.grid(row=3,column=3)
        self.combo2=StringVar()
        self.combom2 = ttk.OptionMenu(self.frame_codes_body1, self.combo2,*self.clopts)
        self.combom2.grid(row=3,column=4)
        self.bt6=ttk.Button(self.frame_codes_body1,text="Exportar", command=lambda: (self.db.export_csv(self.combo1.get(),self.combo2.get())),style="TButton")
        self.bt6.grid(row=3,column=5)

        self.bt7=ttk.Button(self.bottomh,text="Actualizar",command=lambda: (importlib.reload(miningtb),importlib.reload(graphs),self.root.destroy(),MainWindow()), style="TButton")
        self.bt7.grid(row=3)
        self.bt8=ttk.Button(self.bottomf,text="Reset Database",command=lambda: (self.db.reset_db(),varlist), style="second.TButton")
        self.bt8.grid(row=3)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()
    
    def on_closing(self):
        del self.db
        self.root.destroy()

    def localization(self):
        self.top=Toplevel()
        self.top.geometry('200x55+350+100')
        self.top.title("Ruta")
        self.top.resizable(0,0)
        self.fontsizeB='11'
        
        self.lab1=ttk.Label(self.top,text="Ruta: ",font = ('Arial' , self.fontsizeB))
        self.lab1.grid(row=0,column=0,padx=(5,0),pady=(5,0))
        entry=StringVar()
        self.entry1=ttk.Entry(self.top,width=24,textvariable=entry)
        self.entry1.grid(row=0,column=1,pady=(5,0))
        self.bt=ttk.Button(self.top,text="Aceptar", command=lambda: Db.set_path(entry.get()),style="TButton")
        self.bt.grid(row=1,column=1,pady=(0,5))

    def helpw(self):
        self.top=Toplevel()
        self.top.geometry('750x550+100+100')
        self.top.title("Ayuda")
        self.top.resizable(0,0)
        self.fontsizeB='11'

        self.frame=ttk.Frame(self.top)
        self.frame.pack(pady=(20,20))
        
        self.ilab1=ttk.Label(self.frame,text="1: ",font = ('Arial' ,self.fontsizeB,'bold'),justify=CENTER)
        self.ilab1.grid(row=1,column=0,padx=(20,10),pady=(10,0))
        self.ilab2=ttk.Label(self.frame,text="2: ",font = ('Arial' ,self.fontsizeB,'bold'),justify=CENTER)
        self.ilab2.grid(row=2,column=0,padx=(20,10),pady=(10,0))
        self.ilab3=ttk.Label(self.frame,text="3: ",font = ('Arial' ,self.fontsizeB,'bold'),justify=CENTER)
        self.ilab3.grid(row=3,column=0,padx=(20,10),pady=(10,0))
        self.ilab4=ttk.Label(self.frame,text="4: ",font = ('Arial' ,self.fontsizeB,'bold'),justify=CENTER)
        self.ilab4.grid(row=4,column=0,padx=(20,10),pady=(10,0))
        self.ilab5=ttk.Label(self.frame,text="5: ",font = ('Arial' ,self.fontsizeB,'bold'),justify=CENTER)
        self.ilab5.grid(row=5,column=0,padx=(20,10),pady=(10,0))
        self.ilab6=ttk.Label(self.frame,text="6: ",font = ('Arial' ,self.fontsizeB,'bold'),justify=CENTER)
        self.ilab6.grid(row=6,column=0,padx=(20,10),pady=(10,0))
        self.ilab7=ttk.Label(self.frame,text="7: ",font = ('Arial' ,self.fontsizeB,'bold'),justify=CENTER)
        self.ilab7.grid(row=7,column=0,padx=(20,10),pady=(10,0))
        
        self.lab1=ttk.Label(self.frame,text="El programa está orientado al almacenamiento en una base de datos sqlite de información \n importada desde archivos csv y la impresión de gráficos relativos a una tabla de minado, \n que contiene selecciones y constructos obtenidos a partir de la base de datos mencionada:",font = ('Arial' , self.fontsizeB),justify=LEFT)
        self.lab1.grid(row=0,columnspan=2,padx=(10,10))
        self.lab1=ttk.Label(self.frame,text="La estructura de tablas y variables se encuentra reflejada en config.json, junto con los \n comandos para resetear la base de datos. ",font = ('Arial' , self.fontsizeB),justify=LEFT)
        self.lab1.grid(row=1,column=1,padx=(0,10),pady=(10,0))
        self.lab2=ttk.Label(self.frame,text="En el modelo inicial se presentan 2 tablas: individuos, con información estática que no\n cambia entre visitas u observaciones; y seguimiento, con información  variable entre\n los distintos momentos/regiones/unidades de observación; Miningtb, con los resultados\n calculados en el archivo miningtb.py, fácilmente accesible mediante el \nbotón 'Constructos: Editar', a partir de la que se representarán en las gráficas dibujadas\n desde el mismo archivo, se exporta también en formato csv.",font = ('Arial' , self.fontsizeB),justify=LEFT)
        self.lab2.grid(row=2,column=1,padx=(0,10),pady=(10,0))
        self.lab3=ttk.Label(self.frame,text="Aunque el añadido de variables y los cambios de nombre son automáticos durante la \n importación, la eliminación se deberá hacer, mediante el botón correspondiente.",font = ('Arial' , self.fontsizeB),justify=LEFT)
        self.lab3.grid(row=3,column=1,padx=(0,10),pady=(10,0))
        self.lab4=ttk.Label(self.frame,text="La ruta de trabajo desde donde se cargan y a la que se pueden exportar las tablas, se \n establece a través del botón establecido a tal efecto en el menú principal.",font = ('Arial' , self.fontsizeB),justify=LEFT)
        self.lab4.grid(row=4,column=1,padx=(0,10),pady=(10,0))
        self.lab5=ttk.Label(self.frame,text="Para exportar información se puede seleccionar el código del individuo y la tabla         \n deseada, pulsando el botón Exportar.",font = ('Arial' , self.fontsizeB),justify=LEFT)
        self.lab5.grid(row=5,column=1,padx=(0,10),pady=(10,0))
        self.lab6=ttk.Label(self.frame,text="Para importar información se utilizará el botón con ese nombre, y la columna Delete \n + Número, deberá tomar el valor 1 sólo cuando deseemos eliminar una fila de\n información.",font = ('Arial' , self.fontsizeB),justify=LEFT)
        self.lab6.grid(row=6,column=1,padx=(0,10),pady=(10,0))
        self.lab7=ttk.Label(self.frame,text="Las columnas de código (IDnúmero), Delete_número y Last_changed_número \nson obligatorias y lo mismo sucede con la ID_número que identificará la foreign key \n en tablas relacionadas.",font = ('Arial' , self.fontsizeB),justify=LEFT)
        self.lab7.grid(row=7,column=1,padx=(0,10),pady=(10,0))

    def delcol(self):
        self.top=Toplevel()
        self.top.geometry('230x85+100+100')
        self.top.title("Eliminar Variable")
        self.top.resizable(0,0)
        self.fontsizeB='11'
        
        self.frame=ttk.Frame(self.top)
        self.frame.pack(pady=(5,5))
        
        self.lab1=ttk.Label(self.frame,text="Tabla: ",font = ('Arial' , self.fontsizeB))
        self.lab1.grid(row=0,column=0)

        self.clopts=list()
        self.c1opts=self.db.tp["Tables"][1:len(self.db.tp["Tables"])+1]
        self.c1opts.insert(0,'_')
        
        def varlist(event):
            ls2=list()
            for el in self.db.tp["Columns"].keys():
                if self.db.tp["Columns"][el][1]+1==self.db.tp["Tables"].index(self.combo1.get()):
                    ls2.append(el)
            self.combo2=StringVar()
            self.combom2 = ttk.OptionMenu(self.frame, self.combo2,*ls2)
            self.combom2.grid(row=1,column=1,sticky="ew")
        
        self.combo1=StringVar()
        self.combom1 = ttk.OptionMenu(self.frame, self.combo1,*self.c1opts,command=varlist)
        self.combom1.grid(row=0,column=1,sticky="ew")
        
        self.lab2=ttk.Label(self.frame,text="Columna: ",font = ('Arial' , self.fontsizeB))
        self.lab2.grid(row=1,column=0)
        
        self.bt=ttk.Button(self.frame,text="Eliminar", command=lambda: (self.db.del_variables(self.combo2.get(),self.db.tp["Tables"].index(self.combo1.get())),self.top.destroy()),style="TButton")
        self.bt.grid(row=2,column=1)

    def constructs_menu(self):
        fontsizeB=11
        top=Toplevel()
        top.geometry('200x100+100+100')
        self.frame=ttk.Frame(top)
        top.resizable(0,0)
        bta=ttk.Button(self.frame,text="Gráficas", command=lambda: (sp.Popen(["notepad.exe", self.db.tp["Path"]+"/graphs.py"])))
        bta.grid(row=1,column=1)
        bta=ttk.Button(self.frame,text="Columnas", command=lambda: (sp.Popen(["notepad.exe", self.db.tp["Path"]+"/miningtb.py"])))
        bta.grid(row=2,column=1)
        btb=ttk.Button(self.frame,text="Actualizar", command=lambda: (importlib.reload(miningtb),importlib.reload(graphs),self.root.destroy(),MainWindow()))
        btb.grid(row=3,column=1)
        self.frame.pack(pady=(10,10))
        
    def newcol(self,tablen,colu,newindex):
        fontsizeB=11
        top=Toplevel()
        top.title("Columna inexistente")
        lab1=ttk.Label(top,text="La columna "+colu+" no está en la base de datos.",font = ('Arial' , fontsizeB))
        lab1.grid(row=0,columnspan=3)
        bta=ttk.Button(top,text="Seleccionar columna existente", command=lambda: (MainWindow.newcol_choose(self,tablen,colu,newindex),top.destroy()))
        bta.grid(row=1,column=0)
        btb=ttk.Button(top,text="Añadir columna", command=lambda: (MainWindow.newcol_add(self,tablen,colu,newindex),top.destroy()))
        btb.grid(row=1,column=1)
        btc=ttk.Button(top,text="Renombrar columna", command=lambda: (MainWindow.newcol_ren(self,tablen,colu,newindex),top.destroy()))
        btc.grid(row=1,column=3)

    def newcol_ren(self,tablen,colu,newindex):
        Db.load_names(self,tablen)
        fontsizeB=11
        top=Toplevel()
        top.title("Seleccionar columna existente correspondiente a '"+colu+"'")
        combo1=StringVar()
        combo = ttk.OptionMenu(top, combo1,*self.tp["Columns"])
        combo.grid(row=0,columnspan=3)
        bta=ttk.Button(top,text="Elegir columna seleccionada", command=lambda: (Db.ren_variable(self,self.bdih0[newindex],colu,tablen),top.destroy()))
        bta.grid(row=1,column=1)
        btb=ttk.Button(top,text="Otras opciones", command=lambda: (MainWindow.newcol(self,tablen,colu,newindex),top.destroy()))
        btb.grid(row=1,column=2)
        
    def newcol_choose(self,tablen, colu,newindex):
        fontsizeB=11
        top=Toplevel()
        top.title("Seleccionar columna existente correspondiente a '"+colu+"'")
        combo1=StringVar()
        combo = ttk.OptionMenu(top, combo1,*self.tp["Columns"])
        combo.grid(row=0,columnspan=3)
        bta=ttk.Button(top,text="Elegir columna seleccionada", command=lambda: (setattr(self,'newdata[0][newindex]',combo1.get()),top.destroy()))
        bta.grid(row=1,column=1)
        btb=ttk.Button(top,text="Otras opciones", command=lambda: (MainWindow.newcol(self,tablen,colu,newindex),top.destroy()))
        btb.grid(row=1,column=2)
        
    def newcol_add(self,tablen,colu,newindex):
        fontsizeB=11
        top=Toplevel()
        top.title("Añadir variables")
        fontsizeB='11'
        lab1=ttk.Label(top,text="Variable: ",font = ('Arial' , fontsizeB))
        lab1.grid(row=0,column=0,columnspan=1)
        entryv=StringVar()
        entryv.set(colu)
        entry1=ttk.Entry(top,width=24, textvariable=entryv)
        entry1.grid(row=0,column=1,columnspan=2)
        lab2=ttk.Label(top,text="Tipo: ",font = ('Arial' , fontsizeB))
        lab2.grid(row=1,column=0,columnspan=1)
        combo1=StringVar()
        combo1.set('TEXT')
        l = ["TEXT", "INTEGER", "DATE", "REAL"]
        combo = ttk.OptionMenu(top, combo1,*l)
        combo.grid(row=1,column=1,columnspan=2)
        cbnull1=IntVar()
        cbnull1.set(0)
        cbnull=ttk.Checkbutton(top, text="Puede estar vacío", variable=cbnull1)
        cbnull.grid(row=2,column=0,columnspan=2)
        cbstatic1=IntVar()
        cbstatic1.set(1)
        cbstatic=ttk.Checkbutton(top, text="Valor inestable que puede cambiar cada recogida de datos", variable=cbstatic1)
        cbstatic.grid(row=3,column=0,columnspan=2)
        bt=ttk.Button(top,text="Añadir", command=lambda: (Db.add_variables(self,entryv.get(),combo1.get(),cbstatic1.get(),cbnull1.get()),top.destroy()))
        bt.grid(row=4,column=0)
        btb=ttk.Button(top,text="Otras opciones", command=lambda: (MainWindow.newcol(self,tablen,colu,newindex), top.destroy()))
        btb.grid(row=4,column=1)

    def continue_button(self,tablen):
        fontsizeB=11
        top=Toplevel()
        top.geometry('500x30+200+200')
        top.title("Continuar")
        top.resizable(0,0)
        btc=ttk.Button(top,text="Pulse si todas las columnas de la tabla '"+tablen+"' han sido asignadas", command=lambda: (Db.import_data(self, tablen), top.destroy()))
        btc.pack(pady=(2,2))
        
    def continueimport_button(self,tablen):
        fontsizeB=11
        top=Toplevel()
        top.geometry('500x30+200+200')
        top.title("Continuar")
        top.resizable(0,0)
        btc=ttk.Button(top,text="Continuar la importación", command=lambda: (Db.import_starter(self), top.destroy()))
        btc.pack(pady=(2,2))
        self.tablei=self.tablei+1

if __name__=="__main__":
    app=MainWindow()