from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QPushButton, QFrame, 
                             QSpacerItem, QSizePolicy, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QDoubleValidator, QClipboard

try:
    from core.calculator import MarketplaceCalculator
except ImportError:
    # Fallback sederhana jika dijalankan tanpa struktur folder yang benar
    class MarketplaceCalculator:
        @staticmethod
        def get_u7buy_listing_price(target): return target / 1.10
        @staticmethod
        def get_eldorado_listing_price(target, is_item): return target / (0.85 if is_item else 0.90)

class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_result = "0.0000"
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(25)

        # Header Title
        title = QLabel("Smart Pricing Calculator")
        title.setObjectName("calc_title")
        main_layout.addWidget(title)
        
        subtitle = QLabel("Hitung otomatis harga jual yang tepat agar Anda tidak rugi biaya platform.")
        subtitle.setObjectName("calc_subtitle")
        main_layout.addWidget(subtitle)

        # Form Container (Card)
        form_card = QFrame()
        form_card.setObjectName("form_card")
        form_layout = QVBoxLayout(form_card)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)

        # 1. Pilihan Marketplace
        lbl_market = QLabel("Skenario Penjualan:")
        self.combo_market = QComboBox()
        self.combo_market.addItems([
            "U7BUY - Tentukan Harga Pas Pembeli", 
            "Eldorado - Target Bersih Penjual (Kategori Boosting)", 
            "Eldorado - Target Bersih Penjual (Kategori Item)"
        ])
        self.combo_market.currentIndexChanged.connect(self.calculate_price)
        form_layout.addWidget(lbl_market)
        form_layout.addWidget(self.combo_market)

        # 2. Input Target
        lbl_target = QLabel("Nominal Target (USD):")
        self.input_target = QLineEdit()
        self.input_target.setPlaceholderText("Contoh: 10.00")
        
        # Validasi: Hanya menerima format angka desimal (maksimal 99999.99)
        validator = QDoubleValidator(0.00, 99999.99, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.input_target.setValidator(validator)
        self.input_target.textChanged.connect(self.calculate_price)
        
        form_layout.addWidget(lbl_target)
        form_layout.addWidget(self.input_target)
        main_layout.addWidget(form_card)

        # Result Container
        result_card = QFrame()
        result_card.setObjectName("result_card")
        result_layout = QVBoxLayout(result_card)
        result_layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_result_desc = QLabel("Harga Listing yang Harus Anda Pasang:")
        lbl_result_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_result_value = QLabel("$0.0000")
        self.lbl_result_value.setObjectName("result_value")
        self.lbl_result_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        result_layout.addWidget(lbl_result_desc)
        result_layout.addWidget(self.lbl_result_value)
        main_layout.addWidget(result_card)

        # Tombol Aksi
        action_layout = QHBoxLayout()
        action_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        self.btn_copy = QPushButton("📄 Copy Harga Listing")
        self.btn_copy.setFixedWidth(250)
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        action_layout.addWidget(self.btn_copy)
        
        action_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        main_layout.addLayout(action_layout)

        main_layout.addStretch() # Dorong semua elemen ke atas
        self.apply_styles()

    def calculate_price(self):
        text = self.input_target.text().replace(',', '.')
        if not text:
            self.lbl_result_value.setText("$0.0000")
            return
            
        try:
            target = float(text)
            mode = self.combo_market.currentIndex()
            seller_price = 0.0

            if mode == 0:   # U7BUY
                seller_price = MarketplaceCalculator.get_u7buy_listing_price(target)
            elif mode == 1: # Eldorado Boosting
                seller_price = MarketplaceCalculator.get_eldorado_listing_price(target, is_item=False)
            elif mode == 2: # Eldorado Item
                seller_price = MarketplaceCalculator.get_eldorado_listing_price(target, is_item=True)

            self.current_result = f"{seller_price:.4f}"
            self.lbl_result_value.setText(f"${self.current_result}")
            
        except ValueError:
            self.lbl_result_value.setText("Invalid Input")

    def copy_to_clipboard(self):
        if self.current_result != "0.0000":
            clipboard = QApplication.clipboard()
            clipboard.setText(self.current_result)
            
            # Ubah teks tombol sementara sebagai indikator sukses
            self.btn_copy.setText("✅ Berhasil Disalin!")
            self.btn_copy.setStyleSheet("background-color: #a6e3a1; color: #11111b;")
            
            # Kembalikan teks tombol setelah 2 detik menggunakan QTimer (lebih aman dari threading di UI)
            QTimer.singleShot(2000, self.reset_copy_button)
            
    def reset_copy_button(self):
        self.btn_copy.setText("📄 Copy Harga Listing")
        self.btn_copy.setStyleSheet("") # Reset ke style CSS bawaan

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                color: #cdd6f4;
                font-family: 'Segoe UI', Arial;
            }
            QLabel#calc_title {
                font-size: 28px; font-weight: bold; color: #89b4fa;
            }
            QLabel#calc_subtitle {
                font-size: 14px; color: #a6adc8; margin-bottom: 10px;
            }
            QFrame#form_card {
                background-color: #181825; border-radius: 15px;
            }
            QFrame#result_card {
                background-color: #313244; border-radius: 15px;
                border: 2px dashed #45475a;
            }
            QLabel#result_value {
                font-size: 42px; font-weight: 900; color: #a6e3a1;
                margin-top: 10px;
            }
            QLineEdit, QComboBox {
                background-color: #1e1e2e; color: #cdd6f4;
                border: 1px solid #45475a; border-radius: 8px;
                padding: 12px; font-size: 16px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #cba6f7;
            }
            QPushButton {
                background-color: #cba6f7; color: #11111b;
                border: none; border-radius: 8px;
                padding: 15px; font-size: 16px; font-weight: bold;
            }
            QPushButton:hover { background-color: #b4befe; }
            QPushButton:pressed { background-color: #89b4fa; }
        """)