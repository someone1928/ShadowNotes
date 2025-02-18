from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QInputDialog, QListWidget, QMessageBox
from PyQt6.QtGui import QFont
from encryption import EncryptionManager
import database
import os
from config import verify_password
from PyQt6.QtWidgets import QLineEdit
from config import increment_failed_attempts, get_failed_attempts, reset_failed_attempts, self_destruct

class ShadowNotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShadowNotes - Encrypted Notes")
        self.setGeometry(200, 200, 600, 500)
        
        self.password = self.get_password()
        if not self.password:
            exit()
        
        if not verify_password(self.password):
            QMessageBox.critical(self, "Error", "Incorrect Password! Exiting...")
            os.system("python main.py")
            # exit()

        self.encryption_manager = EncryptionManager(self.password)
        database.init_db()
        
        self.initUI()
        self.load_notes()

    def get_password(self):
        password, ok = QInputDialog.getText(self, "Password Required", "Enter your password:", QLineEdit.EchoMode.Password)
        return password if ok else None
    
    def initUI(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.setFont(QFont("Courier", 12))
        
        self.save_button = QPushButton("Save Note")
        self.save_button.clicked.connect(self.save_note)
        
        self.read_button = QPushButton("Read Note")
        self.read_button.clicked.connect(self.read_selected_note)
        
        self.notes_list = QListWidget()

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.save_button)
        layout.addWidget(self.read_button)
        layout.addWidget(self.notes_list)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def save_note(self):
        title, ok = QInputDialog.getText(self, "Note Title", "Enter title:")
        if ok and title:
            content = self.text_edit.toPlainText()
            encrypted_content = self.encryption_manager.encrypt_text(content)
            database.save_encrypted_note(title, encrypted_content)
            self.notes_list.addItem(title)
            self.text_edit.clear()
    
    def load_notes(self):
        notes = database.get_all_notes()
        for note in notes:
            self.notes_list.addItem(note[1])
    
    def read_selected_note(self):
        item = self.notes_list.currentItem()
        if item:
            notes = database.get_all_notes()
            for note in notes:
                if note[1] == item.text():
                    try:
                        decrypted_content = self.encryption_manager.decrypt_text(note[2])
                        self.text_edit.setPlainText(decrypted_content)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Decryption failed: {e}")

    def get_password(self):
        for _ in range(3):
            password, ok = QInputDialog.getText(self, "Password Required", "Enter your password:", QLineEdit.EchoMode.Password)
            if ok:
                try:
                    test_cipher = EncryptionManager(password)
                    reset_failed_attempts()
                    return password
                except Exception:
                    attempts = increment_failed_attempts()
                    print(f"⚠️ Incorrect password! Attempt {attempts}/3")

            if get_failed_attempts() >= 3:
                self_destruct()
                exit()
        
                # exit() 