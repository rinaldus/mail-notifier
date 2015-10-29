#!/usr/bin/env python3

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
        QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMessageBox, QMenu, QPushButton, QSpinBox, QStyle, QSystemTrayIcon,
        QTextEdit, QVBoxLayout)
from PyQt5.QtCore import (QThread, QTimer)
import imaplib
import subprocess
import res

#variables
timers = []
programTitle = "Mail Notifier"

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
        # Menu actions
    def createActions(self):
        self.quitAction = QAction(QIcon(':icons/menu_quit.png'),"&Quit", self,
                triggered=QApplication.instance().quit)
        self.checkNow = QAction(QIcon(':icons/check_now.png'),"&Check now", self,
                triggered=self.checkNow)
     #   self.restoreAction = QAction("&Restore", self,
     #           triggered=self.showNormal)

        # UI functions
    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.checkNow)
        self.trayIconMenu.addAction(self.quitAction)
        #self.trayIconMenu.addAction(self.restoreAction)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    
    def mailboxEmpty(self):
        self.trayIcon.setToolTip ("You have no unread mail")
        self.trayIcon.setIcon(QIcon(":icons/mailbox_empty.png"))

    def mailboxFull(self):
        self.trayIcon.setToolTip ("You have "+ str(Mail().checkMail())+" unread letters")
        self.trayIcon.setIcon(QIcon(":icons/mailbox_full.png"))
        notify ("You have "+ str(Mail().checkMail())+" unread letters")

    def checkNow (self):
        if Mail().checkMail() == 0:
            self.mailboxEmpty()
            notify("You have no unread mail")
        else:
            self.mailboxFull()


    def closeEvent(self, event): 
        print ("Closing the app")

# Common functions
class Mail():
    def __init__(self):
        self.user= 'YOUR_MAILBOX_LOGIN'
        self.password= 'YOUR_MAILBOX_PASSWORD'
        self.M = imaplib.IMAP4_SSL('MAIL_SERVER', 'PORT(i.e 993)')
        self.M.login(self.user, self.password)
        
    def checkMail(self):
        self.M.select()
        self.unRead = self.M.search(None, 'UnSeen')
        return len(self.unRead[1][0].split())

def mail_check():
    if Mail().checkMail() == 0:
        window.mailboxEmpty()
    else:
        window.mailboxFull()
def notify(message):
    subprocess.Popen(['notify-send', programTitle, message])
    return

class Thread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        timer = QTimer()
        timer.timeout.connect(mail_check)
        timer.start(1000*60*5)
        timers.append(timer)

        self.exec_()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Mail notifier",
                "I couldn't detect any system tray on this system.")
        sys.exit(1)
    QApplication.setQuitOnLastWindowClosed(False)
    window = Window()
    window.hide()
    # UI started. Starting required functions after UI start
    mail_check()
    thread_instance = Thread()
    thread_instance.start()
    sys.exit(app.exec_())
