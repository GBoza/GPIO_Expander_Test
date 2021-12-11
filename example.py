import board
import time

board.init()

while(1):
	board.turn_on_led()
	time.sleep(1)
	board.turn_off_led()
	time.sleep(1)

