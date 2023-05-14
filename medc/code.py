import subprocess, signal
import os
p = subprocess.Popen(['ps'], stdout=subprocess.PIPE)
out, err = p.communicate()

#process = 'python3 /root/medc/meter/main.py'
process = 'python3 /root/Meter2/main.py'

for line in out.splitlines():
	line = line.decode()
	#print(line)
	if process in line:
		print(line)
		pid = int(line.split(None, 1)[0])
		print(pid)
		os.kill(pid, signal.SIGKILL)