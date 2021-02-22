#coding=utf-8
import Adafruit_GPIO.I2C as I2C
import RPi.GPIO as GPIO
import time
import json
class modules:
    def __init__(self, address=0x5A):
        I2C.require_repeated_start()
        self._i2c = I2C.Device(address, busnum=1)
        GPIO.setmode(GPIO.BOARD)
        self.laser_Pin = 37 #激光的引脚为26号引脚
        self.buzzer_Pin = 36  # 蜂鸣器为36号引脚

        self.conf_path = "/home/pi/develop/F/data.conf"
    def readAmbient(self):
        return self._readTemp(0x06)
    def readObject1(self):
        return self._readTemp(0x07)
    def readObject2(self):
        return self._readTemp(0x08)
    def _readTemp(self, reg):
        temp = self._i2c.readS16(reg)
        temp = temp * .02 - 273.15
        return temp
    #开启激光
    def laser_start(self):
        GPIO.setup(self.laser_Pin,GPIO.OUT)
        GPIO.output(self.laser_Pin,GPIO.LOW)
    #关闭激光
    def laser_stop(self):
        GPIO.cleanup(self.laser_Pin)
    #蜂鸣器警报
    def warn(self):
        GPIO.setup(self.buzzer_Pin, GPIO.OUT)
        GPIO.output(self.buzzer_Pin, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.cleanup(self.buzzer_Pin)
    #读取阈值数据
    def read_threshold(self):
        with open(self.conf_path,'r') as f:
            data = json.load(f)['temperature']
        return data
    #写入阈值数据
    def write_threshold(self,data):
        temperature = '{"temperature":%s}'%str(data)
        with open(self.conf_path,'w') as f:
            f.write(temperature)
        return True


