################################ MODULE IMPORTS ################################################################
from tkinter import *
from tkinter import messagebox

################################ GATEWAY TO ACCESS SQLTE/MYSQL #################################################

def gateway():
    def D1(event):
        User.delete(0,END)
    def D2(event):
        Password.delete(0,END)
    global root
    root=Tk()
    x=int(root.winfo_screenwidth()/2)
    y=int(root.winfo_screenheight()/2)
    root.title("Gateway")
    try:
        root.iconbitmap("ICON.ico")
    except:
        pass
    root.geometry("+"+str(x-175)+"+"+str(y-75))
    root.geometry("350x150")
    F=Frame(root,bg="red")
    LB=Label(F,text="",bg="red").grid(row=0,column=0)
    L_1=Label(F,text="User : ",font="Rockwell 15 bold",width="10",relief="solid").grid(row=1,column=0)
    User=Entry(F,font="Rockwell 12 bold italic",bd="3")
    User.grid(row=1,column=1)
    L_2=Label(F,text="Password : ",font="Rockwell 15 bold",width="10",relief="solid").grid(row=2,column=0)
    Password=Entry(F,font="Rockwell 12 bold italic",bd="3")
    LB=Label(F,text="",bg="red").grid(row=4,column=0)
    Password.grid(row=2,column=1)
    User.insert(0,"root")
    Password.insert(0,"admin")
    User.bind("<Button-1>",D1)
    Password.bind("<Button-1>",D2)
    def Enter():
        try:
            import mysql.connector
            con=mysql.connector.connect(host="localhost",user=User.get(),password=Password.get())
            
            global user,password
            user=User.get()
            password=Password.get()
            for widget in root.winfo_children():
                widget.destroy()
            Mainpage()
        except:
            User.config(bg="pink")
            Password.config(bg="pink")
            messagebox.showinfo("Note!","Mismatching User and password for Sql Database\nEnsure Mysql Connector is Installed")
            

            
    B_ENTER=Button(root,text="Access",font="Rockwell 15 bold",command=Enter)
    B_ENTER.grid(row=3,column=0,columnspan=2)
    F.grid(row=0,column=0,sticky="W")
    
        
gateway()

########################### DOWNLOAD/ADD MYSQL TABLE TO ARRAY  #################################################

def download():
    Database=E1.get()
    Table=E2.get()
    if Database!="" and Table!="":
        import mysql.connector
        con=mysql.connector.connect(host="localhost",user=user,password=password)
        con.autocommit=True
        cur=con.cursor()
        try:
            query="use "+str(Database)
            cur.execute(query)
            query="select * from "+str(Table) #[[ , ],[ , ]]
            cur.execute(query)
            A=cur.fetchall()
            query="desc "+str(Table)
            cur.execute(query)   
            F=cur.fetchall()     
            global Array
            Array={}
            Array[1]={}
            Array[0]={}
            column=1
            for i in F:                                  # ('B', 'int(11)', 'null', 'KEY', None, ' ')
                
                Array[1]["C_1_"+str(column)]=i[0]        # ('B', 'int(11)', 'YES ', '   ', None, ' ')
                constraints=""
                
                if i[2]=="NO":
                    constraints=constraints+" not null"
                    
                if i[3]=="PRI":
                    constraints=constraints+" Primary Key"  
                Array[0]["C_0_"+str(column)]=i[1]+" "+constraints
                column+=1
            
            row=2
            for i in A:
                column=1
                d={}
                for j in i:
                    d["C_"+str(row)+"_"+str(column)]=j
                    column+=1
                Array[row]=d
                row+=1
            Present()    
        except:
            message=messagebox.showinfo("Note!","The Database or Table doesn't exist")
            
    
