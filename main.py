import serial,time,psutil
from threading import Timer
import mail

ser = serial.Serial("/dev/cu.usbmodem1411")
print(ser.name)

# 使用count来记录process被调用的次数
count=0

def process():
    global count
    print(count)
    if count==0:
        mail_unseen()
        print('mail')
    else:
        if count%2==0:
            cpu()
            print('cpu')
        else:
            memory()
            print('memory')

    count=(count+1)%120
    Timer(1, process).start()

Timer(0.5,process).start()

def cpu():
    val = psutil.cpu_percent()
    ser.write(b"%dC"%int(val*180/100))  # 把CPU使用比换算成180°,传给Arduino

def memory():
    val = psutil.virtual_memory().percent
    ser.write(b"%dM" % int(val * 180 / 100))  # 把内存使用比换算成180°,传给Arduino

def mail_unseen():
    val = mail.count()
    ser.write(b"%dA" % val)  # 把未读邮件总数传给Arduino
    print('mail'+str(val))



# ser.close()