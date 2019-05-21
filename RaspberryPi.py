import RPi.GPIO as GPIO
import spidev
import time
import serial
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


spi_kanal=0
spi_CS_port=0
start_bit=1
stop_bit=0

data_iki=""
data_uc=""
data_dort=""
tutucu=[]

on_tampon=0
arka_tampon=0
sag_yan=0
sol_yan=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(2,GPIO.OUT)
GPIO.output(2,GPIO.LOW)

spi=spidev.SpiDev()
spi.open(spi_kanal,spi_CS_port)

ser=serial.Serial('/dev/ttyUSB0',9600)





def kemer():
    oku=GPIO.input(14)
    if oku==True :
        return "takılı"
    elif oku==False :
        return "takılı değil"


    
def kaza_raporu_hazırlama(zaman,hiz,kemer,darbe_bolgesi,hata):
    with open("kaza/kaza_raporu.txt","w") as dosya:
        rapor="Zaman : {}\nHız : {} Km/s\nKemer : {}\nDarbenin alındığı bölge : {}\nHata mesajı : {}".format(zaman,hiz,kemer,darbe_bolgesi,hata)
        dosya.write(rapor)
    

def dosya_gönder():
    smtp_server = "smtp.gmail.com"                   
    port = 587                            
    kullanici_mail = "utpproje@gmail.com"                          
    sifre  = "1q2w3e4rk."                          
    ad = "rpi"                          
    dosya_yolu = "yol/"                         
    gonderilecek_mail = "bkagan0737@gmail.com"                   
    metin = "kaza raporu"                          
     
    
    class mail_sender:
        def __init__(self):
            self.liste = os.listdir(dosya_yolu)
     
        def login(self):
            print("Sunucuya giris yapiliyor...")
            self.mailServer = smtplib.SMTP(smtp_server, port)
            self.mailServer.set_debuglevel(0)
            self.mailServer.ehlo()
            self.mailServer.starttls()
            self.mailServer.ehlo()
            self.mailServer.login(kullanici_mail, sifre)
            print("Sunucuya basariyla giris yapildi.\n")
     
        def logout(self):
            self.mailServer.close()
        def begin(self):
            self.login()
            
            self.liste = os.listdir(dosya_yolu)
            self.dosya = self.dosyasec()
            print(self.dosya + ' secildi.')
            self.send()
            self.logout()
     
        def dosyasec(self):
            return self.liste[0]
        def mailprep(self):
            mail = MIMEMultipart()
            mail['From'] = ad
            mail['To'] = gonderilecek_mail
            mail['Subject'] = self.dosya     
            mail.attach(MIMEText(metin))
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(dosya_yolu + os.sep + self.dosya, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition','attachment; filename="%s"' % self.dosya)
            mail.attach(part)
            return mail
        def send(self):
            yeni_mail = self.mailprep()
            self.mailServer.sendmail(kullanici_mail, gonderilecek_mail, yeni_mail.as_string())
            print('E-posta yollandi. Dosya = ' + self.dosya)

     
    a = mail_sender()
    a.begin()
        
def hava_yastığı(data,data2,data3,data4,hız,):
    global darbe
    if(data<75 and hız<30):
        GPIO.output(2,GPIO.HIGH)
        darbe="Ön Tampon"
        return 1
    elif(data<115 and 30<=hız<70):
        GPIO.output(2,GPIO.HIGH)
        darbe="Ön Tampon"
        return 1
    elif(data<150 and 70<=hız<120):
        GPIO.output(2,GPIO.HIGH)
        darbe="Ön Tampon"
        return 1
    elif(data<190 and 120<=hız<200):
        GPIO.output(2,GPIO.HIGH)
        darbe="Ön Tampon"
        return 1
    elif(data<220 and 200<=hız):
        GPIO.output(2,GPIO.HIGH)
        darbe="Ön Tampon"
        return 1
    if(data2<80):
        GPIO.output(2,GPIO.HIGH)
        darbe="Arka Tampon"
        return 1
    if(data3<170):
        GPIO.output(2,GPIO.HIGH)
        darbe="Sağ yan"
        return 1
    if(data4<170):
        GPIO.output(2,GPIO.HIGH)
        darbe="Sol yan"
        return 1      
    
    else:
        return 0
    
while 1 :
    data=""
    while 1:
        gecici=ser.read()
        data=data+gecici.decode('UTF-8')
        if gecici==b"\n":
            break
        
    veri=data.split()
    
    if veri[0]=="ERR":
        if tutucu.count(veri[2])==0:
            tutucu.append(veri[2])
            for i in range(len(veri)):
                data_iki=data_iki+" "+veri[i]
            data_iki+="\n"+" "*14
    else:
        data_uc=int(veri[0])
    
    kemerr=kemer()
    on_tampon=kanal_oku(start_bit,stop_bit,0)
    arka_tampon=kanal_oku(start_bit,stop_bit,1)
    sag_yan=kanal_oku(start_bit,stop_bit,2)
    sol_yan=kanal_oku(start_bit,stop_bit,3)
    
    if(hava_yastığı(on_tampon,arka_tampon,sag_yan,sol_yan,data_uc)):
        kaza_raporu_hazırlama(time.strftime('%c'),data_uc,kemerr,darbe,data_iki)
        dosya_gönder()
        break
    
