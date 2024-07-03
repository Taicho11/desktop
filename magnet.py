import smbus
from time import sleep
import numpy as np
 
MPU9265 = 0x68
AK8963 = 0x0c
bus = smbus.SMBus(1)

def main():
    MPU9265_init()
 
    while True:
        magnet = get_magnet()
        print(f'{magnet[1]}')
         
        sleep(0.01)
     
 
def MPU9265_init():
    # スリープモードの解除
    bus.write_i2c_block_data(MPU9265, 0x6B, [0x00])
    sleep(0.01)
  
    # 地磁気センサの起動
    bus.write_i2c_block_data(MPU9265, 0x37, [0x02])
    sleep(0.01)
 
 
    # 取得周期100Hzに設定
    bus.write_i2c_block_data(AK8963, 0x0A, [0x16])
    sleep(0.01)
 
 
def get_magnet():
    magnet = []
    flag = bus.read_i2c_block_data(AK8963, 0x02, 1)
    if flag[0] & 1:
        data = bus.read_i2c_block_data(AK8963, 0x03, 7)
        magnet.append(u2s(data[3] << 8 | data[2]) / float(0x8000) * 4800.0)
        magnet.append(u2s(data[1] << 8 | data[0]) / float(0x8000) * 4800.0)
        magnet.append(u2s(data[5] << 8 | data[4]) / float(0x8000) * 4800.0)
    else:
        return np.array([np.nan, np.nan, np.nan])
 
    return magnet
  
# unsignedをsigned(符号付)に変換
def u2s(x):
    if x & (0x01 << 15):
        return -1 * ((x ^ 0xffff) + 1)
    else:
        return x
 
if __name__ == '__main__':
    main()