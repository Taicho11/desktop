import time
import threading
from math import pi,atan
import BMX055

bmx = BMX055.BMX055()
calibBias = [0.0, 0.0] #地磁気補正用
calibRange = [1.0, 1.0] #地磁気補正用
mag = [0.0, 0.0, 0.0]
acc = [0.0, 0.0, 0.0]
gyro = [0.0, 0.0, 0.0]
CALIBRATION_MILLITIME=20*1000
DATA_SAMPLING_RATE = 0.00001

def calibration(): #地磁気補正用関数
    global calibBias
    global calibRange
    max = [0.0, 0.0]
    min = [0.0, 0.0]
    max[0] = mag[0] #max,minの初期化
    max[1] = mag[1]
    min[0] = mag[0]
    min[1] = mag[1]

    complete = False; #キャリブレーションの完了を判断する変数
    
    while complete==False:
        before = round(time.time()*1000)
        after = before
        while (after-before)<CALIBRATION_MILLITIME:
            if max[0] < mag[0]:
                max[0] = mag[0]
            elif min[0] > mag[0]:
                min[0] = mag[0]
            elif max[1] < mag[1]:
                max[1] = mag[1]
            elif min[1] > mag[1]:
                 min[1] = mag[1]
            after = round(time.time()*1000)()

        if (max[0]-min[0])>20 and (max[1]-min[1])>20:
            print("calibration():  Complete!")
            time.sleep(1)
            complete = True #キャリブレーション完了
        else:
            print("calibration():  False!!!")
            time.sleep(3)
            complete = False
    
    time.sleep(3)
    calibBias[0] = (max[0]+min[0])/2
    calibBias[1] = (max[1]+min[1])/2

    calibRange[0] = (max[0]-min[0])/2
    calibRange[1] = (max[1]-min[1])/2

def setBmxData():
    global acc
    global gyro
    global mag
    global attitude
    acc = bmx.getAcc()
    gyro = bmx.getGyro()
    mag = bmx.getMag()
    for i in range(2): #地磁気補正
        mag[i] = (mag[i]-calibBias[i])/calibRange[i]

def calcAzimuth(): #方位角計算用関数
    global azimuth
    if mag[0] == 0.0:
        mag[0] = 0.0000001
    azimuth = -(180/pi)*atan(mag[1]/mag[0])
    if azimuth<0 and mag[0]<0:
        azimuth += 180
    elif azimuth>0 and mag[0]<0:
        azimuth -= 180
    
	#azimuth += 180

    if azimuth>180:
        azimuth-=360
    else:
        pass


    if acc[2] > 0:
        pass
    else:
        azimuth *= -1
        
    # azimuth += MAG_CONST

    # if azimuth>180:
    #     azimuth -=360
    # if azimuth<180:
    #     azimuth +=360

def setData_thread2():
    while True:
        setBmxData()
        calcAzimuth()
        time.sleep(DATA_SAMPLING_RATE)

def setUp():
    bmx.setUp()
    setBmxData()
    
    writeThread = threading.Thread(target=setData_thread2, args=()) # 上の関数を実行するスレッドを生成
    writeThread.daemon = True
    writeThread.setDaemon(True)
    writeThread.start() # スレッドを起動

def main():
    setUp()
    calibration() 
