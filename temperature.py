import time
import os
from datetime import datetime

mycmd = "cat /sys/class/thermal/thermal_zone0/temp"
mycmd2 = "vcgencmd measure_temp"
mycmd3 = "top -b -d1 -n2 | grep Cpu"

filename = "/home/pi/Programming/python/nannyPhotoFrame/monitor.log"

if not os.path.exists(filename):
	with open(filename,"w") as file:
		file.write("This is the Temperature and CPU Monitoring file")


while True:
	now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

	cpu_usage = os.popen(mycmd3).readline()
	str_result = os.popen(mycmd).readline()
	gpuCmdOP = os.popen(mycmd2).readline()


	CPU_temp = int(str_result)/1000

	gpuTemp1 = gpuCmdOP.replace("temp=","")
	gpuTempStr = gpuTemp1.replace("'C","")
	gpuTempStr = gpuTempStr[0:4]

	#print(now)
	#print("CPU Temp: ", CPU_temp)
	#print("GPU Temp: ", gpuTempStr)
	#print("CPU Usage: ", cpu_usage)

	with open(filename,"a") as file:
		file.write(now)
		file.write(";")
		file.write(str(CPU_temp))
		file.write(";")
		file.write(str(gpuTempStr))
		file.write(";")
		file.write(cpu_usage)

	time.sleep(30)
