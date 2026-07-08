import sqlite3
import os

# ==========================================
# CREATE DATABASE FOLDER
# ==========================================

os.makedirs("database", exist_ok=True)

DATABASE = "database/billing.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    # Enable Foreign Keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # ==========================================
    # BILL TABLE
    # ==========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS bills(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        bill_no TEXT UNIQUE NOT NULL,

        customer_name TEXT NOT NULL,

        customer_address TEXT,

        bill_date TEXT NOT NULL,

        discount REAL DEFAULT 0,

        gst REAL DEFAULT 0,

        grand_total REAL NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ==========================================
    # BILL ITEMS TABLE
    # ==========================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS bill_items(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        bill_id INTEGER NOT NULL,

        item_date TEXT,

        chalan_no TEXT,

        material TEXT NOT NULL,

        quantity INTEGER NOT NULL,

        price REAL NOT NULL,

        total REAL NOT NULL,

        FOREIGN KEY(bill_id)
        REFERENCES bills(id)
        ON DELETE CASCADE

    )

    """)

    # ==========================================
    # INDEXES
    # ==========================================

    cursor.execute("""

    CREATE INDEX IF NOT EXISTS idx_bill_no

    ON bills(bill_no)

    """)

    cursor.execute("""

    CREATE INDEX IF NOT EXISTS idx_customer

    ON bills(customer_name)

    """)

    cursor.execute("""

    CREATE INDEX IF NOT EXISTS idx_bill_date

    ON bills(bill_date)

    """)

    conn.commit()

    conn.close()

    print("===================================")
    print(" Billing Database Ready ")
    print("===================================")


if __name__ == "__main__":

    create_database()