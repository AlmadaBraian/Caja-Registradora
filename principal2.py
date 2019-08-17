#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Usuario
#
# Created:     13/09/2018
# Copyright:   (c) Usuario 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#from tkinter import *
import tkinter
from tkinter import messagebox
import sqlite3
import sys
from datetime import datetime, date
import time
from tkinter import ttk
import tkinter.font as tkFont
import tkinter as tk
from tkinter.filedialog import *

directorio=""
Total=0.0
renglon=0
renglon_noti=0
agregar=True
abierta=False
vueltov=False
cambi=False
listacodigo=[]
listaNombres=[]
donde=""
ide_entrada=0
vuelta=False
compre=False
codi=""
busca=False
valor=0
fecha=str(time.strftime("%d/%m/%Y"))

hora=time.strftime("%H:%M:%S")

meses=("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio",
"Agosto", "Septiembre","Octubre", "Noviembre", "Diciembre")

dias=("Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo")

diaN= time.strftime("%w")

diaN=int(diaN)-1

dia=dias[diaN]

mesN = time.strftime("%m")

mesN=int(mesN)-1

mes=meses[mesN]

FECHA=dia+" "+str(time.strftime("%d"))+" de "+ mes+ " "+str(time.strftime("%Y"))


class EntryEx(ttk.Entry):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = tk.Menu(self, tearoff=False)
        self.menu.add_command(label="Copiar", command=self.popup_copy)
        self.menu.add_command(label="Cortar", command=self.popup_cut)
        self.menu.add_separator()
        self.menu.add_command(label="Pegar", command=self.popup_paste)
        self.bind("<Button-3>", self.display_popup)

    def display_popup(self, event):
        self.menu.post(event.x_root, event.y_root)

    def popup_copy(self):
        self.event_generate("<<Copy>>")
    def popup_cut(self):
        self.event_generate("<<Cut>>")
    def popup_paste(self):
        self.event_generate("<<Paste>>")


