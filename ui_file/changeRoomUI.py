# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'changeRoomUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(347, 127)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 301, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(130, 90, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.roomE = QtWidgets.QLineEdit(Form)
        self.roomE.setGeometry(QtCore.QRect(20, 40, 301, 31))
        self.roomE.setObjectName("roomE")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "房间设置"))
        self.label.setText(_translate("Form", "输入地址或房间号："))
        self.pushButton.setText(_translate("Form", "确定"))
