from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QGroupBox, QFormLayout, QHeaderView, QMessageBox
)
from PySide6.QtGui import QFont
from app.models import Customer, Bill
import re

class BillingUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Billing System")
        self.setGeometry(100, 100, 500, 500)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Customer Details Group
        customer_group = QGroupBox("Customer Details")
        customer_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        customer_layout.addRow("Customer Name:", self.name_input)
        customer_layout.addRow("Customer Email:", self.email_input)
        customer_group.setLayout(customer_layout)

        # Bill Details Group
        bill_group = QGroupBox("Bill Details")
        bill_layout = QFormLayout()
        self.amount_input = QLineEdit()
        bill_layout.addRow("Bill Amount:", self.amount_input)
        bill_group.setLayout(bill_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Save Bill")
        self.submit_button.clicked.connect(self.add_bill)
        self.view_button = QPushButton("View Bills")
        self.view_button.clicked.connect(self.view_bills)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.view_button)

        # Table Widget for displaying bills
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Customer", "Email", "Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Apply Styling
        customer_group.setFont(QFont("Arial", 10, QFont.Bold))
        bill_group.setFont(QFont("Arial", 10, QFont.Bold))
        self.submit_button.setFont(QFont("Arial", 10))
        self.view_button.setFont(QFont("Arial", 10))
        self.table.setFont(QFont("Arial", 10))

        # Add widgets to the main layout
        main_layout.addWidget(customer_group)
        main_layout.addWidget(bill_group)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def add_bill(self):
        """Stores the bill in the database and updates the table."""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        amount = self.amount_input.text().strip()

        if not name or not email or not amount:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return
        
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email):
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address!")
            return
    
        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Bill amount must be a valid number!")
            return

        # Store customer and bill in the database
        customer_id = Customer.add_customer(name, email)
        Bill.add_bill(customer_id, amount)

        self.view_bills()
        self.name_input.clear()
        self.email_input.clear()
        self.amount_input.clear()

        QMessageBox.information(self, "Success", "Bill added successfully!")

    def view_bills(self):
        """Fetches bills from the database and displays them."""
        self.table.setRowCount(0)  # Clear existing table data

        for row_index, bill in enumerate(Bill.get_bills()):
            self.table.insertRow(row_index)
            for col_index, data in enumerate(bill):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(data)))
