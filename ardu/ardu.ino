#include <Servo.h>

Servo myservo;
int incomingByte = 0;
int val = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  myservo.attach(9);
  myservo.write(0);
}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available() > 0) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if (incomingByte != 35) {
      val = val * 10 + (incomingByte - 48);
    } else {
      //把读到的数据呈现在舵机上
      myservo.write(val);
      //say what you got:
      Serial.print("I received: ");
      Serial.println(val);
      val=0;//把val清零
    }
  }

//  while (incomingByte != 35) {
//    Serial.print("byte: ");
//    Serial.println(incomingByte, DEC);
//    val = val * 10 + (incomingByte - 48);
//    incomingByte = Serial.read();
//  }



}
