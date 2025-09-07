import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class lib():
    def __init__(self,root):
        self.root=root
        self.root.title("library management")
        
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text=" Library Management System ", bd=4, relief="groove", bg="sky blue", font=("Arial",50,"bold"))
        title.pack(side="top",fill="x")

        # OPTION  FRAME

        optFrame=tk.Frame(self.root,bd=5,relief="ridge",bg=self.clr(130,230,230))
        optFrame.place(width=self.width/3,height=self.height - 180, x=70, y=100)

        addBtn=tk.Button(optFrame,command=self.regFrame, text="Register_Student", bd=2, relief="raised", width=20, font=("Arial",20,"bold"))
        addBtn.grid(row=0, column=0, padx=30, pady=40)

        allocateBtn=tk.Button(optFrame,command=self.assignFrame, text="Allocate_Book", bd=2, relief="raised",width=20, font=("Arial",20,"bold"))
        allocateBtn.grid(row=1,column=0, padx=30,pady=40)

        returnBtn=tk.Button(optFrame,command=self.retFrame, text="Return_Book", bd=2, relief="raised", width=20, font=("Arial",20,"bold"))
        returnBtn.grid(row=2, column=0, padx=30, pady=40)

        recordBtn=tk.Button(optFrame,command=self.showFun, text="Show_Record", bd=2, relief="raised", width=20, font=("Arial",20,"bold"))
        recordBtn.grid(row=3,column=0, padx=30, pady=40)
        # DETAIL FRAME
        
        self.detFrame=tk.Frame(self.root,bd=5, relief="ridge",bg=self.clr(100,240,200))
        self.detFrame.place(width=self.width/2, height=self.height- 180, x=self.width/3+140, y=100)

        lb = tk.Label(self.detFrame, text="Library Deatils", bd=3, relief="raised", font=("Arial", 20, "bold"))
        lb.pack(side="top",fill="x")
        self.tabFun()
    
    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="cyan")
        tabFrame.place(width=self.width/2 - 40, height = self.height- 270, x=17, y=70)

        x_scroll = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        y_scroll= tk.Scrollbar(tabFrame,orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.table=ttk.Treeview(tabFrame,columns=("rollNo","name","quant","age"),xscrollcommand=x_scroll.set,yscrollcommand=y_scroll.set)
        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)
        
        self.table.heading("rollNo", text="Roll_No")
        self.table.heading("name", text="Student_Name")
        self.table.heading("quant", text="Quantity")
        self.table.heading("age", text="Student_Age")
        self.table["show"]="headings"
        self.table.pack(fill="both",expand=True)

    def regFrame(self):
        self.rFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(10,150,250))
        self.rFrame.place(width=self.width/3, height=self.height - 400, x=self.width/3+100, y=120)

        rollLbl=tk.Label(self.rFrame,text="Roll_No:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        rollLbl.grid(row=0, column=0, padx=20, pady=20)
        self.rollNo =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        self.rollNo.grid(row=0, column=1, padx=10, pady=20)

        namelbl=tk.Label(self.rFrame,text="Name:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        namelbl.grid(row=1, column=0, padx=20, pady=20)
        self.name =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        self.name.grid(row=1, column=1, padx=10, pady=20)

        bookLbl=tk.Label(self.rFrame,text="Book_Name:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        bookLbl.grid(row=2, column=0, padx=20, pady=20)
        self.book =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        self.book.grid(row=2, column=1, padx=10, pady=20)
       
        okBtn= tk.Button(self.rFrame,command=self.regFun, text=" Enter ", width=20, bd= 4, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=3, column=0, padx=70, pady=30, columnspan=2)

    def desReg(self):
        self.rFrame.destroy()

    def regFun(self):
        roll = self.rollNo.get()
        name = self.name.get()
        books= self.book.get()

        if roll and name and books:
            try:
                self.dbFun()
                self.cur.execute("insert into library (rollno,name,quantity) values(%s,%s,%s)",(roll,name,0))
                self.con.commit()
                tk.messagebox.showinfo("Success",f'Student {name} with RollNo: {roll} is registered Successfully.')
                self.desReg()

                self.cur.execute("select * from library where rollNo=%s",roll)
                row=self.cur.fetchone()

                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END,values=row)

                self.con.close()

            except Exception as e:
                tk.messagebox.showerror("Error",str(e))
                self.desReg()


        else:
            tk.messagebox.showerror(" Error ", "Please fill all the details !")
    
    def dbFun(self):
        self.con = pymysql.connect(host="localhost",user="root",password="WJ28@krhps", database="library")
        self.cur = self.con.cursor() 

    def assignFrame(self):
        self.rFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(10,150,250))
        self.rFrame.place(width=self.width/3, height=self.height - 400, x=self.width/3+100, y=120)

        rollLbl=tk.Label(self.rFrame,text="Roll_No:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        rollLbl.grid(row=0, column=0, padx=20, pady=20)
        self.rollNo =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        self.rollNo.grid(row=0, column=1, padx=10, pady=20)

        # namelbl=tk.Label(self.rFrame,text="Name:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        # namelbl.grid(row=1, column=0, padx=20, pady=20)
        # self.name =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        # self.name.grid(row=1, column=1, padx=10, pady=20)

        bookLbl=tk.Label(self.rFrame,text="Book_Name:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        bookLbl.grid(row=2, column=0, padx=20, pady=20)
        self.book =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        self.book.grid(row=2, column=1, padx=10, pady=20)
       
        okBtn= tk.Button(self.rFrame,command=self.assignFun, text=" Enter ", width=20, bd= 4, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=3, column=0, padx=30, pady=30, columnspan=2)


    def desAssign(self):
        self.rFrame.destroy()


    def assignFun(self):
        roll = self.rollNo.get()
        # name = self.name.get()
        books= self.book.get()

        if roll and books:
            try:
                self.dbFun()
                self.cur.execute("select quantity from library where rollno=%s",roll)
                row=self.cur.fetchone()
                if row:
                    upd= row[0]+1
                    self.cur.execute("update library set quantity=%s where rollno=%s",(upd,roll))
                    self.con.commit()
                    tk.messagebox.showinfo("Success", f'Book.{books} is assigned to student with rollNo: {roll}')
                    self.desAssign()

                    self.cur.execute("select * from library where rollno=%s",roll)
                    data = self.cur.fetchone()                   
                    self.tabFun()
                    self.table.delete(*self.table.get_children())
                    self.table.insert('',tk.END, values=data)

                    self.con.close()
                
                else:
                    tk.message.box.showerror("Error :","Invalid RollNo !!!")
            except Exception as e:
                tk.messagebox.showerror("Error",str(e))
                self.desAssign()


        else:
            tk.messagebox.showerror(" Error ", "Please fill all the details !")

    def retFrame(self):
        self.rFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(10,150,250))
        self.rFrame.place(width=self.width/3, height=self.height - 400, x=self.width/3+100, y=120)

        rollLbl=tk.Label(self.rFrame,text="Roll_No:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        rollLbl.grid(row=0, column=0, padx=20, pady=20)
        self.rollNo =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        self.rollNo.grid(row=0, column=1, padx=10, pady=20)

        # namelbl=tk.Label(self.rFrame,text="Name:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        # namelbl.grid(row=1, column=0, padx=20, pady=20)
        # self.name =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        # self.name.grid(row=1, column=1, padx=10, pady=20)

        bookLbl=tk.Label(self.rFrame,text="Book_Name:", bg=self.clr(10,150,250), font=("Arial", 15, "bold"))
        bookLbl.grid(row=2, column=0, padx=20, pady=20)
        self.book =tk.Entry(self.rFrame, bd=2, width=18, font=("Arial", 15))
        self.book.grid(row=2, column=1, padx=10, pady=20)
       
        okBtn= tk.Button(self.rFrame,command=self.retFun, text=" Enter ", width=20, bd= 4, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=3, column=0, padx=30, pady=30, columnspan=2)

    def retFun(self):
        roll = self.rollNo.get()
        # name = self.name.get()
        books= self.book.get()

        if roll and books:
            try:
                self.dbFun()
                self.cur.execute("select quantity from library where rollno=%s",roll)
                row = self.cur.fetchone()
                if row:
                    upd = row[0] - 1
                    self.cur.execute("update library set quantity=%s where rollno=%s",(upd,roll))
                    self.con.commit()
                    tk.messagebox.showinfo("Success ", f"Book {books} is returned from student with rollNo: {roll} ")
                    self.desAssign()

                    self.cur.execute("select * from library where rollno=%s",roll)
                    data = self.cur.fetchone()

                    self.tabFun()
                    self.table.delete(*self.table.get_children())
                    self.table.insert('',tk.END, values=data)

                    self.con.close()
                
                else:
                    tk.messagebox.showerror("Error: ","Invalid RollNo !")

            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desAssign()
        else:
            tk.messagebox.showerror(" Error ", "Please fill all the details !")
    
    def showFun(self):
        try:
            self.dbFun()
            self.cur.execute("select * from library where quantity > 0")
            rows = self.cur.fetchall()

            self.tabFun()
            self.table.delete(*self.table.get_children())
            for i in rows:
                self.table.insert('',tk.END,values=i)

            self.con.close()



        except Exception as e:
            tk.messagebox.showerror("Error: ",f"Error: {e}")


    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"   

root= tk.Tk()
obj = lib(root)
root.mainloop()
        
