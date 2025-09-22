import sys
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QFrame, QTableWidget, QTableWidgetItem, QMainWindow, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_admin.exceptions import FirebaseError

class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        self.is_login_successful = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Surveillance System Login')
        self.showFullScreen()
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 14px;
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QLineEdit:focus {
                border-color: #2980b9;
            }
            QPushButton {
                background-color: #3f51b5;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                padding: 12px 25px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1a237e;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()

        # Header section for Vision Shield text
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        
        vision_shield_label = QLabel("Vision X Complete Protection Surveilliance System ")
        vision_shield_label.setAlignment(Qt.AlignCenter)
        vision_shield_label.setStyleSheet("""
            
            font-size: 40px;
            font-weight: bold;
            color: black;
            margin: 20px;
            margin-top:60px;
            padding: 20px 30px;
        
            border-radius: 15px;
            border: 3px solid black;
            letter-spacing: 2px;
            min-height: 60px;
        """)
        
        header_layout.addStretch()
        header_layout.addWidget(vision_shield_label)
        header_layout.addStretch()
        header_widget.setLayout(header_layout)
        
        # Content section
        content_widget = QWidget()
        content_layout = QHBoxLayout()

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        logo_label = QLabel()
        pixmap = QPixmap('logo.png')
        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        
        company_name = QLabel("SecureView Surveillance")
        company_name.setAlignment(Qt.AlignCenter)
        company_name.setStyleSheet("font-size: 20px; font-weight: bold; color: ;")
        
        left_layout.addStretch()
        left_layout.addWidget(logo_label)
        left_layout.addWidget(company_name)
        left_layout.addStretch()
        
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_frame.setStyleSheet("background-color: #2c3e50; padding: 20px; border-radius: 10px;")
        form_layout = QVBoxLayout()

        title_label = QLabel('Login to Surveillance System')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; margin-bottom: 15px;")

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("User ID")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        form_layout.addWidget(title_label)
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.login_button)
        form_frame.setLayout(form_layout)

        right_layout.addStretch()
        right_layout.addWidget(form_frame)
        right_layout.addStretch()

        right_widget.setLayout(right_layout)

        content_layout.addWidget(left_widget)
        content_layout.addWidget(right_widget)
        content_widget.setLayout(content_layout)

        # Add widgets to main layout
        main_layout.addWidget(header_widget)
        main_layout.addWidget(content_widget)

        self.setLayout(main_layout)

    def login(self):
        user_id = self.id_input.text()
        password = self.password_input.text()

        if user_id == 'admin' and password == 'admin123':
            self.is_login_successful = True
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid User ID or Password')
class RegistrationForm(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('User Registration')
        self.showFullScreen()
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f2f5;
            }
            QLabel {
                color: #1a237e;
                font-family: 'Segoe UI', sans-serif;
                font-size: 18px;
                font-weight: bold;
                padding: 5px;
            }
            QLineEdit {
                padding: 15px;
                border: 2px solid #3f51b5;
                border-radius: 10px;
                font-size: 16px;
                background-color: white;
                margin: 5px;
                min-width: 400px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #1a237e;
                background-color: #e8eaf6;
            }
            QPushButton {
                background-color: #3f51b5;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding: 15px;
                min-width: 200px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #1a237e;
            }
            QTableWidget {
                background-color: white;
                border: 2px solid #3f51b5;
                border-radius: 10px;
                font-size: 16px;
            }
            QHeaderView::section {
                background-color: #3f51b5;
                color: white;
                padding: 10px;
                font-size: 16px;
            }
        """)

        main_layout = QHBoxLayout()
        
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        logo_label = QLabel()
        pixmap = QPixmap('logo.png')
        scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        
        company_name = QLabel("SecureView Surveillance")
        company_name.setAlignment(Qt.AlignCenter)
        company_name.setStyleSheet("font-size: 28px; color: #1a237e; margin: 20px;")
        
        left_layout.addStretch()
        left_layout.addWidget(logo_label)
        left_layout.addWidget(company_name)
        left_layout.addStretch()
        left_widget.setLayout(left_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 20px;
                margin: 20px;
            }
        """)
        form_layout = QVBoxLayout()

        title_label = QLabel('User Registration')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; margin: 20px;")
        form_layout.addWidget(title_label)

        fields_layout = QGridLayout()
        
        self.name_label = QLabel('Full Name:')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        fields_layout.addWidget(self.name_label, 0, 0)
        fields_layout.addWidget(self.name_input, 0, 1)

        self.email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        fields_layout.addWidget(self.email_label, 1, 0)
        fields_layout.addWidget(self.email_input, 1, 1)

        self.number_label = QLabel('Phone Number:')
        self.number_input = QLineEdit()
        self.number_input.setPlaceholderText("Enter your phone number")
        fields_layout.addWidget(self.number_label, 2, 0)
        fields_layout.addWidget(self.number_input, 2, 1)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        fields_layout.addWidget(self.password_label, 3, 0)
        fields_layout.addWidget(self.password_input, 3, 1)

        self.confirm_password_label = QLabel('Confirm Password:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        fields_layout.addWidget(self.confirm_password_label, 4, 0)
        fields_layout.addWidget(self.confirm_password_input, 4, 1)

        form_layout.addLayout(fields_layout)

        buttons_layout = QHBoxLayout()
        
        self.register_button = QPushButton('Register')
        self.register_button.clicked.connect(self.register)
        self.register_button.setCursor(Qt.PointingHandCursor)
        
        self.show_users_button = QPushButton('Show all the Records')
        self.show_users_button.clicked.connect(self.show_all_users)
        self.show_users_button.setCursor(Qt.PointingHandCursor)
        
        buttons_layout.addWidget(self.register_button)
        buttons_layout.addWidget(self.show_users_button)
        
        form_layout.addLayout(buttons_layout)
        form_frame.setLayout(form_layout)
        
        right_layout.addWidget(form_frame)
        right_widget.setLayout(right_layout)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        
        self.setLayout(main_layout)
    def register(self):
        name = self.name_input.text()
        email = self.email_input.text()
        number = self.number_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if password != confirm_password:
            QMessageBox.warning(self, 'Error', 'Passwords do not match')
        else:
            self.firebase_register(name, email, number, password)

    def firebase_register(self, name, email, number, password):
        try:
            user = auth.create_user(email=email, password=password)
            uid = user.uid
            db = firestore.client()
            user_ref = db.collection('Users').document(uid)
            user_ref.set({
                'Name': name,
                'Number': number,
                'password': password,
                'uid': uid
            })
            QMessageBox.information(self, 'Success', 'Registration Successful')
            self.clear_inputs()
        except FirebaseError as e:
            QMessageBox.warning(self, 'Error', f'Registration Failed: {e}')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error: {e}')

    def clear_inputs(self):
        self.name_input.clear()
        self.email_input.clear()
        self.number_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()

    def show_all_users(self):
        try:
            db = firestore.client()
            users_ref = db.collection('Users')
            all_users = users_ref.stream()

            self.users_window = QWidget()
            self.users_window.showFullScreen()
            self.users_window.setWindowTitle('Database Management')
            self.users_window.setStyleSheet("""
                QWidget {
                    background-color: #f0f2f5;
                }
                QTableWidget {
                    background-color: white;
                    border: 2px solid #3f51b5;
                    border-radius: 15px;
                    padding: 10px;
                    gridline-color: #e0e0e0;
                }
                QHeaderView::section {
                    background-color: #3f51b5;
                    color: white;
                    padding: 12px;
                    font-size: 16px;
                    border: none;
                    font-weight: bold;
                }
                QPushButton {
                    background-color: #3f51b5;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    border-radius: 10px;
                    padding: 12px 25px;
                    margin: 10px;
                }
                QPushButton:hover {
                    background-color: #1a237e;
                }
            """)

            main_layout = QVBoxLayout()
            
            header = QLabel('Database Management of Registered Persons')
            header.setStyleSheet("""
                font-size: 28px;
                color: #0000FF;
                font-weight: bold;
                padding: 20px;
                color: white;
                background-color: #3f51b5;
                border-radius: 10px;
                margin: 10px;
            """)
            header.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(header)

            table = QTableWidget()
            table.setColumnCount(4)
            table.setHorizontalHeaderLabels(['Name', 'Number', 'UID', 'Password'])
            
            for i, user in enumerate(all_users):
                data = user.to_dict()
                table.insertRow(i)
                table.setItem(i, 0, QTableWidgetItem(data['Name']))
                table.setItem(i, 1, QTableWidgetItem(data['Number']))
                table.setItem(i, 2, QTableWidgetItem(data['uid']))
                table.setItem(i, 3, QTableWidgetItem(data['password']))

            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.verticalHeader().setVisible(False)
            table.setShowGrid(True)
            table.setAlternatingRowColors(True)
            
            table_container = QWidget()
            table_layout = QVBoxLayout()
            table_layout.setContentsMargins(50, 20, 50, 20)
            table_layout.addWidget(table)
            table_container.setLayout(table_layout)
            
            main_layout.addWidget(table_container)
            
            # Add back button
            back_button = QPushButton('Back')
            back_button.clicked.connect(self.users_window.close)
            back_button.setCursor(Qt.PointingHandCursor)
            
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(back_button)
            button_layout.addStretch()
            
            main_layout.addLayout(button_layout)
            
            self.users_window.setLayout(main_layout)
            self.users_window.show()
            
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error: {e}')

if __name__ == '__main__':
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate('vsntp-9dd28-firebase-adminsdk-3zomc-6c19fa63a0.json')
    firebase_admin.initialize_app(cred)

    app = QApplication(sys.argv)
    login_form = LoginForm()
    if login_form.exec_() == QDialog.Accepted:
        registration_form = RegistrationForm()
        registration_form.exec_()
    sys.exit(app.exec_())