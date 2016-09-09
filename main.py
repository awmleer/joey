import serial,time,psutil
from threading import Timer
import mail

# 开启串口,超时设定为0.1秒
ser = serial.Serial("/dev/cu.usbmodem1411",timeout=0.1)
print(ser.name)

# 使用count来记录process被调用的次数
count=0

# 每隔0.5秒触发一次process函数
def process():
    global count
    print(count)
    if count==0:
        mail_unseen()
    else:
        if count%2==0:
            cpu()
        else:
            memory()
    count=(count+1)%120
    Timer(1, process).start()

Timer(0.5,process).start()


def cpu():
    val = psutil.cpu_percent()
    ser.write(b"%dC"%int(val*180/100))  # 把CPU使用比换算成180°,传给Arduino
    print('CPU %d' % int(val * 180 / 100))

def memory():
    val = psutil.virtual_memory().percent
    ser.write(b"%dM" % int(val * 180 / 100))  # 把内存使用比换算成180°,传给Arduino
    print('memory %d'% int(val * 180 / 100))

def mail_unseen():
    val = mail.count()
    ser.write(b"%dA" % val)  # 把未读邮件总数传给Arduino
    print('mail '+str(val))

while True:
    rec=ser.readline()
    if rec==b'Mark': #如果读取到了'mark'
        print(rec)
        result=mail.mark_seen() #把邮件标为已读
        if result=='success':
            ser.write(b"0A")