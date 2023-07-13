import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog
import pandas as pd
import json

class ConfigWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label_list = QLabel("List File Path:")
        self.line_edit_list = QLineEdit()
        self.button_browse_list = QPushButton("Browse")

        self.label_inventory = QLabel("Inventory File Path:")
        self.line_edit_inventory = QLineEdit()
        self.button_browse_inventory = QPushButton("Browse")

        self.label_result = QLabel("Capacity File Path:")
        self.line_edit_result = QLineEdit()
        self.button_browse_result = QPushButton("Browse")

        self.button_save = QPushButton("Save")

        self.button_browse_list.clicked.connect(self.browse_list_file)
        self.button_browse_inventory.clicked.connect(self.browse_inventory_file)
        self.button_browse_result.clicked.connect(self.browse_result_file)
        self.button_save.clicked.connect(self.save_configuration)

        layout = QVBoxLayout()
        layout.addWidget(self.label_list)
        layout.addWidget(self.line_edit_list)
        layout.addWidget(self.button_browse_list)
        layout.addWidget(self.label_inventory)
        layout.addWidget(self.line_edit_inventory)
        layout.addWidget(self.button_browse_inventory)
        layout.addWidget(self.label_result)
        layout.addWidget(self.line_edit_result)
        layout.addWidget(self.button_browse_result)
        layout.addWidget(self.button_save)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def browse_list_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select List File")
        if file_path:
            self.line_edit_list.setText(file_path)

    def browse_inventory_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Inventory File")
        if file_path:
            self.line_edit_inventory.setText(file_path)

    def browse_result_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Capacity File")
        if file_path:
            self.line_edit_result.setText(file_path)

    def save_configuration(self):
        list_file_path = self.line_edit_list.text()
        inventory_file_path = self.line_edit_inventory.text()
        result_file_path = self.line_edit_result.text()

        # Create a dictionary with the file paths
        config = {
            "list_file_path": list_file_path,
            "inventory_file_path": inventory_file_path,
            "limits_file_path": result_file_path
        }

        # Save the file paths to the configuration file (config.json)
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)

        self.close()

app = QApplication(sys.argv)
window = ConfigWindow()
window.show()
sys.exit(app.exec())
