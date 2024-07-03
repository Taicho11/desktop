import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD) 
import time
from math import sqrt,tan,pi
import calculate_azimuth

MPU9265 = 0x68
AK8963 = 0x0c

        

class cansat_np:
    def __init__(self,rf_pin=38,rb_pin=36,lf_pin=37,lb_pin=35,moter_pin=12,dis_thresh=25,speed=10):
       for pin in [rf_pin,rb_pin,lf_pin,lb_pin,moter_pin]:
          gpio.setup(pin,gpio.OUT)
       
       calculate_azimuth.main()
       self.pin_list=[rb_pin,rf_pin,lb_pin,lf_pin]
       self.moter_pin=moter_pin
      
       self.corn_posi=[0,5000]
       self.dis_thresh=dis_thresh
       self.speed=speed

    def wheel_cont(self,onoff_list):
       '''
       ピンのオンオフ、右輪のduty,左輪のdutyを指定し、回転方向、スピードを決める


       digit_list:[rf,rb,lf,lb]0だったらoff、1だったらon
       [1,0,1,0]:前進
       [1,0,0,1]:左回転
       [0,1,1,0]:右回転
       [0,0,0,0]:停止
       '''
       for (pin,dig) in zip(self.pin_list,onoff_list):
           gpio.output(pin,dig)


    def main(self):
       arpha=azimuth
       beta=arpha
       pro_posi=[0,0]
       pro_time=time.time()
       self.wheel_cont([1,0,1,0])

       while True:
          pro_angle=beta+(pi/2)-arpha
          beta=self.angle()
          now_time=time.time()
          delta_time=now_time-pro_time
          norm=self.speed*delta_time
          cansat_posi=[]
          cansat_posi.append((norm/sqrt(1+tan(pro_angle)^2))+pro_posi[0])
          cansat_posi.append((norm*tan(pro_angle)/sqrt(1+tan(pro_angle)^2))+pro_posi[1])
          if abs(cansat_posi[0])>25:
             if cansat_posi[0]>0:
               while beta!=pi/2-arpha:
                  beta=self.angle()
                  self.wheel_cont([1,0,0,1])

             if cansat_posi[0]<0:
               while beta!=pi/2-arpha:
                  beta=self.angle()
                  self.wheel_cont([0,1,1,0])
             self.wheel_cont[1,0,1,0]
             time.sleep(cansat_posi[0]*self.speed)
         
          pro_posi=cansat_posi
          pro_time=now_time
            
          

kurasu=cansat_np()


