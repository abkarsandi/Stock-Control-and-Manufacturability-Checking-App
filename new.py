import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget
import openpyxl
import pandas as pd
import numpy as np

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.combo1 = QComboBox()
        self.combo1.addItems(["M8", "M10", "M12", "M14", "M16", "M18", "M20", "M22"])

        self.combo2 = QComboBox()
        self.combo2.addItems(["DIN 931", "DIN 933", "DIN 6914", "DIN 6921"])

        self.label = QLabel("")

        btn = QPushButton("Check Availability")
        btn.clicked.connect(self.run_code)

        layout = QVBoxLayout()
        layout.addWidget(self.combo1)
        layout.addWidget(self.combo2)
        layout.addWidget(btn)
        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def run_code(self):
        product = self.combo1.currentText() + "-" + self.combo2.currentText()
        needed_product = product
        print(needed_product,len(needed_product))
        df = pd.read_excel("C:/Users/abkarsandi/Desktop/demo/list.xlsx", dtype=str)

        products = df["PRODUCT NAME"]

        part_list = []

        for i in range(len(products)):
            if needed_product == products[i]:
                part_list = df.iloc[i][1:].values

        raw_list = {}

        for i in range(len(part_list)):
            if part_list[i] in raw_list:
                raw_list[part_list[i]] += 1
            else:
                raw_list[part_list[i]] = 1

        list_with_neededs = {}

        for i in raw_list:
            try:
                if np.isnan(i) == False:
                    list_with_neededs[i] = raw_list[i]
            except:
                list_with_neededs[i] = raw_list[i]

        data = pd.read_excel("C:/Users/abkarsandi/Desktop/demo/inventory.xlsx", dtype=str)
        all_parts = data["PART"]

        items = []
        result = ""
        for i in list_with_neededs:
            if list_with_neededs[i] in all_parts:
                for j in range(len(all_parts)):
                    if i == all_parts[j]:
                        if int(list_with_neededs[i]) > int(data.iloc[j][4]):
                            result += "We have " + str(int(list_with_neededs[i]) - int(data.iloc[j][4])) + " missing parts of " + str(all_parts[j]) + "\n"
                        else:
                            result += "We have " + str(int(data.iloc[j][4])) + " parts of " + str(all_parts[j]) + " ✓\n"
            else:
                result += "Not in inventory!\n"
        self.label.setText(result)
        
app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())

