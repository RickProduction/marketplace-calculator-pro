from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QFormLayout, 
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt

class SettingsWidget(QWidget):
    def __init__(self, db_manager=None):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        title = QLabel("Application Settings")
        title.setObjectName("settings_title")
        main_layout.addWidget(title)

        subtitle = QLabel("Konfigurasi API Keys untuk sinkronisasi otomatis (Fitur Mendatang).")
        subtitle.setObjectName("settings_subtitle")
        main_layout.addWidget(subtitle)

        form_card = QFrame()
        form_card.setObjectName("form_card")
        form_layout = QFormLayout(form_card)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)

        # Input Eldorado API
        self.inp_eldorado_api = QLineEdit()
        self.inp_eldorado_api.setPlaceholderText("Masukkan Eldorado API Key...")
        self.inp_eldorado_api.setEchoMode(QLineEdit.EchoMode.Password) # Disembunyikan seperti password
        form_layout.addRow("Eldorado API Key:", self.inp_eldorado_api)

        # Input U7BUY API
        self.inp_u7buy_api = QLineEdit()
        self.inp_u7buy_api.setPlaceholderText("Masukkan U7BUY API Key...")
        self.inp_u7buy_api.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("U7BUY API Key:", self.inp_u7buy_api)

        main_layout.addWidget(form_card)

        action_layout = QHBoxLayout()
        action_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        self.btn_save = QPushButton("💾 Simpan Pengaturan")
        self.btn_save.setFixedWidth(200)
        self.btn_save.clicked.connect(self.save_settings)
        action_layout.addWidget(self.btn_save)
        
        main_layout.addLayout(action_layout)
        main_layout.addStretch()
        self.apply_styles()

    def load_settings(self):
        """Memuat kunci API yang sudah tersimpan di Database saat halaman dibuka."""
        if self.db:
            eldorado_key = self.db.get_setting("eldorado_api_key", "")
            u7buy_key = self.db.get_setting("u7buy_api_key", "")
            
            if eldorado_key: self.inp_eldorado_api.setText(eldorado_key)
            if u7buy_key: self.inp_u7buy_api.setText(u7buy_key)

    def save_settings(self):
        if self.db:
            self.db.save_setting("eldorado_api_key", self.inp_eldorado_api.text())
            self.db.save_setting("u7buy_api_key", self.inp_u7buy_api.text())
            
            QMessageBox.information(self, "Sukses", "Pengaturan berhasil disimpan!")

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { color: #cdd6f4; font-family: 'Segoe UI'; }
            QLabel#settings_title { font-size: 28px; font-weight: bold; color: #a6adc8; }
            QLabel#settings_subtitle { font-size: 14px; color: #7f849c; margin-bottom: 20px; }
            
            QFrame#form_card { background-color: #181825; border-radius: 15px; }
            QLabel { font-size: 16px; font-weight: bold; color: #bac2de; }
            
            QLineEdit {
                background-color: #313244; color: #cdd6f4;
                border: 1px solid #45475a; border-radius: 8px;
                padding: 12px; font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #cba6f7; }
            
            QPushButton {
                background-color: #89b4fa; color: #11111b; border: none; border-radius: 8px;
                padding: 15px; font-size: 16px; font-weight: bold;
            }
            QPushButton:hover { background-color: #b4befe; }
        """)