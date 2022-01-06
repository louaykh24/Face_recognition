import imghdr
import sqlite3
from email.message import EmailMessage
from tkinter.messagebox import showinfo

import cv2
import numpy as np
import face_recognition
import os
import smtplib
import configi
from tkinter.messagebox import *


def bd():
    fichierD = "C:/bd/image.sq3"
    conn = sqlite3.connect(fichierD)
    curr = conn.cursor()
    m = curr.execute("""
    SELECT * FROM ImageData""")
    for x in m:
        rec_data = x[2]

        with open("C:/Users/loayk/PycharmProjects\pythonProject3/ImagesAttendAnce/{}.jpg".format(x[1]), "wb") as f:
            f.write(rec_data)
name=""
img_counter = 0
Sender_Email = "loaykh24@gmail.com"
Reciever_Email = "loaykh24@gmail.com"
Password = "239094__qL"
newMessage = EmailMessage()
newMessage['Subject'] = "Security Alert"
newMessage['From'] = Sender_Email
newMessage['To'] = Reciever_Email
newMessage.set_content('Alert, This person is  trying to open your account ')

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
if myList==[]:
    bd()
    myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl) [0])
print(classNames)

def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(configi.EMAIL_ADDRESS, configi.PASSWORD)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(configi.EMAIL_ADDRESS, configi.EMAIL_ADDRESS, message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")




def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList



encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
x=4
while x==4:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches [matchIndex]:
            name = classNames [matchIndex].upper()
            cv2.imshow('Webcam', img)
            cv2.waitKey(1)
            showinfo('Résultat', 'Authentification de l admin est terminé avec succé.')

            x=1
        else:
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, img)
                print("{} written!".format(img_name))
                img_counter += 1
                with open(img_name, 'rb') as f:
                    cv2.imshow('Webcam', img)
                    cv2.waitKey(1)
                    image_data = f.read()
                    image_type = imghdr.what(f.name)
                    image_name = f.name
                    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(Sender_Email, Password)
                        smtp.send_message(newMessage)
                        showwarning('Résultat', 'Mot de passe incorrect.\nVeuillez recommencer !')






