# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addCourseDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(437, 411)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/toolImage/gpa_calculator.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet("QWidget{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton{\n"
"background-color: rgb(129, 157, 200);\n"
"padding:15px;\n"
"border-radius:5px;\n"
"font-size:14px;\n"
"font-weight:bold;\n"
"font-family:\"Arial Rounded MTBold\";\n"
"color:white;\n"
"}\n"
"QLineEdit{\n"
"border:3px solid rgb(129, 157, 200);\n"
"padding:15px;\n"
"border-radius:10px;\n"
"margin-bottom:10px;\n"
"    font: 14pt \"Arial\";\n"
"    color: rgb(111, 105, 200);\n"
"}\n"
"QLabel{\n"
"font: 20pt \"Arial Rounded MT Bold\";\n"
"    color: rgb(111, 105, 200);\n"
"}\n"
"#submitbutton:hover{\n"
"background-color:rgb(111,105,200)\n"
"}\n"
"QComboBox{\n"
"border:3px solid rgb(129, 157, 200);\n"
"padding:15px;\n"
"border-radius:10px;\n"
"margin-bottom:10px;\n"
"    font: 14pt \"Arial\";\n"
"    color: rgb(111, 105, 200);\n"
"}\n"
"")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.addcourse = QtWidgets.QLabel(Dialog)
        self.addcourse.setAlignment(QtCore.Qt.AlignCenter)
        self.addcourse.setObjectName("addcourse")
        self.verticalLayout.addWidget(self.addcourse)
        self.courseline = QtWidgets.QLineEdit(Dialog)
        self.courseline.setToolTip("")
        self.courseline.setObjectName("courseline")
        self.verticalLayout.addWidget(self.courseline)
        self.unitline = QtWidgets.QLineEdit(Dialog)
        self.unitline.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.unitline.setObjectName("unitline")
        self.verticalLayout.addWidget(self.unitline)
        self.gradecombo = QtWidgets.QComboBox(Dialog)
        self.gradecombo.setToolTip("")
        self.gradecombo.setToolTipDuration(-1)
        self.gradecombo.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.gradecombo.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.gradecombo.setObjectName("gradecombo")
        self.gradecombo.addItem("")
        self.gradecombo.addItem("")
        self.gradecombo.addItem("")
        self.gradecombo.addItem("")
        self.gradecombo.addItem("")
        self.verticalLayout.addWidget(self.gradecombo)
        self.submitbutton = QtWidgets.QPushButton(Dialog)
        self.submitbutton.setObjectName("submitbutton")
        self.verticalLayout.addWidget(self.submitbutton)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AddCourseForm"))
        self.addcourse.setText(_translate("Dialog", "ADD COURSE"))
        self.courseline.setPlaceholderText(_translate("Dialog", "Course Code"))
        self.unitline.setPlaceholderText(_translate("Dialog", "Unit"))
        self.gradecombo.setItemText(0, _translate("Dialog", "A"))
        self.gradecombo.setItemText(1, _translate("Dialog", "B"))
        self.gradecombo.setItemText(2, _translate("Dialog", "C"))
        self.gradecombo.setItemText(3, _translate("Dialog", "D"))
        self.gradecombo.setItemText(4, _translate("Dialog", "F"))
        self.submitbutton.setText(_translate("Dialog", "SUBMIT"))

import actionImages

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

