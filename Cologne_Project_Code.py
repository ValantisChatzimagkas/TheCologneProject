""" CLASS MONITORING SYSTEM WITH RASPBERRY PI 3 , HC-SR501 PIR SENSOR, RASPBERRY PI CAMERA 

###############################################################################################
This project was a collaboration project between THOMAS MORE COLLEGE and the Cologne University
and it involved the Electronics department of both universities. It is a monitoring system which
involves a raspberry pi, a raspberry pi camera and a PIR motion sensor. This system receives an
interrupt via the PIR sensor , next the raspberry pi automatically will take a picture using the
camera , after this step the photo will go through face detection and find how many faces are there
and last it will upload the timestamp and the number of faces found in a local host server which
has a database.This has also been achieved for a remote server as well
###############################################################################################

----------------------------------------LICENSE----------------------------------------------------
 OpenCV License : https://opencv.org/license.html
 I do not own openCV nor I do have any rights upon this product
 
 This software is provided by the copyright holders and contributors “as is” and any 
 express or implied warranties, including, but not limited to, the implied warranties of
 merchantability and fitness for a particular purpose are disclaimed. In no event shall 
 copyright holders or contributors be liable for any direct, indirect, incidental, special, 
 exemplary, or consequential damages (including, but not limited to, procurement of substitute 
 goods or services; loss of use, data, or profits; or business interruption) however
 caused and on any theory of liability, whether in contract, strict liability, or tort (including 
 negligence or otherwise) arising in any way out of the use of this software, even if 
 advised of the possibility of such damage.
 ----------------------------------------------------------------------------------------------------
 
 The following code is a product of research and development and has non profit purposes , I do not own
 any copyrights. The only reason why I upload this code is  to help and share the results of my research 
 during the Cologne project.
 
 Anyone who would like to use this code , please contact first the openCV for any licenses. I do not have
 any legal responsibilities in any case you ignore these instructions.

 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
Last I would like to make clear that you cannot take pictures without asking the permission of others.
In case you would like to use this system you should inform people that they are being monitored and 
that there is camera in the place where you have set this system. 
 
"""


import RPi.GPIO as GPIO#We use GPIO pin for our sensor
from time import sleep#We use time delay
import time
import sys#Needed for lines 5&6 our modules where saved to wrong path, OpenCV saved in different path
sys.path.append('/usr/local/lib/python3.4/site-packages')#If you face the same problem
sys.path.append('/usr/local/lib/python2.7/dist-packages')#Search where opencv might be saved
from picamera import PiCamera#Camera module
import numpy as np#Used for calculations of face detection
import cv2#The module which does the face detection
import pymysql#The module we used to send data to a database
import pymysql.cursors#used for the database data insertion
import urllib.request#used to upload data to remote server
camera = PiCamera()#Camera
camera.rotation = 180#Camera is upside down


GPIO.setmode(GPIO.BCM)#We refer to GPIO numbering

PIR_PIN = 26#GPIO 26 is connected to our PIR sensor

GPIO.setup(PIR_PIN, GPIO.IN)#We use PIN 26 as input PIN


def PHOTOSHOOT(PIR_PIN) :#We enter this routine when interrupt occurs
    shoot=time.asctime( time.localtime(time.time()))#save date&time 
    camera.annotate_text=str(shoot)#we tag date&time to our photo
    camera.capture('/home/pi/Desktop/OpenCV_WORKSPACE/image'+shoot +'.jpg')
    
    print("Photoshooting")
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')#haar cascade for face recognition
    image = cv2.imread('image'+shoot+'.jpg')#load image for proccesing
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)#grayscale conversion
    faces = face_cascade.detectMultiScale(grayImage, 1.3,5)
    print (type(faces))
    print(faces)
    print(faces.shape)
    print("Number of faces detected: " + str(faces.shape[0]) + ' ' + shoot)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
 
        cv2.rectangle(image, ((0,image.shape[0] -25)),(270, image.shape[0]), (255,255,255), -1)
        
        cv2.putText(image, "Number of faces detected: " + str(faces.shape[0]), (0,image.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)#Prints faces found
         
    #image write with rectangles here
    cv2.imwrite('image'+shoot+'.jpg',image)
       
        
    value = str(faces.shape[0])
	#data uplod to remote server 
    urllib.request.urlopen('http://healthmonitor.ddns.net/insert_people.php?people='+value)
    
	""" ---------------Localhost data upload----------------- 
    db = pymysql.connect("localhost","root","root","People" )
    cursor = db.cursor()
    cursor.execute("INSERT INTO People_and_Time(People)"
               "VALUES(%s)", value)
    db.commit()"""
    

try:
     #when an interrupt occurs we jump to our interrupt routine   
	GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=PHOTOSHOOT)#checks motion was detected
	
	#Wait until and interrupt occurs and stay idle
	while 1:
		pass
		
except KeyboardInterrupt:#if a key from keyboard was pressed it will exit our code 
	print("Quit")
	GPIO.cleanup();



