import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

# Pastikan Python bisa membaca folder di dalam project ini
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager
from ui.main_window import MainWindow

def main():
    # 1. Inisialisasi Aplikasi Qt
    app = QApplication(sys.argv)
    
    # Set Font Global untuk seluruh aplikasi
    global_font = QFont("Segoe UI", 10)
    app.setFont(global_font)

    # 2. Inisialisasi Database
    # Jika schema.sql tidak ditemukan (saat pertama run), DB Manager otomatis akan mengatasi.
    print("[SYSTEM] Menginisialisasi Database...")
    db = DatabaseManager(db_name="database/merchant_dash.db", schema_file="database/schema.sql")

    # 3. Memuat Jendela Utama (Main Window) dan menyuntikkan koneksi Database
    print("[SYSTEM] Memuat Antarmuka Utama...")
    window = MainWindow(db_manager=db)
    
    # 4. Tampilkan Jendela
    window.show()
    
    print("[SYSTEM] OmniTrade Hub Berhasil Berjalan!")
    # 5. Jalankan Event Loop Aplikasi
    sys.exit(app.exec())

if __name__ == '__main__':
    main()