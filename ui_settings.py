# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/settings.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(585, 282)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/mailbox_empty.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Settings.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(20, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.boolifNotify = QtWidgets.QCheckBox(Settings)
        self.boolifNotify.setGeometry(QtCore.QRect(21, 42, 231, 20))
        self.boolifNotify.setChecked(True)
        self.boolifNotify.setObjectName("boolifNotify")
        self.groupBox = QtWidgets.QGroupBox(Settings)
        self.groupBox.setGeometry(QtCore.QRect(20, 70, 541, 161))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.txtboxMailServer = QtWidgets.QLineEdit(self.groupBox)
        self.txtboxMailServer.setGeometry(QtCore.QRect(90, 30, 181, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtboxMailServer.sizePolicy().hasHeightForWidth())
        self.txtboxMailServer.setSizePolicy(sizePolicy)
        self.txtboxMailServer.setText("")
        self.txtboxMailServer.setObjectName("txtboxMailServer")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(310, 30, 31, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(40, 60, 41, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(280, 60, 61, 21))
        self.label_6.setObjectName("label_6")
        self.txtboxPassword = QtWidgets.QLineEdit(self.groupBox)
        self.txtboxPassword.setGeometry(QtCore.QRect(350, 60, 181, 22))
        self.txtboxPassword.setText("")
        self.txtboxPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtboxPassword.setPlaceholderText("")
        self.txtboxPassword.setObjectName("txtboxPassword")
        self.txtboxLogin = QtWidgets.QLineEdit(self.groupBox)
        self.txtboxLogin.setGeometry(QtCore.QRect(90, 60, 181, 22))
        self.txtboxLogin.setText("")
        self.txtboxLogin.setObjectName("txtboxLogin")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(11, 31, 71, 21))
        self.label_3.setObjectName("label_3")
        self.txtboxPort = QtWidgets.QLineEdit(self.groupBox)
        self.txtboxPort.setGeometry(QtCore.QRect(350, 30, 41, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtboxPort.sizePolicy().hasHeightForWidth())
        self.txtboxPort.setSizePolicy(sizePolicy)
        self.txtboxPort.setText("")
        self.txtboxPort.setObjectName("txtboxPort")
        self.boolifSSL = QtWidgets.QCheckBox(self.groupBox)
        self.boolifSSL.setGeometry(QtCore.QRect(10, 90, 161, 20))
        self.boolifSSL.setObjectName("boolifSSL")
        self.btnTestConnection = QtWidgets.QPushButton(self.groupBox)
        self.btnTestConnection.setEnabled(True)
        self.btnTestConnection.setGeometry(QtCore.QRect(10, 120, 121, 22))
        self.btnTestConnection.setToolTip("")
        self.btnTestConnection.setObjectName("btnTestConnection")
        self.lblTestOutput = QtWidgets.QLabel(self.groupBox)
        self.lblTestOutput.setGeometry(QtCore.QRect(150, 120, 371, 21))
        self.lblTestOutput.setText("")
        self.lblTestOutput.setObjectName("lblTestOutput")
        self.txtboxPort.raise_()
        self.txtboxMailServer.raise_()
        self.label_4.raise_()
        self.label_3.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.txtboxPassword.raise_()
        self.txtboxLogin.raise_()
        self.boolifSSL.raise_()
        self.btnTestConnection.raise_()
        self.lblTestOutput.raise_()
        self.label = QtWidgets.QLabel(Settings)
        self.label.setGeometry(QtCore.QRect(20, 20, 181, 16))
        self.label.setObjectName("label")
        self.checkFreq = QtWidgets.QSpinBox(Settings)
        self.checkFreq.setGeometry(QtCore.QRect(200, 15, 52, 23))
        self.checkFreq.setMinimum(1)
        self.checkFreq.setMaximum(120)
        self.checkFreq.setProperty("value", 15)
        self.checkFreq.setObjectName("checkFreq")
        self.label_2 = QtWidgets.QLabel(Settings)
        self.label_2.setGeometry(QtCore.QRect(260, 20, 61, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Settings)
        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Mail Notifier - Settings"))
        self.boolifNotify.setText(_translate("Settings", "Use also pop-up notification"))
        self.groupBox.setTitle(_translate("Settings", "IMAP settings"))
        self.txtboxMailServer.setPlaceholderText(_translate("Settings", "mail.example.com"))
        self.label_4.setText(_translate("Settings", "Port"))
        self.label_5.setText(_translate("Settings", "Login"))
        self.label_6.setText(_translate("Settings", "Password"))
        self.txtboxLogin.setPlaceholderText(_translate("Settings", "name@example.com"))
        self.label_3.setText(_translate("Settings", "Mail server"))
        self.txtboxPort.setPlaceholderText(_translate("Settings", "143"))
        self.boolifSSL.setText(_translate("Settings", "Use SSL connection"))
        self.btnTestConnection.setText(_translate("Settings", "Test connection"))
        self.label.setText(_translate("Settings", "Check for unread mail every"))
        self.label_2.setText(_translate("Settings", "minutes"))

