########
# This file is part of FreePasswordManager.
#
# FreePasswordManager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FreePasswordManager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
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
