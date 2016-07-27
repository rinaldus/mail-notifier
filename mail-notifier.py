#!/usr/bin/env python3

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
        QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMessageBox, QMenu, QPushButton, QSpinBox, QStyle, QSystemTrayIcon,
        QTextEdit, QVBoxLayout, QInputDialog)
from PyQt5.QtCore import (QThread, QTimer, QFile, QSettings)
import imaplib
import email
imaplib._MAXLINE = 400000
import subprocess
import resources_rc
from ui_settings import Ui_Settings
from ui_about import Ui_about
from ui_details import Ui_Details
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import socket
import time
from datetime import datetime, date, time

#variables
programTitle = "Mail Notifier"
programVersion = "3.0-dev"
settings = QSettings(os.path.expanduser("~")+"/.config/mail-notifier/settings.conf", QSettings.NativeFormat)
def GlobalSettingsExist():
    if ((settings.contains("CheckInterval") and settings.value("CheckInterval") != "") and
        (settings.contains("Notify") and settings.value("Notify") != "")):
        return True
    else:
        return False
        
def AccountExist():
    groups = settings.childGroups()
    if (len(groups)) != 0:
        settings.beginGroup(groups[0])
        if ((settings.contains("MailServer") and settings.value("MailServer") != "") and
        (settings.contains("Port") and settings.value("Port") != "") and
        (settings.contains("Login") and settings.value("Login") != "") and
        (settings.contains("Password") and settings.value("Password") != "") and
        (settings.contains("SSL") and settings.value("SSL") != "")):
            n = True
        else:
            n = False
        settings.endGroup()
    else:
        n = False
    if (n):
        return True
    else:
        return False

