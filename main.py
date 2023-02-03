"""
Version: 0a
Tecnocoli - @04/2022
Author: Jeferson Coli - jcoli@tecnocoli.com.br
OBD2 test
Main
"""

import sys
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QTableView, QMessageBox
from PyQt5.QtCore import QFile, QTimer, QTime, Qt
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from pathlib import Path
from forms.mainwindow import Ui_MainWindow

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import obd
from obd import Unit, OBDResponse
from obd import ECU
from obd.protocols.protocol import Message
from obd.utils import OBDStatus
from obd.OBDCommand import OBDCommand
from obd.decoders import noop

import hashlib
import serial
from datetime import datetime
import time
from time import sleep

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
text_date = datetime.now().strftime('%d-%m-%Y')
scanner_file = 'simulator-' + text_date+'.log'
handler = logging.FileHandler(scanner_file)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

from functions.get_qtcss import get_style, available_styles
from functions.variables import Variables


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.var1 = Variables
        self.tab_bar.setCurrentIndex(0)
        self.init_form()


    def obd_connect(self):
        if not (self.functionObd.odb_scan_serial()) is None:
            if (self.functionObd.odb_scan_serial()) == 0:
                self.append_text_datetime('No OBD-II adapters found')
                self.status_bar.showMessage('No OBD-II adapters found')
                self.var1.obdConnect = False
            else:
                lports = self.functionObd.odb_scan_serial()
                for nport in lports:
                    self.append_text_datetime('OBD2 scan port: ' + nport)
                try:
                    obd.logger.setLevel(obd.logging.DEBUG)
                    self.functionObd.obd_connect()
                    self.var1.connect_car = self.functionObd.support_command(obd.commands[1][0x0C])

    def init_form(self):
        self.btn_connect.setText("Connect")
        self.statusbar.setStyleSheet("background-color: rgb(255,140,0); color: rgb(0,0,0)")
        self.statusbar.showMessage('Waiting Connection')
        self.btn_connect.clicked.connect(self.obd_connect())



app = QtWidgets.QApplication(sys.argv)
style_string = get_style("dark_blue")
app.setStyleSheet(style_string)
window = MainWindow()
window.show()
app.exec()