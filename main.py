print("loading packages...")
import urllib
import urllib.request
import cv2
import face_recognition
import numpy as np
import os
import RPi.GPIO as GPIO
import time
from time import sleep
import smtplib
from datetime import datetime
import traceback
from skpy import Skype 
import sys
print("All packages have been loaded.")


""" SETUP KEYPAD FOR RASPBERRY BASED ON CONNECTED PORTS """
# These are GPIO pin numbers where the 
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Referring to the pins by the Broadcom SOC channel number
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
# Expect the stronger force to pull it up --->>> GPIO.PUD_DOWN
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine(line, characters):
    """ GET CHARACTER PRESSED BY USER """
    # Character is 4 button of rows that pressed
    # Set pressed row to high voltage
    GPIO.output(line, GPIO.HIGH)
    character = ""
    if(GPIO.input(C1) == 1):
        character = characters[0]
    if(GPIO.input(C2) == 1):
        character = characters[1]
    if(GPIO.input(C3) == 1):
        character = characters[2]
    if(GPIO.input(C4) == 1):
        character = characters[3]
    # Set line to low voltage again
    GPIO.output(line, GPIO.LOW)
    return character

class Person:
    """ Person AS ADMIN OF DOOR OPENER """
    def __init__(self, name, email, e_pass):
        self.name = name
        self.email = email
        self.email_pass  = e_pass

    def change_name(self,name):
        self.name = name

    def change_email(self,e, e_pass):
        self.email = e
        self.email_pass = e_pass
        
