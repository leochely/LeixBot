#include <LedControl.h>
int DIN = 10;
int CS =  9;
int CLK = 8;

LedControl lc=LedControl(DIN,CLK,CS,0);

void setup(){
 lc.shutdown(0,false);       
 lc.setIntensity(0,15);      //Adjust the brightness maximum is 15
 lc.clearDisplay(0);    
}

void loop(){ 
    
    //Facial Expression
    byte smile[8]=   {0x3C,0x42,0xA5,0x81,0xA5,0x99,0x42,0x3C};
    byte neutral[8]= {0x3C,0x42,0xA5,0x81,0xBD,0x81,0x42,0x3C};
    byte sad[8]=   {0x3C,0x42,0xA5,0x81,0x99,0xA5,0x42,0x3C};

   
//Facial Expression   
    printByte(smile);
     
    delay(1000);

    printByte(neutral);
    
    delay(1000);

    printByte(sad);    

    delay(1000);
   
 
}

void printByte(byte character [])
{
  int i = 0;
  for(i=0;i<8;i++)
  {
    lc.setRow(0,i,character[i]);
  }
}
