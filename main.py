import serial,time,psutil
from threading import Timer
import mail

# 开启串口,超时设定为0.1秒
ser = serial.Serial("/dev/cu.usbmodem1411",timeout=0.1)
print(ser.name)

# 使用count来记录process被调用的次数
count=0

# 每隔1秒触发一次process函数
def process():
    global count
    print(count)
    #使用双层的if，是为了防止出现120秒时串口会同时传两个数据的问题
    if count==0: #每隔120秒更新一次mail的数据
        mail_unseen()
    else:
        if count%2==0: #每隔2秒更新一次CPU的数据
            cpu()
        else: #每隔2秒更新一次memory的数据
            memory()
    count=(count+1)%120
    Timer(1, process).start()# 触发下一次的定时器


# 先等待2秒（确保Arduino就绪），再触发process()函数
time.sleep(2)
process()


def cpu():
    val = psutil.cpu_percent()
    ser.write(b"%dC"%int(180 - val*180/100))  # 把CPU使用比换算成180°,传给Arduino
    print('CPU %d' % int(180 - val * 180 / 100))

def memory():
    val = psutil.virtual_memory().percent
    ser.write(b"%dM" % int(180 - val * 180 / 100))  # 把内存使用比换算成180°,传给Arduino
    print('memory %d'% int(180 - val * 180 / 100))

def mail_unseen():
    val = mail.count()
    ser.write(b"%dA" % val)  # 把未读邮件总数传给Arduino
    print('mail '+str(val))

while True:
    rec=ser.readline()
    if rec==b'Mark': #如果读取到了'mark'
        print(rec)
        result=mail.mark_seen() #把邮件标为已读
        if result=='success': #标记已读成功
            ser.write(b"0A")