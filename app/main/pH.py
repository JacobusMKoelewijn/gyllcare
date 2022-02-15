import serial
import sys
import time
from serial import SerialException

from app.config import IN_PRODUCTION

def read_line():
	"""
	taken from the ftdi library and modified to 
	use the ezo line separator "\r"
	"""
	lsl = len(b'\r')
	line_buffer = []
	while True:
		next_char = ser.read(1)
		if next_char == b'':
			break
		line_buffer.append(next_char)
		if (len(line_buffer) >= lsl and
				line_buffer[-lsl:] == [b'\r']):
			break
	return b''.join(line_buffer)


def read_lines():
	"""
	also taken from ftdi lib to work with modified readline function
	"""
	lines = []
	try:
		while True:
			line = read_line()
			if not line:
				break
				ser.flush_input()
			lines.append(line)
		return lines
	
	except SerialException as e:
		print( "Error, ", e)
		return None	


def send_cmd(cmd):
	"""
	Send command to the Atlas Sensor.
	Before sending, add Carriage Return at the end of the command.
	:param cmd:
	:return:
	"""
	buf = cmd + "\r"     	# add carriage return
	try:
		ser.write(buf.encode('utf-8'))
		return True
	except SerialException as e:
		print ("Error, ", e)
		return None
			

def read_pH(cmd):
	send_cmd(cmd)
	time.sleep(1.3)
	lines = read_lines()
	pretty_pH = float(str(lines[0])[2:7])
	print(type(pretty_pH))
	return pretty_pH
	# for i in range(len(lines)):
		# print( lines[i].decode('utf-8'))

if IN_PRODUCTION:
	usbport = '/dev/ttyAMA0'
else:
	usbport = '/dev/ttyAMA1'


try:
	ser = serial.Serial(usbport, 9600, timeout=0)
except serial.SerialException as e:
	print( "Error, ", e)
	sys.exit(0)

# command_EZO_pH_circuit("T,?")
