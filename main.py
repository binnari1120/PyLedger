from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys
import os
import pandas as pd

class QCalendarWidget_(QCalendarWidget):
    def __init__(self, current_btn):
        super().__init__()
        self.current_btn = current_btn

class QPushButton_(QPushButton):
    def __init__(self, str, current_cell_row = None):
        super().__init__(str)
        self.current_cell_row = current_cell_row

class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.data_file_name_with_path = os.path.join(os.path.dirname(__file__), "data.csv")

        self.h_layout_1 = QHBoxLayout()
        self.h_layout_2 = QHBoxLayout()
        self.h_layout_3 = QHBoxLayout()
        self.h_layout_4 = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.v_layout.addLayout(self.h_layout_1)
        self.v_layout.addLayout(self.h_layout_2)
        self.v_layout.addLayout(self.h_layout_3)
        self.v_layout.addLayout(self.h_layout_4)

        self.income_type_labels = ["Salary", "Financial Earning", "Others"]
        self.expenditure_type_labels = ["Utility Bill", "Food", "Transport", "Saving", "Others"]
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 1000, 500)
        self.setWindowTitle("PyLedger")

        menu_bar = QMenuBar()
        file_menu = menu_bar.addMenu("File")
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.is_save_btn_clicked)
        edit_action = file_menu.addAction("Load")
        edit_action.triggered.connect(self.is_load_btn_clicked)

        edit_menu = menu_bar.addMenu("Edit")
        clear_action = edit_menu.addAction("Clear")
        clear_action.triggered.connect(self.is_clear_btn_clicked)

        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction("About PyLedger")

        self.h_layout_1.addWidget(menu_bar)



        self.table = QTableWidget()
        self.table.setColumnCount(5)
        # self.table.setRowCount(1)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalHeaderLabels(["Date", "Type", "Detail", "Amount", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.h_layout_2.addWidget(self.table)

        add_record_btn = QPushButton("Add record")
        add_record_btn.clicked.connect(self.is_add_record_btn_clicked)
        self.h_layout_3.addWidget(add_record_btn)


        show_records_group_box = QGroupBox("Records Visualization")
        self.h_layout_4.addWidget(show_records_group_box)

        show_records_group_box_h_layout = QHBoxLayout()
        show_records_group_box.setLayout(show_records_group_box_h_layout)

        self.year_combo_box = QComboBox()
        self.year_combo_box.addItems(["2018", "2019"])
        show_records_group_box_h_layout.addWidget(self.year_combo_box)

        self.months_combo_box = QComboBox()
        self.months_combo_box.addItem("All")
        self.months_combo_box.addItems(str(i) for i in range(1, 13))
        show_records_group_box_h_layout.addWidget(self.months_combo_box)

        show_records_btn = QPushButton("Show records")
        show_records_btn.clicked.connect(self.is_show_records_btn_clicked)
        show_records_group_box_h_layout.addWidget(show_records_btn)


        self.setLayout(self.v_layout)
        self.show()

    def is_add_record_btn_clicked(self):
        current_row_count = self.table.rowCount()
        self.table.setRowCount(current_row_count + 1)
        self.table.cellChanged.connect(self.is_valid_value)

        date_pick_button = QPushButton("Select Date")
        date_pick_button.clicked.connect(self.is_select_date_btn_clicked)
        self.table.setCellWidget(current_row_count, 0, date_pick_button)

        type_combox_box = QComboBox()
        type_combox_box.addItems(["Income", "Expenditure"])
        type_combox_box.currentTextChanged.connect(self.refresh)
        self.table.setCellWidget(current_row_count, 1, type_combox_box)

        detail_combox_box = QComboBox()
        self.table.setCellWidget(current_row_count, 2, detail_combox_box)

        delete_btn = QPushButton_("Del", current_row_count)
        delete_btn.clicked.connect(self.is_delete_record_btn_clicked)
        self.table.setCellWidget(current_row_count, 4, delete_btn)
        self.refresh()



    def is_show_records_btn_clicked(self):
        sender = self.sender()
        if sender.text() == "Show records":
            if self.are_all_dates_valid() == True and self.are_all_amount_valid_value() == True:
                total_income = 0
                total_expenditure = 0

                salary = 0
                financial_earnings = 0
                other_income = 0

                utility_bill = 0
                food = 0
                transport = 0
                saving = 0
                other_expenditure = 0
                for i in range(self.table.rowCount()):
                    amount = int(self.table.item(i, 3).text())
                    if self.year_combo_box.currentText() == self.table.cellWidget(i, 0).text()[0:4]:
                        if self.months_combo_box.currentText() == "All":
                            if self.table.cellWidget(i, 1).currentText() == "Income":
                                total_income = total_income + amount
                                if self.table.cellWidget(i, 2).currentText() == "Salary":
                                    salary = salary + amount
                                elif self.table.cellWidget(i, 2).currentText() == "Financial Earning":
                                    financial_earnings = financial_earnings + amount
                                elif self.table.cellWidget(i, 2).currentText() == "Others":
                                    other_income = other_income + amount
                            elif self.table.cellWidget(i, 1).currentText() == "Expenditure":
                                total_expenditure = total_expenditure + amount
                                if self.table.cellWidget(i, 2).currentText() == "Utility Bill":
                                    utility_bill = utility_bill + amount
                                elif self.table.cellWidget(i, 2).currentText() == "Food":
                                    food = food + amount
                                elif self.table.cellWidget(i, 2).currentText() == "Transport":
                                    transport = transport + amount
                                elif self.table.cellWidget(i, 2).currentText() == "Saving":
                                    saving = saving + amount
                                elif self.table.cellWidget(i, 2).currentText() == "Others":
                                    other_expenditure = other_expenditure + amount
                        else:
                            if self.months_combo_box.currentText() == self.table.cellWidget(i, 0).text()[5:7]:
                                if self.table.cellWidget(i, 1).currentText() == "Income":
                                    total_income = total_income + amount
                                    if self.table.cellWidget(i, 2).currentText() == "Salary":
                                        salary = salary + amount
                                    elif self.table.cellWidget(i, 2).currentText() == "Financial Earning":
                                        financial_earnings = financial_earnings + amount
                                    elif self.table.cellWidget(i, 2).currentText() == "Others":
                                        other_income = other_income + amount
                                elif self.table.cellWidget(i, 1).currentText() == "Expenditure":
                                    total_expenditure = total_expenditure + amount
                                    if self.table.cellWidget(i, 2).currentText() == "Utility Bill":
                                        utility_bill = utility_bill + amount
                                    elif self.table.cellWidget(i, 2).currentText() == "Food":
                                        food = food + amount
                                    elif self.table.cellWidget(i, 2).currentText() == "Transport":
                                        transport = transport + amount
                                    elif self.table.cellWidget(i, 2).currentText() == "Saving":
                                        saving = saving + amount
                                    elif self.table.cellWidget(i, 2).currentText() == "Others":
                                        other_expenditure = other_expenditure + amount

                print("======================================================")
                print("[", self.year_combo_box.currentText(), "/", self.months_combo_box.currentText(), "] total_income: ", total_income)
                print(" - salary: ", salary)
                print(" - financial_earnings: ", financial_earnings)
                print(" - others: ", other_income)
                print("[", self.year_combo_box.currentText(), "/", self.months_combo_box.currentText(), "] total_expenditure: ", total_expenditure)
                print(" - utility_bill: ", utility_bill)
                print(" - food: ", food)
                print(" - transport: ", transport)
                print(" - saving: ", saving)
                print(" - other_expenditure: ", other_expenditure)



    def are_all_dates_valid(self):
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 0).text() == "Select Date":
                print("Please select date!")
                return False
        return True

    def are_all_amount_valid_value(self):
        for i in range(self.table.rowCount()):
            if self.table.item(i, 3).text().isdigit() != True:
                print("Please provide valid value!")
                self.table.item(i, 3).text().setText("")
                return False
        return True



    def is_load_btn_clicked(self):
        if os.path.exists(self.data_file_name_with_path) == False:
            print("No data file to load!")
        else:
            df = pd.read_csv(self.data_file_name_with_path)

            for i in range(df.shape[0]):
                self.is_add_record_btn_clicked()
            for i in range(df.shape[0]):
                self.table.cellWidget(i, 0).setText(str(df.loc[i][1]))
            for i in range(df.shape[0]):
                self.table.cellWidget(i, 1).setCurrentText(str(df.loc[i][2]))
            for i in range(df.shape[0]):
                self.table.cellWidget(i, 2).setCurrentText(str(df.loc[i][3]))
            for i in range(df.shape[0]):
                item = QTableWidgetItem()
                item.setText(str(df.loc[i][4]))
                self.table.setItem(i, 3, item)


    def is_save_btn_clicked(self):
        if self.table.rowCount() == 0:
            print("No data to save")
        else:
            rows = []
            for i in range(self.table.rowCount()):
                row = [
                    self.table.cellWidget(i, 0).text(),
                    self.table.cellWidget(i, 1).currentText(),
                    self.table.cellWidget(i, 2).currentText(),
                    self.table.item(i, 3).text()
                ]
                rows.append(row)
            df = pd.DataFrame(data=rows, columns=["Date", "Type", "Detail", "Amount"])
            df.to_csv(self.data_file_name_with_path)


    def is_clear_btn_clicked(self):
        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalHeaderLabels(["Date", "Type", "Detail", "Amount", ""])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


    def is_delete_record_btn_clicked(self):
        sender = self.sender()
        self.table.removeRow(sender.current_cell_row)


    def is_select_date_btn_clicked(self):
        sender = self.sender()
        self.dialog = QDialog()
        dialog_hLayout_1 = QHBoxLayout()
        # self.calendar = QCalendarWidget()
        self.calendar = QCalendarWidget_(sender)
        self.calendar.setGridVisible(True)
        dialog_hLayout_1.addWidget(self.calendar)

        dialog_hLayout_2 = QHBoxLayout()
        confirm_btn = QPushButton("Apply")
        confirm_btn.clicked.connect(self.is_confirm_btn_clicked)
        dialog_hLayout_2.addWidget(confirm_btn)

        dialog_vLayout = QVBoxLayout()
        dialog_vLayout.addLayout(dialog_hLayout_1)
        dialog_vLayout.addLayout(dialog_hLayout_2)

        self.dialog.setLayout(dialog_vLayout)
        self.dialog.exec()


    def is_confirm_btn_clicked(self):
        date = self.calendar.selectedDate().toString("yyyy.MM.dd")
        self.calendar.current_btn.setText(date)
        self.dialog.close()


    def refresh(self):
        for i in range(self.table.rowCount()):
            if self.table.cellWidget(i, 1).currentText() == "Income":
                if self.table.cellWidget(i, 2).currentText() not in self.income_type_labels:
                    self.table.cellWidget(i, 2).clear()
                    self.table.cellWidget(i, 2).addItems(self.income_type_labels)
            elif self.table.cellWidget(i, 1).currentText() == "Expenditure":
                if self.table.cellWidget(i, 2).currentText() not in self.expenditure_type_labels:
                    self.table.cellWidget(i, 2).clear()
                    self.table.cellWidget(i, 2).addItems(self.expenditure_type_labels)

    def is_valid_value(self, row, column):
        if self.table.item(row, column).text().isdigit() != True:
            self.table.item(row, column).setText("")


if __name__ == "__main__":
    app = QApplication([])
    main = Main()
    app.exec()
    sys.exit()
