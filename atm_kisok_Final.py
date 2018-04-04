import tkinter as tk
import time
from tkinter import font  as tkfont
import pymysql
from tkinter import messagebox
account=0
withd = 0
                    

class ATM(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("ATM KIOSK")
        
        container = tk.Frame(self)
        container.pack(side="top", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFourD, PageFourW, PageFourF, PageWithdrawed, SetPin,PageDeposited,PageBalance):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):

        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        global account
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        localtime=time.asctime(time.localtime(time.time()))

        label2=tk.Label(self,text=localtime,width=20,height=1,fg="blue",font=('robotic',20,'bold'))
        label2.pack(side="top", pady=20)

        self.label1=tk.Label(self,text="Enter Account Number",width=20,height=2,fg="black",bg="powder blue",font=('robotic',30,'bold'))
        self.label1.pack(side="top", pady=20)

        self.entry1 = tk.Entry(self,relief="sunken",bd=3,validate="key",insertwidth=4)
        def acc_validation():
            global account
            acc=int(self.entry1.get())
            
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root')
            cursor=self.conn.cursor()
            cursor.execute("SELECT name FROM user_details WHERE account_no='%d'"%(acc))
            row=cursor.fetchall()
            if(row!=()):
                cursor.execute("SELECT name FROM user_details WHERE account_no='%d'"%(acc))
                out=cursor.fetchone()
                account = acc
                self.entry1.delete(0,'end')
                controller.show_frame("PageOne")
            else:
                tk.messagebox.showinfo("Validation", "Account Not Found")
                self.entry1.delete(0,"end")

        button1 = tk.Button(self, text="Submit", command=lambda:acc_validation())
        
        self.entry1.pack(side = "top", pady="10")
        button1.pack(side = "top", pady="20")

    

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        global account
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        label1=tk.Label(self,text="Enter Pin",width=20,height=2,fg="black",bg="powder blue",font=('robotic',30,'bold'))
        label1.pack(side="top", pady=20)

        self.entry1 = tk.Entry(self,relief="sunken",show="*",bd=3,validate="key")
    
        def pin_validation():
            global account
            pin=int(self.entry1.get())
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
            cursor=self.conn.cursor()
            cursor.execute("SELECT pin FROM user_details WHERE account_no= '%d' and pin='%d' "%(account,pin))
            row=cursor.fetchall()
            if(row!=()):
                cursor.execute("SELECT pin FROM user_details WHERE account_no= '%d' and pin='%d' "%(account,pin))
                out=cursor.fetchone()
                self.entry1.delete(0,'end')
                controller.show_frame("PageTwo")
                
            else:
                tk.messagebox.showinfo("Validation", "Invalid Pin")
                self.entry1.delete(0,"end")
        button2 = tk.Button(self, text="Submit",
                            command=lambda:pin_validation())

        self.entry1.pack(side = "top", pady="10")
        button2.pack(side = "top", pady="20")
       

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        label1 = tk.Label(self, text="Choose An Option", width=20, height=2, fg="black", bg="powder blue",
                          font=('robotic', 30, 'bold'))
        label1.pack(side="top", pady="10")

        def savings():
            
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
            cursor=self.conn.cursor()
            cursor.execute("update account_details set account_type='%s' where acc_no='%d'"%('S',account))
            self.conn.commit()
            controller.show_frame("PageThree")
            

        def current():
            
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
            cursor=self.conn.cursor()
            cursor.execute("update account_details set account_type='%s' where acc_no='%d'"%('C',account))
            self.conn.commit()
            controller.show_frame("PageThree")
            
        button1 = tk.Button(self, text="Savings",command=lambda: savings(), height="3",width="20")

        button2 = tk.Button(self, text="Current",
                            command=lambda: current(),height ="3",width = "20")

        
        button3= tk.Button(self, text="Change Pin",
                            command=lambda: controller.show_frame("SetPin"),height ="3",width = "20")
        
        button1.pack(side = "bottom", pady=(20,20))
        button2.pack(side = "bottom", pady=(20,20))
        button3.pack(side = "bottom", pady=(20,20))


