from gpiozero import MotionSensor
from picamera import PiCamera
import datetime
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

print("Application started..")
pir = MotionSensor(4)
camera = PiCamera()

def email(timeDate):
    print("Email called..")
    fromaddr = "raspberryscamera@gmail.com"
    toaddr = "raspberryscamera@gmail.com"
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Intruder! " + timeDate
    
    body = ""
    
    msg.attach(MIMEText(body, 'plain'))
    
    filename = timeDate + ".jpg"
    attachment = open("/home/pi/Desktop/security-pictures/"+filename, "rb")
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(fromaddr,'Sophie123!')
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Email sent!")

while True:
    pir.wait_for_motion()
    timeDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Detected! " + timeDate)
    time.sleep(1)
    camera.capture('/home/pi/Desktop/security-pictures/' + timeDate + '.jpg')
    print("Picture saved!")
    email(timeDate)
    pir.wait_for_no_motion()
    print("Undetected! " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
