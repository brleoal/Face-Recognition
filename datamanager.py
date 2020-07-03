""" 
    Facial recognition system database manager
    Author: Bruno Alonso Leon Alata
    Date: Mar 07 2020
    Email: b.leonalata@protonmail.com

    This program is free software: you can redistribute it and/or modify
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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QLineEdit
from PyQt5 import uic
import manage_database as db

class NewUser(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('newuser.ui', self)
        self.trainData = ''
        self.userPhoto = ''
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.pushButton.clicked.connect(self.browseTrain)
        self.pushButton_2.clicked.connect(self.loadPhoto)
        self.pushButton_3.clicked.connect(self.addUser)
        self.pushButton_4.clicked.connect(self.cancelAdd)

    def browseTrain(self):
        fname = QFileDialog.getOpenFileName(self, 'Load file', '', 'Facemark training model (*.yml)')
        if fname[0]:
            self.trainData = fname[0]
            self.label_5.setText(self.trainData)

    def loadPhoto(self):
        fname = QFileDialog.getOpenFileName(self, 'Load image', '', 'Images (*.png *.jpg)')
        if fname[0]:
            self.userPhoto = fname[0]
            with open(self.userPhoto, 'rb') as f:
                userPhoto = f.read()
            qimg = QtGui.QImage.fromData(userPhoto)
            pixmap = QtGui.QPixmap(self.userPhoto)
            gfxPixItem = self.scene.addPixmap(pixmap)
            self.graphicsView.fitInView(gfxPixItem)

    def addUser(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        retypepwd = self.lineEdit_3.text()
        alert = QMessageBox()
        if username and password and self.trainData and self.userPhoto:
            if password == retypepwd:
                newID = db.getLastID() + 1
                db.insertData(newID, username, password, self.userPhoto, self.trainData)
                alert.setIcon(QMessageBox.Information)
                alert.setText('Your account has been created')
                alert.setWindowTitle('Add New User')
                self.close()
            else:
                alert.setIcon(QMessageBox.Critical)
                alert.setText('Password fields must match')
                alert.setWindowTitle('Validation Error')
        else:
            alert.setIcon(QMessageBox.Critical)
            alert.setText('Please all the required fields')
            alert.setWindowTitle('Validation Error')
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()

    def cancelAdd(self):
        self.close()

class ChangePwd(QtWidgets.QWidget):

    updatePwd = pyqtSignal(str)

    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('changepassword.ui', self)
        self.user = username
        self.pushButton.clicked.connect(self.checkPwd)
        self.pushButton_2.clicked.connect(self.cancelPwd)

    def checkPwd(self):
        oldPwd = self.lineEdit.text()
        newPwd = self.lineEdit_2.text()
        retPwd = self.lineEdit_3.text()
        alert = QMessageBox()
        if oldPwd and newPwd:
            if newPwd == retPwd:
                db.updateData(param=0, username=self.user, passwd=newPwd, photo=None)
                alert.setIcon(QMessageBox.Information)
                alert.setText('Password has been changed')
                alert.setWindowTitle('Change Password')
                alert.setStandardButtons(QMessageBox.Ok)
                retval = alert.exec_()
                if retval == QMessageBox.Ok:
                    self.updatePwd.emit(newPwd)
            else:
                alert = QMessageBox()
                alert.setIcon(QMessageBox.Critical)
                alert.setText('Password fields must match')
                alert.setWindowTitle('Validation Error')
                alert.setStandardButtons(QMessageBox.Ok)
                alert.exec_()
        else:
            alert.setIcon(QMessageBox.Critical)
            alert.setText('Please all the required fields')
            alert.setWindowTitle('Validation Error')
            alert.setStandardButtons(QMessageBox.Ok)
            alert.exec_()

    def cancelPwd(self):
        self.close()

class ChangePhoto(QtWidgets.QWidget):

    updateImg = pyqtSignal(str)

    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi('changephoto.ui', self)
        self.user = username
        self.userPhoto = ''
        self.pushButton.clicked.connect(self.browsePhoto)
        self.pushButton_2.clicked.connect(self.updatePhoto)
        self.pushButton_3.clicked.connect(self.cancelPhoto)

    def browsePhoto(self):
        fname = QFileDialog.getOpenFileName(self, 'Load image', '', 'Images (*.png *.jpg)')
        if fname[0]:
            self.userPhoto = fname[0]
            self.label_2.setText(self.userPhoto)

    def updatePhoto(self, user):
        alert = QMessageBox()
        if self.userPhoto:
            db.updateData(param=1, username=self.user, passwd=None, photo=self.userPhoto)
            alert.setIcon(QMessageBox.Information)
            alert.setText('User photo has been changed')
            alert.setWindowTitle('Change User Photo')
            alert.setStandardButtons(QMessageBox.Ok)
            retval = alert.exec_()
            if retval == QMessageBox.Ok:
                self.updateImg.emit(self.userPhoto)
        else:
            alert.setIcon(QMessageBox.Critical)
            alert.setText('Please select a photo')
            alert.setWindowTitle('Validation Error')
            alert.setStandardButtons(QMessageBox.Ok)
            alert.exec_()

    def cancelPhoto(self):
        self.close()

class DatabaseManager(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi('databasemanager.ui', self)
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.pushButton.clicked.connect(self.searchbyItem)
        self.pushButton_2.clicked.connect(self.changePassword)
        self.pushButton_3.clicked.connect(self.updatePhoto)
        self.pushButton_4.clicked.connect(self.addUser)
        self.pushButton_5.clicked.connect(self.deleteUser)
        self.pushButton_6.clicked.connect(self.closeManager)

    def searchbyItem(self):
        auth, okPressed = QInputDialog.getText(self, 'Authentication Required',
                                               'Password:', QLineEdit.Password, '')
        if auth and okPressed:
            if self.radioButton.isChecked():
                userID = self.lineEdit_4.text()
                record = db.getData(param=0, id=userID, user=None, passwd=auth)
            elif self.radioButton_2.isChecked():
                username = self.lineEdit_5.text()
                record = db.getData(param=1, id=None, user=username, passwd=auth)
            if record is not None:
                self.lineEdit.setText(str(record[0]))
                self.lineEdit_2.setText(record[1])
                self.lineEdit_3.setText(record[2])
                photo = record[3]
                qimg = QtGui.QImage.fromData(photo)
                pixmap = QtGui.QPixmap.fromImage(qimg)
                gfxPixItem = self.scene.addPixmap(pixmap)
                self.graphicsView.fitInView(gfxPixItem)
            else:
                alert = QMessageBox()
                alert.setIcon(QMessageBox.Critical)
                alert.setText('Inserted data are incorrect. Try again.')
                alert.setWindowTitle('Login Failed')
                alert.setStandardButtons(QMessageBox.Ok)
                alert.exec_()
        else:
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Critical)
            alert.setText('Invalid password')
            alert.setWindowTitle('Login Failed')
            alert.setStandardButtons(QMessageBox.Ok)
            alert.exec_()

    @pyqtSlot(str)
    def refreshPwd(self, auth):
        if self.radioButton.isChecked():
            userID = self.lineEdit_4.text()
            record = db.getData(param=0, id=userID, user=None, passwd=auth)
        elif self.radioButton_2.isChecked():
            username = self.lineEdit_5.text()
            record = db.getData(param=1, id=None, user=username, passwd=auth)
        self.lineEdit_3.setText(record[2])
        self.chpwd.close()

    @pyqtSlot(str)
    def refreshPhoto(self, photo):
        with open(photo, 'rb') as f:
            userPhoto = f.read()
        qimg = QtGui.QImage.fromData(userPhoto)
        pixmap = QtGui.QPixmap.fromImage(qimg)
        gfxPixItem = self.scene.addPixmap(pixmap)
        self.graphicsView.fitInView(gfxPixItem)
        self.chphoto.close()

    def changePassword(self):
        self.chpwd = ChangePwd(self.lineEdit_2.text())
        self.chpwd.updatePwd.connect(self.refreshPwd)
        self.chpwd.show()

    def updatePhoto(self):
        self.chphoto = ChangePhoto(self.lineEdit_2.text())
        self.chphoto.updateImg.connect(self.refreshPhoto)
        self.chphoto.show()

    def addUser(self):
        self.newusr = NewUser()
        self.newusr.show()

    def deleteUser(self):
        alert = QMessageBox()
        alert.setIcon(QMessageBox.Question)
        alert.setText('Are you sure to remove this user from database?')
        alert.setWindowTitle('Remove User')
        alert.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = alert.exec_()
        if retval == QMessageBox.Ok:
            db.deleteData(self.lineEdit_2.text())
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.scene.clear()
        elif retval == QMessageBox.Cancel:
            alert.close()

    def closeManager(self):
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DatabaseManager()
    window.show()
    sys.exit(app.exec_())
