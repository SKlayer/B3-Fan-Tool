import time,paramiko,_thread
cmd ="devmem2 0x43c00084 w 0x0000064"
def tim():
	return(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))))
def init():
	print("""
	B3风扇调速工具 第一步输入IP地址，之后输入风扇转速比值0到100调速。
	B3 Fan speed ctrl tool. first input miner's ip address,then input speed value 0~100.
	本工具可用于T9+控制器的机型 切记B3芯片尽量不要超过60度，否则不稳定
	Warning !! Don't make B3 chip over 60 C. It will make your miner dead!!
	BTM FAN TOOL    BY Sklayer.........
	""")
	global cmd
	ipipt=input("Input Miner IP Address: ")
	null=None
	print("Miner Connection Thread Starting......")
	_thread.start_new_thread(set_pwm,(ipipt,null))
	while 1:
		while 1:
			try:
				pwm=int(input('Input A INT 0-100: '))
				break
			except:
				print("Input A Valid Number.")
			
		if pwm<0 or pwm >100:
			print('Input A Valid Number.')
		else:
			print('Set OK')
			pwm_H=int(pwm*64/100)
			pwm_L=64-pwm_H
			if pwm_H <=9:
				pwm_H="0"+str(pwm_H)
			if pwm_L <=9:
				pwm_L="0"+str(pwm_L)
			cmd="devmem2 0x43c00084 w 0x00"+str(pwm_H)+"00"+str(pwm_L)# 0x 0032 0032 SUM MUST BE 0064

def set_pwm(ip,null):
	global cmd
	while 1:
		try:
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			port=22
			ssh.connect(ip,port,'root','admin')
			while 1:
				stdin,stdout,stderr = ssh.exec_command(cmd)
				#print(cmd)
				outmsg,errmsg = stdout.read(),stderr.read()
				if errmsg == "":
					print(outmsg)
			ssh.close()
			return True
		except:
			pass

init()
