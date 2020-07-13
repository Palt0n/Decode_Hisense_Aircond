#!/usr/bin/env python3

import io
import sys
import os

while True:
	a = sys.stdin.readline().rstrip("\n\r")
	if not a:
		break

	first_space = True
	n = 0

	print ("    name", a)

	for line in os.popen('timeout 5s mode2 -d /dev/lirc0 2> /dev/null').read().split('\n'):
		words = line.split()
		if len(words) < 2:
			continue

		if words[0] != 'space' and words[0] != 'pulse':
			continue
		if first_space and words[0] == 'space':
			first_space = False
			continue

		if n % 4 == 0:
			print()
			print("        ", end = '')

		print (words[1], "  ", end = '')
		n = n+1

	print()
	print()