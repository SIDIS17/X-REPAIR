#include <Wire.h>
#define ADXL345 0x53
#define REG_DEVID 0x00
#define REG_BW_RATE 0x2C
#define REG_POWER_CTL 0x2D
#define REG_DATA_FORMAT 0x31
#define REG_DATAX0 0x32

const float G_PER_LSB=0.0039f;

void wr(uint8_t r,uint8_t v){Wire.beginTransmission(ADXL345);Wire.write(r);Wire.write(v);Wire.endTransmission();}
uint8_t rd(uint8_t r){Wire.beginTransmission(ADXL345);Wire.write(r);Wire.endTransmission(false);Wire.requestFrom(ADXL345,(uint8_t)1);return Wire.available()?Wire.read():0xFF;}
bool xyz(int16_t&x,int16_t&y,int16_t&z){
  Wire.beginTransmission(ADXL345);Wire.write(REG_DATAX0);
  if(Wire.endTransmission(false)!=0)return false;
  Wire.requestFrom(ADXL345,(uint8_t)6); if(Wire.available()<6)return false;
  uint8_t x0=Wire.read(),x1=Wire.read(),y0=Wire.read(),y1=Wire.read(),z0=Wire.read(),z1=Wire.read();
  x=(int16_t)((x1<<8)|x0);y=(int16_t)((y1<<8)|y0);z=(int16_t)((z1<<8)|z0);return true;
}
void setup(){
  Serial.begin(230400);Wire.begin(21,22);Wire.setClock(400000);delay(200);
  if(rd(REG_DEVID)!=0xE5){Serial.println("# ADXL345 non detecte");while(true)delay(1000);}
  wr(REG_DATA_FORMAT,0x0B);wr(REG_BW_RATE,0x0E);wr(REG_POWER_CTL,0x08);
}
void loop(){
  int16_t x,y,z;if(xyz(x,y,z)){Serial.print(x*G_PER_LSB,6);Serial.print(",");Serial.print(y*G_PER_LSB,6);Serial.print(",");Serial.println(z*G_PER_LSB,6);}
  delayMicroseconds(625);
}
