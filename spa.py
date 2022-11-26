from tkinter import *
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk
from tkinter import messagebox
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
        op = messagebox.showinfo("Login","Returned to Login Window")
        if op > 0:
            root.destroy()
        else:
            return




if __name__ == "__main__":
    root = Tk()
    obj = Smart_Parking_System(root)
    root.mainloop()

