# Python-smart-video-door-opener-raspberry-pi
Python smart video door opener with different modes built on a Raspberry Pi 3, and controllerd using a keypad.

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
- Automatic: The door will automatically open for those, whose faces the video door opener recognizes. 

- Child: The door will open if the video door opener recognizes the face of the person ringing the door.

  - Note that in this mode the door will only open for one single individual.

- Empty: The door won't open, and upon ringing the door a picture will be taken and sent to the owner's Skype account.

## Some pictures of the hardware used in the making of this project:
# LCD and keypad:
![Monitor](/Lcd.jpg)
# Closer shot of the keypad:
![Keypad](/Keypad.jpg)
# Raspberry Pi as the main component and its connections:
![Raspberry](/Raspberry-pi-with-connections.jpg)

# How to run:
- Download pi camera or a similar app, that lets you use your phone as a camera, Set up a server on it, and pass your ip to the code as instructed below.
- Connect the Raspberry Pi to the network of your phone (preferably using hotspot).
- Connect the keypad ports and LCD as shown in the pictures above.
- Run main.py

# Step-by-step guide
+ Install Raspberry Pi OS to your sd card.[Download](https://www.raspberrypi.com/software/)
+ Create .ssh in /boot and wpa file for ssh connection [manual](https://spin.atomicobject.com/2019/06/09/raspberry-pi-laptop-display/)
+ Create your env to run 'main.py', for which you need to have met all the requirements written in 'requirments.txt'.
+ Install RPI.GPIO.
+ Run the program using the following command:
+ for running you have to pass 3 arguments like bellow 
```console
python3 main.py -n admin -sk live:.cid.2ed8ea3282acdacd -img 192.168.204.44:8080
```

<li>

-n: Name of the owner (cannot be changed during runtime)

-sk: The skype id of the owner (cannot be changed during runtime)

-img: IP:Port of your camera.
</li>
