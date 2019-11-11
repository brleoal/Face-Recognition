""" This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
import manage_database as db
import detector
import face_login as login

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi('facerecognition.ui', self)
        self.pushButton.clicked.connect(self.login)
        self.scene = QtWidgets.QGraphicsScene()
        
    def authError(self, username, password):
        if self.scene.isActive():
            self.scene.clear()
        self.label_3.clear()
        self.label_3.setStyleSheet("background-color: #FFFFFF;")
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Critical)
        if not username or not password:
            alert.setText('Invalid username or password')
        else:
            alert.setText('Incorrect username or password')
        alert.setWindowTitle("Login Failed")
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        auth = detector.faceRecognizer(username, password)
        if auth is not None:
            if auth < 50:
                record = db.getData(username, password)
                photo = record[3] 
                self.graphicsView.setScene(self.scene)
                qimg = QtGui.QImage.fromData(photo)
                pixmap = QtGui.QPixmap.fromImage(qimg)
                gfxPixItem = self.scene.addPixmap(pixmap)
                self.graphicsView.fitInView(gfxPixItem)                
                self.label_3.setText('MATCH {:.1f}%'.format(100.0-auth))
                self.label_3.setStyleSheet("color: #FFFFFF; background-color: #00FF00;")
                login.face_login()
            else:
                self.label_3.setText('NO MATCH')
                self.label_3.setStyleSheet("color: #FFFFFF; background-color: #FF0000;")
        else:
            self.authError(username, password)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
