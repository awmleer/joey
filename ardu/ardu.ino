#include <Button.h>
#include <Servo.h>

Servo servo_cpu;
Servo servo_memory;
Button btn(13);

int incomingByte = 0;
int val = 0;//val用来临时存放从串口中读取到的数字
int p = 0;//p用来标记按钮是否被按下

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // 等待串口就绪
  }
  //引脚定义
  for (int i = 2; i <= 9; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  }
  servo_cpu.attach(10);
  servo_cpu.write(0);
  servo_memory.attach(11);
  servo_memory.write(0);
  btn.begin();
}

void loop() {
  //判断串口中是否有数据传来
  if (Serial.available()) {
    serialRead();//调用serialRead来读取串口中的数据并做处理
  }

  //监听按钮
  if (p) {
    if (btn.released()) {
      p = 0;
      Serial.write("Mark");//通过串口传给计算机数据
      int i=0;
      //让LEDbar显示循环点亮动画,直到从串口收到'0A'的消息
      while (true) {
        i=(i+1)%9;
        LEDbar(i);
        for (int k = 0; k < 30000; k++) {
          if (Serial.available()) {
            serialRead();
            return;//直接退出本次的loop
          }
        }
      }
    }
  } else {
    if (btn.pressed()) {
      p = 1;
    }
  }

}

void serialRead() {
  // 读取一个字节
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
  } else if (incomingByte == 65) { //如果获取到的是A,表示是未读邮件数量
    LEDbar(val);
    val = 0;
  } else { //如果出现非法字符,则可能是数据出错,此时清零val
    val = 0;
  }
}


//控制LEDbar点亮的个数
void LEDbar(int val) {
  for (int i = 0; i < 8; i++) {
    if (i < val) {
      digitalWrite(i + 2, LOW);
    } else {
      digitalWrite(i + 2, HIGH);
    }
  }
}

