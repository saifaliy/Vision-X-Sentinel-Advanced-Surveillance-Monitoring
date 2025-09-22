import sys
import firebase_admin
from firebase_admin import credentials, db
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit, QHeaderView
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor

# Initialize Firebase
cred = credentials.Certificate("toll-system-e0cab-firebase-adminsdk-e9rsl-8c0690839d.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://toll-system-e0cab-default-rtdb.firebaseio.com/'  # Replace with your database URL
})

class FirebaseTableApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setWindowTitle('CNIC Data Viewer')
        self.setGeometry(100, 100, 900, 600)

        layout = QVBoxLayout()

        self.label = QLabel("CNIC Data from Firebase Realtime Database", self)
        self.label.setFont(QFont("Arial", 18, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        
        self.searchBar = QLineEdit(self)
        self.searchBar.setPlaceholderText("Search by Name...")
        self.searchBar.textChanged.connect(self.filterTable)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["CNIC Number", "Date of Birth", "Date of Issue", "Date of Expiry", "Name"])

        # Styling the table
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setFont(QFont("Arial", 12, QFont.Bold))
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;
                alternate-background-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 10px;
                border: 1px solid #d0d0d0;
            }
            QTableWidget::item:selected {
                background-color: #3399ff;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #0066cc;
                color: white;
                padding: 8px;
                border: 1px solid #d0d0d0;
            }
        """)
        self.tableWidget.setAlternatingRowColors(True)

        layout.addWidget(self.label)
        layout.addWidget(self.searchBar)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        # Refresh data every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.loadData)
        self.timer.start(5000)

    def loadData(self):
        # Fetch data from Realtime Database
        ref = db.reference('cnic-data')
        data = ref.get()

        # Clear previous data
        self.tableWidget.setRowCount(0)

        if data:
            for i, (key, value) in enumerate(data.items()):
                self.tableWidget.insertRow(i)
                self.tableWidget.setItem(i, 0, QTableWidgetItem(value.get("cnic_number", "")))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(value.get("dob", "")))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(value.get("doi", "")))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(value.get("doe", "")))
                self.tableWidget.setItem(i, 4, QTableWidgetItem(value.get("name", "")))

    def filterTable(self):
        filter_text = self.searchBar.text().lower()
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 4)  # Assuming "Name" is in the 5th column
            self.tableWidget.setRowHidden(i, filter_text not in item.text().lower())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirebaseTableApp()
    ex.show()
    sys.exit(app.exec_())