class Door:
    """ DOOR CLASS """
    def __init__(self,person, image_url):
        """
        GET ADMIN, GET IP OF CAMERA IN URL, INITIALIZE MODE TO NORMAL, KNOWNPICTURES FOLDER HAVE ADDED PICTURE 
        AND ENCODE ALL OF PICS IN IT CALLED KONWN_ENCODINGS, REALTIME FOLDER CONSIST ALL PICS THAT CAPTURED
        """
        print("loading saved encodings")
        self.mode = 2 # Default mode is normal
        self.admin = person
        self.url = image_url
        self.skype_id = person.email # "8:live:.cid.adcd7618e369c625" for test
        
        os.system("mkdir realTime")
        os.system("mkdir knownpics")
        os.system("mkdir knownpicforchild")
        self.img_id = 0
        folder_dir_knownpics = f'./knownpics'
        folder_dir_knownpic_for_child = f'./knownpicforchild'
        self.sk = Skype("arya.jalali1379@yahoo.com", "cA5%@57WZ042") # login to skype 

        # Set known_encoding_for_child by the one of the correct picture of knownpic_for_child folder before turning off the door opener
        for img in os.listdir(folder_dir_knownpic_for_child):
            print(img)
            encoded = face_recognition.face_encodings(cv2.imread(folder_dir_knownpic_for_child+"/"+img))
            # If it cannot find face in picture so ignore this picture
            if len(encoded) <= 0:
                continue
            # Set just first face that found in picture
            self.known_encoding_for_child = encoded[0]
            print("child mode pic is set.")
            break
                
        self.known_encodings = []
        for img in os.listdir(folder_dir_knownpics):
            print(img)
            # Encode image
            encoded = face_recognition.face_encodings(cv2.imread(folder_dir_knownpics+"/"+img))
            # If it cannot find face in picture so ignore this picture
            if len(encoded) <= 0:
                continue
            # Set all faces found in the pictures
            for i in encoded:
                self.known_encodings.append(i)

        print("encodings loaded len = ")
        print(len(self.known_encodings))
        

    def new_id(self):
        """ GET NEW ID FOR IMAGE CAPTURED ... CAN SAVE ONLY 40 IMAGES """
        self.img_id += 1
        self.img_id %= 40
        return self.img_id
    
    def capture_realtime(self):
        """ SAVE THE PICTURE IN REALTIME FOLDER WHEN SOMEONE BELLED """
        img = self.capture_image()
        self.save_image(img , f'realTime/{self.new_id()}.jpg')
        self.save_image(img , f'realTime/last.jpg')
        return img

    def capture_image(self):
        """ CAPTURE IMAGE AND RETURN IMAGE """
        response = urllib.request.urlopen(self.url) # Open url and get http response
        imgNp = np.array(bytearray(response.read()), dtype = np.uint8) # Convert picture to numpy array
        img = cv2.imdecode(imgNp, -1) # Set flag to -1 -> IMRead Unchanged
        print("Picture taken.")
        return img

    def save_image(self, img, path):
        """ SAVE IMAGE IN THE PATH BY CV2 METHOD """
        cv2.imwrite(path, img)

    def send_message(self,txt = "someone belled and tryed to enter house. picture is attached."):
        """ SEND MESSAGE FROM LOGINED SKYPE ACCOUNT TO SKYPE_ID THAT HAS SET WHEN CALLING DOOR OPENER """
        try:
            ch = self.sk.chats[self.skype_id] # Get desired chat
            msg_flag = ch.sendMsg(txt) # Send message
            with open("realTime/last.jpg","rb") as f:
                    ch.sendFile(f, "last.jpg", image = True) # Send last image captured to owner
            print("Message sent.")
        except:
            print("Failed to send the message.")

    def open_door(self):
        print("Door opened.")

    def close_door(self):
        print("Door didn't open.")
        
    def image_is_known_normal_mode(self, unknownImg):
        """ CHECK AT LEAST ONE FACE IN IMAGE IS KNOWN OR NOT """
        for unkonwn_encoding in face_recognition.face_encodings(unknownImg):
            for res in face_recognition.compare_faces(self.known_encodings, unkonwn_encoding):
                if res:
                    return True
        return False
    
    def image_is_known_child_mode(self, unknownImg):
        """ CHECK AT LEAST ONE FACE IN IMAGE IS KNOWN OR NOT """
        for unkonwn_encoding in face_recognition.face_encodings(unknownImg):
            if face_recognition.compare_faces([self.known_encoding_for_child], unkonwn_encoding)[0]:
                return True
        return False
        
    def read_from_key_board(self, L, arr):
        """ REPEAT LOOP UNTILL ONE KEY PRESSED L IS PORT NUMBER ARR IS ALL KEY VALID """
        c = readLine(L, arr)
        while not (c in arr):
            c = readLine(L, arr)
            sleep(0.1)
        sleep(1)
        return c
        
    def person_update(self):
        """ UPDATE ADMIN SET NAME, SKYPE ID AND PASSWORD """
        print("Update admin credentials.")
        name = input("enter name\n")
        email = input("enter skype_id\n")
        e_pass = "hi"
        self.admin.change_name(name)
        self.admin.change_email("8:"+email ,e_pass)
        
    def get_pic_encode_faces(self, dir):
        """ CAPTURE IMAGE AND SAVE IT TO DIRECTORY AND RETURN ENCODED FACES """
        img = self.capture_image()
        self.save_image(img, dir)
        return face_recognition.face_encodings(img)
        
    def add_picture_normal_mode(self):
        """ ADD PICTURE IN NORMAL MODE """
        print("Before encoding len = ", len(self.known_encodings))
        encoded_faces = self.get_pic_encode_faces(f'./knownpics/{datetime.now()}.jpg')
        # All faces in picture append to list of known encodings
        for im in encoded_faces:
            self.known_encodings.append(im)
        print("Pics added len = ",len(self.known_encodings))
        
    def add_picture_child_mode(self):
        """ ADD PICTURE IN CHILD MODE """
        encoded_faces = self.get_pic_encode_faces(f'./knownpicforchild/last.jpg')
        # Only pictures with one face are valid
        if len(encoded_faces) == 1:
            self.known_encoding_for_child = encoded_faces[0]
            print("Pictures for child mode have been added.")
        else:
            print("More than one face was found in the picture, please try again.")
        
    def menu(self):
        """ MENU HARWARE IN A LOOP """
        while True:
            print("1) change mode\n2) bell\n3) settings\nA) going to main menu from anywhere.")
            # Read from keyboard
            c = self.read_from_key_board(L1, ["1","2","3","A"]) 
            if c == "1":
                print("Your mode is: ",self.mode)
                print("1) child mode , 2) normal , 3) Empty")
                c = self.read_from_key_board(L1, ["1","2","3","A"])
                if c == "1":
                    self.mode = 1
                elif c == "2":
                    self.mode = 2
                elif c == "3":
                    self.mode = 3
                print("Current mode is: ",self.mode)

            elif c == "2":
                print("Ring the door.")
                if self.mode == 2:
                    img = self.capture_realtime()
                    if self.image_is_known_normal_mode(img):
                        self.open_door()
                        self.send_message("this person entered house")
                    else:
                        self.close_door()
                elif self.mode == 3:
                    print("empty")
                    img = self.capture_realtime()
                    self.send_message()
                else:
                    print("child")
                    img = self.capture_realtime()
                    if self.image_is_known_child_mode(img):
                        self.open_door()
                        self.send_message("this person entered house while your child is home")
                    else:
                        self.send_message()
                        self.close_door()
                    
            elif c == "3":
                print("setting")
                print("1 -> admin update\n2 -> add picture normal (place your face in front of camera)\n3 -> add picture for child mode(place your face in front of camera)")
                sleep(0.5)
                c = self.read_from_key_board(L1, ["1","2","3","A"])
                if c == "1":
                    self.person_update()
                elif c == "2":
                    self.add_picture_normal_mode()
                elif c == "3":
                    self.add_picture_child_mode()
                

if __name__ == "__main__":
    print(sys.argv)
    l = sys.argv
    name = "embedded"
    skype = "8:live:.cid.adcd7618e369c625"
    img_url = "http://192.168.234.84:8080/shot.jpg"
    for index,a in enumerate(l):
        print(a)
        if a == "-n":
            name = l[index+1]
        elif a == "-sk":
            skype = "8:"+l[index+1]
        elif a == "-img":
            img_url = f"http://{l[index+1]}/shot.jpg"

    admin = Person(name,skype,"23")
    door_bell = Door(admin,img_url)
    print("starting manager")
    door_bell.menu()
