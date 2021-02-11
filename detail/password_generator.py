########
# MIT License
#
# Copyright 2019 Marvin Manese
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
########
import os
import sys

def __generateRandomNumber():
	number = os.getrandom(32, flags=0)
	return int.from_bytes(number, byteorder = sys.byteorder)
	
def __generatePassword(passwordLength, dictionary):
	password = ""
	for i in range(passwordLength):
		index = __generateRandomNumber()
		index = index % len(dictionary)
		word = dictionary[index]		
		password += word
		
	return password

def generateRandomPassword(passwordLength):
	dictionary = []
	dictionary.append('a')
	dictionary.append('b')
	dictionary.append('c')
	dictionary.append('d')
	dictionary.append('e')
	dictionary.append('f')
	dictionary.append('g')
	dictionary.append('h')
	dictionary.append('i')
	dictionary.append('j')
	dictionary.append('k')
	dictionary.append('l')
	dictionary.append('m')
	dictionary.append('n')
	dictionary.append('o')
	dictionary.append('p')
	dictionary.append('q')
	dictionary.append('r')
	dictionary.append('s')
	dictionary.append('t')
	dictionary.append('u')
	dictionary.append('v')
	dictionary.append('w')
	dictionary.append('x')
	dictionary.append('y')
	dictionary.append('z')
	dictionary.append('A')
	dictionary.append('B')
	dictionary.append('C')
	dictionary.append('D')
	dictionary.append('E')
	dictionary.append('F')
	dictionary.append('G')
	dictionary.append('H')
	dictionary.append('I')
	dictionary.append('J')
	dictionary.append('K')
	dictionary.append('L')
	dictionary.append('M')
	dictionary.append('N')
	dictionary.append('O')
	dictionary.append('P')
	dictionary.append('Q')
	dictionary.append('R')
	dictionary.append('S')
	dictionary.append('T')
	dictionary.append('U')
	dictionary.append('V')
	dictionary.append('W')
	dictionary.append('X')
	dictionary.append('Y')
	dictionary.append('Z')
	dictionary.append('1')
	dictionary.append('2')
	dictionary.append('3')
	dictionary.append('4')
	dictionary.append('5')
	dictionary.append('6')
	dictionary.append('7')
	dictionary.append('8')
	dictionary.append('9')
	dictionary.append('0')
	dictionary.append('!')
	dictionary.append('@')
	dictionary.append('#')
	dictionary.append('$')
	dictionary.append('%')
	dictionary.append('^')
	dictionary.append('&')
	dictionary.append('*')
	dictionary.append('(')
	dictionary.append(')')
	dictionary.append('[')
	dictionary.append(']')
	dictionary.append('{')
	dictionary.append('}')
	dictionary.append(';')
	dictionary.append(':')
	dictionary.append('\'')
	dictionary.append('\"')
	dictionary.append(',')
	dictionary.append('<')
	dictionary.append('.')
	dictionary.append('>')
	dictionary.append('/')
	dictionary.append('?')
	dictionary.append('~')
	dictionary.append('\\')
	dictionary.append('|')
	dictionary.append('-')
	dictionary.append('_')
	dictionary.append('+')
	dictionary.append('=')
	
	return __generatePassword(passwordLength, dictionary)
