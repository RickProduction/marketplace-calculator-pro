from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QAbstractItemView, QDialog, QFormLayout, 
                             QLineEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class AddTransactionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Transaksi Manual")
        self.setFixedSize(400, 450)
        self.setStyleSheet("""
            QDialog { background-color: #1e1e2e; color: #cdd6f4; font-family: 'Segoe UI'; }
            QLabel { font-size: 14px; font-weight: bold; color: #a6adc8; }
            QLineEdit, QComboBox { 
                background-color: #313244; color: #cdd6f4; 
                border: 1px solid #45475a; border-radius: 6px; padding: 8px; font-size: 14px;
            }
            QPushButton {
                background-color: #cba6f7; color: #11111b; border: none; border-radius: 6px;
                padding: 10px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #b4befe; }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(15)

        self.cb_market = QComboBox()
        self.cb_market.addItems(["U7BUY", "Eldorado"])
        layout.addRow("Marketplace:", self.cb_market)

        self.cb_category = QComboBox()
        self.cb_category.addItems(["Item", "Boosting", "Account"])
        layout.addRow("Category:", self.cb_category)

        self.inp_target = QLineEdit("0.00")
        layout.addRow("Target Amount ($):", self.inp_target)

        self.inp_listing = QLineEdit("0.00")
        layout.addRow("Listing Price ($):", self.inp_listing)

        self.inp_net = QLineEdit("0.00")
        layout.addRow("Net Income ($):", self.inp_net)
        
        self.inp_buyer = QLineEdit("0.00")
        layout.addRow("Buyer Paid ($):", self.inp_buyer)

        self.cb_status = QComboBox()
        self.cb_status.addItems(["Listed", "Sold", "Completed"])
        layout.addRow("Status:", self.cb_status)

        # Tombol Simpan
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Simpan Transaksi")
        btn_save.clicked.connect(self.accept) # Menutup dialog dengan status Accepted
        btn_layout.addWidget(btn_save)
        layout.addRow(btn_layout)

    def get_data(self):
        try:
            return {
                "marketplace": self.cb_market.currentText(),
                "category": self.cb_category.currentText(),
                "target_amount": float(self.inp_target.text()),
                "listing_price": float(self.inp_listing.text()),
                "net_income": float(self.inp_net.text()),
                "buyer_paid": float(self.inp_buyer.text()),
                "status": self.cb_status.currentText(),
                "notes": "Manual Entry"
            }
        except ValueError:
            return None # Jika user memasukkan teks selain angka

class HistoryWidget(QWidget):
    def __init__(self, db_manager=None):
        super().__init__()
        self.db = db_manager
        self.init_ui()
        self.load_data()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header dengan Tombol Aksi
        header_layout = QHBoxLayout()
        title = QLabel("Transaction History")
        title.setObjectName("history_title")
        header_layout.addWidget(title)

        self.btn_add = QPushButton("➕ Tambah Manual")
        self.btn_add.setObjectName("btn_action")
        self.btn_add.clicked.connect(self.add_manual_transaction)
        
        self.btn_delete = QPushButton("🗑️ Hapus Terpilih")
        self.btn_delete.setObjectName("btn_danger")
        self.btn_delete.clicked.connect(self.delete_selected)

        header_layout.addStretch()
        header_layout.addWidget(self.btn_add)
        header_layout.addWidget(self.btn_delete)
        main_layout.addLayout(header_layout)

        # Setup Tabel
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Date", "Marketplace", "Category", 
            "Target ($)", "Listed ($)", "Net ($)", "Status"
        ])
        
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        main_layout.addWidget(self.table)
        self.apply_styles()

    def load_data(self):
        if not self.db:
            return

        self.table.setRowCount(0)
        transactions = self.db.get_all_transactions(limit=200)
        self.table.setRowCount(len(transactions))
        
        for row_idx, tx in enumerate(transactions):
            items = [
                QTableWidgetItem(str(tx['id'])),
                QTableWidgetItem(str(tx['transaction_date']).split(' ')[0]),
                QTableWidgetItem(tx['marketplace']),
                QTableWidgetItem(tx['category']),
                QTableWidgetItem(f"${tx['target_amount']:.2f}"),
                QTableWidgetItem(f"${tx['listing_price']:.2f}"),
                QTableWidgetItem(f"${tx['net_income']:.2f}"),
                QTableWidgetItem(tx['status'])
            ]

            for col_idx, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                # Pewarnaan Status
                if col_idx == 7:
                    if tx['status'] == 'Completed': item.setForeground(QColor("#a6e3a1"))
                    elif tx['status'] == 'Sold': item.setForeground(QColor("#f9e2af"))
                    elif tx['status'] == 'Listed': item.setForeground(QColor("#89b4fa"))
                self.table.setItem(row_idx, col_idx, item)

    def add_manual_transaction(self):
        dialog = AddTransactionDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data and self.db:
                self.db.add_transaction(**data)
                self.load_data()
            elif not data:
                QMessageBox.warning(self, "Error", "Input nominal harus berupa angka yang valid!")

    def delete_selected(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Info", "Pilih baris yang ingin dihapus terlebih dahulu.")
            return

        row = selected_rows[0].row()
        tx_id = self.table.item(row, 0).text() # Ambil ID dari kolom pertama

        reply = QMessageBox.question(
            self, "Konfirmasi Hapus", 
            f"Apakah Anda yakin ingin menghapus Transaksi ID: {tx_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes and self.db:
            self.db.delete_transaction(tx_id)
            self.load_data()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { color: #cdd6f4; font-family: 'Segoe UI'; }
            QLabel#history_title { font-size: 24px; font-weight: bold; color: #f9e2af; }
            
            QPushButton#btn_action {
                background-color: #a6e3a1; color: #11111b; border: none; border-radius: 8px;
                padding: 10px 20px; font-weight: bold; font-size: 14px;
            }
            QPushButton#btn_action:hover { background-color: #8bd5ca; }
            
            QPushButton#btn_danger {
                background-color: #f38ba8; color: #11111b; border: none; border-radius: 8px;
                padding: 10px 20px; font-weight: bold; font-size: 14px;
            }
            QPushButton#btn_danger:hover { background-color: #eba0ac; }
            
            QTableWidget {
                background-color: #181825; border-radius: 12px; border: none; padding: 10px;
            }
            QTableWidget::item { padding: 12px; border-bottom: 1px solid #313244; }
            QTableWidget::item:selected { background-color: #313244; }
            QHeaderView::section {
                background-color: #181825; color: #a6adc8; padding: 10px;
                font-weight: bold; font-size: 14px; border: none; border-bottom: 2px solid #313244;
            }
        """)