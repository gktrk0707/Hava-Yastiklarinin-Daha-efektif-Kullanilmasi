#include <SoftwareSerial.h>
#define hiz A0
SoftwareSerial seri(10,11);

String veri="";
int hata1=7;
int hata2=6;
int hata3=5;

uint16_t deger=0;
uint16_t oncekideger=0;
String hizz;

void setup() {
  Serial.begin(115200);
  seri.begin(9600);
  Serial.println("basliyoruz");
  pinMode(hata1,INPUT);
  pinMode(hata2,INPUT);
  pinMode(hata3,INPUT);
    

}

void loop() {
  if(digitalRead(hata1)){
  
seri.write("ERR NO: 101 Fren balatalarinda asinma tespit edildi.\n");
delay(0.5);
  
  }

  if(digitalRead(hata2)){
  

seri.write("ERR NO: 102 Motor yag basincinda dusme tespit edildi.\n");
delay(0.5);
  
  }

  if(digitalRead(hata3)){
  

seri.write("ERR NO: 103 ABS fren sistemi devre disi.\n");
delay(0.5);
  
  }

deger=analogRead(hiz);
deger=((float)300/1023)*deger;


if (deger!=oncekideger)
{


oncekideger=deger;
seri.println(deger);
Serial.println(deger);
delay(0.5);


  
  }


  
  
}
