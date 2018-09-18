#!/usr/bin/python3
import sys
import os

#print(sys.argv)
if len(sys.argv) < 2:
	print('not enought arguments')
	exit(0)

filepath = sys.argv[1]
data = open(filepath).read()

try:
    a = data.index('<div class=statements_info><table>')
except: 
    a = data.index('<div class="statements_info"><table>')
b = data.index('</table></div>') + len('</table></div>')
data = data[:a] + data[b:]

open(filepath, 'w').write(data)
