#References
# https://www.researchgate.net/publication/327554338_A_Video_based_Vehicle_Detection_Counting_and_Classification_System
# Research paper for guidance: https://www.researchgate.net/publication/261059609_Vehicle_detection_using_morphological_image_processing_technique

import cv2
import numpy as np
from time import sleep

def detectVehicles(path):
    #Declaration of Kernel for blurring and dilation
    kernal_size_blur=(7,7)
    kernal_size_dilated=(13,13)


    #Reading the video
    cap = cv2.VideoCapture(path)
    sub = cv2.bgsegm.createBackgroundSubtractorMOG()


    #Initializing count for vehicles
    t_vehicles = 0
    ltv = 0
    htv = 0

    #Loop for iterating over frames
    while True:
        ret , frame = cap.read()
        centers = []

        # #Reading image in grayscale
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # #Gaussian Blur
        blur = cv2.GaussianBlur(gray,kernal_size_blur,5)
        subtracted_image = sub.apply(blur)


        # #Dilation
        dilated_image = cv2.dilate(subtracted_image,np.ones((5,5)))

        # #Closing Morphological Operation
        morph_close= cv2.morphologyEx (dilated_image, cv2. MORPH_CLOSE , kernal_size_dilated)
        morph_close = cv2.morphologyEx (morph_close, cv2. MORPH_CLOSE , kernal_size_dilated)


        # #Contours
        contours , hierarcy = cv2.findContours(morph_close,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


        #Filtering contours of vehicles
        valid_contour = []
        for c in contours:
            (x,y,w,h) = cv2.boundingRect(c)
            if w >= 80 and h >= 80:
                valid_contour.append(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


        y_line=550
        img = np.zeros_like(frame)
        cv2.drawContours(img, valid_contour, -1, (0, 255, 0), 3)
        cv2.line(frame, (140, y_line), (1050, y_line), (255,0,255), 2)

        #Loop for matching the coordinates of centre of vehicle and line
        for c in valid_contour:
            (x, y, w, h) = cv2.boundingRect(c)
            x1 = int(w / 2)
            y1 = int(h / 2)
            c1 = x + x1
            c2 = y + y1
            center =(c1, c2)

            centers.append(center)
            cv2.circle(frame, center, 2, (0, 0,255), -1)

            if c2 < (y_line + 7)  and c2 > (y_line - 3):
                t_vehicles = t_vehicles + 1
                area = cv2.contourArea(c)
                print (area)
                if area > 500 and area < 15000:
                    ltv = ltv + 1
                elif area > 15000 and area < 125000:
                    htv = htv + 1



        #Showing vehicle count
        cv2.putText(frame, "Total Vehicles Count : " + str(t_vehicles), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),3)
        cv2.putText(frame, "LTV : " + str(ltv), (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)
        cv2.putText(frame, "HTV : " + str(htv), (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),3)

        cv2.imshow("detecting vehicles",frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()



