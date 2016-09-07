import serial,time,psutil
import mail
ser = serial.Serial("/dev/cu.usbmodem1411")
print(ser.name)
while True:
    # line = ser.readline()
    #todo 为了监听串口回传的数据,不能使用sleep这种阻断的方式
    time.sleep(0.5)
    # 每5秒向窗口写一个hello
    val = psutil.cpu_percent()
    ser.write(b"%dC"%int(val*180/100))  # 把CPU使用比换算成180°,传给Arduino

    time.sleep(0.5)
    val = psutil.virtual_memory().percent
    ser.write(b"%dM" % int(val * 180 / 100))  # 把内存使用比换算成180°,传给Arduino

    time.sleep(0.5)
    val = mail.count()
    ser.write(b"%dA" % int(val * 180 / 100))  # 把未读邮件总数传给Arduino

ser.close()