class Table(tk.Frame):
    def __init__(self, parent=None, title="", headers=[], height=10, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._title = tk.Label(self, text=title, background="#ECCCCE", font=("Helvetica", 16))
        self._headers = headers
        self._tree = ttk.Treeview(self,
                                  height=height,
                                  columns=self._headers,
                                  show="headings")
        self._title.pack(side=tk.TOP, fill="x")

        # Agregamos dos scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self._tree.xview)
        hsb.pack(side='bottom', fill='x')

        self._tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        self._tree.pack(side="left")

        for header in self._headers:
            self._tree.heading(header, text=header.title())
            self._tree.column(header, stretch=True,
                              width=tkFont.Font().measure(header.title()))

    def add_row(self, row):
        self._tree.insert('', 'end', values=row)
        for i, item in enumerate(row):
            col_width = tkFont.Font().measure(item)
            if self._tree.column(self._headers[i], width=None) < col_width:
                    self._tree.column(self._headers[i], width=col_width)

#funciones de botones y banderas

def fnKeyPress(key):
    global codi
    global cambi
    global abierta

    if (key.keycode==13):

        if cambi==True:
            introducirproducto()
        else:
            agregarticket()

    else:
        if abierta==False:
            cambi=True
            keyPressed = key.char
            codi+=keyPressed


def cambio():
    global cambi
    cambi=True

def presiona(key):
    global busca
    if (key.keycode==13):
        busca=True

def press(key):
    global vueltov
    if (key.keycode==13):
            vueltov=False


def cambiar():
    global abierta
    abierta=False

def cambia2():
    global vueltov
    vueltov=False

def ingreso_egreso(periodo,comando):

    Totano=0.0

    total=0.0

    conexion=sqlite3.connect("Super.sql")#abre la base de datos

    cursor=conexion.cursor()

    cursor.execute(comando)

    filas = cursor.fetchall()

    for elem in filas:

        mes=elem[1]

        ano=elem[0].find(periodo[0])
        numero=str(elem[3])

        if ano>=0:
            if not numero=="":
                numero=float(numero)
                if mes==periodo[1]:

                    total+=numero
                Totano+=numero

    cursor.close()
    conexion.commit()
    conexion.close()

    return [total, Totano]

def simpledialog(parent,titulo,mensaje):

    global busca
    global cambi
    cambi=False

    abi=True
    t3 = tk.Toplevel(parent)
    t3.title(titulo)
    t3.geometry("210x150")
    t3.focus()
    t3.grab_set()
    t3.protocol("WM_DELETE_WINDOW",cambio)


    lblMensaje = Label(t3,text=mensaje,font=("", 15)).place(x=15,y=10)

    entra=StringVar()

    entra.set("")

    txtBusqueda=EntryEx(t3,textvariable=entra)

    txtBusqueda.focus_set()

    txtBusqueda.place(x=30,y=50)

    btnAceptar=Button(t3,text="Aceptar",
    command=cambio,
    font=("Arial",13),width=10).place(x=50,y=90)


    t3.bind("<Key>", presiona)

    while abi==True:

        for i in range(200):

            if busca==True or cambi==True:
                busca=False
                cambi=False
                abi=False
                t3.destroy()
                return entra.get()

            t3.update()



def libro():

    global meses
    global abierta
    parent=ventana
    vuelta=False
    mostrar=False

    if abierta==False:

        abierta=True;

        t3 = tk.Toplevel(parent, bg="#E8C8CD")
        t3.title("Libro")
        t3.geometry('255x390')
        t3.configure(bg="#E8C8CD")
        t3.focus()
        t3.grab_set()
        t3.protocol("WM_DELETE_WINDOW",cambiar)

        comboMes=ttk.Combobox(t3)
        comboMes["values"]=meses
        comboMes.current(0)
        comboMes.place(x=50,y=110)

        comboAno=ttk.Combobox(t3)
        comboAno["values"]=("2017","2018")
        comboAno.current(0)
        comboAno.place(x=50,y=50)

        lblAno = Label(t3,text="Año",
        background="white").place(x=105,y=20)

        lblPeriodo = Label(t3,text="Periodo",
        background="white").place(x=95,y=80)

        lblIngresos = Label(t3,text="Ingresos del Mes",
        background="white").place(x=10,y=150)

        lblEgresos = Label(t3,text="Egresos del Mes",
        background="white").place(x=130,y=150)

        lblNeto = Label(t3,text="Total neto Mensual",
        background="white").place(x=70,y=230)

        lblTot = Label(t3,text="Total ingreso Anual",
        background="white").place(x=10,y=310)

        comand_in="SELECT * FROM Ventas"

        comand_out="SELECT * FROM Egresos"

        peri=comboMes.get()

        periA=comboAno.get()

        while abierta:

            for i in range(200):

                if not abierta:
                    t3.destroy()
                    break

                periodo=[comboAno.get(),comboMes.get()]

                if not (peri == periodo[1]) or not (periA==periodo[0]) :

                    mostrar=True

                    peri=periodo[1]

                    periA=periodo[0]

                    ing=ingreso_egreso(periodo,comand_in)
                    totalIn=ing[0]

                    Eg=ingreso_egreso(periodo,comand_out)
                    totalEg=Eg[0]

                    netmen= float(totalIn) - float(totalEg)

                    lblIngre.destroy()
                    lblNet.destroy()
                    lblTotal.destroy()
                    lblEgre.destroy()


                if vuelta==False:

                    vuelta=True
                    mostrar=True

                    ing=ingreso_egreso(periodo,comand_in)
                    totalIn=ing[0]

                    Eg=ingreso_egreso(periodo,comand_out)
                    totalEg=Eg[0]

                    netmen= float(totalIn) - float(totalEg)

                if mostrar==True:
                    mostrar=False
                    lblIngre = Label(t3,text="$ "+str(totalIn)+"0",font=("", 15),fg="blue",
                    background="white")

                    lblEgre = Label(t3,text="$ "+str(totalEg)+"0",font=("", 15),fg="blue",
                    background="white")

                    lblNet = Label(t3,text="$ "+str(netmen)+"0",font=("", 15),fg="blue",
                    background="white")

                    lblTotal = Label(t3,text="$ "+str(ing[1])+"0",font=("", 15),fg="blue",
                    background="white")


                    lblIngre.place(x=7,y=180)
                    lblEgre.place(x=130,y=180)
                    lblNet.place(x=70,y=260)
                    lblTotal.place(x=10,y=340)

                t3.update()



#crea una ventana para consultar las tablas de la base de datos

def ventana_reporte():
    global abierta
    global busca
    parent=ventana
    global cambi
    cambi==False
    primera=True
    clientes_headers =("")
    lista=[]

    if abierta==False:
        abierta=True;

        t3 = tk.Toplevel(parent, bg="#E8C8CD")
        t3.title("Reporte")
        t3.geometry('800x400')
        t3.configure(bg="#E8C8CD")
        t3.focus()
        t3.grab_set()

        select=IntVar()#la guarda para los radiobuttons

        entra=StringVar()

        entra.set("")

        txtBusqueda=EntryEx(t3,textvariable=entra)

        txtBusqueda.focus_set()

        txtBusqueda.place(x=210,y=340)

        comboCampo=ttk.Combobox(t3)

        #botones

        btnHistor=Radiobutton(t3,text="Historial",
        value=0,variable=select,command=cambio,
        font=("Arial",13),width=10).place(x=15,y=295)

        btnProd=Radiobutton(t3,text="Productos",
        value=1,variable=select,command=cambio,
        font=("Arial",13),width=10).place(x=145,y=295)

        btnVent=Radiobutton(t3,text="Ventas",
        value=2,variable=select,command=cambio,
        font=("Arial",13),width=10).place(x=275,y=295)

        btnEgre=Radiobutton(t3,text="Egresos",
        value=4,variable=select,command=cambio,
        font=("Arial",13),width=10).place(x=405,y=295)

        btnFalt=Radiobutton(t3,text="Faltantes",
        value=3,variable=select,command=cambio,
        font=("Arial",13),width=10).place(x=535,y=295)

        t3.protocol("WM_DELETE_WINDOW",cambiar)#al precionar el boton "cerrar" llama a la funcion que cambia el
                                               #valor de la variable "abierta" a false.
        t3.bind("<Key>", presiona)

        conexion=sqlite3.connect("Super.sql")#abre la base de datos

        cursor=conexion.cursor()

        while abierta:

            for i in range(200):

                valor=select.get()#obtenemos el valor actual de los radiobuttons

                if not abierta:
                    #si la ventana se cierra, cerramos tambien la base de datos
                    cursor.close()
                    conexion.commit()
                    conexion.close()
                    t3.destroy()
                    break

                if valor==0:

                    titulo="Historial"

                    comando="SELECT * FROM Historial"

                    clientes_headers = ("ID",   "Fecha", "Hora",
                                        "Evento", "Descripcion")

                    if cambi==True:

                        clientes_tab.destroy()

                elif valor==1:

                    titulo="Productos"

                    comando="SELECT * FROM Productos"

                    clientes_headers = ("ID", "Marca", "Variedad",
                                        "Tipo", "Codigo", "Precio", "Cantidad")

                    if cambi==True:
                        clientes_tab.destroy()

                elif valor==2:

                    titulo="Ventas"

                    comando="SELECT * FROM Ventas"

                    clientes_headers = ("Fecha", "Mes",
                    "Producto", "Monto")

                    if cambi==True:
                        clientes_tab.destroy()

                elif valor==3:

                    titulo="Faltantes"

                    comando="SELECT * FROM Faltante"

                    clientes_headers = ("Codigo", "Marca","Variedad",
                    "Tipo", "Cantidad")

                    if cambi==True:
                        clientes_tab.destroy()

                elif valor==4:

                    titulo="Egresos"

                    comando="SELECT * FROM Egresos"

                    clientes_headers = ("Fecha", "Mes","Distribuidor",
                    "Monto", "Boleta")

                    if cambi==True:
                        clientes_tab.destroy()

                if busca==True:

                    cambi=True

                    combo=comboCampo.get()
                    busqueda=entra.get()
                    indice=0

                    for i in range(len(clientes_headers)):

                        if combo==clientes_headers[i]:
                            indice=i

                    comando="SELECT * FROM "+titulo

                    cursor.execute(comando)

                    filas = cursor.fetchall()

                    for fila in filas:

                        cosa=str(fila[indice]).lower()
                        cosa2=busqueda.lower()
                        bus=cosa.find(cosa2)

                        if bus>=0:

                            lista.append(fila)

                    clientes_tab.destroy()

                if cambi==True or primera==True:

                    #al hacer click en un radiobuton el valor de "cambi" pasara
                    #a ser True, lo que provocara la creacion de la tabla
                            #combobox
                    comboCampo["values"]=clientes_headers

                    if primera==True:
                        comboCampo.current(0)

                    comboCampo.place(x=15,y=340)

                    clientes_tab = Table(t3, title=titulo, headers=clientes_headers)
                    cambi=False
                    primera=False

                    if busca==False:

                        cursor.execute(comando)

                        for row in cursor:

                            clientes_tab.add_row(row)

                            clientes_tab.pack()

                    elif busca==True:

                        busca=False
                        print(len(lista))
                        if len(lista)>0:

                            for row in lista:

                                clientes_tab.add_row(row)

                                clientes_tab.pack()

                        elif len(lista)==0:

                            cursor.execute(comando)

                            for row in cursor:

                                clientes_tab.add_row(row)

                                clientes_tab.pack()

                            messagebox.showinfo(title="Error",
                            message="No se encontraron coincidencias")

                            t3.focus()



                        lista=[]

                t3.update()#actualizamos la ventana

def insertar(comando,lista):

    conexion=sqlite3.connect("Super.sql")
    consulta=conexion.cursor()
    consulta.execute(comando%lista)

    consulta.close()
    conexion.commit()
    conexion.close()


def editar(texto,ide,columna,NomColumna):

    conexion=sqlite3.connect("Super.sql")
    consulta=conexion.cursor()

    consulta.execute(texto,(columna,ide))

    consulta.close()
    conexion.commit()
    conexion.close()

    descripcion="Columna: "+NomColumna+" / ID Producto: " + str(ide)
    #este sera el texto que se agregara en el historial

    historial("Modificacion de datos",descripcion)

    control_stock()

def elegir_archivo():
    global directorio
    directorio=askopenfilename()

def boleta():
    global abierta
    global directorio

    global mes

    fecha=str(time.strftime("%d/%m/%Y"))

    if abierta==False:

        abierta=True;

        #creamos una ventana
        boletaV=Toplevel()

        boletaV.title("Compra nuevo producto")

        boletaV.geometry("220x400")

        boletaV.focus()

        boletaV.grab_set()

        #boton

        btnAceptar=Button(boletaV,text="Aceptar",
        command=cambiar,
        font=("Arial",13),width=10).place(x=50,y=355)

        btnElegir=Button(boletaV,text="Buscar\nboleta",
        command=elegir_archivo,
        font=("Arial",13),width=10).place(x=50,y=235)

        #etiquetas
        lblCodigo = Label(boletaV,text="Distribuidor",
        background="white").place(x=55,y=15)

        lblCantidad = Label(boletaV,text="Monto",
        background="white").place(x=75,y=80)

        lblBoleta= Label(boletaV,text="Boleta",
        background="white").place(x=75,y=145)

        distribuidor=StringVar()

        monto=StringVar()

        direc=StringVar()

        StrDistribuidor=EntryEx(boletaV,textvariable=distribuidor)

        StrMonto=EntryEx(boletaV,textvariable=monto)
        StrMonto.place(x=45,y=115)

        StrBoleta=EntryEx(boletaV,textvariable=direc).place(x=45,y=180)

        StrDistribuidor.focus_set()

        StrDistribuidor.place(x=45,y=45)

        boletaV.protocol("WM_DELETE_WINDOW",cambiar)

        comando="""INSERT INTO Egresos (Fecha,Mes,Distribuidor,Monto,
        Boleta) VALUES ("%s","%s","%s","%s","%s")"""

        while abierta:

            for i in range(200):

                if len(directorio)>0:

                    direc.set(directorio)
                    boletaV.focus()

                if not abierta:

                    lista=(fecha,mes,distribuidor.get(),monto.get(),directorio)

                    if len(distribuidor.get())>0 and len(monto.get())>0:

                        insertar(comando,lista)
                        Evento="Registro de Egreso"
                        Descripcion="Compra en "+distribuidor.get()+" por $ "+monto.get()+"0"
                        historial(Evento,Descripcion)

                    boletaV.destroy()

                    break

                boletaV.update()

        #compra()

def compra():

    global abierta
    global compre
    global busca
    global codi
    global vuelta
    global cambi
    vuelta=False
    cosa=False
    Cantiactual=0
    nombre="Producto: "
    precio="Precio: $ "
    cantidad="Cantidad: "
    pre=""
    co=""

    if abierta==False:

        abierta=True;

        #creamos una ventana
        compra_vent=Toplevel()

        compra_vent.title("Registrar Egreso")

        compra_vent.geometry("220x400")

        compra_vent.focus_set ()

        compra_vent.grab_set()

        #creamos un frame
        FrmInfo= Frame (compra_vent,width=210,height=90,bg="white")

        FrmInfo2= Frame (compra_vent,width=210,height=90,bg="white")

        #etiquetas
        lblCodigo = Label(compra_vent,text="Codigo de barras",
        background="white").place(x=55,y=15)

        lblCantidad = Label(compra_vent,text="Cantidad adquirida",
        background="white").place(x=55,y=80)

        lblPrecio = Label(compra_vent,text="Precio actual",
        background="white").place(x=65,y=145)

        lblNombre = Label(FrmInfo,text=nombre,
        fg="blue",background="white")

        lblPrecio = Label(FrmInfo,text=precio,
        fg="blue",background="white")

        lblCantidad = Label(FrmInfo,text=cantidad,
        fg="blue",background="white")

        #cuadros de texto

        Codigo=StringVar()

        Cantidad=StringVar()

        PrecioS=StringVar()

        StrCodigo=EntryEx(compra_vent,textvariable=Codigo)

        StrCodigo.focus_set()

        StrCodigo.place(x=45,y=45)

        StrCantidad=EntryEx(compra_vent,textvariable=Cantidad)

        StrCantidad.place(x=45,y=115)

        StrPrecio=EntryEx(compra_vent,textvariable=PrecioS).place(x=45,y=180)

        #Botones
        btnFin=Button(compra_vent,text="Finalizar",
        command=cambiar,
        font=("Arial",13),width=10).place(x=7,y=225)

        btnAceptar=Button(compra_vent,text="Aceptar",
        command=cambio,
        font=("Arial",13),width=10).place(x=115,y=225)

        compra_vent.protocol("WM_DELETE_WINDOW",cambiar)

        compra_vent.bind("<Key>", presiona)#se activa al presionar "ENTER"
        #cambia el valor de la variable "busca" a True

        while abierta:

            for i in range(200):

                if not abierta:
                    cambi=False
                    compra_vent.destroy()
                    break


                if cambi==True:
                        #Al presionar el boton "aceptar", entrara aqui.
                        #Aca se registra lo echo en el historial y se actualiza
                        #la informacion modificada

                        if len(Codigo.get())==0 or len(Cantidad.get())==0:
                            cambi=False

                        else:

                            descripcion="ingreso " + nom

                            historial("Compra",descripcion)

                            FrmInfo.destroy()
                            texto="UPDATE Productos SET Cantidad=? WHERE Id=?"
                            texto2="UPDATE Productos SET Precio=? WHERE Id=?"
                            ide=busqueda[6]
                            prec=PrecioS.get()
                            codi=Codigo.get()
                            columna=int(Cantidad.get())+Cantiactual

                            editar(texto,ide,columna,"Cantidad")
                            print("Precios ",PrecioS.get())
                            print("Pre ",pre)

                            if prec==pre:

                                print("entro")

                            else:
                                print("Entra")
                                editar(texto2,ide,prec,"Precio")

                            cambi=False
                            Codigo.set("")
                            Cantidad.set("")
                            PrecioS.set("")
                            nombre="Producto: "
                            precio="Precio: $ "
                            cantidad="Cantidad: "
                            busca=False
                            vuelta=False
                            StrCodigo.focus_set()

                            FrmInfo= Frame (compra_vent,width=210,height=90,bg="white")

                            lblNombre = Label(FrmInfo,text=nombre,
                            fg="blue",background="white")

                            lblPrecio = Label(FrmInfo,text=precio,
                            fg="blue",background="white")

                            lblCantidad = Label(FrmInfo,text=cantidad,
                            fg="blue",background="white")


                if busca == True and vuelta==False:

                    StrCantidad.focus_set()

                    if cosa==True:
                        FrmInfo.destroy()
                        cosa=False
                        FrmInfo= Frame (compra_vent,width=210,height=90,bg="white")

                    if len(Codigo.get())==0:
                        busca=False

                    elif len(Codigo.get())>1:

                        busqueda=buscarproducto(Codigo.get())

                        nom=busqueda[3]+" "+busqueda[1]+" "+busqueda[2]

                        nombre+=nom

                        precio+=str(busqueda[0])

                        PrecioS.set(busqueda[0])

                        pre=str(busqueda[0])
                        co=str(busqueda[4])
                        cantidad+=str(busqueda[5])


                        lblNombre = Label(FrmInfo,text=nombre,
                        fg="blue",background="white")

                        lblPrecio = Label(FrmInfo,text=precio,
                        fg="blue",background="white")

                        lblCantidad = Label(FrmInfo,text=cantidad,
                        fg="blue",background="white")

                        if not busqueda==False:

                            Cantiactual=(busqueda[5])

                            print("cantidad actual", Cantiactual)

                            busca=False
                            vuelta=True

                        elif busqueda==False:
                            codi=Codigo.get()
                            Codigo.set("")
                            Cantidad.set("")
                            PrecioS.set("")
                            busca=False

                            messagebox.showinfo(title="Error",message="El codigo del producto no existe")

                            MsgBox = messagebox.askquestion ('¿Que desea hacer?','¿Desea registrar el codigo como un nuevo producto?',icon = 'warning')

                            if MsgBox == 'yes':

                               compre=True
                               abierta=False
                               busca=False
                               cambi=False
                               compra_vent.destroy()
                               nuevo()
                               break

                            else:

                                compra_vent.focus_set ()

                elif busca==True and vuelta==True:

                    c=Codigo.get()

                    if not co==codi:
                        vuelta=False
                        cosa=True
                        nombre="Producto: "
                        precio="Precio: $ "
                        cantidad="Cantidad: "

                    if len(c)>1 and len(Cantidad.get())>1:
                        cambio()

                lblNombre.place(x=5,y=5)
                lblPrecio.place(x=5,y=25)
                lblCantidad.place(x=5,y=45)
                FrmInfo.place(x=5,y=305)

                compra_vent.update()
        boleta()

def cancelar():

    lstMaterias.delete(0,END)

    lstPrecios.delete(0,END)

    mostrarTotal()

def actualizar_producto(Producto):

    codigo=Producto[0]
    prod=buscarproducto(codigo)
    ide=prod[6]
    marca=Producto[1]
    variedad=Producto[2]
    tipo=Producto[3]
    precio=Producto[4]
    cantidad=Producto[5]
    conexion=sqlite3.connect("Super.sql")
    consulta=conexion.cursor()

    consulta.execute("""UPDATE Productos SET Marca=? WHERE Id=?""",(marca,ide))
    consulta.execute("""UPDATE Productos SET Variedad=? WHERE Id=?""",(variedad,ide))
    consulta.execute("""UPDATE Productos SET Tipo=? WHERE Id=?""",(tipo,ide))
    consulta.execute("""UPDATE Productos SET Precio=? WHERE Id=?""",(precio,ide))
    consulta.execute("""UPDATE Productos SET Cantidad=? WHERE Id=?""",(cantidad,ide))

    consulta.close()
    conexion.commit()
    conexion.close()

    control_stock()

def limpiar_fromulario(lista):

    for elem in lista:

        elem.set("")

def Guardar_nuevo(lista):
    global renglon
    check=False

    for i in range(len(lista)-1):

        if len(lista[i])>0:

            check=True

        else:

            check=False
            return

    if check==True:
        conexion=sqlite3.connect("Super.sql")

        consulta=conexion.cursor()

        sql = "SELECT * FROM Productos"

        #lista=[Codigo,Marca,Variedad,Tipo,Precio,Cantidad]

        consulta.execute(sql)

        filas = consulta.fetchall()

        for elem in filas:
            ide=elem[0]

        consulta.execute("""INSERT INTO Productos (Id,Marca,Variedad,Tipo,Codigo,
        Precio, Cantidad)VALUES ("%s","%s","%s","%s","%s","%s","%s")"""%(ide+1,lista[1],
        lista[2],lista[3],lista[0],lista[4],lista[5]))

        consulta.close()
        conexion.commit()
        conexion.close()

        descripcion=lista[1]+" "+lista[2]+" "+lista[3]

        historial("Ingreso Nuevo Producto",descripcion)


def nuevo():
    global abierta
    global cambi
    global busca
    existe=False
    global abierta
    global vuelta
    global compre
    global codi
    vuelta=False

    if abierta==False:

        abierta=True;

        introducir=Toplevel()

        introducir.focus()

        introducir.title("Introducir nuevo producto")

        introducir.geometry("400x250")

        introducir.grab_set()

        lblCodigo = Label(introducir,text="Codigo de barras",
        background="white").place(x=85,y=15)

        lblMarca = Label(introducir,text="Marca",
        background="white").place(x=10,y=75)

        lblVariedad = Label(introducir,text="Variedad",
        background="white").place(x=160,y=75)

        lblTipo = Label(introducir,text="Tipo",
        background="white").place(x=10,y=130)

        lblPrecio = Label(introducir,text="Precio",
        background="white").place(x=160,y=130)

        lblCantidad = Label(introducir,text="Cantidad",
        background="white").place(x=10,y=185)

        Codigo=StringVar()

        Marca=StringVar()

        Variedad=StringVar()

        Tipo=StringVar()

        Precio=StringVar()

        Cantidad=StringVar()

        lista=[Codigo,Marca,Variedad,Tipo,Precio,Cantidad]

        limpiar_fromulario(lista)

        StrCodigo=EntryEx(introducir,textvariable=Codigo)

        StrCodigo.focus_set()

        StrCodigo.place(x=75,y=45)

        StrMarca=EntryEx(introducir,textvariable=Marca).place(x=10,y=105)

        StrVariedad=EntryEx(introducir,textvariable=Variedad).place(x=150,y=105)

        StrTipo=EntryEx(introducir,textvariable=Tipo).place(x=10,y=155)

        StrPrecio=EntryEx(introducir,textvariable=Precio).place(x=150,y=155)

        StrCantidad=EntryEx(introducir,textvariable=Cantidad).place(x=10,y=205)

        introducir.bind("<Key>", presiona)

        introducir.protocol("WM_DELETE_WINDOW",cambio)

        btnAceptar=Button(introducir,text="Aceptar",
        command=cambio,
        font=("Arial",13),width=10).place(x=175,y=205)

        while abierta:

            for i in range(200):

                if not abierta:
                    introducir.destroy()
                    break

                if compre==True:

                    Codigo.set(codi)
                    compre=False
                    codi=""

                else:
                    codi=""

                if cambi==True and existe==False:

                    precio=str(Precio.get())

                    Producto=[Codigo.get(),Marca.get(),Variedad.get(),Tipo.get(),Precio.get(),Cantidad.get()]

                    limpiar_fromulario(lista)

                    Guardar_nuevo(Producto)

                    cambi=False
                    abierta=False


                elif cambi==True and existe==True:

                    Producto=[Codigo.get(),Marca.get(),Variedad.get(),Tipo.get(),Precio.get(),Cantidad.get()]

                    actualizar_producto(Producto)

                    historial("Modificacion de datos",str(Producto))

                    limpiar_fromulario(lista)

                    cambi=False
                    existe=False
                    abierta=False

                if busca==True and vuelta==False:

                    busqueda=buscarproducto(Codigo.get())

                    if not busqueda==False:

                        existe=True

                        Precio.set(busqueda[0])
                        Marca.set(busqueda[1])
                        Variedad.set(busqueda[2])
                        Tipo.set(busqueda[3])
                        Cantidad.set(busqueda[5])

                        Producto=[Codigo.get(),Marca.get(),Variedad.get(),Tipo.get(),Precio.get(),Cantidad.get()]

                        busca=False
                        vuelta=True

                    busca=False

                elif busca==True and vuelta==True:

                    c=Codigo.get()

                    if len(c)>1:
                        vuelta=False
                        cambio()

                introducir.update()

def notificaciones():

    global renglon_noti

    vuelta=0

    FrmNotifi2= Frame (ventana,width=195,height=300,bg="white").place(x=370,y=5)
    FrmNotifi= Frame (ventana,width=170,height=300,bg="white")

    notificacion = Label(FrmNotifi,text="Notificaciones",font=("", 15),
    fg="blue",background="white").grid(row=renglon_noti, column=0)

    conexion=sqlite3.connect("Super.sql")

    consulta=conexion.cursor()

    sql = "SELECT * FROM Faltante"

    if (consulta.execute(sql)):

        filas = consulta.fetchall()

        for fila in filas:

            if vuelta<=4:
                renglon_noti+=1

                Mensaje="Quedan "+str(fila[4])+" unidades de\n"+fila[3]+" "+fila[1]+"\n"+fila[2]

                etiqueta = Label(FrmNotifi,text=Mensaje,
                fg="red",background="white").grid(row=renglon_noti, column=0)

                vuelta+=1

    FrmNotifi.place(x=400,y=5)

def control_stock():

    global renglon_noti

    conexion=sqlite3.connect("Super.sql")

    consulta=conexion.cursor()

    sql = "SELECT * FROM Productos"
    consulta.execute("SELECT * FROM Faltante")
    codigosfaltante= consulta.fetchall()
    lista=[]

    for elem in codigosfaltante:
          lista.append(elem[0])

    if (consulta.execute(sql)):

        filas = consulta.fetchall()

        for fila in filas:

            if fila[6]<=10:

                consulta.execute("SELECT * FROM Faltante")

                filos = consulta.fetchall()

                if len(filos) == 0 or fila[4] not in lista:

                    consulta.execute("""INSERT INTO Faltante (Codigo,
                    Marca,Variedad,Tipo,
                    CantidadF)VALUES ("%s","%s","%s","%s","%s")"""%(fila[4],
                    fila[1],fila[2],fila[3],fila[6]))

                else:
                       renglon_noti=0

            if fila[4] in lista and fila[6]>10:
                codigo=fila[4]
                texto="DELETE FROM Faltante where Codigo = "+str(fila[4])

                consulta.execute(texto)
                renglon_noti=0

        consulta.close()
        conexion.commit()
        conexion.close()
        notificaciones()


def introducirproducto():
    global abierta
    global donde
    global codi
    global cambi

    seleccion=["Fiambreria","Carniceria","Verduleria"]

    if abierta==False:

        abierta=True;

        introducirw=Toplevel()

        introducirw.title("Introducir producto")

        introducirw.geometry("270x150")

        introducirw.focus()

        introducirw.grab_set()

        selec=IntVar()

        #rdBAnimo2=Radiobutton(introducirw,text="Almacen",value=0,
        #variable=selec).place(x=180,y=10)

        rdBAnimo=Radiobutton(introducirw,text="Fiambreria",value=0,
        variable=selec).place(x=180,y=20)

        rdBAnimoE=Radiobutton(introducirw,text="Carniceria",value=1,
        variable=selec).place(x=180,y=40)

        rdBAnimoEj=Radiobutton(introducirw,text="Verduleria",value=2,
        variable=selec).place(x=180,y=60)

        #entrada=StringVar()

        #entrada.set("")
        #entry.pack()

        if cambi==True:
            entrada.set(codi)

        txtProducto=EntryEx(introducirw,textvariable=entrada)

        txtProducto.focus_set()

        txtProducto.place(x=50,y=40)


        btnSig=Button(introducirw,text="Siguiente",
        command=agregarticket,
        font=("Arial",13),width=10).place(x=10,y=95)

        btnFinalizar=Button(introducirw,text="Aceptar",
        command=cambiar,
        font=("Arial",13),width=10).place(x=130,y=95)

        introducirw.protocol("WM_DELETE_WINDOW",cambiar)

        introducirw.bind("<Key>", fnKeyPress)

        while abierta:
          for i in range(200):
            if not abierta:
                introducirw.destroy()
                break
            if cambi==True:
                cambi=False
                codi=""
                agregarticket()

            s=selec.get()
            donde=seleccion[s]

            introducirw.update()


def agregarbotones():

    global agregar

    btnBorrar=Button(ventana,text="Borrar",
    command=borrardeLista,
    font=("Arial",13),width=10).place(x=210,y=35)

    btnFinalizar=Button(ventana,text="Finalizar",
    command=finalizar,
    font=("Arial",13),width=10).place(x=210,y=119)

    btnCancelar=Button(ventana,text="Cancelar",
    command=cancelar,
    font=("Arial",13),width=10).place(x=210,y=159)

def manual():

    global renglon
    global donde

    lstPrecios.insert(renglon,str(entrada.get()))
    lstMaterias.insert(renglon,donde)

    entrada.set("")

    renglon+=1

    mostrarTotal()


def finalizar():

    global indicelista
    global vueltov
    global Total
    indicelista=lstPrecios.size()
    monto=subtotal()

    if indicelista>0:

        answer = simpledialog(ventana,"Vuelto","¿Con cuanto paga?")
        if answer is not None:
            vuelto=float(answer)-monto

        vueltov=True;
        Frmvuelto=Toplevel()
        Frmvuelto.geometry("200x130")
        Frmvuelto.title("Vuelto")
        Frmvuelto.focus_force()

        etiqueta = Label(Frmvuelto,text="Su vuelto es de: ",
        font=("", 15),fg="blue",
        background="white").place(x=20,y=20)

        etiqueta2 = Label(Frmvuelto,text="$ "+str(vuelto)+"0    ",
        font=("", 15),fg="blue",
        background="white").place(x=40,y=50)

        btnAcepta=Button(Frmvuelto,text="Aceptar",
        command=cambia2,
        font=("Arial",10),width=10).place(x=50,y=80)

        Frmvuelto.bind("<Key>", press)

        Frmvuelto.protocol("WM_DELETE_WINDOW",cambia2)

        while vueltov:
          for i in range(200):

            if not vueltov:

                indicelista=lstMaterias.size()

                for i in range (indicelista):

                    listaTicket = lstMaterias.get(i)

                    listaMonto = lstPrecios.get(i)

                    historial("Venta",listaTicket)

                    guardar_venta(listaMonto,listaTicket)

                actualizardeposito()

                lstMaterias.delete(0,END)

                lstPrecios.delete(0,END)

                mostrarTotal()

                Frmvuelto.destroy()

                break

            Frmvuelto.update()




def historial(Evento,Descripcion):

    global hora

    fecha=str(time.strftime("%d/%m/%Y"))

    conexion=sqlite3.connect("Super.sql")

    consulta=conexion.cursor()

    consulta.execute("INSERT INTO Historial (Fecha,Hora,Evento,Descripcion)VALUES (?,?,?,?)",
    (fecha,hora,Evento,Descripcion))

    consulta.close()
    conexion.commit()
    conexion.close()


def guardar_venta(monto,nombre):

    global mes

    lista=[]

    conexion=sqlite3.connect("Super.sql")

    consulta=conexion.cursor()

    fecha=str(time.strftime("%d/%m/%Y"))


    consulta.execute("INSERT INTO Ventas (Fecha,Mes,Producto,Monto)VALUES (?,?,?,?)",(fecha,mes,nombre,monto))

    consulta.close()
    conexion.commit()
    conexion.close()



def buscarproducto(codigo):

    conexion=sqlite3.connect("Super.sql")

    consulta=conexion.cursor()

    sql = "SELECT * FROM Productos"

    if (consulta.execute(sql)):
        filas = consulta.fetchall()
        for fila in filas:
            if fila[4]==codigo:

                consulta.close()
                conexion.commit()
                conexion.close()

                return [fila[5],fila[1],fila[2],fila[3],fila[4],fila[6],fila[0]]

        consulta.close()
        conexion.commit()
        conexion.close()

        return False

def agregarticket():

    global renglon
    global listacodigo
    global listaNombres
    global donde
    global codi

    agregarbotones()
    codigo=entrada.get()

    if len(str(codigo))>10:
        floatentrada=buscarproducto(codigo)

        nombre=floatentrada[3]+" "+floatentrada[1]+" "+floatentrada[2]

        lstPrecios.insert(renglon,floatentrada[0])
        lstMaterias.insert(renglon,nombre)
        listacodigo.append(floatentrada[4])
        listaNombres.append(nombre)
        entrada.set("")
        codi=""
        renglon+=1

        mostrarTotal()

    elif len(str(codigo))>=1 and len(str(codigo))<10:
        manual()

def mostrarTotal():

    Total=subtotal()

    etiTotal = Label(text="Sub Total: $ " + str(Total)+"0     ",
    font=("", 15),fg="blue",background="white").place(x=0,y=250)

def actualizardeposito():
    global listacodigo
    global listaNombres

    for elem in listacodigo:

        producto=buscarproducto(elem)
        ide=producto[6]
        codigo=producto[4]
        cantidad=int(producto[5])-1
        conexion=sqlite3.connect("Super.sql")
        consulta=conexion.cursor()

        consulta.execute("""UPDATE Productos SET Cantidad=? WHERE Id=?""",(cantidad,ide))
        if cantidad<=10:
            consulta.execute("""UPDATE Faltante SET CantidadF=? WHERE Codigo=?""",(cantidad,codigo))
        consulta.close()
        conexion.commit()
        conexion.close()
    listacodigo=[]
    listaNombres=[]
    control_stock()

def subtotal():

    lista=[]

    subtot=0.0

    indicelista=lstPrecios.size()

    for i in range (indicelista):

        listaTicket = float(lstPrecios.get(i))

        lista.append(listaTicket)

    for elem in lista:

        subtot+=elem

    return subtot


def borrardeLista():

    if len(lstPrecios.curselection())>=0:

        itemSeleccionado=lstPrecios.curselection()

    if len(lstMaterias.curselection())>=0:

        itemSeleccionado=lstMaterias.curselection()

    indiceElementos=len(itemSeleccionado)

    while (indiceElementos>0):

        lstMaterias.delete(itemSeleccionado[0])

        lstPrecios.delete(itemSeleccionado[0])

        itemSeleccionado=lstPrecios.curselection()

        itemSeleccionado=lstMaterias.curselection()

        indiceElementos=len(itemSeleccionado)

    mostrarTotal()

def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)


