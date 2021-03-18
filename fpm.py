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
from PyQt5.QtWidgets import *
import detail.mainwindow
import sys

def main():
	app = QApplication([])
	
	mainWindow = detail.mainwindow.MainWindow()
	if len(sys.argv) == 2:
		mainWindow.openPAC(sys.argv[1])
	mainWindow.show()

	app.exec_()

if __name__ == "__main__":
    main()
