#include <Servo.h>

Servo servo_cpu;
Servo servo_memory;
int incomingByte = 0;
int val = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  servo_cpu.attach(10);
  servo_cpu.write(0);
  servo_memory.attach(11);
  servo_memory.write(0);
}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available()) {
    // read the incoming byte:
    incomingByte = Serial.read();
    if (incomingByte < 58 && incomingByte > 47) {//如果获取到的是数字
      val = val * 10 + (incomingByte - 48);
    } else if (incomingByte == 67) { //如果获取到的是C,表示是CPU
      //把读到的数据呈现在舵机上
      servo_cpu.write(val);
      val = 0; //把val清零
    } else if (incomingByte == 77) { //如果获取到的是M,表示是memory 内存
      servo_memory.write(val);
      val = 0; //把val清零
    }
  }

  //      say what you got:
  //      Serial.print("I received: ");
  //      Serial.println(val);

  //  todo 监测按钮

  //  while (incomingByte != 35) {
  //    Serial.print("byte: ");
  //    Serial.println(incomingByte, DEC);
  //    val = val * 10 + (incomingByte - 48);
  //    incomingByte = Serial.read();
  //  }



}
