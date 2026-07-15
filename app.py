import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, 
                             QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QDoubleValidator

class CalculatorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MerchantDash - Smart Pricing")
        self.setFixedSize(450, 550)
        self.init_ui()

    def init_ui(self):
        # Main Widget & Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 40, 30, 40)
        main_layout.setSpacing(20)

        # Stylesheet (Modern Dark Theme - Catppuccin Mocha Inspired)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; }
            QLabel { color: #cdd6f4; font-family: 'Segoe UI'; font-size: 14px; }
            QLabel#title { color: #89b4fa; font-size: 24px; font-weight: bold; }
            QLabel#result_label { color: #a6e3a1; font-size: 36px; font-weight: bold; }
            
            QLineEdit { 
                background-color: #313244; color: #cdd6f4; 
                border: 2px solid #45475a; border-radius: 10px; 
                padding: 12px; font-size: 16px; font-weight: bold;
            }
            QLineEdit:focus { border: 2px solid #89b4fa; background-color: #1e1e2e;}
            
            QComboBox {
                background-color: #313244; color: #cdd6f4;
                border: 2px solid #45475a; border-radius: 10px;
                padding: 12px; font-size: 14px;
            }
            QComboBox::drop-down { border: 0px; }
            
            QPushButton {
                background-color: #89b4fa; color: #11111b;
                border: none; border-radius: 10px;
                padding: 15px; font-size: 16px; font-weight: bold;
            }
            QPushButton:hover { background-color: #b4befe; }
            QPushButton:pressed { background-color: #74c7ec; }
            
            QFrame#card {
                background-color: #181825; border-radius: 15px;
            }
        """)

        # Title
        title = QLabel("Pricing Calculator")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Marketplace Selector
        self.combo_market = QComboBox()
        self.combo_market.addItems([
            "U7BUY (Target Harga Pas Pembeli)", 
            "Eldorado - Boosting (Target Bersih)", 
            "Eldorado - Item (Target Bersih)"
        ])
        self.combo_market.currentIndexChanged.connect(self.calculate_price)
        main_layout.addWidget(self.combo_market)

        # Input Field
        self.input_label = QLabel("Masukkan Nominal Target (USD):")
        main_layout.addWidget(self.input_label)

        self.input_target = QLineEdit()
        self.input_target.setPlaceholderText("Contoh: 10.00")
        # Hanya menerima angka dan desimal
        self.input_target.setValidator(QDoubleValidator(0.99, 99999.99, 2)) 
        self.input_target.textChanged.connect(self.calculate_price)
        main_layout.addWidget(self.input_target)

        # Result Card
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 30, 20, 30)
        
        self.desc_label = QLabel("Harga yang harus Anda pasang:")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label = QLabel("$0.00")
        self.result_label.setObjectName("result_label")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(self.desc_label)
        card_layout.addWidget(self.result_label)
        main_layout.addWidget(card)
        
        main_layout.addStretch()

        # Copy Button
        self.btn_copy = QPushButton("Copy Harga Jual")
        self.btn_copy.clicked.connect(self.copy_to_clipboard)
        main_layout.addWidget(self.btn_copy)

    def calculate_price(self):
        text = self.input_target.text().replace(',', '.')
        if not text:
            self.result_label.setText("$0.00")
            return
            
        try:
            target = float(text)
            mode = self.combo_market.currentIndex()
            seller_price = 0.0

            if mode == 0:   # U7BUY
                seller_price = target / 1.10
            elif mode == 1: # Eldorado Boosting
                seller_price = target / 0.90
            elif mode == 2: # Eldorado Item
                seller_price = target / 0.85

            # Menampilkan 4 angka di belakang koma untuk akurasi Marketplace
            self.result_label.setText(f"${seller_price:.4f}")
            self.current_result = f"{seller_price:.4f}"
            
        except ValueError:
            self.result_label.setText("Invalid")

    def copy_to_clipboard(self):
        if hasattr(self, 'current_result'):
            QApplication.clipboard().setText(self.current_result)
            self.btn_copy.setText("Tersalin!")
            # Reset text after 2 seconds
            import threading
            threading.Timer(2.0, lambda: self.btn_copy.setText("Copy Harga Jual")).start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorUI()
    window.show()
    sys.exit(app.exec())