-- STREAMING_CHUNK: Membuat tabel settings untuk menyimpan konfigurasi API...
-- Tabel untuk menyimpan pengaturan aplikasi dan API Keys
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- STREAMING_CHUNK: Membuat tabel transactions untuk riwayat penjualan...
-- Tabel utama untuk riwayat kalkulasi dan pendapatan nyata
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT,                 
    marketplace TEXT NOT NULL,     
    category TEXT NOT NULL,        
    
    target_amount REAL NOT NULL,   
    listing_price REAL NOT NULL,   
    net_income REAL NOT NULL,      
    buyer_paid REAL NOT NULL,      
    
    status TEXT DEFAULT 'Listed',  
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

-- STREAMING_CHUNK: Menambahkan indexing untuk performa query...
-- Indexing untuk mempercepat pencarian jika data sudah banyak
CREATE INDEX IF NOT EXISTS idx_marketplace ON transactions(marketplace);
CREATE INDEX IF NOT EXISTS idx_status ON transactions(status);