class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()

        # UI
        self.createActions()
        self.setTitle=programTitle
        self.createTrayIcon()
        # Draw system tray icon
        pixmap = QtGui.QPixmap(QtGui.QPixmap(":icons/mailbox_empty.png"))
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QColor(255, 0, 0))
        painter.setFont(QtGui.QFont('Arial', QtGui.QFont.Bold))
        painter.drawText(QtCore.QRectF(pixmap.rect()), QtCore.Qt.AlignCenter, "0")
        painter.end()
        self.trayIcon.setIcon(QtGui.QIcon(pixmap))
        # End drawing system tray icon
        
        self.trayIcon.setToolTip("You have no unread letters")
        self.trayIcon.show()
        
        # setup settings
        self.ui = Ui_Settings()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(os.path.dirname(os.path.realpath(__file__))+"/icons/mailbox_empty.png"))
        self.SettingsRestore()
        
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.btnOK_clicked)
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.btnCancel_clicked)
        self.ui.btnTestConnection.clicked.connect(self.btnTestConnection_clicked)
        self.ui.comboAccounts.currentTextChanged.connect(self.comboAccounts_changed)
        self.ui.btnAddAccount.clicked.connect(self.btnAddAccount_clicked)
        self.ui.btnRenameAccount.clicked.connect(self.btnRenameAccount_clicked)
        self.ui.btnSaveAccount.clicked.connect(self.btnSaveAccount_clicked)
        self.ui.btnRemoveAccount.clicked.connect(self.btnRemoveAccount_clicked)
        
        # Main timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(mail_check)
        
        self.lastCheckCount = 0 # variable for prevent annoying popup notification when mail count didn't change since last check
        
        # Menu actions
    def createActions(self):
        self.detailsShow = QAction(QIcon(':icons/details.png'),"&Details", self, triggered=self.detailsShow)
        self.aboutShow = QAction(QIcon(':icons/mailbox_empty.png'),"&About", self, triggered=self.aboutShow)
        self.checkNow = QAction(QIcon(':icons/check_now.png'),"&Check now", self, triggered=mail_check)
        self.restoreAction = QAction(QIcon(":icons/settings.png"),"&Settings", self, triggered=self.showNormal)
        self.quitAction = QAction(QIcon(':icons/menu_quit.png'),"&Quit", self, triggered=QApplication.instance().quit)

        # UI functions
    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.aboutShow)
        self.trayIconMenu.addAction(self.detailsShow)
        self.trayIconMenu.addAction(self.checkNow)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.activated.connect(self.trayIconActivated)

    def SettingsRestore(self):
        if (GlobalSettingsExist() and AccountExist()):
            groups = settings.childGroups()
            for i in range (len(groups)):
                self.ui.comboAccounts.addItem(groups[i])
                self.ui.comboAccounts.setCurrentText(groups[i])
                settings.beginGroup(groups[i])
                self.ui.txtboxMailServer.setText(settings.value("MailServer"))
                self.ui.txtboxPort.setText(settings.value("Port"))
                self.ui.txtboxLogin.setText(settings.value("Login"))
                self.ui.txtboxPassword.setText(settings.value("Password"))
                self.ui.boolifSSL.setChecked(bool(settings.value("SSL")))
                settings.endGroup()
            if (self.ui.comboAccounts.count() == 0):
                self.ui.comboAccounts.addItem("Default")
                self.ui.comboAccounts.setCurrentText("Default")
            self.ui.checkFreq.setValue(int(settings.value("CheckInterval")))
            self.ui.boolifNotify.setChecked(bool(settings.value("Notify")))
           
    def SettingsSave(self,account):
        settings.setValue("CheckInterval",self.ui.checkFreq.value())
        settings.setValue("Notify", self.ui.boolifNotify.isChecked())
        settings.beginGroup(account)
        settings.setValue("MailServer",self.ui.txtboxMailServer.text())
        settings.setValue("Port",self.ui.txtboxPort.text())
        settings.setValue("Login",self.ui.txtboxLogin.text())
        settings.setValue("Password",self.ui.txtboxPassword.text())
        settings.setValue("SSL",self.ui.boolifSSL.isChecked())
        settings.endGroup()
            
    def SettingsRemove(self,group):
        settings.beginGroup(group)
        settings.remove("")
        settings.endGroup()
    
    def btnOK_clicked(self):
        self.SettingsSave(self.ui.comboAccounts.currentText())
        
        if (settings.value("MailServer") == "" or settings.value("Port") == "" or settings.value("Login") == "" or settings.value("Password") == ""):
            QMessageBox.critical(self, "Warning","You should fill all fields in IMAP settings!")
            self.show()
        mail_check()
        self.ui.lblTestOutput.setText("")
        self.stop()
        self.start()
			
    def btnCancel_clicked(self):
        self.SettingsRestore()
        self.ui.lblTestOutput.setText("")
        
    def btnTestConnection_clicked(self):
        try:
            if self.ui.boolifSSL.isChecked:
                self.imap = imaplib.IMAP4_SSL(self.ui.txtboxMailServer.text(), self.ui.txtboxPort.text())
            else:
                self.imap = imaplib.IMAP4(self.ui.txtboxMailServer.text(), self.ui.txtboxPort.text())
            self.imap.login(self.ui.txtboxLogin.text(), self.ui.txtboxPassword.text())
            output = "Connection was established successfully"
        except:
            output = "Unable to establish connection to mailbox"
        finally:
            self.ui.lblTestOutput.setText(output)
    
    def btnAddAccount_clicked(self):
        GroupName = QInputDialog.getText(self,"Enter account name","Enter account name",QLineEdit.Normal,"")
        if (GroupName[0]):
            self.ui.comboAccounts.addItem(GroupName[0])
            self.ui.comboAccounts.setCurrentText(GroupName[0])
            
    def btnRenameAccount_clicked(self):
        Index = self.ui.comboAccounts.currentIndex()
        OldGroupName = self.ui.comboAccounts.currentText()
        GroupName = QInputDialog.getText(self,"Enter account name","Enter account name",QLineEdit.Normal,self.ui.comboAccounts.currentText())
        if (GroupName[0]):
            self.SettingsSave(GroupName[0])
            self.ui.comboAccounts.setItemText(Index, GroupName[0])
            self.ui.comboAccounts.setCurrentText(GroupName[0])
            self.SettingsRemove(OldGroupName)
    
    def btnSaveAccount_clicked(self):
        self.SettingsSave(self.ui.comboAccounts.currentText())
        self.ui.lblTestOutput.setText("Account saved")
            
    def btnRemoveAccount_clicked(self):
        reply = QMessageBox.warning(self, 'Warning!', "Delete this account permanently?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (reply == QMessageBox.Yes):
            Index = self.ui.comboAccounts.currentIndex()
            GroupName = self.ui.comboAccounts.currentText()
            self.ui.comboAccounts.removeItem(Index)
            self.SettingsRemove(GroupName)
            
    def comboAccounts_changed(self):
        self.ui.lblTestOutput.setText("")
        settings.beginGroup(self.ui.comboAccounts.currentText())
        self.ui.txtboxMailServer.setText(settings.value("MailServer"))
        self.ui.txtboxPort.setText(settings.value("Port"))
        self.ui.txtboxLogin.setText(settings.value("Login"))
        self.ui.txtboxPassword.setText(settings.value("Password"))
        self.ui.boolifSSL.setChecked(bool(settings.value("SSL")))
        settings.endGroup()
        
    def aboutShow(self):
        if (about.isMinimized):
            about.hide()
        about.show()
        about.activateWindow()
        
    def detailsShow(self):
        details.show()
        details.activateWindow()
        
    def trayIconActivated(self, reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            details.show()
            details.activateWindow()
                        
    def start(self):
        if (GlobalSettingsExist() and AccountExist()):
            CheckInterval = 1000*60*int(settings.value("CheckInterval"))
        else:
            CheckInterval = 1000*60*5
        self.timer.setInterval (CheckInterval)
        self.timer.start()
        
    def stop (self):
        self.timer.stop()
        
class About(QDialog):
    def __init__(self):
        super(About, self).__init__()
        
        self.ui = Ui_about()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setFixedSize(483,334)
        
        self.ui.lblNameVersion.setText(programTitle + " " + programVersion)
        
        f = QtCore.QFile(":/LICENSE.txt")
        if f.open(QtCore.QIODevice.ReadOnly | QtCore.QFile.Text):
            text = QtCore.QTextStream(f).readAll()
            f.close()
        self.ui.txtLicense.setPlainText(text)
                
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        
class Details(QDialog):
    def __init__(self):
        super(Details, self).__init__()
        
        self.ui = Ui_Details()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.ui.btnRefresh.clicked.connect(self.Refresh_clicked)
        
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        
    def Refresh_clicked(self):
        mail_check()
        
# Common functions

class Mail():
    def __init__(self):
        socket.setdefaulttimeout(5)
        
    def login(self,mailserver,port,user,password,ssl):
        try:
            if ssl:
                self.imap = imaplib.IMAP4_SSL(mailserver, port)
                
            else:
                self.imap = imaplib.IMAP4(mailserver, port)
            self.imap.login(user, password)
            return True
        except:
            print("Login error")
            return False
        
    def checkMail(self):
        try:
            self.imap.select()
            self.unRead = self.imap.search(None, 'UNSEEN')
            return len(self.unRead[1][0].split())
        except:
            print("Unable to check mail")
            return "ERROR"
    def parseMail(self,header):
        try:
            output=[]
            self.imap.select(readonly=True)
            typ, data = self.imap.search(None, 'UNSEEN')
            for num in data[0].split():
                typ, data = self.imap.fetch(num, '(RFC822)')
                raw_mail = data[0][1]
                mail=email.message_from_bytes(raw_mail)
                h=email.header.decode_header(mail.get(header))
                if (h[0][1] != "unknown-8bit"):
                    msg = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]
                else:
                    msg = "Unknown charset"
                output.append(msg)
            return output
        except:
            print("Unable to get mail data")
            return "ERROR"

def mail_check():
    details.ui.statusBar.setText(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")+" - Starting mail check")
    mail_count = 0
    AllFroms=[]
    AllSubjs=[]
    AllDates=[]
    details.ui.tableWidget.clearContents()
    details.ui.tableWidget.setRowCount(0)
    details.ui.tableWidget.setColumnCount(0)
    if (GlobalSettingsExist() and AccountExist()):
        m = Mail()
        groups = settings.childGroups()
        for i in range (len(groups)):
            settings.beginGroup(groups[i])
            group = groups[i]
            user = settings.value("Login")
            password = settings.value("Password")
            mailserver = settings.value("MailServer")
            port = settings.value("Port")
            ssl = settings.value("SSL")
            settings.endGroup()
            if m.login(mailserver,port,user,password,ssl):
                if (mail_count == "ERROR" or m.checkMail() == "ERROR"):
                    mail_count = "ERROR"
                else:
                    mail_count += m.checkMail()
                    AllFroms.extend(m.parseMail("From"))
                    AllSubjs.extend(m.parseMail("Subject"))
                    AllDates.extend(m.parseMail("Date"))
            else:
                mail_count = "CONNECTION_ERROR"
    else:
        mail_count = "CONFIGURATION_ERROR"
        
    # Parsing mail_count values
    
    if mail_count == 0:
        # When mailbox have not unread letters
        window.trayIcon.setToolTip ("You have no unread mail")
        # Draw text on icon
        pixmap = QtGui.QPixmap(QtGui.QPixmap(":icons/mailbox_empty.png"))
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QColor(255, 0, 0))
        painter.setFont(QtGui.QFont('Arial', 100,QtGui.QFont.Bold))
        painter.drawText(QtCore.QRectF(pixmap.rect()), QtCore.Qt.AlignCenter, "0")
        painter.end()
        # End drawing text on icon
        window.trayIcon.setIcon(QtGui.QIcon(pixmap))
        details.ui.statusBar.setText(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")+" - Mail check completed. You have no unread letters")
    elif mail_count == "ERROR":
        window.trayIcon.setIcon(QIcon(":icons/mailbox_error.png"))
        window.trayIcon.setToolTip ("Error checking mail.")
        details.ui.statusBar.setText(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")+" - Error checking mail")
    elif mail_count == "CONNECTION_ERROR":
        window.trayIcon.setToolTip("Unable to establish connection to mailbox. Check your mail settings and make sure that you have not network problems.")
        notify("Unable to establish connection to mailbox. Check your mail settings and make sure that you have not network problems.")
        window.trayIcon.setIcon(QIcon(":icons/mailbox_error.png"))
        details.ui.statusBar.setText(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")+" - Unable to establish connection to mailbox. Check your mail settings and make sure that you have not network problems")
    elif mail_count == "CONFIGURATION_ERROR":
        window.trayIcon.setIcon(QIcon(":icons/mailbox_error.png"))
        window.trayIcon.setToolTip("Cannot find configuration file. You should give access to your mailbox")
        details.ui.statusBar.setText(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")+" - Cannot find configuration file. You should give access to your mailbox")
    else:
        # When mailbox has unread letters
        window.trayIcon.setToolTip ("You have "+ str(mail_count)+" unread letters")
        # Draw text on icon
        pixmap = QtGui.QPixmap(QtGui.QPixmap(":icons/mailbox_full.png"))
        painter = QtGui.QPainter(pixmap)
        painter.setPen(QtGui.QColor(255, 255, 255))
        painter.setFont(QtGui.QFont('Arial', 100,QtGui.QFont.Bold))
        painter.drawText(QtCore.QRectF(pixmap.rect()), QtCore.Qt.AlignCenter, str(mail_count))
        painter.end()
        # End drawing text on icon
        window.trayIcon.setIcon(QtGui.QIcon(pixmap))
        # Popup notification appears only if mail count changed since last check
        if (mail_count != window.lastCheckCount):
            notify ("You have "+ str(mail_count) +" unread letters")
            
        # Filling table
        data = {"From":AllFroms,
                "Subject":AllSubjs,
                "Date":AllDates,}
        details.ui.tableWidget.setRowCount(len(AllFroms))
        details.ui.tableWidget.setColumnCount(3)
        #Enter data onto Table
        horHeaders = []
        for n, key in enumerate(sorted(data.keys())):
            #print(data.keys())
            horHeaders.append(key)
            for m, item in enumerate(data[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                details.ui.tableWidget.setItem(m, n, newitem)
        
        #Add Header
        details.ui.tableWidget.setHorizontalHeaderLabels(horHeaders)        

        #Adjust size of Table
        details.ui.tableWidget.resizeColumnsToContents()
        details.ui.tableWidget.resizeRowsToContents()
        details.ui.statusBar.setText(datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")+" - Mail check completed. You have "+ str(mail_count) +" unread letters")
    # check was successfull, lastCheckCount is updating
    window.lastCheckCount = mail_count
def notify(message):
    if settings.value("Notify"):
        subprocess.Popen(['notify-send', programTitle, message])
    return
    

    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    systemtray_timeout = 0
    # Check if DE supports system tray
    while not QSystemTrayIcon.isSystemTrayAvailable():
        systemtray_timeout += 1
        time.sleep (20)
        if systemtray_timeout == 5:
            QMessageBox.critical(None, "Mail notifier",
                    "I couldn't detect any system tray on this system.")
            sys.exit(1)
    QApplication.setQuitOnLastWindowClosed(False)
    window = Window()
    about = About()
    details = Details()
    if (GlobalSettingsExist() and AccountExist()):
        window.hide()
    else:
        window.show()
    # UI started. Starting required functions after UI start
    mail_check()
    window.start()
    sys.exit(app.exec_())
