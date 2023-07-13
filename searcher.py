import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget, QScrollArea, QTextEdit, QLineEdit
import openpyxl
import pandas as pd
import numpy as np
import capacities as cp
import setFinderv2 as sf
import json


def searcher(list_data):
    with open("config.json") as f:
        config = json.load(f)

    inventory_path = config["inventory_file_path"]

    data = pd.read_excel(inventory_path, dtype=str)
    all_parts = data["PART"]

    try:
        part_list = list_data.tolist()
    except:
        return "No Die List"

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

    result = ""

    database_checker = 0

    print(list_with_neededs)
    print(len(list_with_neededs))

    for i in list_with_neededs:
            database_checker = 0  # Moved inside the outer loop
            if list_with_neededs[i] in all_parts:
                for j in range(len(all_parts)):
                    if i == all_parts[j]:
                        database_checker = 1
                        if int(list_with_neededs[i]) > int(data.iloc[j][4]):
                            result += (str(all_parts[j]) + " parçasından " + str(int(list_with_neededs[i]) - int(data.iloc[j][4])) + " adet eksik. Elde olan: "
                                + str(int(data.iloc[j][4])) + " İhtiyaç: " + str(int(list_with_neededs[i])) + "\n")
                        else:
                            result += (str(all_parts[j]) + " parçasından " + str(int(data.iloc[j][4])) + " adet mevcut. Gereken: " + str(int(list_with_neededs[i])) + "✓\n")
            if database_checker == 0:  # Moved outside the inner loop
                result += str(i) + " veritabanında bulunamadı! \n"
    return result

