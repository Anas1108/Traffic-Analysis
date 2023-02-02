#References
# https://www.researchgate.net/publication/327554338_A_Video_based_Vehicle_Detection_Counting_and_Classification_System
# Research paper for guidance: https://www.researchgate.net/publication/261059609_Vehicle_detection_using_morphological_image_processing_technique


import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk


window = tk.Tk()
window.geometry("800x600")
window.title("Vehicle Detection")


#creating button
buttonFrame = tk.Frame(window, width=800, height=250,bg="gray")
buttonFrame.place(relx=0,rely=0)

#Creating Frame
imageFrame = tk.Frame(window, width=800, height=450,bg="white")
imageFrame.place(relx=0,rely=0.25)


#Capture video frames
lmain = tk.Label(imageFrame,text="video section",bg="white")
lmain.place(x=10,y=10)


# Reading the video
cap = cv2.VideoCapture("dataset1.mp4")
cap1 = cv2.VideoCapture("dataset2.mp4")

sub = cv2.bgsegm.createBackgroundSubtractorMOG()
sub1 = cv2.bgsegm.createBackgroundSubtractorMOG()

kernal_size_blur = (7, 7)
kernal_size_dilated = (13, 13)

# Initializing count for vehicles
t_vehicles1 = 0
ltv1 = 0
htv1 = 0

t_vehicles2= 0
ltv2 = 0
htv2 = 0



def show_frame():
    text = button1.cget('text')
    if text == "pause":
        ret, frame = cap.read()
        centers = []

        # #Reading image in grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # #Gaussian Blur
        blur = cv2.GaussianBlur(gray, kernal_size_blur, 5)
        subtracted_image = sub.apply(blur)

        # #Dilation
        dilated_image = cv2.dilate(subtracted_image, np.ones((5, 5)))

        # #Closing Morphological Operation
        morph_open = cv2.morphologyEx(dilated_image, cv2.MORPH_CLOSE, kernal_size_dilated)
        morph_open = cv2.morphologyEx(morph_open, cv2.MORPH_CLOSE, kernal_size_dilated)

        # #Contours
        contours, hierarcy = cv2.findContours(morph_open, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filtering contours of vehicles
        valid_contour = []
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            if w >= 80 and h >= 80:
                valid_contour.append(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        y_line = 550

        img = np.zeros_like(frame)
        cv2.drawContours(img, valid_contour, -1, (0, 255, 0), 3)

        cv2.line(frame, (140, y_line), (1050, y_line), (255, 0, 255), 2)

        # Loop for matching the coordinates of centre of vehicle and line
        global t_vehicles1
        global htv1
        global ltv1

        for c in valid_contour:
            (x, y, w, h) = cv2.boundingRect(c)
            x1 = int(w / 2)
            y1 = int(h / 2)
            c1 = x + x1
            c2 = y + y1
            center = (c1, c2)

            centers.append(center)
            cv2.circle(frame, center, 2, (0, 0, 255), -1)

            if c2 < (y_line + 7) and c2 > (y_line - 3):
                t_vehicles1 = t_vehicles1 + 1
                area = cv2.contourArea(c)
                print(area)
                if area > 500 and area < 15000:
                    ltv1 = ltv1 + 1
                elif area > 15000 and area < 125000:
                    htv1 = htv1 + 1

        # Showing vehicle count
        cv2.putText(frame, "Total Vehicles Count : " + str(t_vehicles1), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255),
                    3)
        cv2.putText(frame, "LTV : " + str(ltv1), (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.putText(frame, "HTV : " + str(htv1), (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image).resize((760, 400))
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)
    else:
        return

def show_frame1():
    text = button2.cget('text')
    if text == "pause":
        ret, frame = cap1.read()
        centers = []

        # #Reading image in grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # #Gaussian Blur
        blur = cv2.GaussianBlur(gray, kernal_size_blur, 5)
        subtracted_image = sub1.apply(blur)

        # #Dilation
        dilated_image = cv2.dilate(subtracted_image, np.ones((5, 5)))

        # #Closing Morphological Operation
        morph_open = cv2.morphologyEx(dilated_image, cv2.MORPH_CLOSE, kernal_size_dilated)
        morph_open = cv2.morphologyEx(morph_open, cv2.MORPH_CLOSE, kernal_size_dilated)

        # #Contours
        contours, hierarcy = cv2.findContours(morph_open, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filtering contours of vehicles
        valid_contour = []
        for c in contours:
            (x, y, w, h) = cv2.boundingRect(c)
            if w >= 80 and h >= 80:
                valid_contour.append(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        y_line = 550

        img = np.zeros_like(frame)
        cv2.drawContours(img, valid_contour, -1, (0, 255, 0), 3)

        cv2.line(frame, (140, y_line), (1050, y_line), (255, 0, 255), 2)

        # Loop for matching the coordinates of centre of vehicle and line
        global t_vehicles2
        global htv2
        global ltv2

        for c in valid_contour:
            (x, y, w, h) = cv2.boundingRect(c)
            x1 = int(w / 2)
            y1 = int(h / 2)
            c1 = x + x1
            c2 = y + y1
            center = (c1, c2)

            centers.append(center)
            cv2.circle(frame, center, 2, (0, 0, 255), -1)

            if c2 < (y_line + 7) and c2 > (y_line - 3):
                t_vehicles2 = t_vehicles2 + 1
                area = cv2.contourArea(c)
                print(area)
                if area > 500 and area < 15000:
                    ltv2 = ltv2 + 1
                elif area > 15000 and area < 125000:
                    htv2 = htv2 + 1

        # Showing vehicle count
        cv2.putText(frame, "Total Vehicles Count : " + str(t_vehicles2), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255),
                    3)
        cv2.putText(frame, "LTV : " + str(ltv2), (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0 , 0), 3)
        cv2.putText(frame, "HTV : " + str(htv2), (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image).resize((760, 400))
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame1)
    else:
        return


def show_video1():
    text = button1.cget('text')
    if text == "video1":
        button1.config(text="pause")
        show_frame()
    elif text == "pause":
        button1.config(text="video1")

def show_video2():
    text = button2.cget('text')
    if text == "video2":
        button2.config(text ="pause")
        show_frame1()
    elif text == "pause":
        button2.config(text="video2")


x_axis = 80

button1 = tk.Button(buttonFrame,text="video1",command = show_video1 )
button1.place(x=x_axis+100,y=10)

button2 = tk.Button(buttonFrame,text="video2",command = show_video2 )
button2.place(x=x_axis+300,y=10)

window.mainloop()