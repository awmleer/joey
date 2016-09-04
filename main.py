import serial,time,psutil
ser = serial.Serial("/dev/cu.usbmodem1411")
print(ser.name)
while True:
    # line = ser.readline()
    time.sleep(0.5)
    # 每5秒向窗口写一个hello
    val = psutil.cpu_percent()
    ser.write(b"%dC"%int(val*180/100))  # 把CPU使用比换算成180°,传给Arduino

    time.sleep(0.5)
    val = psutil.virtual_memory().percent
    ser.write(b"%dM" % int(val * 180 / 100))  # 把内存使用比换算成180°,传给Arduino

ser.close()