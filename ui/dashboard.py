import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QPushButton, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

class Dashboard(QWidget):
    def __init__(self, db_manager=None):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_data()

    def init_ui(self):
        # Layout Utama
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(25)

        # Header Title
        header_layout = QHBoxLayout()
        title = QLabel("Dashboard Overview")
        title.setObjectName("main_title")
        header_layout.addWidget(title)
        
        # Tombol Refresh
        self.btn_refresh = QPushButton("↻ Refresh Data")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.load_data)
        header_layout.addWidget(self.btn_refresh, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.main_layout.addLayout(header_layout)

        # --- STATS CARDS SECTION ---
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(20)
        
        # Inisialisasi Kartu
        self.card_orders = self.create_stat_card("Total Orders", "0", "#89b4fa")     # Biru
        self.card_revenue = self.create_stat_card("Net Revenue (Cair)", "$0.00", "#a6e3a1") # Hijau
        self.card_pending = self.create_stat_card("Pending Income", "$0.00", "#f9e2af")  # Kuning
        
        self.stats_layout.addWidget(self.card_orders)
        self.stats_layout.addWidget(self.card_revenue)
        self.stats_layout.addWidget(self.card_pending)
        
        self.main_layout.addLayout(self.stats_layout)

        # --- TABLE SECTION ---
        table_label = QLabel("Recent Transactions")
        table_label.setObjectName("section_title")
        self.main_layout.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Marketplace", "Category", 
            "Target ($)", "Listed ($)", "Net ($)", "Status"
        ])
        
        # Pengaturan Tabel
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setVisible(False)
        
        # Resize Header
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Kolom ID
        
        self.main_layout.addWidget(self.table)

        # Apply Stylesheet Global untuk Dashboard
        self.apply_styles()

    def create_stat_card(self, title_text, value_text, color_hex):
        """Fungsi helper untuk membuat kartu statistik."""
        card = QFrame()
        card.setObjectName("stat_card")
        layout = QVBoxLayout(card)
        
        title = QLabel(title_text)
        title.setObjectName("card_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        value = QLabel(value_text)
        value.setObjectName("card_value")
        value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value.setStyleSheet(f"color: {color_hex};")
        
        layout.addWidget(title)
        layout.addWidget(value)
        return card

    def load_data(self):
        """Memuat data dari database dan memperbarui UI."""
        # Jika database belum disambungkan, kita pakai data dummy untuk preview UI
        if not self.db:
            self.load_dummy_data()
            return

        # 1. Update Statistik
        stats = self.db.get_dashboard_stats()
        self.card_orders.findChild(QLabel, "card_value").setText(str(stats["total_orders"]))
        self.card_revenue.findChild(QLabel, "card_value").setText(f"${stats['total_revenue']:.2f}")
        self.card_pending.findChild(QLabel, "card_value").setText(f"${stats['pending_revenue']:.2f}")

        # 2. Update Tabel
        transactions = self.db.get_all_transactions(limit=100)
        self.table.setRowCount(len(transactions))
        
        for row, tx in enumerate(transactions):
            self.add_table_row(row, tx)

    def load_dummy_data(self):
        """Preview data jika database belum terhubung (untuk testing UI)."""
        self.card_orders.findChild(QLabel, "card_value").setText("142")
        self.card_revenue.findChild(QLabel, "card_value").setText("$1,240.50")
        self.card_pending.findChild(QLabel, "card_value").setText("$320.00")
        
        dummy_txs = [
            {"id": 1, "transaction_date": "2024-05-20", "marketplace": "U7BUY", "category": "Item", "target_amount": 10.00, "listing_price": 9.09, "net_income": 9.09, "status": "Completed"},
            {"id": 2, "transaction_date": "2024-05-21", "marketplace": "Eldorado", "category": "Boosting", "target_amount": 50.00, "listing_price": 55.55, "net_income": 50.00, "status": "Sold"},
            {"id": 3, "transaction_date": "2024-05-21", "marketplace": "Eldorado", "category": "Account", "target_amount": 100.00, "listing_price": 117.65, "net_income": 100.00, "status": "Listed"},
        ]
        
        self.table.setRowCount(len(dummy_txs))
        for row, tx in enumerate(dummy_txs):
            self.add_table_row(row, tx)

    def add_table_row(self, row_idx, tx):
        """Memasukkan satu baris data ke dalam tabel dengan warna kustom."""
        # Helper format angka
        def fmt(val): return f"${val:.2f}"

        items = [
            QTableWidgetItem(str(tx['id'])),
            QTableWidgetItem(str(tx['transaction_date']).split(' ')[0]), # Hanya ambil tanggal
            QTableWidgetItem(tx['marketplace']),
            QTableWidgetItem(tx['category']),
            QTableWidgetItem(fmt(tx['target_amount'])),
            QTableWidgetItem(fmt(tx['listing_price'])),
            QTableWidgetItem(fmt(tx['net_income'])),
            QTableWidgetItem(tx['status'])
        ]

        # Penyesuaian UI Item Tabel
        for col_idx, item in enumerate(items):
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Pewarnaan untuk kolom Status (Indikator Visual)
            if col_idx == 7:
                if tx['status'] == 'Completed':
                    item.setForeground(QColor("#a6e3a1")) # Hijau
                elif tx['status'] == 'Sold':
                    item.setForeground(QColor("#f9e2af")) # Kuning
                elif tx['status'] == 'Listed':
                    item.setForeground(QColor("#89b4fa")) # Biru
                    
            self.table.setItem(row_idx, col_idx, item)

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', Arial;
            }
            QLabel#main_title {
                font-size: 28px;
                font-weight: bold;
                color: #cba6f7; /* Ungu/Mauve */
            }
            QLabel#section_title {
                font-size: 18px;
                font-weight: bold;
                color: #cdd6f4;
                margin-top: 15px;
            }
            
            /* Style Kartu Statistik */
            QFrame#stat_card {
                background-color: #181825;
                border-radius: 15px;
                padding: 20px;
            }
            QLabel#card_title {
                font-size: 14px;
                color: #a6adc8;
            }
            QLabel#card_value {
                font-size: 32px;
                font-weight: bold;
                margin-top: 10px;
            }
            
            /* Style Tabel */
            QTableWidget {
                background-color: #181825;
                border-radius: 15px;
                border: none;
                padding: 10px;
            }
            QTableWidget::item {
                padding: 15px;
                border-bottom: 1px solid #313244;
            }
            QTableWidget::item:selected {
                background-color: #313244;
            }
            QHeaderView::section {
                background-color: #181825;
                color: #a6adc8;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border: none;
                border-bottom: 2px solid #313244;
            }
            
            /* Style Scrollbar */
            QScrollBar:vertical {
                border: none;
                background: #1e1e2e;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #45475a;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #585b70;
            }
            
            /* Style Button Refresh */
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
            QPushButton:pressed {
                background-color: #585b70;
            }
        """)

# --- Untuk Test Run UI secara Standalone ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Dashboard()
    window.resize(900, 600)
    window.setWindowTitle("MerchantDash - Dashboard Preview")
    window.show()
    sys.exit(app.exec())