from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import pickle
import cvzone
import numpy as np
import random
from datetime import datetime
from time import strftime
from receipt import Receipt
from database import Database
from help import Help


def main():
    win=Tk()
    app=Login(win)
    win.mainloop()


class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x800+0+0")
        self.root.title("Login")
        self.c_v1=IntVar(value=0)
        self.txtpass_str=StringVar()

        # variable
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar()
        self.var_securityA = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()

        img = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\bg.jpg")
        img = img.resize((1530, 800), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        lbl_bg=Label(self.root,image=self.photoimg)
        lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)

        frame=Frame(self.root,bg="white")
        frame.place(x=610,y=170,width=340,height=430)

        # imglogo
        img_logo = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\logo.jpg")
        img_logo = img_logo.resize((250, 180), Image.Resampling.LANCZOS)
        self.photoimg_logo = ImageTk.PhotoImage(img_logo)

        img_logo_lbl = Label(self.root, image=self.photoimg_logo, borderwidth=0)
        img_logo_lbl.place(x=0, y=0, width=250, height=180)

        # img2
        img2 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\login.png")
        img2 = img2.resize((100, 100), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        img2_lbl = Label(self.root, image=self.photoimg2,borderwidth=0)
        img2_lbl.place(x=730, y=175, width=100, height=100)

        get_str=Label(frame,text="Get Started", font =("times",20,"bold"), fg="black",bg="white")
        get_str.place(x=95,y=100)

        #username
        username=lbl=Label(frame,text="Username", font =("times",15,"bold"), fg="black",bg="white")
        username.place(x=70,y=155)

        self.txtuser=ttk.Entry(frame, font =("times",15,"bold"))
        self.txtuser.place(x=40,y=180, width=270)

        # password
        password=lbl = Label(frame, text="Password", font=("times", 15, "bold"), fg="black", bg="white")
        password.place(x=70, y=225)

        self.txtpass = ttk.Entry(frame, show="*",textvariable=self.txtpass_str,width=15,font =("times",15,"bold"))
        self.txtpass.place(x=40, y=250, width=270)

        #icon images
        img3 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\username.png")
        img3 = img3.resize((25, 25), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        img3_lbl = Label(self.root, image=self.photoimg3, borderwidth=0)
        img3_lbl.place(x=650, y=323, width=25, height=25)

        img4 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\password.png")
        img4 = img4.resize((25, 25), Image.Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        img4_lbl = Label(self.root, image=self.photoimg4, borderwidth=0)
        img4_lbl.place(x=650, y=395, width=25, height=25)


        #buttons
        loginbtn=Button(frame,text="Login",relief=RIDGE,command=self.login, font =("times",15,"bold"), fg="black",bg="blue",activeforeground="black",activebackground="red").place(x=110,y=300,width=120,height=35)
        chkbtn=ttk.Checkbutton(frame,text="Show Password",variable=self.c_v1, onvalue=1,offvalue=0,command=self.my_show).place(x=200,y=280,width=120,height=20)
        registerbtn = Button(frame, text="Register new user", relief=RIDGE, command=self.register_window, font=("times", 10, "bold"), fg="black",borderwidth=0,
                          bg="white", activeforeground="red", activebackground="white").place(x=20,y=350,width=160)
        forgetbtn = Button(frame, text="Forget Password", relief=RIDGE, command=self.forgot_pass_window, font=("times", 10, "bold"),fg="black",borderwidth=0,
                             bg="white", activeforeground="red", activebackground="white").place(x=17, y=370, width=160)
        exitbtn = Button(frame, text="Exit Application", relief=RIDGE, command=self.exit_app,
                           font=("times", 10, "bold"), fg="red", borderwidth=0,
                           bg="white", activeforeground="brown", activebackground="white").place(x=200, y=400, width=160)


    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)

    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error","All fields Required",parent=self.root)
        elif self.txtuser.get()=="admin" and self.txtpass.get()=="admin":
            messagebox.showinfo("Success","Welcome to SAP")
        else:
            conn = mysql.connector.connect(host='localhost', username='root', password='saurabh', database='spa')
            my_cursor = conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s",(
                                                                                    self.txtuser.get(),
                                                                                    self.txtpass.get()
                                                                            ))
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid username & Password")
            else:
                open_main=messagebox.askyesno("Yes/No","Access only admin")
                if open_main>0:
                    self.new_window=Toplevel(self.root)
                    self.app=Smart_Parking_System(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()


    def my_show(self):
        if(self.c_v1.get()==1):
            self.txtpass.config(show='')
        else:
            self.txtpass.config(show='*')

    def exit_app(self):
        self.root.destroy()


    #reset password
    def reset_pass(self):
        if self.securityQ_combo.get()=="Select":
            messagebox.showerror("Error","Select Security Question",parent=self.root2)
        elif self.txt_security.get()=="":
            messagebox.showerror("Error","Please enter the name",parent=self.root2)
        elif self.txt_new_password.get()=="":
            messagebox.showerror("Error","Please enter new password",parent=self.root2)
        else:
            conn = mysql.connector.connect(host='localhost', username='root', password='saurabh', database='spa')
            my_cursor = conn.cursor()
            query=("select * from register where email=%s and securityQ=%s and securityA=%s")
            value=(self.txtuser.get(),self.securityQ_combo.get(),self.txt_security.get())
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Answer is Incorrect",parent=self.root2)
            else:
                query=("update register set password=%s where email=%s")
                value=(self.txt_new_password.get(),self.txtuser.get())
                my_cursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Info","Your Password has been reset",parent=self.root2)
                self.root2.destroy()




    #forgot password
    def forgot_pass_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please Enter email address to Reset password")
        else:
            conn = mysql.connector.connect(host='localhost', username='root', password='saurabh', database  ='spa')
            my_cursor = conn.cursor()
            query=("select * from register where email=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()

            if row==None:
                messagebox.showerror("Error","Please enter valid username")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forget Password")
                self.root2.geometry("340x450+610+170")

                l=Label(self.root2,text="Forget Password", font=("times",14,"bold"),fg="red",bg="white")
                l.place(x=0,y=10,relwidth=1)

                self.securityQ = Label(self.root2, text="Select Security Questions", font=("times", 15, "bold"), fg="black")
                self.securityQ.place(x=50, y=80)

                self.securityQ_combo = ttk.Combobox(self.root2,font=('times new roman', 18, 'bold'), state="read only", width=22)
                self.securityQ_combo["values"] = ("Select", "Your Birth Place", "Favourite Food", "Your Pet name", "Favourite Person")
                self.securityQ_combo.current(0)
                self.securityQ_combo.place(x=50, y=110, width=250)

                securityA = Label(self.root2, text="Security Answer", font=("times", 15, "bold"), fg="black")
                securityA.place(x=50, y=150)

                self.txt_security = ttk.Entry(self.root2, width=15, font=("times", 15, "bold"))
                self.txt_security.place(x=50, y=180, width=250)

                new_password = Label(self.root2, text="New Password", font=("times", 15, "bold"), fg="black")
                new_password.place(x=50, y=220)

                self.txt_new_password = ttk.Entry(self.root2, width=15, font=("times", 15, "bold"))
                self.txt_new_password.place(x=50, y=250, width=250)

                btn=Button(self.root2,text="Reset",command=self.reset_pass,font=("times", 15, "bold"),fg="white",bg="green")
                btn.place(x=100,y=290)



class Register:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1600x900+0+0")
        self.root.title("Register")

        #variable
        self.var_fname=StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar()
        self.var_securityA = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()

        #bg image
        img_bg = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\regbg.jpg")
        img_bg = img_bg.resize((1600, 900), Image.Resampling.LANCZOS)
        self.photoimg_bg = ImageTk.PhotoImage(img_bg)


        lbl_bg = Label(self.root, image=self.photoimg_bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # left image
        img_left = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\left.jpg")
        img_left = img_left.resize((470, 550), Image.Resampling.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        lbl_bg = Label(self.root, image=self.photoimg_left)
        lbl_bg.place(x=50, y=100, width=470, height=550)

        #main frame
        frame = Frame(self.root, bg="white")
        frame.place(x=520, y=100, width=800, height=550)
        register_lbl = Label(frame, text="REGISTER HERE", font=("times", 20, "bold"), fg="darkgreen", bg="white")
        register_lbl.place(x=20, y=20)

        # label & entry
        #------------------row 1
        fname =Label(frame, text="First Name", font=("times", 15, "bold"), fg="black", bg="white")
        fname.place(x=50, y=100)

        self.fname = ttk.Entry(frame, width=15,textvariable=self.var_fname, font=("times", 15, "bold"))
        self.fname.place(x=50, y=130, width=250)

        lname =Label(frame, text="Last Name", font=("times", 15, "bold"), fg="black", bg="white")
        lname.place(x=370, y=100)

        self.lname = ttk.Entry(frame, width=15,textvariable=self.var_lname, font=("times", 15, "bold"))
        self.lname.place(x=370, y=130, width=250)

        #--------------------row2
        contact =Label(frame, text="Contact No.", font=("times", 15, "bold"), fg="black", bg="white")
        contact.place(x=50, y=170)

        self.contact = ttk.Entry(frame, width=15,textvariable=self.var_contact, font=("times", 15, "bold"))
        self.contact.place(x=50, y=200, width=250)

        email = Label(frame, text="Email", font=("times", 15, "bold"), fg="black", bg="white")
        email.place(x=370, y=170)

        self.email = ttk.Entry(frame, width=15, textvariable=self.var_email,font=("times", 15, "bold"))
        self.email.place(x=370, y=200, width=250)

        # --------------row3
        self.securityQ = Label(frame, text="Select Security Questions", font=("times", 15, "bold"), fg="black", bg="white")
        self.securityQ.place(x=50, y=240)

        self.securityQ_combo = ttk.Combobox(frame, textvariable=self.var_securityQ, font=('times new roman', 18, 'bold'), state="read only",
                                  width=22)
        self.securityQ_combo["values"] = ("Select", "Your Birth Place", "Favourite Food", "Your Pet name", "Favourite Person")
        self.securityQ_combo.current(0)
        self.securityQ_combo.place(x=50, y=270, width=250)

        securityA =Label(frame, text="Security Answer", font=("times", 15, "bold"), fg="black", bg="white")
        securityA.place(x=370, y=240)

        self.fname = ttk.Entry(frame,textvariable=self.var_securityA, width=15, font=("times", 15, "bold"))
        self.fname.place(x=370, y=270, width=250)

        #--------------row 4
        pswd = Label(frame, text="Password", font=("times", 15, "bold"), fg="black", bg="white")
        pswd.place(x=50, y=310)

        self.pswd = ttk.Entry(frame, width=15,textvariable=self.var_pass, font=("times", 15))
        self.pswd.place(x=50, y=340, width=250)

        confirm_pswd = lbl = Label(frame, text="Confirm Password", font=("times", 15, "bold"), fg="black", bg="white")
        confirm_pswd.place(x=370, y=310)

        self.confirm_pswd = ttk.Entry(frame, width=15,textvariable=self.var_confpass, font=("times", 15, "bold"))
        self.confirm_pswd.place(x=370, y=340, width=250)


        #buttons
        img = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\register.png")
        img = img.resize((200, 60), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        b1 = Button(frame, image=self.photoimg,command=self.register_data, cursor="hand2", borderwidth=0,font=("times", 15, "bold"),fg="black", bg="white")
        b1.place(x=50, y=420, width=200)

        img1 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\loginnow.jpg")
        img1 = img1.resize((200, 61), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        b2 = Button(frame, image=self.photoimg1,command=self.return_login, cursor="hand2", borderwidth=0, font=("times", 15, "bold"), fg="black", bg="white")
        b2.place(x=370, y=420, width=200)

        # fn declaration
    def register_data(self):
        if self.var_fname.get()=="" or self.var_email.get()=="" or self.var_securityQ.get()=="Select":
            messagebox.showerror("Error","All fields required",parent=self.root)
        elif self.var_pass.get()!=self.var_confpass.get():
            messagebox.showerror("Error","Password and Conform Password must be same",parent=self.root)
        else:
            conn = mysql.connector.connect(host='localhost', username='root', password='saurabh', database='spa')
            cur = conn.cursor()
            query=("select * from register where email=%s")
            value=(self.var_email.get(),)
            cur.execute(query,value)
            row=cur.fetchone()
            if row!=None:
                messagebox.showerror("Error","User email already exists",parent=self.root)
            else:
                cur.execute("insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                        self.var_fname.get(),
                        self.var_lname.get(),
                        self.var_contact.get(),
                        self.var_email.get(),
                        self.var_securityQ.get(),
                        self.var_securityA.get(),
                        self.var_pass.get()
                                 ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success","Registration Successfull",parent=self.root)


    def return_login(self):
        self.root.destroy()


class Smart_Parking_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1600x900+0+0")
        self.root.title("Smart Park Assist System")

        img = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\spabg.jpg")
        img = img.resize((1600, 900), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=600, width=1530, height=790)

        bg_img = Label(self.root, image=self.photoimg)
        bg_img.place(x=0, y=180, width=1530, height=790)

        title_lbl = Label(bg_img, text="Smart Park Assist",bg="gold",
                          font=("times new roman", 35, "bold"), fg="black")
        title_lbl.place(x=0, y=0, width=1530, height=55)

        #img1
        img1 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\parkimg1.jpg")
        img1 = img1.resize((550, 180), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=0, y=0, width=550, height=180)

        #img2
        img2 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\parkimg.jpg")
        img2 = img2.resize((550, 180), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=500, y=0, width=550, height=180)

        #img3
        img3 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\parkimg2.jpg")
        img3 = img3.resize((550, 180), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        f_lbl = Label(self.root, image=self.photoimg3)
        f_lbl.place(x=1000, y=0, width=550, height=180)

        #imglogo
        img_logo = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\logo.jpg")
        img_logo = img_logo.resize((250, 180), Image.Resampling.LANCZOS)
        self.photoimg_logo = ImageTk.PhotoImage(img_logo)

        img_logo_lbl = Label(self.root, image=self.photoimg_logo, borderwidth=0)
        img_logo_lbl.place(x=0, y=0, width=250,height=180)


        #time
        def time():
            string = strftime('%H:%M:%S %p')
            lbl.config(text=string)
            lbl.after(1000,time)

        lbl = Label(title_lbl, font=('times',15,'bold'),bg='gold',fg='blue')
        lbl.place(x=10,y=0,width=110,height=50)
        time()


        #button

        img4 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\cam.png")
        img4 = img4.resize((200, 200), Image.Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1 = Button(bg_img, command=self.parking, image=self.photoimg4, cursor="hand2")
        b1.place(x=250, y=100, width=220, height=220)

        b1_1 = Button(bg_img, command=self.parking, text="Enter Camera", cursor="hand2",
                      font=("times new roman", 15, "bold"), bg="Blue", fg="white")
        b1_1.place(x=250, y=300, width=220, height=40)

        img5 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\receipt.jpeg")
        img5 = img5.resize((280, 280), Image.Resampling.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)

        b2 = Button(bg_img, command=self.addVehicle, image=self.photoimg5, cursor="hand2")
        b2.place(x=650, y=100, width=220, height=220)

        b2_1 = Button(bg_img, command=self.addVehicle, text="Receipt", cursor="hand2",
                      font=("times new roman", 15, "bold"), bg="Blue", fg="white")
        b2_1.place(x=650, y=300, width=220, height=40)

        img7 = Image.open(r"C:\Users\saura\PycharmProjects\Smart-Vehicle-Parking-System-main\photodata\data_Storage.jpg")
        img7 = img7.resize((200, 200), Image.Resampling.LANCZOS)
        self.photoimg7 = ImageTk.PhotoImage(img7)

        b4 = Button(bg_img, command=self.addData, image=self.photoimg7, cursor="hand2")
        b4.place(x=1050, y=100, width=220, height=220)

        b4_1 = Button(bg_img, command=self.addData, text="Open Database", cursor="hand2",
                      font=("times new roman", 15, "bold"), bg="Blue", fg="white")
        b4_1.place(x=1050, y=300, width=220, height=40)


        b3_1 = Button(bg_img, command=self.iExit, text="Return to Login", cursor="hand2", font=("times new roman", 15, "bold"),
                      bg="red", fg="white")
        b3_1.place(x=1200, y=580, width=150, height=40)


        b5_1 = Button(bg_img,command=self.help, text="Help?", cursor="hand2", font=("times new roman", 15, "bold"),
                      bg="Red", fg="white")
        b5_1.place(x=150, y=580, width=150, height=40)




    def parking(self):
        cap = cv2.VideoCapture('carPark.mp4')

        with open('CarParkPos', 'rb') as f:
            posList = pickle.load(f)

        width, height = 107, 48

        def checkParkingSpace(imgPro):
            spaceCounter = 0

            for pos in posList:
                x, y = pos

                imgCrop = imgPro[y:y + height, x:x + width]
                # cv2.imshow(str(x * y), imgCrop)
                count = cv2.countNonZero(imgCrop)

                if count < 900:
                    color = (0, 255, 0)
                    thickness = 5
                    spaceCounter += 1
                else:
                    color = (0, 0, 255)
                    thickness = 2

                cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
                cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                                   thickness=2, offset=0, colorR=color)

            cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (0, 50), scale=3,
                               thickness=5, offset=20, colorR=(0, 0, 0))
            if spaceCounter > 0:
                cvzone.putTextRect(img, f'There are {spaceCounter} Free lines', (360, 60), scale=2,
                                   thickness=2, offset=8, colorT=(0, 0, 0))

        while True:

            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            success, img = cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                 cv2.THRESH_BINARY_INV, 25, 16)
            imgMedian = cv2.medianBlur(imgThreshold, 5)
            kernel = np.ones((3, 3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

            checkParkingSpace(imgDilate)
            cv2.imshow("Image", img)
            cv2.waitKey(10)
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break

    def addVehicle(self):
        self.new_window=Toplevel(self.root)
        self.app=Receipt(self.new_window)


    def addData(self):
        self.new_window=Toplevel(self.root)
        self.app=Database(self.new_window)

    def help(self):
        self.new_window=Toplevel(self.root)
        self.app=Help(self.new_window)



    def iExit(self):
        self.root.destroy()






if __name__ == "__main__":
    main()
