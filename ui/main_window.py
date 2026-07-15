import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QStackedWidget, 
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QCursor

# Kita gunakan try-except agar script tetap bisa jalan meskipun file lain belum sempurna
try:
    from ui.dashboard import Dashboard
    from ui.calculator import CalculatorWidget
    from ui.history import HistoryWidget
    from ui.settings import SettingsWidget
except ImportError:
    # Fallback jika dashboard.py tidak ditemukan di path yang benar
    class Dashboard(QWidget):
        def __init__(self, db_manager=None):
            super().__init__()
            layout = QVBoxLayout(self)
            layout.addWidget(QLabel("Dashboard Module Not Found.\nPlease ensure 'ui/dashboard.py' exists.", alignment=Qt.AlignmentFlag.AlignCenter))

class PlaceholderWidget(QWidget):
    """Widget sementara untuk halaman yang belum dibuat (seperti Settings/History)"""
    def __init__(self, title, color):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"font-size: 24px; color: {color}; font-weight: bold;")
        layout.addWidget(label)

class MainWindow(QMainWindow):
    def __init__(self, db_manager=None):
        super().__init__()
        self.setWindowTitle("MerchantDash - OmniTrade Hub")
        self.setMinimumSize(1100, 700)
        
        # Database Manager diterima dari app.py dan di-pass ke child widget
        self.db = db_manager 
        
        self.init_ui()
        self.apply_global_styles()

    def init_ui(self):
        # Widget Utama (Container untuk seluruh jendela)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout Utama (Horizontal: Sidebar Kiri + Konten Kanan)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Setup Sidebar
        self.create_sidebar()
        
        # 2. Setup Area Konten (Stacked Widget)
        self.content_area = QStackedWidget()
        self.content_area.setObjectName("content_area")
        self.main_layout.addWidget(self.content_area)

        self.page_dashboard = Dashboard(db_manager=self.db)
        
        # Integrasi Real Calculator Widget
        try:
            self.page_calculator = CalculatorWidget()
        except NameError:
            self.page_calculator = PlaceholderWidget("Smart Pricing Calculator\n(Widget Gagal Dimuat)", "#89b4fa")
            
        try:
            self.page_history = HistoryWidget(db_manager=self.db)
        except NameError:
            self.page_history = PlaceholderWidget("Transaction History\n(Gagal Dimuat)", "#f9e2af")
            
        try:
            self.page_settings = SettingsWidget(db_manager=self.db)
        except NameError:
            self.page_settings = PlaceholderWidget("Application Settings\n(Gagal Dimuat)", "#a6adc8")

        # Menambahkan halaman ke Stacked Widget
        self.content_area.addWidget(self.page_dashboard)   # Index 0
        self.content_area.addWidget(self.page_calculator)  # Index 1
        self.content_area.addWidget(self.page_history)     # Index 2
        self.content_area.addWidget(self.page_settings)    # Index 3

        # Set Halaman Default
        self.nav_buttons[0].setChecked(True)
        self.switch_page(0)

    def create_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 30, 0, 30)
        sidebar_layout.setSpacing(10)

        # Logo / Judul Aplikasi di Sidebar
        app_title = QLabel("MerchantDash")
        app_title.setObjectName("app_title")
        app_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(app_title)
        
        app_subtitle = QLabel("OmniTrade Hub")
        app_subtitle.setObjectName("app_subtitle")
        app_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(app_subtitle)
        
        sidebar_layout.addSpacing(30) # Spasi setelah logo

        # Definisi Menu Navigasi
        menus = [
            ("📊 Dashboard", 0),
            ("🧮 Calculator", 1),
            ("📝 History", 2),
            ("⚙️ Settings", 3)
        ]
        
        self.nav_buttons = []

        # Membuat tombol navigasi
        for text, index in menus:
            btn = QPushButton(text)
            btn.setObjectName("nav_button")
            btn.setCheckable(True) # Agar tombol bisa berstatus "Aktif"
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            
            # Lambda dengan default argument untuk menghindari masalah late binding
            btn.clicked.connect(lambda checked, idx=index: self.switch_page(idx))
            
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch() # Mendorong tombol ke atas

        # Label Versi di bagian bawah
        version_label = QLabel("v1.0.0-beta")
        version_label.setObjectName("version_label")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)

        self.main_layout.addWidget(self.sidebar)

    def switch_page(self, index):
        """Fungsi untuk mengganti halaman dan mengubah style tombol aktif"""
        self.content_area.setCurrentIndex(index)
        
        # Update status checkable untuk pewarnaan CSS
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setChecked(True)
            else:
                btn.setChecked(False)

    def apply_global_styles(self):
        self.setStyleSheet("""
            /* Gaya Global Base */
            QMainWindow, QWidget#content_area {
                background-color: #1e1e2e; /* Catppuccin Base */
            }
            
            /* Sidebar Panel */
            QFrame#sidebar {
                background-color: #11111b; /* Catppuccin Crust - Lebih gelap dari background */
                border-right: 1px solid #313244;
            }
            
            /* Judul Aplikasi */
            QLabel#app_title {
                color: #cba6f7; /* Mauve/Ungu */
                font-size: 24px;
                font-weight: 800;
                font-family: 'Segoe UI', Arial;
            }
            QLabel#app_subtitle {
                color: #a6adc8; /* Subtext */
                font-size: 12px;
                font-family: 'Segoe UI', Arial;
                margin-bottom: 20px;
            }
            QLabel#version_label {
                color: #585b70;
                font-size: 11px;
            }
            
            /* Tombol Navigasi Sidebar */
            QPushButton#nav_button {
                background-color: transparent;
                color: #a6adc8;
                border: none;
                text-align: left;
                padding: 15px 25px;
                font-size: 15px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial;
                border-left: 4px solid transparent; /* Border kiri transparan secara default */
            }
            
            /* Efek Hover Tombol */
            QPushButton#nav_button:hover {
                background-color: #181825;
                color: #cdd6f4;
            }
            
            /* Efek Tombol Saat Aktif (Checked) */
            QPushButton#nav_button:checked {
                background-color: #313244; /* Surface 0 */
                color: #cba6f7; /* Teks ungu saat aktif */
                border-left: 4px solid #cba6f7; /* Garis indikator ungu di kiri */
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Optional: Set font global (bisa juga via CSS)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())