#include <Button.h>
#include <Servo.h>

Servo servo_cpu;
Servo servo_memory;
Button btn(13);
int incomingByte = 0;
int val = 0;
int p=0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  for(int i=2;i<=9;i++){
    pinMode(i,OUTPUT);
    digitalWrite(i,HIGH);
  }
  servo_cpu.attach(10);
  servo_cpu.write(0);
  servo_memory.attach(11);
  servo_memory.write(0);
  btn.begin();
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
    } else if(incomingByte == 65){ //如果获取到的是A,表示是未读邮件数量
      LEDbar(val);
      val=0;
    }else { //如果出现非法字符,则可能是数据出错,此时清零val
      val=0;
    }
  }

  //监听按钮
  if(p){
    if(btn.released()){
      p=0;
      LEDbar(7);
      Serial.write("Mark");
    }
  }else{
    if(btn.pressed()){
      p=1;
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


void LEDbar(int val){
  for(int i=0;i<8;i++){
    if(i<val){
      digitalWrite(i+2,LOW);
    }else{
      digitalWrite(i+2,HIGH);
    }
  }
}

