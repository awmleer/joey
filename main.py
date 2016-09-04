import serial
import time

ser = serial.Serial("/dev/cu.usbmodem1411")
print(ser.name)
while True:
    # line = ser.readline()
    time.sleep(5)
    # 每5秒向窗口写一个hello
    ser.write(b"150#")  # write a string

ser.close()
