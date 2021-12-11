import tca9535
from tca9535 import Pin
from periphery import GPIO


def init():
	global dev
	dev = tca9535.TCA9535()
	dev.set_polarity(0x00, 0x00) 
	dev.config_ports(0xff, 0xff) #all inputs
	dev.pin_mode(Pin.P1_3, tca9535.Mode.OUTPUT) #led output

	global gpio_door
	gpio_door = GPIO("/dev/gpiochip0", 1, "out")

	global gpio_door_ramp
	gpio_door_ramp = GPIO("/dev/gpiochip0", 2, "in")

	global gpio_siren
	gpio_siren = GPIO("/dev/gpiochip0", 3, "out")

	global gpio_door_bell
	gpio_door_bell = GPIO("/dev/gpiochip0", 4, "in")
	
	global gpio_exander_int
	gpio_exander_int = GPIO("/dev/gpiochip0", 5, "in")

def turn_on_siren():
	gpio_siren.write(True)

def turn_off_siren():
	gpio_siren.write(False)

def turn_on_door_relay():
	gpio_door.write(True)

def turn_off_door_relay():
	gpio_door.write(False)

def door_ramp_status():
	return gpio_door_ramp.read()

def door_bell_status():
	return gpio_door_bell.read()

def expander_int_status():
	return gpio_exander_int.read()

def aux_do_status():
	return dev.read_pin(Pin.P0_1)

def aux_di_status():
	return dev.read_pin(Pin.P0_2)

def door_sensor_nc_status():
	return dev.read_pin(Pin.P0_3)

def door_sensor_no_status():
	return dev.read_pin(Pin.P0_4)

def motion1_status():
	return dev.read_pin(Pin.P0_5)

def motion2_status():
	return dev.read_pin(Pin.P0_6)

def exit_button_no_status():
	return dev.read_pin(Pin.P0_7)

def exit_button_nc_status():
	return dev.read_pin(Pin.P1_0)

def trigger_no_status():
	return dev.read_pin(Pin.P1_1)

def trigger_nc_status():
	return dev.read_pin(Pin.P1_2)

def acc_int1_status():
	return dev.read_pin(Pin.P1_4)

def acc_int2_status():
	return dev.read_pin(Pin.P1_5)

def turn_on_led():
	dev.write_pin(Pin.P1_3, 1)

def turn_off_led():
	dev.write_pin(Pin.P1_3, 0)
