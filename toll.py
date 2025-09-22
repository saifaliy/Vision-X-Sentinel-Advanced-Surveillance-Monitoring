import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QFont, QPainter
from PyQt5.QtCore import QDateTime, QSizeF, Qt, QRectF
import firebase_admin
from firebase_admin import credentials, db
import qrcode
from PyQt5.QtPrintSupport import QPrinter

# Initialize Firebasejson
cred = credentials.Certificate("toll-system-e0cab-firebase-adminsdk-e9rsl-8c0690839d.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://toll-system-e0cab-default-rtdb.firebaseio.com/"
})

class TollSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Toll System")
        self.setGeometry(200, 200, 400, 300)
        
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.car_number_label = QLabel("Car Number:")
        self.car_number_input = QLineEdit()
        layout.addWidget(self.car_number_label)
        layout.addWidget(self.car_number_input)

        self.car_model_label = QLabel("Car Model:")
        self.car_model_input = QLineEdit()
        layout.addWidget(self.car_model_label)
        layout.addWidget(self.car_model_input)

        self.entry_button = QPushButton("Generate Entry")
        self.entry_button.clicked.connect(self.generate_entry)
        layout.addWidget(self.entry_button)
        
        self.checkout_label = QLabel("Enter Car Number for Checkout:")
        self.checkout_input = QLineEdit()
        layout.addWidget(self.checkout_label)
        layout.addWidget(self.checkout_input)

        self.checkout_button = QPushButton("Checkout Car")
        self.checkout_button.clicked.connect(self.checkout_car)
        layout.addWidget(self.checkout_button)

        self.print_slip_button = QPushButton("Print Slip")
        self.print_slip_button.clicked.connect(self.print_slip)
        layout.addWidget(self.print_slip_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def generate_entry(self):
        name = self.name_input.text()
        car_number = self.car_number_input.text()
        car_model = self.car_model_input.text()
        entry_time = QDateTime.currentDateTime().toString()

        if not name or not car_number or not car_model:
            QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return
        
        data = {
            "name": name,
            "car_number": car_number,
            "car_model": car_model,
            "entry_time": entry_time,
            "out_time": ""
        }
        
        # Save to Firebase
        ref = db.reference("entries")
        ref.push(data)

        QMessageBox.information(self, "Entry Generated", "Entry generated.")

    def checkout_car(self):
        car_number = self.checkout_input.text()
        out_time = QDateTime.currentDateTime().toString()

        if not car_number:
            QMessageBox.warning(self, "Input Error", "Please enter car number.")
            return
        
        # Search for the entry with the given car number
        ref = db.reference("entries")
        entries = ref.get()
        if entries:
            for entry_id, entry in entries.items():
                if entry["car_number"] == car_number and not entry["out_time"]:
                    ref.child(entry_id).update({"out_time": out_time})
                    QMessageBox.information(self, "Checkout Successful", "Car checked out successfully.")
                    return

        QMessageBox.warning(self, "Error", "Car number not found or already checked out.")

    def print_slip(self):
        car_number = self.car_number_input.text()
        if not car_number:
            QMessageBox.warning(self, "Input Error", "Please enter car number.")
            return

        # Get other relevant data
        name = self.name_input.text()
        car_model = self.car_model_input.text()
        entry_time = QDateTime.currentDateTime().toString()

        # Generate QR code containing all the data
        qr_data = f"Name: {name}\nCar Number: {car_number}\nCar Model: {car_model}\nEntry Time: {entry_time}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Save QR code to a temporary file
        qr_image_path = "temp_qr_code.png"
        qr_image.save(qr_image_path)

        # Print slip
        self.print_slip_dialog(qr_image_path, car_number)

    def print_slip_dialog(self, file_path, car_number):
        printer = QPrinter(QPrinter.HighResolution)

        # Set printer options
        printer.setPageSize(QPrinter.Custom)
        printer.setFullPage(False)
        printer.setResolution(300)  # Set printer resolution

        # Open file dialog to choose printer
        printer_dialog = QFileDialog(self)
        printer_dialog.setOption(QFileDialog.DontUseNativeDialog)
        printer_dialog.setAcceptMode(QFileDialog.AcceptSave)
        printer_dialog.setNameFilter("Printer (*.*)")

        if printer_dialog.exec_() == QFileDialog.Accepted:
            printer_path = printer_dialog.selectedFiles()[0]
        else:
            return

        printer.setOutputFileName(printer_path)

        painter = QPainter(printer)
        pixmap = QPixmap(file_path)

        # Calculate slip size based on content
        slip_width = max(300, pixmap.width() + 200)
        slip_height = pixmap.height() + 300

        # Set paper size
        printer.setPaperSize(QSizeF(slip_width, slip_height), QPrinter.Point)

        # Start painting slip
        painter.begin(printer)

        # Calculate text position
        text_x = (slip_width - pixmap.width()) / 2
        text_y = 50

        # Draw company name
        company_font = QFont("Arial", 16, QFont.Bold)
        painter.setFont(company_font)
        painter.drawText(QRectF(0, text_y, slip_width, 50), Qt.AlignCenter, "VSNT P")

        # Draw car number
        car_number_font = QFont("Arial", 12)
        text_y += 50  # Increase Y position for next element
        painter.setFont(car_number_font)
        painter.drawText(QRectF(0, text_y, slip_width, 50), Qt.AlignCenter, f"Car Number: {car_number}")

        # Draw QR code
        painter.drawPixmap(QRectF((slip_width - pixmap.width()) / 2, text_y + 50, pixmap.width(), pixmap.height()), pixmap)

        # End painting
        painter.end()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TollSystem()
    window.show()
    sys.exit(app.exec_())
