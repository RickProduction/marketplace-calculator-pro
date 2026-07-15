import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="database/merchant_dash.db", schema_file="database/schema.sql"):
        os.makedirs(os.path.dirname(db_name) if os.path.dirname(db_name) else '.', exist_ok=True)
        self.db_name = db_name
        self.schema_file = schema_file
        self.initialize_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row 
        return conn

    def initialize_db(self):
        if not os.path.exists(self.schema_file):
            print(f"[WARNING] File schema {self.schema_file} tidak ditemukan.")
            return

        with self._connect() as conn:
            with open(self.schema_file, 'r') as f:
                schema_script = f.read()
            conn.executescript(schema_script)

    def add_transaction(self, marketplace, category, target_amount, listing_price, net_income, buyer_paid, status="Listed", notes=""):
        query = """
            INSERT INTO transactions 
            (marketplace, category, target_amount, listing_price, net_income, buyer_paid, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (marketplace, category, target_amount, listing_price, net_income, buyer_paid, status, notes))
            return cursor.lastrowid

    def get_all_transactions(self, limit=100):
        query = "SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT ?"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def update_transaction_status(self, transaction_id, new_status):
        query = "UPDATE transactions SET status = ? WHERE id = ?"
        with self._connect() as conn:
            conn.execute(query, (new_status, transaction_id))

    def delete_transaction(self, transaction_id):
        """Menghapus transaksi dari riwayat berdasarkan ID."""
        query = "DELETE FROM transactions WHERE id = ?"
        with self._connect() as conn:
            conn.execute(query, (transaction_id,))

    def get_dashboard_stats(self):
        query = """
            SELECT 
                COUNT(*) as total_orders,
                SUM(CASE WHEN status = 'Completed' THEN net_income ELSE 0 END) as total_revenue,
                SUM(CASE WHEN status = 'Sold' THEN net_income ELSE 0 END) as pending_revenue
            FROM transactions
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return {
                "total_orders": result["total_orders"] or 0,
                "total_revenue": result["total_revenue"] or 0.0,
                "pending_revenue": result["pending_revenue"] or 0.0
            }

    def save_setting(self, key, value):
        """Menyimpan atau memperbarui pengaturan (Upsert)."""
        query = """
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP
        """
        with self._connect() as conn:
            conn.execute(query, (key, value))

    def get_setting(self, key, default=""):
        """Mengambil nilai pengaturan berdasarkan key."""
        query = "SELECT value FROM settings WHERE key = ?"
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (key,))
            row = cursor.fetchone()
            return row["value"] if row else default