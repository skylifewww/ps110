import sys
import re

def func(x):
	out = ""
	i = 0
	while i < x:
		r = 0
		while r < x:
			if r < i:
				out += (" ")
			else:
				out += ("#")
			r += 1
		i += 1
	return out[:-1]

  
print "(" + func(6) + ")"

def test_ourfunc():
	rgx = re.compile("##")
	assert rgx.match('(.*)'), func(3)
