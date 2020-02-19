# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reqco_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_reqco_window(object):
    def setupUi(self, reqco_window):
        reqco_window.setObjectName(_fromUtf8("reqco_window"))
        reqco_window.resize(850, 468)
        reqco_window.setMinimumSize(QtCore.QSize(850, 468))
        reqco_window.setMaximumSize(QtCore.QSize(850, 468))
        self.centralwidget = QtGui.QWidget(reqco_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_5 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.title_3 = QtGui.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(14)
        self.title_3.setFont(font)
        self.title_3.setObjectName(_fromUtf8("title_3"))
        self.gridLayout_3.addWidget(self.title_3, 0, 0, 1, 1)
        self.run_button = QtGui.QPushButton(self.groupBox_2)
        self.run_button.setToolTip(_fromUtf8(""))
        self.run_button.setWhatsThis(_fromUtf8(""))
        self.run_button.setObjectName(_fromUtf8("run_button"))
        self.gridLayout_3.addWidget(self.run_button, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.title_4 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(14)
        self.title_4.setFont(font)
        self.title_4.setObjectName(_fromUtf8("title_4"))
        self.gridLayout_2.addWidget(self.title_4, 0, 0, 1, 1)
        self.run_button_2 = QtGui.QPushButton(self.groupBox)
        self.run_button_2.setToolTip(_fromUtf8(""))
        self.run_button_2.setWhatsThis(_fromUtf8(""))
        self.run_button_2.setObjectName(_fromUtf8("run_button_2"))
        self.gridLayout_2.addWidget(self.run_button_2, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox, 0, 1, 2, 1)
        self.frame_1 = QtGui.QFrame(self.centralwidget)
        self.frame_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_1.setLineWidth(5)
        self.frame_1.setObjectName(_fromUtf8("frame_1"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_1)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.title_2 = QtGui.QLabel(self.frame_1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(14)
        self.title_2.setFont(font)
        self.title_2.setObjectName(_fromUtf8("title_2"))
        self.gridLayout_4.addWidget(self.title_2, 0, 0, 1, 1)
        self.lineEdit_pulse = QtGui.QLineEdit(self.frame_1)
        self.lineEdit_pulse.setObjectName(_fromUtf8("lineEdit_pulse"))
        self.gridLayout_4.addWidget(self.lineEdit_pulse, 1, 0, 1, 1)
        self.title = QtGui.QLabel(self.frame_1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Verdana"))
        font.setPointSize(14)
        self.title.setFont(font)
        self.title.setObjectName(_fromUtf8("title"))
        self.gridLayout_4.addWidget(self.title, 2, 0, 1, 1)
        self.done_button = QtGui.QPushButton(self.frame_1)
        self.done_button.setToolTip(_fromUtf8(""))
        self.done_button.setWhatsThis(_fromUtf8(""))
        self.done_button.setCheckable(True)
        self.done_button.setAutoExclusive(False)
        self.done_button.setObjectName(_fromUtf8("done_button"))
        self.gridLayout_4.addWidget(self.done_button, 3, 0, 1, 1)
        self.impossible_button = QtGui.QPushButton(self.frame_1)
        self.impossible_button.setToolTip(_fromUtf8(""))
        self.impossible_button.setWhatsThis(_fromUtf8(""))
        self.impossible_button.setCheckable(True)
        self.impossible_button.setAutoExclusive(False)
        self.impossible_button.setObjectName(_fromUtf8("impossible_button"))
        self.gridLayout_4.addWidget(self.impossible_button, 4, 0, 1, 1)
        self.closed_button = QtGui.QPushButton(self.frame_1)
        self.closed_button.setToolTip(_fromUtf8(""))
        self.closed_button.setWhatsThis(_fromUtf8(""))
        self.closed_button.setCheckable(True)
        self.closed_button.setAutoExclusive(False)
        self.closed_button.setObjectName(_fromUtf8("closed_button"))
        self.gridLayout_4.addWidget(self.closed_button, 5, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame_1, 1, 0, 1, 1)
        reqco_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(reqco_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 850, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        reqco_window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(reqco_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        reqco_window.setStatusBar(self.statusbar)

        self.retranslateUi(reqco_window)
        QtCore.QMetaObject.connectSlotsByName(reqco_window)

    def retranslateUi(self, reqco_window):
        reqco_window.setWindowTitle(_translate("reqco_window", "SET pulse in Reqco", None))
        self.title_3.setText(_translate("reqco_window", "SCAN DATABASE", None))
        self.run_button.setText(_translate("reqco_window", "run ", None))
        self.title_4.setText(_translate("reqco_window", "<html><head/><body><p>DOWNLOAD</p><p>DATABASE</p></body></html>", None))
        self.run_button_2.setText(_translate("reqco_window", "run ", None))
        self.title_2.setText(_translate("reqco_window", "SINGLE PULSE", None))
        self.lineEdit_pulse.setText(_translate("reqco_window", "insert JPN", None))
        self.title.setText(_translate("reqco_window", "mark pulse as", None))
        self.done_button.setText(_translate("reqco_window", "DONE", None))
        self.impossible_button.setText(_translate("reqco_window", "IMPOSSIBLE", None))
        self.closed_button.setText(_translate("reqco_window", "CLOSED", None))