########################## PRESENT TABLE FROM ARRAY ############################################################


                
def Present(Exceptional_Value=None):
    global Array
    try:
        if type(Exceptional_Value)is list:
            Array=Exceptional_Value
    except:
        pass
        
    global F1
    try:
        F1.destroy()
    except:
        pass
    F1=Frame(root)
    F1.grid(row=1,column=0,columnspan=2)
    global row,column
    row=1
    for i in Array:
        if i!=0:
            column=1
            for j in Array[i]:
                if row==1:
                    exec("global "+str(j)+"\n"+str(j)+"=Entry(F1,font='Rockwell 14 bold',fg='black',bg='Dodger blue',width="+str(Wid)+")\n"+str(j)+".grid(row="+str(row)+",column="+str(column)+")")
                    if Array[i][j]!="":
                        exec(str(j)+".insert("+"END,'"+str(Array[i][j])+"')")
                if row!=1:
                    exec("global "+str(j)+"\n"+str(j)+"=Entry(F1,font='Rockwell 14 bold',fg='black',bg='white',width="+str(Wid)+")\n"+str(j)+".grid(row="+str(row)+",column="+str(column)+")")

                    if Array[i][j]!="":
                        exec(str(j)+".insert("+"END,'"+str(Array[i][j])+"')")
                column+=1
                    
            row+=1

    column=1
    try:
        for j in Array[0]:
            exec("global "+str(j)+"\n"+str(j)+"=Entry(F1,font='Rockwell 14 bold',fg='white',bg='grey',width="+str(Wid)+")\n"+str(j)+".grid(row="+str(row)+",column="+str(column)+")")
            if Array[0][j]!="":
                exec(str(j)+".insert("+"END,'"+str(Array[0][j])+"')")
                        
            column+=1
    except:
        pass

############################### TO SAVE DATA, ADJUST AND CHANGE ROWS/COLUMNS ###################################

def SAVE_DATA():
    row=0
    for i in Array:
        column=0
        for j in Array[i]:
            halfcode=j+".get()"
            try:
                Array[i][j]=eval(halfcode)
            except:
                pass
            column+=1
        row+=1
    
def add_row():
    SAVE_DATA()
    global Array
    for i in Array:
        if i!=0:
            ROW_END=i
            for j in Array[i]:
                COL_END=j
    COL_END=COL_END.split("_")[-1]
    ROW_END+=1
    d={}
    i=1
    while i<=int(COL_END):
        d["C_"+str(ROW_END)+"_"+str(i)]=""
        i+=1
    Array[ROW_END]=d
    Present()

def add_column():
    SAVE_DATA()
    global Array
    for i in Array:
        if i!=0:
            ROW_END=i
            for j in Array[i]:
                COL_END=j
    COL_END=int(COL_END.split("_")[-1])+1
    for i in Array:
        Array[i]["C_"+str(i)+"_"+str(COL_END)]=""
    Present()
    
def remove_row():
    SAVE_DATA()
    global Array
    if len(Array)>2:
        for i in Array:
            if i!=0:
                ROW_END=i

        Array.pop(ROW_END)
        Present()
        
def remove_column():
    SAVE_DATA()
    global Array
    if len(Array[1])>1:

        for i in Array:
            if i!=0:
                for j in Array[i]:
                    COL_END=j
        COL_END=int(COL_END.split("_")[-1])

        for i in Array:
            Array[i].pop("C_"+str(i)+"_"+str(COL_END))

        Present()
        
                

######################## HIDDEN CLICKS AND BIND ACTIONS ########################################################

def SHOW(event=None):
    Database=E1.get()
    
    import mysql.connector
    con=mysql.connector.connect(host="localhost",user="root",password="admin")
    cur=con.cursor()
    d={}
    if Database=="":
        query="show databases"
        d["C_1_1"]="Database"
        
    else:
        try:
            query="use "+str(Database)
            cur.execute(query)
            query="show tables"
            d["C_1_1"]="Tables"
        except:
            query="show databases"
            d["C_1_1"]="Database"
            
        
    cur.execute(query)
    L=cur.fetchall()
    global Array
    Array={}
    Array[1]=d
    row_count=2
    count=2
    for i in L:
        column_count=1
        d={}
        for j in i:
            d["C_"+str(row_count)+"_"+str(column_count)]=j
            column_count+=1
        row_count+=1
        Array[count]=d
        count+=1
    Present()

