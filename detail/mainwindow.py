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
import pyperclip

from detail import passworddialog
from detail import userdetail

class MainWindow(QMainWindow):
	WINDOW_TITLE = "FreePasswordManager v.1.00 [%s]"
	
	def __init__(self):
		super().__init__()
		super().setMinimumSize(400, 300)
		self.setWindowTitle(self.WINDOW_TITLE % "Untitled")
		
		# Fix from: https://stackoverflow.com/questions/27131294/error-qobjectstarttimer-qtimer-can-only-be-used-with-threads-started-with-qt
		self.setAttribute(Qt.WA_DeleteOnClose) 
		
		self.__mUserList = userdetail.UserDetailList()
		self.__mFilename = ""
		self.__mSelectedItem = -1
		self.__mSelectedTabIndex = -1
		self.__mModified = False

		# Create file menu item
		self.__mFileNew = QAction(self.tr("New"))
		self.__mFileOpen = QAction(self.tr("Open..."))
		self.__mFileSave = QAction(self.tr("Save"))
		self.__mFileSaveAs = QAction(self.tr("Save As..."))
		self.__mFileClose = QAction(self.tr("Close"))
		self.__mFileExit = QAction(self.tr("Exit"))

		# Create edit menu item
		self.__mEditNewCategory = QAction(self.tr("New Category..."))
		self.__mEditNewPassword = QAction(self.tr("New Password..."))
		self.__mEditRemovePassword = QAction(self.tr("Remove Password"))
		self.__mEditModifyPassword = QAction(self.tr("Modify Password..."))

		# Create option menu item
		self.__mOptionsChangeMasterPassword = QAction(self.tr("Change Master Password..."))

		# Create help menu item
		self.__mHelpAbout = QAction(self.tr("About..."))
				
		# Create the menus
		fileMenu = self.menuBar().addMenu(self.tr("&File"))
		editMenu = self.menuBar().addMenu(self.tr("&Edit"))
		optionsMenu = self.menuBar().addMenu(self.tr("&Option"))
		helpMenu = self.menuBar().addMenu(self.tr("&Help"))

		# Add file menus
		fileMenu.addAction(self.__mFileNew)
		fileMenu.addSeparator()
		fileMenu.addAction(self.__mFileOpen)
		fileMenu.addAction(self.__mFileSave)
		fileMenu.addAction(self.__mFileSaveAs)
		fileMenu.addSeparator()
		fileMenu.addAction(self.__mFileClose)
		fileMenu.addSeparator()
		fileMenu.addAction(self.__mFileExit)

		# Add edit menus
		editMenu.addAction(self.__mEditNewCategory)
		editMenu.addSeparator()
		editMenu.addAction(self.__mEditNewPassword)
		editMenu.addAction(self.__mEditRemovePassword)
		editMenu.addAction(self.__mEditModifyPassword)

		# Add option menus
		optionsMenu.addAction(self.__mOptionsChangeMasterPassword)

		# Add help menus
		helpMenu.addAction(self.__mHelpAbout)
				
		# Add the tab
		self.__mTabBar = QTabWidget(self)
		self.__mTabBar.tabBar().setExpanding(False)
		self.__mTabBar.tabBarClicked.connect(self.__tabSelectionChanged)
		self.__mTabBar.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
		self.__mTabBar.tabBar().customContextMenuRequested.connect(self.__tabContextRequested)
		self.setCentralWidget(self.__mTabBar)

		# Connect slots
		self.__mFileNew.triggered.connect(self.__newAction)
		self.__mFileOpen.triggered.connect(self.__openAction)
		self.__mFileSave.triggered.connect(self.__saveAction)
		self.__mFileSaveAs.triggered.connect(self.__saveAsAction)
		self.__mFileClose.triggered.connect(self.__closeAction)
		self.__mFileExit.triggered.connect(self.__exitAction)
		
		self.__mEditNewCategory.triggered.connect(self.__newCategoryAction)
		self.__mEditNewPassword.triggered.connect(self.__newPasswordAction)
		self.__mEditRemovePassword.triggered.connect(self.__removePasswordAction)
		self.__mEditModifyPassword.triggered.connect(self.__modifyPasswordAction)
		
		self.__mOptionsChangeMasterPassword.triggered.connect(self.__changeMasterPasswordAction)
		
		self.__mHelpAbout.triggered.connect(self.__aboutAction)
		
		# Disable actions
		self.__mOptionsChangeMasterPassword.setEnabled(False)
		self.__disableCreationActions()
		self.__disablePasswordModifierActions()
		
	def __newAction(self):
		if self.__mModified:
			result = QMessageBox.warning(self, self.tr("Warning"), self.tr("The file has been modifed, do you want to save it?"), QMessageBox.Yes | QMessageBox.No)
			if result == QMessageBox.Yes:
				self.__saveAction()
			
		self.__closeAction()
		
	def __openAction(self):
		filenameTuple = QFileDialog.getOpenFileName(self, "Open Password Container File...", "", self.tr("FreePasswordManager Container Files (*.fpc)"))
		if len(filenameTuple[0]) > 0:
			header = self.__mUserList.loadHeaderFromFile(filenameTuple[0])
			if header == None:
				QMessageBox.warning(self, self.tr("Warning"), self.tr("Invalid PAC file!"))
			else:
				if header.encrypted():
					tries = 0
					finished = False
					opened = False
					
					while tries < 3 and not finished:
						passphrase = QInputDialog.getText(self, self.tr("Password Input"), self.tr("Enter master password:"), QLineEdit.Password)
						
						if passphrase[1]:
							if len(passphrase[0]) > 0:
								self.__mUserList.setMasterKey(passphrase[0])
								
								result = self.__mUserList.loadFromFile(filenameTuple[0])
								print(result)
								if result == -1:
									tries += 1
								elif result == -2:
									finished = True
								elif result == 0:
									finished = True
									opened = True
								else:
									finished = True
							else:
								tries += 1
					
					if finished:
						if not opened:
							QMessageBox.warning(self, self.tr("Warning"), self.tr("Cannot open file \"" + filenameTuple[0] + "\"!"))
						else:
							self.__mFilename = filenameTuple[0]
							self.setWindowTitle(self.WINDOW_TITLE % filenameTuple[0])
							self.__enableCreationActions()
							self.__updateList()
							self.__mOptionsChangeMasterPassword.setEnabled(True)
					else:
						QMessageBox.warning(self, self.tr("warning"), self.tr("Reached the limit of password tries"))
				else:
					if self.__mUserList.loadFromFile(filenameTuple[0]) == 0:					
						self.__mFilename = filenameTuple[0]
						self.setWindowTitle(self.WINDOW_TITLE % filenameTuple[0])
						self.__enableCreationActions()
						self.__updateList()
						self.__mOptionsChangeMasterPassword.setEnabled(True)
					else:
						QMessageBox.warning(self, self.tr("Warning"), self.tr("Cannot open file \"" + filenameTuple[0] + "\"!"))
	def __saveAction(self):
		if len(self.__mFilename) > 0:
			if not self.__mUserList.saveToFile(self.__mFilename):
				QMessageBox.warning(self, self.tr("Warning"), self.tr("Cannot save to file \"" + self.__mFilename + "\"!"))
			else:
				self.__mModified = False
				self.__mFileSave.setEnabled(False)
		else:
			self.__saveAsAction()
						
	def __saveAsAction(self):
		filenameTuple = QFileDialog.getSaveFileName(self, self.tr("Save Password Container File..."), "", self.tr("FreePasswordManager Container Files (*.fpc)"))
		if len(filenameTuple[0]) > 0:
			self.__tryAddPassword(True)
			
			if not self.__mUserList.saveToFile(filenameTuple[0]):
				QMessageBox.warning(self, self.tr("Warning"), self.tr("Cannot save to file \"" + filenameTuple[0] + "\"!"))
			else:
				self.__mFilename = filenameTuple[0]
				self.setWindowTitle(self.WINDOW_TITLE % filenameTuple[0])
				self.__mModified = False
				self.__mFileSave.setEnabled(False)
				self.__mOptionsChangeMasterPassword.setEnabled(True)
				
	def __closeAction(self):
		self.__mModified = False
		self.__mFilename = ""
		self.__mUserList.clear()
		self.__mTabBar.clear()
		
		self.__mOptionsChangeMasterPassword.setEnabled(False)
		self.__disableCreationActions()
		self.__disablePasswordModifierActions()
		
	def __exitAction(self):
		if self.__mModified or (self.__mFilename == "" and len(self.__mUserList.getCategoryList()) > 0):
			result = QMessageBox.warning(self, self.tr("Warning"), self.tr("The file has been modified. Save before exit?"), QMessageBox.Ok | QMessageBox.No)
			if result == QMessageBox.Ok:
				self.__saveAction()
			
		self.close()
		
	def __newCategoryAction(self):
		categoryTuple = QInputDialog.getText(self, self.tr("Text Input"), self.tr("Enter the name of the new category:"))
		
		if categoryTuple[1] and len(categoryTuple[0]):
			if self.__mUserList.addCategory(categoryTuple[0]):
				self.__updateList()
				self.__enableCreationActions()
				self.__mModified = True
				self.__mFileSave.setEnabled(True)
				
	def __renameCategoryAction(self):
		if self.__mSelectedTabIndex >= 0:
			categoryTuple = QInputDialog.getText(self, self.tr("New Category"), self.tr("Enter the new category name:"))
			
			if categoryTuple[1] and len(categoryTuple[0]):
				if self.__mUserList.modifyCategory(self.__mSelectedTabIndex, categoryTuple[0]):
					self.__updateList()
				
			self.__mSelectedTabIndex = -1
			
	def __removeCategoryAction(self):
		if self.__mSelectedTabIndex >= 0:
			result = QMessageBox.warning(self, self.tr("Warning"), self.tr("Removing a category will remove all the saved username / password in that category. Continue?"), QMessageBox.Ok | QMessageBox.Cancel)
			if result == QMessageBox.Ok:
				self.__mUserList.removeCategory(self.__mSelectedTabIndex)
				self.__mSelectedTabIndex = -1
				self.__updateList()
				
				if len(self.__mUserList.getCategoryList()) == 0:
					self.__disableCreationActions()
			
	def __newPasswordAction(self):		
		passwordDialog = passworddialog.PasswordDialog("New Password", "", "")
		result = passwordDialog.exec_()
		
		if result == QDialog.Accepted:
			if len(passwordDialog.getUsername()) > 0 and len(passwordDialog.getPassword()):		
				self.__mUserList.addUser(self.__mTabBar.currentIndex(), passwordDialog.getUsername(), passwordDialog.getPassword())
				self.__updateList()
				self.__mModified = True
				self.__mFileSave.setEnabled(True)
			else:
				QMessageBox.warning(self, "Warning", "There was an unknown error")
			
	def __removePasswordAction(self):
		if self.__mSelectedItem >= 0:
			if QMessageBox.warning(self, self.tr("Warning"), self.tr("This will delete the username / password pair, continue?"), QMessageBox.Ok | QMessageBox.Cancel) == QMessageBox.Ok:
				self.__mUserList.removeUser(self.__mTabBar.currentIndex(), self.__mSelectedItem)
				self.__updateList()
				self.__mModified = True
				self.__mFileSave.setEnabled(True)
				
				for i in range(self.__mTabBar.count()):
					self.__mTabBar.widget(i).selectionModel().clearSelection()
				
	def __modifyPasswordAction(self):
		if self.__mSelectedItem >= 0:
			userDetail = self.__mUserList.getUserListInCategory(self.__mTabBar.currentIndex())[self.__mSelectedItem]
			passwordDialog = passworddialog.PasswordDialog("New Password", userDetail.getUsername(), userDetail.getPassword())
			result = passwordDialog.exec_()
			
			if result == QDialog.Accepted:
				if len(passwordDialog.getUsername()) > 0 and len(passwordDialog.getPassword()):		
					self.__mUserList.modifyUser(self.__mTabBar.currentIndex(), self.__mSelectedItem, passwordDialog.getUsername(), passwordDialog.getPassword())
					self.__updateList()
					self.__mModified = True
					self.__mFileSave.setEnabled(True)
				else:
					QMessageBox.warning(self, "Warning", "There was an unknown error")
					
	def __changeMasterPasswordAction(self):
		self.__tryAddPassword(False)
		
	def __aboutAction(self):
		QMessageBox.about(self, "About", "<center><img src=\"icon.png\"><br /><br /><font size=4>FreePasswordManager v.1.00</font><br /><font size=3>by Marvin Manese</font><br><br><font size=2>Copyright (c) 2019</font></center>")
	
	def __copyUsernameAction(self):
		if self.__mTabBar.currentIndex() >= 0 and self.__mSelectedItem >= 0:
			pyperclip.copy(self.__mUserList.getUserListInCategory(self.__mTabBar.currentIndex())[self.__mSelectedItem].getUsername())
			QMessageBox.information(self, self.tr("Information"), self.tr("Copied username to clipboard"))
			
	def __copyPasswordAction(self):
		if self.__mTabBar.currentIndex() >= 0 and self.__mSelectedItem >= 0:
			pyperclip.copy(self.__mUserList.getUserListInCategory(self.__mTabBar.currentIndex())[self.__mSelectedItem].getPassword())
			QMessageBox.information(self, self.tr("Information"), self.tr("Copied password to clipboard"))
		
	def __enableCreationActions(self):
		self.__mFileSaveAs.setEnabled(True)
		self.__mFileClose.setEnabled(True)
		
		if len(self.__mUserList.getCategoryList()) > 0:
			self.__mEditNewPassword.setEnabled(True)
			
	def __disableCreationActions(self):
		self.__mFileSave.setEnabled(False)
		self.__mFileSaveAs.setEnabled(False)
		self.__mFileClose.setEnabled(False)
		self.__mEditNewPassword.setEnabled(False)
		
	def __enablePasswordModifierActions(self):
		self.__mEditRemovePassword.setEnabled(True)
		self.__mEditModifyPassword.setEnabled(True)
		
	def __disablePasswordModifierActions(self):
		self.__mEditRemovePassword.setEnabled(False)
		self.__mEditModifyPassword.setEnabled(False)
		
	def __treeViewSelectionChanged(self, newSelected, oldSelected):
		if newSelected != None and len(newSelected.indexes()) > 0:
			self.__mSelectedItem = newSelected.indexes()[0].data(Qt.UserRole)
			self.__enablePasswordModifierActions()
			
	def __tabSelectionChanged(self, index):
		for i in range(self.__mTabBar.count()):
			self.__mTabBar.widget(i).selectionModel().clearSelection()
		self.__disablePasswordModifierActions()
		
	def __tabContextRequested(self, mousePosition):
		for i in range(self.__mTabBar.tabBar().count()):
			if self.__mTabBar.tabBar().tabRect(i).contains(mousePosition):
				self.__mSelectedTabIndex = i
				contextMenu = QMenu()
				renameAction = contextMenu.addAction(self.tr("Rename Category"))
				removeAction = contextMenu.addAction(self.tr("Remove Category"))
				
				renameAction.triggered.connect(self.__renameCategoryAction)
				removeAction.triggered.connect(self.__removeCategoryAction)
				
				contextMenu.exec_(self.__mTabBar.tabBar().mapToGlobal(mousePosition))
				
	def __treeContextRequested(self, mousePosition):
		if len(self.__mUserList.getUserListInCategory(self.__mTabBar.currentIndex())) >= 0 and self.__mSelectedItem >= 0:
			contextMenu = QMenu()
			renameAction = contextMenu.addAction(self.tr("Modify Password"))
			removeAction = contextMenu.addAction(self.tr("Remove Password"))
			copyUsernameAction = contextMenu.addAction(self.tr("Copy Username to clipboard"))
			copyPasswordAction = contextMenu.addAction(self.tr("Copy Password to clipboard"))
			
			renameAction.triggered.connect(self.__modifyPasswordAction)
			removeAction.triggered.connect(self.__removePasswordAction)
			copyUsernameAction.triggered.connect(self.__copyUsernameAction)
			copyPasswordAction.triggered.connect(self.__copyPasswordAction)
			
			contextMenu.exec_(self.__mTabBar.tabBar().mapToGlobal(mousePosition))
			
	def __tryAddPassword(self, optional):
		if optional:
			done = False
			while not done:
				passwordTuple = QInputDialog.getText(self, self.tr("Password Input"), self.tr("Enter a master password (leave blank if you don't want a password):"), QLineEdit.Password)
				
				if passwordTuple[1] and len(passwordTuple[0]):
					repeatPasswordTuple = QInputDialog.getText(self, self.tr("Password Input"), self.tr("Re-enter master password:"), QLineEdit.Password)
					
					if repeatPasswordTuple[1] and len(repeatPasswordTuple[0]) and repeatPasswordTuple[0] == passwordTuple[0]:
						self.__mUserList.setMasterKey(passwordTuple[0])
						done = True
				else:
					done = True
		else:
			done = False
			while not done:
				passwordTuple = QInputDialog.getText(self, self.tr("Password Input"), self.tr("Enter a master password:"), QLineEdit.Password)
				
				if passwordTuple[1]:
					if len(passwordTuple[0]):
						repeatPasswordTuple = QInputDialog.getText(self, self.tr("Password Input"), self.tr("Re-enter master password:"), QLineEdit.Password)
						
						if repeatPasswordTuple[1] and len(repeatPasswordTuple[0]) and repeatPasswordTuple[0] == passwordTuple[0]:
							self.__mUserList.setMasterKey(passwordTuple[0])
							done = True
				else:
					done = True
				
	def __updateList(self):
		self.__mTabBar.clear()
		userList = []
								
		for i in range(len(self.__mUserList.getCategoryList())):
			standardItemModel = QStandardItemModel(len(self.__mUserList.getUserListInCategory(i)), 2)
			standardItemModel.setHorizontalHeaderLabels(["Username", "Password"])
			
			for j in range(len(self.__mUserList.getUserListInCategory(i))):
				userDetail = self.__mUserList.getUserListInCategory(i)[j]

				itemFlag = 0
				itemFlag |= Qt.ItemIsSelectable
				itemFlag |= Qt.ItemIsEnabled
				
				usernameItem = QStandardItem(userDetail.getUsername())
				passwordItem = QStandardItem(str('*') * len(userDetail.getPassword()))
				
				usernameItem.setData(QVariant(j), Qt.UserRole)
				passwordItem.setData(QVariant(j), Qt.UserRole)
				
				usernameItem.setFlags(itemFlag)
				passwordItem.setFlags(itemFlag)
				
				standardItemModel.setItem(j, 0, usernameItem)
				standardItemModel.setItem(j, 1, passwordItem)
				
			treeView = QTreeView(self.__mTabBar)
			treeView.setModel(standardItemModel)
			treeView.selectionModel().selectionChanged.connect(self.__treeViewSelectionChanged)
			treeView.setContextMenuPolicy(Qt.CustomContextMenu)
			treeView.customContextMenuRequested.connect(self.__treeContextRequested)
			self.__mTabBar.addTab(treeView, self.__mUserList.getCategoryList()[i])
