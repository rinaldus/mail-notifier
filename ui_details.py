# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/details.ui'
#
# Created by: PyQt5 UI code generator 5.6.1.dev1604271126
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Details(object):
    def setupUi(self, Details):
        Details.setObjectName("Details")
        Details.resize(1048, 619)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/mailbox_empty.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Details.setWindowIcon(icon)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Details)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnRefresh = QtWidgets.QPushButton(Details)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRefresh.sizePolicy().hasHeightForWidth())
        self.btnRefresh.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/check_now.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRefresh.setIcon(icon1)
        self.btnRefresh.setObjectName("btnRefresh")
        self.verticalLayout_2.addWidget(self.btnRefresh)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtWidgets.QTableWidget(Details)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Details)
        QtCore.QMetaObject.connectSlotsByName(Details)

    def retranslateUi(self, Details):
        _translate = QtCore.QCoreApplication.translate
        Details.setWindowTitle(_translate("Details", "Mail Notifier"))
        self.btnRefresh.setText(_translate("Details", "Refresh"))

import resources_rc
