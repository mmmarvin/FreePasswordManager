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
# along with FreePasswordManager.  If not, see <https://www.gnu.org/licenses/>.
########
import json
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def _pad(binaryData):
	# From https://stackoverflow.com/questions/12562021/aes-decryption-padding-with-pkcs5-python
	return binaryData + ((algorithms.AES.block_size - len(binaryData) % algorithms.AES.block_size) * chr(algorithms.AES.block_size - len(binaryData) % algorithms.AES.block_size)).encode("utf-8")

def _unpad(binaryData):
	# From https://stackoverflow.com/questions/12562021/aes-decryption-padding-with-pkcs5-python
	return binaryData[0:-ord(binaryData[-1])]

def _decryptData(binaryData, key, iv):
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	decryptor = cipher.decryptor()
	
	decryptedData = decryptor.update(binaryData) + decryptor.finalize()
	return _unpad(decryptedData.decode("utf-8")).encode('utf-8')
	
def _saveUserFile(filename, encryptedData, key):
	try:
		with open(filename, "wb") as file:
			file.write(b"fpc")
			file.write(b"1")
			file.write(b"2")
			if key == b"":
				file.write(b"0")
			else:
				file.write(b"1")
			
			file.write(encryptedData)
	except:
		return False
		
	return True
		
def _encryptData(binaryData, key, iv):
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
	encryptor = cipher.encryptor()
	
	return encryptor.update(_pad(binaryData)) + encryptor.finalize()
	
class PasswordContainerHeader:
	def __init__(self, header0, header1, header2, isEncrypted):
		self.__mHeader0 = header0
		self.__mHeader1 = header1
		self.__mHeader2 = header2
		self.__mIsEncrypted = isEncrypted
		
	def header0(self):
		return self.__mHeader0
		
	def header1(self):
		return self.__mHeader1
		
	def header2(self):
		return self.__mHeader2
		
	def encrypted(self):
		return self.__mIsEncrypted

class UserDetail:
	def __init__(self, username, password):
		self.__mUsername = username
		self.__mPassword = password

	def getUsername(self):
		return self.__mUsername

	def getPassword(self):
		return self.__mPassword