################################### ESTABLISHING THE MAIN WINDOW ###############################################
            
def Mainpage():
    global Pseudo_Array
    Pseudo_Array={}
    def Clear():
        global Array
        E1.delete(0,END)
        E2.delete(0,END)
        Array={1:{"C_1_1":"","C_1_2":"","C_1_3":"","C_1_4":""},2:{"C_2_1":"","C_2_2":"","C_2_3":"","C_2_4":""},3:{"C_3_1":"","C_3_2":"","C_3_3":"","C_3_4":""},4:{"C_4_1":"","C_4_2":"","C_4_3":"","C_4_4":""},5:{"C_5_1":"","C_5_2":"","C_5_3":"","C_5_4":""},0:{"C_0_1":"","C_0_2":"","C_0_3":"","C_0_4":""}}
        
        Present()
    global Wid
    Wid=10
    def WID(VAL_w):
        for i in Array:
            for j in Array[i]:
                try:
                    exec(str(j)+".config(width="+str(VAL_w)+")")
                    global Wid
                    Wid=VAL_w
                except:
                    pass
            
    global root,Array,F1,F,E1,E2,B1,F2
    root.title("SQLTE")
    HEIGHT=root.winfo_screenheight()
    WIDTH=root.winfo_screenwidth()
    root.geometry(str(WIDTH)+"x"+str(HEIGHT))
    root.geometry("+0+0")
    try:
        root.iconbitmap("ICON.ico")
    except:
        pass
    Array={1:{"C_1_1":"","C_1_2":"","C_1_3":"","C_1_4":""},2:{"C_2_1":"","C_2_2":"","C_2_3":"","C_2_4":""},3:{"C_3_1":"","C_3_2":"","C_3_3":"","C_3_4":""},4:{"C_4_1":"","C_4_2":"","C_4_3":"","C_4_4":""},5:{"C_5_1":"","C_5_2":"","C_5_3":"","C_5_4":""},0:{"C_0_1":"","C_0_2":"","C_0_3":"","C_0_4":""}}
    F1=Frame(root)    
    F=Frame(root,bg="orange")
    LB=Label(F,text="",bg="orange").grid(row=0,column=0)
    L_1=Label(F,text="Database : ",font="Rockwell 15 bold",width="10",relief="solid").grid(row=1,column=0)
    E1=Entry(F,font="Rockwell 12 bold italic",bd="3")
    E1.grid(row=1,column=1)
    L_2=Label(F,text="Table   : ",font="Rockwell 15 bold",width="10",relief="solid").grid(row=2,column=0)
    E2=Entry(F,font="Rockwell 12 bold italic",bd="3")
    LB=Label(F,text="",bg="orange").grid(row=3,column=0)
    E2.grid(row=2,column=1)
    L=Label(F,text="",bg="orange").grid(row=4,column=0)
    F.grid(row=0,column=0,sticky="W")
    B1=Button(F,text=" Download ",bg="lime",width="18",fg="white",font="Rockwell 13 bold",bd="3",relief="raised",command=download)
    B1.grid(row=3,column=1)
    L=Label(F,text=" ",bg="orange").grid(row=1,column=3)
    L=Label(F,text="Cell Width: ",font="Rockwell 13 bold",relief="sunken",width="12",bg="black",fg="white").grid(row=1,column=4)
    B_width=Scale(F,from_=10,to=40,command=WID,orient="horizontal",bg="red",fg="white",width="20")
    B_width.grid(row=2,column=4)
    Clear=Button(F,text="Clear ✗",bg="purple",fg="white",relief="raised",bd="5",font="Rockwell 13 bold",width="12",command=Clear)
    Clear.grid(row=2,column=5,sticky="S")
    Present()
    F.bind("<Triple-Button-1>",SHOW)
    L=Label(root,text="").grid(row=row+1,column=0)
    F1.grid(row=1,column=0)
    
    global F2
    try:
        F2.destroy()
    except:
        pass

    L=Label(F,text="   ",bg="orange").grid(row=2,column=6)
    
    F2=Frame(F,bg="seashell2",bd="5",relief="solid")
    L1=Label(F2,text="")
    L1.grid(row=0,column=0)
    L2=Label(F2,text="")
    L2.grid(row=3,column=0)
    B=Button(F2,text="Convert",bg="red",width="25",fg="white",font="Rockwell 13 bold",bd="3",relief="raised",command=upload)
    B.grid(row=2,column=0,columnspan=4)
    B_Row=Button(F2,text="Add Row",width="15",font="Rockwell 13 bold",bg="Dodger blue",fg="white",command=add_row)
    B_Row.grid(row=4,column=1)
    B_Column=Button(F2,text="Add Column",width="15",font="Rockwell 13 bold",bg="orange",fg="white",command=add_column)
    B_Column.grid(row=4,column=2)
    B_Row_r=Button(F2,text="Remove Row",width="15",font="Rockwell 13 bold",bg="orange",fg="white",command=remove_row)
    B_Row_r.grid(row=5,column=1)
    B_Column_r=Button(F2,text="Remove Column",width="15",font="Rockwell 13 bold",bg="Dodger blue",fg="white",command=remove_column)
    B_Column_r.grid(row=5,column=2)
    F2.grid(row=1,column=7,rowspan=3)
    Present()
    
