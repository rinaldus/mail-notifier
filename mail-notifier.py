#!/usr/bin/env python3

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
        QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMessageBox, QMenu, QPushButton, QSpinBox, QStyle, QSystemTrayIcon,
        QTextEdit, QVBoxLayout)
from PyQt5.QtCore import (QThread, QTimer, QFile, QSettings)
import imaplib
imaplib._MAXLINE = 400000
import subprocess
import res
from ui_settings import Ui_Settings
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import socket
import hashlib, uuid
import time

#variables
timers = []
programTitle = "Mail Notifier"
settings = QSettings(os.path.expanduser("~")+"/.config/mail-notifier/settings.conf", QSettings.NativeFormat)
def SettingsExist():
    if ((settings.contains("CheckInterval") and settings.value("CheckInterval") != "") and
        (settings.contains("Notify") and settings.value("Notify") != "") and
        (settings.contains("MailServer") and settings.value("MailServer") != "") and
        (settings.contains("Port") and settings.value("Port") != "") and
        (settings.contains("Login") and settings.value("Login") != "") and
        (settings.contains("Password") and settings.value("Password") != "") and
        (settings.contains("SSL") and settings.value("SSL") != "")):
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
        self.trayIcon.setIcon(QIcon(":icons/mailbox_empty.png"))
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
        # Menu actions
    def createActions(self):
        self.quitAction = QAction(QIcon(':icons/menu_quit.png'),"&Quit", self,
                triggered=QApplication.instance().quit)
        self.checkNow = QAction(QIcon(':icons/check_now.png'),"&Check now", self,
                triggered=mail_check)
        self.restoreAction = QAction(QIcon(":icons/settings.png"),"&Settings", self,
                triggered=self.showNormal)

        # UI functions
    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.checkNow)
        self.trayIconMenu.addAction(self.restoreAction)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def SettingsRestore(self):
        if SettingsExist():
            self.ui.checkFreq.setValue(int(settings.value("CheckInterval")))
            self.ui.boolifNotify.setChecked(bool(settings.value("Notify")))
            self.ui.txtboxMailServer.setText(settings.value("MailServer"))
            self.ui.txtboxPort.setText(settings.value("Port"))
            self.ui.txtboxLogin.setText(settings.value("Login"))
            self.ui.txtboxPassword.setText(settings.value("Password"))
            self.ui.boolifSSL.setChecked(bool(settings.value("SSL")))
    def SettingsSave(self):
        settings.setValue("CheckInterval",self.ui.checkFreq.value())
        settings.setValue("Notify", self.ui.boolifNotify.isChecked())
        settings.setValue("MailServer",self.ui.txtboxMailServer.text())
        settings.setValue("Port",self.ui.txtboxPort.text())
        settings.setValue("Login",self.ui.txtboxLogin.text())
        settings.setValue("Password",self.ui.txtboxPassword.text())
        settings.setValue("SSL",self.ui.boolifSSL.isChecked())
    
    def btnOK_clicked(self):
        self.SettingsSave()
        
        if (settings.value("MailServer") == "" or settings.value("Port") == "" or settings.value("Login") == "" or settings.value("Password") == ""):
            QMessageBox.critical(self, "Warning","You should fill all fields in IMAP settings!")
            self.show()
        mail_check()
        self.ui.lblTestOutput.setText("")
			
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

    def closeEvent(self, event): 
        print ("Closing the app")
        
# Common functions

class Mail():
    def __init__(self):
        socket.setdefaulttimeout(5)
        self.user = settings.value("Login")
        self.password = settings.value("Password")
        self.mailserver = settings.value("MailServer")
        self.port = settings.value("Port")
        
    def login(self):
        try:
            if settings.value("SSL"):
                self.imap = imaplib.IMAP4_SSL(self.mailserver, self.port)
                
            else:
                self.imap = imaplib.IMAP4(self.mailserver, self.port)
            self.imap.login(self.user, self.password)
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

def mail_check():
    if SettingsExist():
        m = Mail()
        if m.login():
            mail_count = m.checkMail()
            if mail_count == 0:
                window.trayIcon.setToolTip ("You have no unread mail")
                window.trayIcon.setIcon(QIcon(":icons/mailbox_empty.png"))
            else:
                window.trayIcon.setToolTip ("You have "+ str(mail_count)+" unread letters")
                window.trayIcon.setIcon(QIcon(":icons/mailbox_full.png"))
                notify ("You have "+ str(mail_count) +" unread letters")
        else:
            window.trayIcon.setToolTip("Unable to establish connection to mailbox. Check your mail settings and make sure that you have not network problems.")
            notify("Unable to establish connection to mailbox. Check your mail settings and make sure that you have not network problems.")
            window.trayIcon.setIcon(QIcon(":icons/mailbox_error.png"))
    else:
        window.trayIcon.setToolTip("Cannot find configuration file. You should give access to your mailbox")
def notify(message):
    if settings.value("Notify"):
        subprocess.Popen(['notify-send', programTitle, message])
    return
    
def hash(password):
    salt = uuid.uuid4().hex
    return hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()

class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        timer = QTimer()
        timer.timeout.connect(mail_check)
        if SettingsExist():
            CheckInterval = 1000*60*int(settings.value("CheckInterval"))
        else:
            CheckInterval = 1000*60*5
        timer.start(CheckInterval)
        timers.append(timer)

        self.exec_()

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
    if SettingsExist():
        window.hide()
    else:
        window.show()
    # UI started. Starting required functions after UI start
    mail_check()
    thread_instance = Thread()
    thread_instance.start()
    sys.exit(app.exec_())
