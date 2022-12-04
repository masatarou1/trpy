import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("./test_data.csv", delimiter=",")
data = data[:,1]

sample_size = 25000
sampleRate = 6.25E6
sampleRate = 10e9
recordLength = 500000
freq = 100e3

pattern = "float"

data_min, data_max = data.min(), data.max()
original_min, original_max = -0.5, 3.0

# (失敗例）元データのmin, maxは考える必要ない
# data_min, data_max = original_min, original_max

#defaultの方法
if pattern == "Default":
    wave_form = 2*(data - data_min)/(data_max - data_min) - 1

    to_transfer = np.ones(len(wave_form), dtype=np.uint16) * (2**13)
    to_transfer += np.require(np.rint(8191*wave_form), np.uint16)
    
    scale = data_max - data_min
    offset = data_min + 0.5*scale
    display_data = to_transfer / to_transfer.max() - 0.5
    restored_data = end_data*scale + offset
    
    # → -0.5 ←→ +0.5 のデータになるので、

#unsigned 正しい方法？
elif pattern == "unsigned Long":
    wave_form = (data- data_min) / (data_max - data_min)
    
    to_transfer = np.round(wave_form*(2**15), decimals= 0)
    to_transfer = np.require(to_transfer, np.uint16)
    
    scale = (data_max - data_min) / 2
    offset = data_min + scale
    display_data = to_transfer / 2**15 * 2 - 1
    restored_data = display_data * scale + offset
    
#signed Longで送る場合
elif pattern == "signed Long":

    abs_max = np.abs(data_max).max()
    wave_form = data / abs_max
    
    to_transfer = np.round(wave_form * (2**15-1), decimals = 0)
    to_transfer = np.require(to_transfer, np.int16)
    
    scale = abs_max
    offset = 0
    display_data = to_transfer / 2**15
    restored_data = display_data * scale + offset
    
elif pattern == "float":

    to_transfer = np.require(data, np.float16)
    

plt.plot(to_transfer)
plt.show()


plt.plot(display_data)
plt.show()

plt.plot(data)
plt.show()

plt.plot(restored_data)
plt.show()

#floatで送れるなら, dtype:fとしてしまえばそのまま送れる？
