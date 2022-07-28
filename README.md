# Python-smart-video-door-opener-raspberry-pi
Python smart video door opener with different modes built with Raspberry Pi 3 , keypad.

Final project of the Embedded systems course taught by Dr.Ansari.

## Hardware:
- Raspberry Pi (Monitor, keypad)
- Phone with a working camera.(install camera IP)

## Packages:
- face_recognition
- RPi.GPIO
- time
- urllib
- cv2
- numpy
- os
- datetime
- skpy

## Connect keypad to Raspberry Pi:
Connect the data lines of the keypad to the Raspberry Pi GPIO pins as shown in the picture below:

![Keypad GPIO-pin setup](/keypad-how-to-connect.jpg)

## Modes:
- Automatic: In this mode the door will automatically open for those whose faces the video door opener recognizes, and there is no need for ringing the door. 

- Child: In this mode the door can only be opened if the video door opener recognizes the face of the person ringing the door.

- Empty: In this mode the door won't be opened, and upon ringing the door a picture will be taken and sent to the owner's Skype account.

## Some pictures of the hardware used in the making of this project:
# LCD and keypad:
![Monitor](/Lcd.jpg)
# Closer shot of the keypad:
![Keypad](/Keypad.jpg)
# Raspberry Pi as the main component and its connections:
![Raspberry](/Raspberry-pi-with-connections.jpg)

# How to run:
- Download pi camera or a similar app that lets you use your phone as a camera, create server from it, and place your ip in code as url of Door class
- Connect the Raspberry Pi to the network of your phone (preferably using hotspot).
- Connect the keypad ports and LCD as shown in the pictures above.
- Run main.py

# run step by step
+ first you have to install raspbian on your sd card. here is [manual](https://www.raspberrypi.com/software/)
+ then create .ssh in /boot and wpa file for ssh connection [manual](https://spin.atomicobject.com/2019/06/09/raspberry-pi-laptop-display/)
+ after those step you should now create your env to run main.py for doing that use requirments.txt to create env with all packages you need with pip.
install RPI.GPIO.
+ for running you have to pass 3 arguments like bellow 
```
python3 main.py -n admin -sk live:.cid.2ed8ea3282acdacd -img 192.168.204.44:8080
```
which are name and skype id and camera IP ip.

<li>

-n is name

-sk is skype id

-img is ip and port of your camera IP 
</li>
