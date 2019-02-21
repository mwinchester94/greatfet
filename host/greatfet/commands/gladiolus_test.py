#!/usr/bin/env python
#
# This file is part of GreatFET

from __future__ import print_function

import inspect
import errno
import sys
import re

from greatfet import GreatFET
from greatfet.utils import GreatFETArgumentParser

import IPython

import time

def main():


	# Set up a simple argument parser.
	parser = GreatFETArgumentParser(
		description="Convenience shell for working with GreatFET devices.")
	parser.add_argument('-e', '--exec', metavar="code", type=str, help="Executes the provided code as though it were passed" +
			"to a greatfet shell, and then terminates.", dest="code")

	args = parser.parse_args()
	gf = parser.find_specified_device()

	# Handle any inline execution.
	if args.code:

		# Replace any ;'s with newlines, so we can execute more than one statement.
		code = re.sub(";\s*", "\n", args.code)
		lines = code.split("\n")

		# And execute the code.
		for line in lines:
			result = repr(eval(line))

		# Print the last result and return.
		print(result)
		sys.exit(0)


	# Break into IPython for the shell.
	#print("Spwaning an IPython shell for easy access to your GreatFET.")
	#print("Like normal python, you can use help(object) to get help for that object.")
	#print("Try help(gf.apis.example) to see the documentation for the example API.\n")
	#print("A GreatFET object has been created for you as 'gf'. Have fun!\n")
	#IPython.start_ipython(user_ns={"gf": gf}, display_banner=False, argv=[])


	#set up GPIO pins as outputs
	pin_clk = gf.gpio.get_pin('J1_P16')
	pin_sleep = gf.gpio.get_pin('J1_P8')
	#pin_cmode = gf.gpio.get_pin('J1_P14')
	#pin_mode = gf.gpio.get_pin('J1_P19')

	pin0 = gf.gpio.get_pin('J1_P15') #LSB
	pin1 = gf.gpio.get_pin('J1_P18')
	pin2 = gf.gpio.get_pin('J1_P17')
	pin3 = gf.gpio.get_pin('J1_P20')
	pin4 = gf.gpio.get_pin('J1_P22')
	pin5 = gf.gpio.get_pin('J1_P21')
	pin6 = gf.gpio.get_pin('J1_P26')
	pin7 = gf.gpio.get_pin('J1_P25') #MSB

	pin_clk.set_direction(1)
	pin_sleep.set_direction(1)
	#pin_cmode.set_direction(1)
	#pin_mode.set_direction(1)
	pin0.set_direction(1)
	pin1.set_direction(1)
	pin2.set_direction(1)
	pin3.set_direction(1)
	pin4.set_direction(1)
	pin5.set_direction(1)
	pin6.set_direction(1)
	pin7.set_direction(1)

	#initialize pins
	pin_sleep.write(0)
	pin_clk.write(0)
	#pin_cmode.write(0)
	#pin_mode.write(0)

	val = 0

	pin0.write(val)
	pin1.write(val)
	pin2.write(val)
	pin3.write(val)
	pin4.write(val)
	pin5.write(val)
	pin6.write(val)
	pin7.write(val)


	#clock pulse function
	def clock_pulse():
		pin_clk.write(0)
		#time.sleep(0.1)
		pin_clk.write(1)
		#time.sleep(0.1)
		pin_clk.write(0)

	def write_pin(pin, value):
		pin.write(value)

	#why do we need two clock pulses to get correct output? There can be a reset button between pulses and it stills works afterwards
	write_pin(pin7,0)
	clock_pulse()
	clock_pulse()


	while False:
		pin7.write(1)
		clock_pulse()
		time.sleep(2)
		pin7.write(0)
		clock_pulse()
		time.sleep(2)



if __name__ == '__main__':
	main()
