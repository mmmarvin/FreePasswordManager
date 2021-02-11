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
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from detail import password_generator

class PasswordDialog(QDialog):
	def __init__(self, title, username, password):
		super().__init__()
		self.setWindowTitle(title)
		
		self.__mUsername = ""
		self.__mPassword = ""
		
		self.__mLayout = QGridLayout(self)
		fieldLayout = QGridLayout()
		self.__mLayout.addLayout(fieldLayout, 0, 0, 1, 1)
		
		self.__mUsernameLabel = QLabel(self.tr("Username: "), self)
		self.__mPasswordLabel = QLabel(self.tr("Password: "), self)
		self.__mRepeatPasswordLabel = QLabel(self.tr("Repeat Password: "), self)
		self.__mUsernameText = QLineEdit(username, self)
		self.__mPasswordText = QLineEdit(password, self)
		self.__mRepeatPasswordText = QLineEdit(password, self)
		
		self.__mPasswordText.setEchoMode(QLineEdit.Password)
		self.__mRepeatPasswordText.setEchoMode(QLineEdit.Password)
		
		self.__mOkButton = QPushButton(self.tr("Ok"), self)
		self.__mOkButton.setEnabled(False)
		self.__mCancelButton = QPushButton(self.tr("Cancel"), self)
		self.__mRandomPasswordButton = QPushButton(self.tr("Generate Random Password"), self)
		
		self.__mUsernameText.setFixedHeight(max(self.__mUsernameText.font().pixelSize(), self.__mUsernameText.font().pointSize() * 3))
		self.__mPasswordText.setFixedHeight(max(self.__mPasswordText.font().pixelSize(), self.__mPasswordText.font().pointSize() * 3))
		self.__mRepeatPasswordText.setFixedHeight(max(self.__mPasswordText.font().pixelSize(), self.__mPasswordText.font().pointSize() * 3))
		
		fieldLayout.addWidget(self.__mUsernameLabel, 0, 0, 1, 1)
		fieldLayout.addWidget(self.__mUsernameText, 0, 1, 1, 1)
		fieldLayout.addWidget(self.__mPasswordLabel, 1, 0, 1, 1)
		fieldLayout.addWidget(self.__mPasswordText, 1, 1, 1, 1)
		fieldLayout.addWidget(self.__mRepeatPasswordLabel, 2, 0, 1, 1)
		fieldLayout.addWidget(self.__mRepeatPasswordText, 2, 1, 1, 1)
		
		buttonLayout = QGridLayout()
		buttonLayout.addWidget(self.__mOkButton, 0, 0, 1, 1)
		buttonLayout.addWidget(self.__mCancelButton, 0, 1, 1, 1)
		buttonLayout.addWidget(self.__mRandomPasswordButton, 0, 2, 1, 1)
		self.__mLayout.addLayout(buttonLayout, 1, 0, 1, 1)
		
		self.__mOkButton.clicked.connect(self.__okAction)
		self.__mCancelButton.clicked.connect(self.__cancelAction)
		self.__mRandomPasswordButton.clicked.connect(self.__generateRandomPasswordAction)
		self.__mUsernameText.textChanged.connect(self.__textChangedAction)
		self.__mPasswordText.textChanged.connect(self.__textChangedAction)
		self.__mRepeatPasswordText.textChanged.connect(self.__textChangedAction)
		
	def getUsername(self):
		return self.__mUsername
		
	def getPassword(self):
		return self.__mPassword
		
	def __okAction(self):
		username = self.__mUsernameText.text()
		password = self.__mPasswordText.text()
		repeatPassword = self.__mRepeatPasswordText.text()
		if len(username) > 0 and len(password) > 0 and password == repeatPassword:		
			self.__mUsername = username
			self.__mPassword = password
			self.accept()
		
	def __cancelAction(self):
		self.reject()
		
	def __generateRandomPasswordAction(self):
		passwordLength = QInputDialog.getInt(self, self.tr("Password Length"), self.tr("Enter the desired password length:"), 6, 6, 100)
		
		if passwordLength[1]:
			password = password_generator.generateRandomPassword(passwordLength[0])
			self.__mPasswordText.setText(password)
			self.__mRepeatPasswordText.setText(password)
		
	def __textChangedAction(self):
		username = self.__mUsernameText.text()
		password = self.__mPasswordText.text()
		repeatPassword = self.__mRepeatPasswordText.text()
		
		if len(username) > 0 and len(password) > 0 and password == repeatPassword:
			self.__mOkButton.setEnabled(True)
		else:
			self.__mOkButton.setEnabled(False)
