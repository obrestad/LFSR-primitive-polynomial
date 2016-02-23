#!/usr/bin/python3

import sys

from polynomial import Polynomial
from ast import literal_eval

if(len(sys.argv) < 2):
	print("Usage: %s <input_file>" % sys.argv[0])
	sys.exit(1)

try:
	f = open(sys.argv[1], 'r')
except IOError as e:
	print("Could not open file")
	print(e)
	sys.exit(2)

polynomials=literal_eval(f.read())

least = None

for p in polynomials:
	if(not least):
		least = p
	if(bin(int(p)).count('1') < bin(int(least)).count('1')):
		least = p

print(int(least), Polynomial(int(least)))
