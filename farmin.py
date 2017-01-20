import curses
import traceback
import serial
import subprocess
from math import pi

def main(scr, ser):
	# Define the vertical lines between windows
	speed_y=int(curses.COLS / 3 + 1)
	time_y=int(curses.COLS / 3 * 2 + 1)
	scr.vline(0, speed_y - 1, curses.ACS_VLINE, curses.LINES)
	scr.vline(0, time_y - 1, curses.ACS_VLINE, curses.LINES)
	scr.refresh()
	
	# Create distance window
	dstw=curses.newwin(curses.LINES, int(curses.COLS / 3), 0, 0)
	dstw.addstr(subprocess.run(['banner', '0.00 km'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.decode())
	
	# Create speed window
	spdw=curses.newwin(curses.LINES, int(curses.COLS / 3), 0, speed_y)
	spdw.addstr(subprocess.run(['banner', '0.00'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.decode())
	spdw.addstr(subprocess.run(['banner', 'km/h'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.decode())
	
	# Create time window
	timw=curses.newwin(curses.LINES, int(curses.COLS / 3), 0, time_y)
	timw.addstr(subprocess.run(['banner', '00:00'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.decode())
	
	dstw.refresh()
	spdw.refresh()
	timw.refresh()
	
	# Initialise serial connection
	ser.port='/dev/ttyACM0'
	ser.boudrate=115200
	ser.timeout=2
	
	# Set up stats
	seconds=0
	distance=0
	
	ser.open()
	while ser.is_open:
		pings_raw=ser.read()
		# invalid reading
		if pings_raw==b'':
			continue
		pings=int(pings_raw)
		# millimeters to kilometers
		distance_current=(700 * pi * pings) / 1000000
		distance+=distance_current
		# kilometers per two seconds to kmh
		speed=distance_current * 1800
		
		spdw.addstr(0, 0, subprocess.run(['banner', format(speed, '.2f')], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.decode())
		spdw.refresh()
		
		dstw.addstr(0, 0, subprocess.run(['banner', format(distance, '.2f') + ' km'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.decode())
		dstw.refresh()

try:
	scr=curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)
	scr.keypad(True)
	
	ser=serial.Serial()
	
	main(scr, ser)
	
	curses.nocbreak()
	scr.keypad(False)
	curses.echo()
	curses.endwin()
except:
	ser.close()
	curses.nocbreak()
	scr.keypad(False)
	curses.echo()
	curses.endwin()
	traceback.print_exc()
