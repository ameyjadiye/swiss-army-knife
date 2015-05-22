#!/usr/bin/python

from random import choice
import string

def get_shit(length=32, chars=string.letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


for i in range(1,10):
	print get_shit()