################################### UPLOAD AND CONVERT #########################################################

def upload():
    global Array
    row=0
    for i in Array:
        column=0
        for j in Array[i]:
            halfcode=j+".get()"
            Array[i][j]=eval(halfcode)
            column+=1
        row+=1
    
    Fill_table()

def Fill_table():
    try:
        Database=E1.get()
        Table="test"
        
        import mysql.connector
        con=mysql.connector.connect(host="localhost",user="root",password="admin")
        con.autocommit=True
        cur=con.cursor()
        query="create database if not exists "+Database
        cur.execute(query)
        query="use "+Database
        cur.execute(query)
        query="drop table if exists "+Table
        cur.execute(query)
        part=""
        count=0
        for i in Array[1]:
            count+=1
            LINE=Array[1]["C_1_"+i[-1]]+" "+Array[0]["C_0_"+i[-1]]
            part=part+LINE+","
            
        part=part[0:len(part)-1]

        
        whole="create table "+Table+"("+part+")"
        query=whole
        
        cur.execute(query)
        STRING="%s,"*count
        STRING=STRING[0:len(STRING)-1]    
        for i in Array:
            if i!=1 and i!=0:
                T=()
                for j in Array[i]:
       
                    T=T+(str(Array[i][j]),)    
                query="insert into "+Table+" values("+STRING+")"
                cur.execute(query,(T))

        

        Database=E1.get()
        Table=E2.get()
        query="create database if not exists "+Database
        cur.execute(query)
        query="use "+Database
        cur.execute(query)
        
        query="drop table if exists "+Table
        cur.execute(query)
        
        part=""
        count=0
        for i in Array[1]:
            count+=1
            LINE=Array[1]["C_1_"+i[-1]]+" "+Array[0]["C_0_"+i[-1]]
            part=part+LINE+","
            
        part=part[0:len(part)-1]

        
        whole="create table "+Table+"("+part+")"
        query=whole
        
        cur.execute(query)
        STRING="%s,"*count
        STRING=STRING[0:len(STRING)-1]    
        for i in Array:
            if i!=1 and i!=0:
                T=()
                for j in Array[i]:
                    T=T+(str(Array[i][j]),)    
                query="insert into "+Table+" values("+STRING+")"
                cur.execute(query,(T))
        message=messagebox.showinfo("Note!","Successfully uploaded the Database and Table into MySql :) ")
        query="drop table if exists test"
        cur.execute(query)
        
    except:
        message=messagebox.showinfo("Note!","Errors in Your Input")
root.mainloop()
################################################################################################################