ventana=tkinter.Tk()

ventana.geometry("600x400")

ventana.title("Registradora 0.03")

time1 = ''

#Frames

FrmTicket= Frame (ventana,width=600,height=400)

FrmMenu= Frame (ventana,width=400,height=100,bg="white")

#Scrollbar

scrollbar=Scrollbar(FrmTicket)

scrollbar.pack(side=RIGHT, fill=Y)

#Etiquetas y entradas

clock = Label(ventana, font=('Arial', 15),fg="blue",bg='white')
clock.place(x=430,y=360)

fecha = Label(ventana,text=FECHA, font=('Arial', 15),fg="blue", bg='white')
fecha.place(x=325,y=320)

etiqueta = Label(text="Ticket",font=("", 20),
fg="blue",background="white").place(x=50,y=5)


entrada=StringVar()

entrada.set("")

#Botones

btnIntroducir=Button(ventana,text="Iniciar",
command=introducirproducto,
font=("Arial",13),width=10).place(x=210,y=75)

btnNuevo=Button(FrmMenu,text="Nuevo",
command=nuevo,
font=("Arial",13),width=10,bg="green").grid(row=0, column=0)

btnCompra=Button(FrmMenu,text="Compra",
command=compra,
font=("Arial",13),width=10,bg="red").grid(row=0, column=1)

btnBase=Button(FrmMenu,text="Tablas",
command=ventana_reporte,
font=("Arial",13),width=10).grid(row=1, column=0)

btnLibro=Button(FrmMenu,text="Libros",
command=libro,
font=("Arial",13),width=10).grid(row=1, column=1)


#Listas

lstMaterias=Listbox(FrmTicket,
width=22,
selectmode = MULTIPLE,
yscrollcommand=scrollbar.set)

lstPrecios=Listbox(FrmTicket,
width=5,
selectmode = MULTIPLE,
yscrollcommand=scrollbar.set)

lstMaterias.pack(side=LEFT,fill=BOTH)

lstPrecios.pack(side=LEFT,fill=BOTH)

scrollbar.config(command=lstPrecios.yview)

#Pack de Frames

FrmTicket.place(x=10,y=50)

FrmMenu.place(x=3,y=300)

#Detecta tecla

ventana.bind("<Key>", fnKeyPress)

#imprime y actualiza la etiqueta Total

mostrarTotal()

#abrir sqlite3

conexion=sqlite3.connect("Super.sql")

#Actualiza el stock

control_stock()

tick()

#entry = EntryEx(ventana)
#entry.pack()

ventana.mainloop()
