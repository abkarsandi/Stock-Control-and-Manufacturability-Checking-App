# 13.07.2023
# This Stock Control App is written by Ahmet Buğra KARSANDI
#
#
# Version 4
# The instructions are given in the README file

import sys,os
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QTextEdit, QLineEdit, QGroupBox, QWidget
from PySide6.QtGui import QIcon
import openpyxl
import pandas as pd
import numpy as np
import capacities as cp
import setFinderv2 as sf
import searcher as src
import json

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300,300,1500,600)

        with open(os.getcwd() + "\\parameters.json") as f:
            parameters = json.load(f)

        self.combo1 = QComboBox()
        self.combo1.addItems(parameters["combo1"])

        self.combo2 = QComboBox()
        self.combo2.addItems(parameters["combo2"])

        self.combo3 = QComboBox()
        self.combo3.addItems(parameters["combo3"])

        self.combo4 = QComboBox()
        self.combo4.addItems(parameters["combo4"])

        self.combo5 = QComboBox()
        self.combo5.addItems(parameters["combo5"])

        self.label1 = QLabel("Length:")
        self.line_edit = QLineEdit()

        self.infoText = QLabel()

        self.label = QTextEdit("")
        self.label.setReadOnly(True)

        self.last_note = QLabel()    

        btn = QPushButton("Check Availability")
        btn.clicked.connect(self.run_code)

        btn2 = QPushButton("Refresh")
        btn2.clicked.connect(self.refresher)

        layout = QVBoxLayout()
        layout.addWidget(self.combo1)
        layout.addWidget(self.combo2)
        layout.addWidget(self.combo3)
        layout.addWidget(self.combo4)
        layout.addWidget(self.combo5)
        layout.addWidget(self.line_edit)
        layout.addWidget(btn)
        

        self.result_boxes = QHBoxLayout()
        self.result_boxes.addWidget(self.label)

        self.note_boxes = QHBoxLayout()
        self.note_boxes.addWidget(self.last_note)
        

        layout.addLayout(self.result_boxes)
        layout.addLayout(self.note_boxes)

        bottom_side = QHBoxLayout()
        bottom_side.addWidget(self.infoText)
        bottom_side.addWidget(btn2)
        layout.addLayout(bottom_side)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def run_code(self):
        try:
            self.clear_layout(self.result_boxes)
        except:
            print(None)
        limits = cp.capacity(self.combo4.currentText(),self.combo1.currentText(),self.combo3.currentText(),self.combo2.currentText(), self.line_edit.text())

        with open(os.getcwd() + "\\config.json") as f:
            config = json.load(f)


        list_data = sf.setfinder(self.combo1.currentText(), self.combo3.currentText(), self.combo5.currentText(), self.combo2.currentText(), self.line_edit.text())

        part_list = list(list_data[1])
        note_list = list(list_data[0])
        print(part_list)

        num_of_boxes = len(part_list)
    
        try:
            mock_list= part_list[0].tolist()
        except:
            self.label.setPlainText("Parçaya ait kalıp seti bulunamadı")

        result_sets = []

        for i in range(num_of_boxes):
            result_set = src.searcher(part_list[i])
            result_sets.append(result_set)
            self.sets(result_set,note_list[i],i)
        
        self.infoText.setText(limits)        

    def sets(self,result_set, note,i):
        if i == 0:
            self.label.setPlainText(result_set)
            self.last_note.setText(note[0] + " " + note[1])
        else:
            text_edit = QTextEdit()
            new_note = QLabel(note[0] + " " + note[1])
            text_edit.setPlainText(result_set.replace("\n", "\r\n"))  # Replace newline characters
            self.result_boxes.addWidget(text_edit)
            self.note_boxes.addWidget(new_note)

    def clear_layout(self,layout):
        while layout.count():
            item = layout.takeAt(1)
            widget = item.widget()
            try:
                if widget is not None:
                    widget.setParent(None)
                    widget.deleteLater()
            except:
                self.label.setPlainText("")    

    def refresher(self):
        try:
            self.clear_layout(self.result_boxes)
            self.clear_layout(self.note_boxes)
        except:
            self.label.setPlainText("")
            self.infoText.setText("")

app = QApplication(sys.argv)
window = MyApp()
window.setWindowIcon(QIcon("Capture.ico"))
window.show()
sys.exit(app.exec())