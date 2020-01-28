import time
import sys
import spidev

spi = spidev.SpiDev()
spi.open(0,0)

def buildReadCommand(channel):
	# read command is:
	# bit 13 Configuration update
	# bit 12:10 Input channel configuration
	# bit 9:7 Input channel selection
	# bit 6 Bandwidth
	# bit 5:3 Reference/buffer selection
	# bit 2:1 Channel sequencer
	# bit 0: Readback register
	
	read_command = 0x3C49
	read_command <<= 2
	
	return read_command
	
def processAdcValue(result):
	'''Take in result as array of three bytes.
		Return the two lowest bits of the 2nd byte and
		all of the third byte'''
	byte2 = (result[1] & 0x03)
    return (byte2 << 8) | result[2]

def readAdc(channel):
	if ((channel > 7) or (channel < 0)):
		return -1
	r = spi.xfer2(buildReadCommand(channel))
	return r
	
if __name__ == '__main__':
	try:
		while True:
			val = readAdc(0)
			print "ADC Result: ", str(val)
			time.sleep(5)
	except KeyboardInterrupt:
		spi.close()
		sys.exit(0)