class PageThree(tk.Frame):

    def __init__(self, parent, controller):

        
        
        tk.Frame.__init__(self, parent,bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        
        label1=tk.Label(self,text="Please Select Option",width=20,height=2,fg="black",bg="powder blue",font=('robotic',30,'bold'))
        label1.pack(side="top", pady=20)
        
        def PageBalance():
            global account

            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
            cursor=self.conn.cursor()
            cursor.execute("Select balance from account_details where acc_no='%d'"%(account))
            self.conn.commit()
            out = cursor.fetchone()

            tk.messagebox.showinfo("Balance","Your balance is  Rs "+str(out[0]))
            controller.show_frame("PageThree")
            
            s = out[0]
            lambda: controller.show_frame("PageBalance(out[0])")

        def newFrame():
            global account
            
            tk.Frame.__init__(self, parent)
            self.controller = controller
            label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
            label.pack(side="top", pady=(30,10))

            label1 = tk.Label(self, text="Your Balance is ", width=20, height=4, fg="black", bg="powder blue",
                              font=('robotic', 30, 'bold'))
            label1.pack(side="top", pady=10)
            
            label2 = tk.Label(self, text="Hello", width=20, height=4, fg="black", bg="powder blue",
                              font=('robotic', 30, 'bold'))
            label2.pack(side="top", pady=10)
            
            button1 = tk.Button(self, text="Continue",
                                command=lambda: controller.show_frame("PageThree"), height="5",width="50")

            button2 = tk.Button(self, text="Cancel",
                                command=lambda: controller.show_frame("StartPage"),height ="5",width = "50")
            button1.pack(side = "right",  pady="50")
            button2.pack(side = "left", padx=(500,20),pady="80")


        button1 = tk.Button(self, text="Deposit", 
                            command=lambda: controller.show_frame("PageFourD"), height="3", width="30")

        button2 = tk.Button(self, text="Cash Withdrawal", 
                             command=lambda: controller.show_frame("PageFourW"), height="3", width="30")

        button3 = tk.Button(self, text="Fast Cash",
                            command=lambda: controller.show_frame("PageFourF"), height="3", width="30")

        button4 = tk.Button(self, text="Balance Enquiry",
                            command=lambda: PageBalance(), height="3",width="30")

        """button5 = tk.Button(self, text="Mini Statement",
                            command=lambda: PageBalance(),height ="3",width = "30")"""

        button1.pack(side = "bottom",pady=(10,10))
        button2.pack(side = "bottom",pady=(10,10))
        button3.pack(side = "bottom",pady=(10,10))
        button4.pack(side = "bottom",pady=(10,10))
        """button5.pack(side = "bottom")"""
        
class PageFourD(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width
                         =20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        label1=tk.Label(self,text="Enter amount to be deposited",width=30,height=2,fg="black",bg="powder blue",font=('robotic',20,'bold'))
        label1.pack(side="top", pady=20)

        self.entry1 = tk.Entry(self,relief="sunken",bd=3,validate="key")
        def deposit():
            global account
            global withd
            deposit=int(self.entry1.get())
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root')
            cursor=self.conn.cursor()
            cursor.execute("insert into transaction(amount,account_no,status) values(%d,%d,'C')"%(deposit,account))
            cursor.execute("Update account_details set balance =balance+'%d' WHERE acc_no='%d'"%(deposit,account))
            self.conn.commit()
            out=cursor.fetchone()
            row=cursor.fetchall()
            if(row!=True):
                cursor.execute("Select balance from account_details where acc_no='%d'"%(account))
                out=cursor.fetchone()
                tk.messagebox.showinfo("Response", "Successfully Deposit Rs"+ str(deposit))
                controller.show_frame("PageDeposited")
                
            else:
                tk.messagebox.showinfo("Response", "Failed")
                self.entry1.delete(0,"end")
        
        
        button2 = tk.Button(self, text="Submit",
                            command=lambda:deposit())

        self.entry1.pack(side = "top", pady="10")
        button2.pack(side = "top", pady="20")

class PageFourW(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        label1=tk.Label(self,text="Enter amount for withdrawal",width=30,height=2,fg="black",bg="powder blue",font=('robotic',20,'bold'))
        label1.pack(side="top", pady=20)

        self.entry1 = tk.Entry(self,relief="sunken",bd=3,validate="key")
        def withdrawal():
            global account
            global withd
            withdraw=int(self.entry1.get())
            withd=withdraw
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
            cursor=self.conn.cursor()
            cursor.execute("Select account_type from account_details where acc_no='%d'"%(account))
            self.conn.commit()
            out = cursor.fetchone()
            if str(out[0])=='C':
                cursor.execute("select balance from account_details where acc_no='%d'"%(account))
                out = cursor.fetchone()
                if out[0]>=withdraw:
                    cursor.execute("insert into transaction(amount,account_no,status) values(%d,%d,'D')"%(withdraw,account))
                    cursor.execute("Update account_details set balance =balance-'%d' WHERE acc_no='%d'"%(withdraw,account))
                    self.conn.commit()
                    out=cursor.fetchone()
                    row=cursor.fetchall()
                    if(row!=True):
                        cursor.execute("Select balance from account_details where acc_no='%d'"%(account))
                        out=cursor.fetchone()
                        tk.messagebox.showinfo("Withdrawal", "Successfully Withdrew Rs" + str(withdraw))
                        controller.show_frame("PageWithdrawed")
                
            else:
                cursor.execute("select balance from account_details where acc_no='%d'"%(account))
                out = cursor.fetchone()
                if out[0]>=withdraw and withdraw<=25000-withd:
                    cursor.execute("insert into transaction(amount,account_no,status) values(%d,%d,'D')"%(withdraw,account))
                    cursor.execute("Update account_details set balance =balance-'%d' WHERE acc_no='%d'"%(withdraw,account))
                    self.conn.commit()
                    out=cursor.fetchone()
                    row=cursor.fetchall()
                    if(row!=True):
                        tk.messagebox.showinfo("Withdrawal", "Successfully Withdrew Rs" + str(withdraw))
                        controller.show_frame("PageWithdrawed")
                else:
                    tk.messagebox.showinfo("Withdrawal", "Amount exceeded the withdrawal limit")
                    controller.show_frame("PageThree")

                    
        
        
        button2 = tk.Button(self, text="Submit",
                            command=lambda:withdrawal())

        self.entry1.pack(side = "top", pady="10")
        button2.pack(side = "top", pady="20")

class PageFourF(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        
        label1=tk.Label(self,text="Select an option",width=30,height=2,fg="black",bg="powder blue",font=('robotic',20,'bold'))
        label1.pack(side="top", pady=20)

        def fastcash(amt):
            global account
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
            cursor=self.conn.cursor()
            cursor.execute("Select balance from account_details where acc_no='%d'"%(account))
            out=cursor.fetchone()
            if out[0]>=amt:
                cursor.execute("insert into transaction(amount,account_no,status) values(%d,%d,'D')"%(amt,account))
                cursor.execute("Update account_details set balance =balance-'%d' WHERE acc_no='%d'"%(amt,account))
                self.conn.commit()
                out=cursor.fetchone()
                row=cursor.fetchall()
                if(row!=True):
                    cursor.execute("Select balance from account_details where acc_no='%d'"%(account))
                    out=cursor.fetchone()
                    tk.messagebox.showinfo("Fast Cash", "Successfully Withdrew Rs" + str(amt))
                    controller.show_frame("PageWithdrawed")
                
            else:
                tk.messagebox.showinfo("Validation", "Amount is too low for this transaction. Please check your balance")
                controller.show_frame("PageThree")
            

        button1 = tk.Button(self, text="1000",
                            command=lambda: fastcash(1000), height="3", width="30")

        button2 = tk.Button(self, text="2000",
                            command=lambda: fastcash(2000), height="3", width="30")

        button3 = tk.Button(self, text="3000",
                            command=lambda: fastcash(3000), height="3", width="30")

        button4 = tk.Button(self, text="5000",
                            command=lambda: fastcash(5000), height="3",width="30")

        button1.pack(side = "bottom",  pady=(10,10))
        button2.pack(side = "bottom",  pady=(10,10))
        button3.pack(side = "bottom",  pady=(10,10))
        button4.pack(side = "bottom",  pady=(10,10))



"""class PageFourM(tk.Frame):

    def __init__(self, parent, controller):
        global account
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller

        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        label1 = tk.Label(self, text="Mini-Statement", width=20, height=4, fg="black", bg="powder blue",font=('robotic', 30, 'bold'))
        label1.pack(side="top", pady=10)
        
        def showallrecords():
            global accountno 
            data = readfromdatabase()
            table = tk.table.Table(self,state= "disabled",titlerows=1,rows=self.rows,cols=5)
            for index, dat in enumerate(data):
                tk.Label(self, text=dat[0]).grid(row=index+1, column=0)
                tk.Label(self, text=dat[1]).grid(row=index+1, column=1)
                tk.Label(self, text=dat[2]).grid(row=index+1, column=2)

        def readfromdatabase():
            global account
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
            cursor=self.conn.cursor()
            self.rows=cursor.execute("Select count(transaction_id) from transaction where account_no='%d'"%(account))
            cursor.execute("SELECT * FROM transaction where account_no='%d'"%(account))
            return cursor.fetchall()
        button = tk.Button(self, text="Click here to continue",
                            command=lambda:showallrecords(), height="5",width="50")
        button.pack(side="left")

        button1 = tk.Button(self, text="Click here to continue",
                            command=lambda: controller.show_frame("PageThree"), height="5",width="50")
        button1.pack(side="bottom")
"""

class PageWithdrawed(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        label1 = tk.Label(self, text="Please collect your money", width=25, height=2, fg="black", bg="powder blue",
                          font=('robotic', 30, 'bold'))
        label1.pack(side="top", pady=10)

        label2 = tk.Label(self, text="ThankYou for Banking with us", width=30, height=2, fg="black", bg="powder blue",
                          font=('robotic', 30, 'bold'))
        label2.pack(side="top", pady=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame("StartPage"), height="5",width="50")

        
        button1.pack(side = "bottom",  pady=(10,10))


class PageDeposited(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller
        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        label1 = tk.Label(self, text="Amount has been Deposited", width=25, height=2, fg="black", bg="powder blue",font=('robotic', 30, 'bold'))
        label1.pack(side="top", pady=10)

        label2 = tk.Label(self, text="ThankYou for Banking with us", width=30, height=2, fg="black", bg="powder blue",font=('robotic', 30, 'bold'))
        label2.pack(side="top", pady=10)

        button1 = tk.Button(self, text="Home",command=lambda: controller.show_frame("StartPage"), height="5",width="50")
        
        button1.pack(side = "bottom",  pady=(10,10))

class SetPin(tk.Frame):

    def __init__(self, parent, controller):
        global account
        tk.Frame.__init__(self, parent, bg = "#4B0082")
        self.controller = controller


        label = tk.Label(self, text="ATM KIOSK",width=20,height=1,fg="white",bg="black",font=('Acme', 60, 'bold'),highlightcolor="orange")
        label.pack(side="top", pady=(30,10))

        self.label1=tk.Label(self,text="Enter new pin",width=20,height=2,fg="black",bg="powder blue",font=('robotic',30,'bold'))
        self.label1.pack(side="top", pady=20)

        self.entry1 = tk.Entry(self,relief="sunken",bd=3,validate="key",insertwidth=4, show="*")
        def pin_setting():
            global account
            pin=int(self.entry1.get())
            self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
            cursor=self.conn.cursor()
            cursor.execute("SELECT name FROM user_details WHERE account_no='%d'"%(account))
            row=cursor.fetchall()
            if(row!=()):
                cursor.execute("UPDATE user_details set pin='%d' WHERE  account_no='%d'"%(pin,account))
                out=cursor.fetchone()
                self.conn.commit()
                cursor.execute("SELECT pin FROM user_details WHERE account_no='%d'"%(account))
                out=cursor.fetchone()
                tk.messagebox.showinfo("Validation", "Pin changed Successfully")
                controller.show_frame("PageTwo")
            else:
                tk.messagebox.showinfo("Validation", "Some problem occured Please try again after some time")
                self.entry1.delete(0,"end")

        button1 = tk.Button(self, text="Submit", command=lambda:pin_setting())
        
        self.entry1.pack(side = "top", pady="10")
        button1.pack(side = "top", pady="20")



class PageBalance(tk.Frame):

    def __init__(self, parent, controller):
        global account
        tk.Frame.__init__(self, parent, bg ="#4B0082")
        self.controller = controller

        label1 = tk.Label(self, text="Your Balance is", width=20, height=4, fg="black", bg="powder blue",font=('robotic', 30, 'bold'))
        label1.pack(side="top", pady=10)
              
        self.conn=pymysql.connect(host='localhost',database='atm',user='root',password='root',autocommit=True)
        cursor=self.conn.cursor()
        cursor.execute("Select balance from account_details where acc_no='%d'"%(account))
        self.conn.commit()
        out = cursor.fetchone()

        label = tk.Label(self, text="Hello", width=20, height=4, fg="black", bg="powder blue",font=('robotic', 30, 'bold'))
        label.pack(side="top", pady=10)

        label2 = tk.Label(self, text="ThankYou for Banking with us", width=20, height=4, fg="black", bg="powder blue",font=('robotic', 30, 'bold'))
        label2.pack(side="top", pady=10)

        button1 = tk.Button(self, text="Continue",command=lambda: controller.show_frame("PageThree"), height="5",width="50")
        button2 = tk.Button(self, text="Cancel",command=lambda: controller.show_frame("StartPage"),height ="5",width = "50")

        button1.pack(side = "right",  pady="50")
        button2.pack(side = "left", padx=(500,20),pady="80")

if __name__ == "__main__":
    app = ATM()
    app.geometry("800x600+420+50")
    app.resizable(0,0)
    app.mainloop()
