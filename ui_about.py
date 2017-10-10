# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/about.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_about(object):
    def setupUi(self, about):
        about.setObjectName("about")
        about.resize(511, 334)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(about.sizePolicy().hasHeightForWidth())
        about.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/mailbox_empty.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        about.setWindowIcon(icon)
        self.txtLicense = QtWidgets.QPlainTextEdit(about)
        self.txtLicense.setGeometry(QtCore.QRect(50, 120, 381, 201))
        self.txtLicense.setPlainText("")
        self.txtLicense.setObjectName("txtLicense")
        self.lblLogo = QtWidgets.QLabel(about)
        self.lblLogo.setGeometry(QtCore.QRect(50, 0, 131, 111))
        self.lblLogo.setText("")
        self.lblLogo.setPixmap(QtGui.QPixmap(":/icons/mailbox_empty.png"))
        self.lblLogo.setScaledContents(True)
        self.lblLogo.setObjectName("lblLogo")
        self.lblNameVersion = QtWidgets.QLabel(about)
        self.lblNameVersion.setGeometry(QtCore.QRect(200, 40, 291, 31))
        self.lblNameVersion.setMinimumSize(QtCore.QSize(203, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lblNameVersion.setFont(font)
        self.lblNameVersion.setScaledContents(True)
        self.lblNameVersion.setObjectName("lblNameVersion")

        self.retranslateUi(about)
        QtCore.QMetaObject.connectSlotsByName(about)

    def retranslateUi(self, about):
        _translate = QtCore.QCoreApplication.translate
        about.setWindowTitle(_translate("about", "Mail Notifier"))
        self.lblNameVersion.setText(_translate("about", "Mail Notifier"))

import resources_rc
