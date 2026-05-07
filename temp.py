import time

import utils.mcp23017
import utils.rotary
from machine import I2C, Pin

i2c = I2C(scl=Pin(25), sda=Pin(32))
mcp = utils.mcp23017.MCP23017(i2c)

# encoder pins
sw_pin = 5
clk_pin = 3
dt_pin = 4

# callback: prints value and switch state reported by Rotary
def cb(val, sw):
	volume = '\u2590' * val + '\xb7' * (10 - val)
	if sw:
		btn = '\u2581\u2583\u2581'
	else:
		btn = '\u2581\u2587\u2581'
	print(volume + ' ' + btn)
# init rotary (polling)
r = utils.rotary.Rotary(mcp.porta, clk_pin, dt_pin, sw_pin, cb)

# debug: print raw gpio and button changes so we can verify the switch
prev_raw = None
prev_sw = None
prev_value = None

while True:
	# raw = mcp.porta.gpio
	# sw = (raw >> sw_pin) & 1
	# if raw != prev_raw:
	# 	print('mcp raw gpio: {:016b} ({})'.format(raw, raw))
	# 	prev_raw = raw
	# if sw != prev_sw:
	# 	print('button raw state changed -> {}'.format(sw))
	# 	prev_sw = sw

	# call poll and watch for value changes from the Rotary callback
	r.poll()
	if r.value != prev_value:
		print('rotary value changed -> {}'.format(r.value))
		prev_value = r.value

	# faster polling for encoder responsiveness
	time.sleep_ms(2)