class UserDetailList:
	SALT_DATA = b"\x2c\x00\x9c\xba\x2d\xe5\x44\x70\x89\xfe\x90\xa3\xb1\xcc\x32\xca"
	IDENT_DATA = b"fpc"
	
	def __init__(self):
		self.__mUserList = []
		self.__mKey = b""
		
	def loadHeaderFromFile(self, filename):
		try:
			with open(filename, "rb") as file:
				return self.__loadHeaderFromStream(file)
		except:
			pass
			
		return None
		
	def loadFromFile(self, filename):
		self.clear()
		return self.__loadFromFile(filename)
		
	def saveToFile(self, filename):
		return self.__saveToFile(filename)
		
	def setMasterKey(self, passphrase):
		bytePassphrase = b""
		if isinstance(passphrase, str):
			bytePassphrase = passphrase.encode("utf-8") 
		elif isinstance(passphrase, (bytes, bytearray)):
			bytePassphrase = passphrase
		else:
			raise RuntimeError("Key must be either a byte or a string")
			
		if len(passphrase) == 0 or len(passphrase) > 1024:
			raise RuntimeError("Key length must be 0 < and <= 1024")
		
		self.__mKey = hashlib.pbkdf2_hmac("sha256", bytePassphrase, self.SALT_DATA, 100000)
		
	def clear(self):
		while len(self.__mUserList) > 0:
			self.__mUserList.pop(0)
		
	def addCategory(self, categoryName):
		if len(categoryName) > 0:
			self.__mUserList.append((categoryName, []))
			return True
			
		return False
		
	def removeCategory(self, categoryIndex):
		self.__mUserList.pop(categoryIndex)
		
	def modifyCategory(self, categoryIndex, categoryName):
		if len(categoryName) > 0:
			self.__mUserList[categoryIndex] = (categoryName, self.__mUserList[categoryIndex][1])
			return True
			
		return False
			
	def addUser(self, categoryIndex, username, password):
		if categoryIndex < len(self.__mUserList):
			self.__mUserList[categoryIndex][1].append(UserDetail(username, password))
			return True
			
		return False
		
	def removeUser(self, categoryIndex, userIndex):
		if categoryIndex < len(self.__mUserList):
			self.__mUserList[categoryIndex][1].pop(userIndex)
			return True
			
		return False
		
	def modifyUser(self, categoryIndex, userIndex, username, password):
		if categoryIndex < len(self.__mUserList):
			self.__mUserList[categoryIndex][1][userIndex] = UserDetail(username, password)
			return True
			
		return False
		
	def getCategoryList(self):
		ret = []
		for categoryTuple in self.__mUserList:
			ret.append(categoryTuple[0])
			
		return ret
		
	def getUserListInCategory(self, categoryIndex):
		ret = []
		if categoryIndex < len(self.__mUserList):
			for userDetail in self.__mUserList[categoryIndex][1]:
				ret.append(userDetail)
			
		return ret
		
	def __loadHeaderFromStream(self, file):
		try:
			header0 = file.read(3)
			header1 = file.read(1)
			header2 = file.read(1)
			encryptedBit = file.read(1)
			
			isEncrypted = False
			if encryptedBit == b"1":
				isEncrypted = True
			
			return PasswordContainerHeader(header0, header1, header2, isEncrypted)
		except:
			pass
			
		return None
		
	def __loadFromFile(self, filename):
		try:
			with open(filename, "rb") as file:
				header = self.__loadHeaderFromStream(file)
				if header == None:
					return -1
				if not header.header0() == b"fpc" or not header.header1() == b"1" or not header.header2() == b"2":
					return -1
				
				iv = file.read(16)
				if len(iv) != 16:
					return -1
								
				jsonBin = self.__loadData(header, file, iv)
				if len(jsonBin) > 0:
					if jsonBin[:3] == self.IDENT_DATA:
						jsonData = json.loads(jsonBin[3:].decode("utf-8"))
						if jsonData:
							return self.__loadUserData(jsonData)
					else:
						return -2
		except:
			return -1
			
		return -1
		
	def __loadData(self, header, file, iv):		
		if header.encrypted():
			jsonBin = _decryptData(file.read(), self.__mKey, iv)
			return jsonBin
			
		jsonBin = file.read()
		return jsonBin
		
	def __loadUserData(self, jsonData):
		try:			
			for category in jsonData["categories"]:
				self.addCategory(category)
				
			for userObject in jsonData["users"]:
				self.addUser(userObject["categoryIndex"], userObject["username"], userObject["password"])
		except:
			return -1
			
		return 0
		
	def __saveToFile(self, filename):
		jsonString = self.__generateJson()
		
		if len(self.__mUserList) > 0 and len(jsonString) == 0:
			return False
			
		data = self.IDENT_DATA + jsonString.encode("utf-8")
		return self.__saveData(filename, data)
		
	def __saveData(self, filename, data):
		iv = os.urandom(16)
		if self.__mKey == b"":
			return _saveUserFile(filename, iv + data, self.__mKey)
		
		return _saveUserFile(filename, iv + _encryptData(data, self.__mKey, iv), self.__mKey)
		
	def __generateJson(self):
		ret = "{\n"
		ret += "\t\"categories\": [\n"
		firstCategoryWritten = False
		for category in self.__mUserList:
			if firstCategoryWritten:
				ret += ",\n"
			ret += "\t\t\"" + category[0] + "\""
			firstCategoryWritten = True
		ret += "\n\t],\n"
		ret += "\t\"users\": [\n"
		firstUserWritten = False
		for i in range(len(self.__mUserList)):
			for user in self.__mUserList[i][1]:
				if firstUserWritten:
					ret += ",\n"
				ret += "\t\t{\n"
				ret += "\t\t\t\"categoryIndex\": " + str(i) + ",\n"
				ret += "\t\t\t\"username\": \"" + user.getUsername() + "\",\n"
				ret += "\t\t\t\"password\": \"" + user.getPassword() + "\"\n"
				ret += "\t\t}"
				firstUserWritten = True
		ret += "\n\t]\n"
		ret += "}"
		
		return ret
