import sqlite3

DB_NAME = "bot_data.db"

def init_db():
    """Ma'lumotlar bazasi va jadvallarni yaratish"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name VARCHAR(100),
            username VARCHAR(50),
            is_active INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS elonlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name VARCHAR(50),
            category VARCHAR(50),
            price VARCHAR(50),
            status VARCHAR(50),
            image VARCHAR(255),
            phone VARCHAR(20),
            is_active INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    
    conn.commit()
    conn.close()

def add_user(user_id, full_name, username):
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, full_name, username)
            VALUES (?, ?, ?)
        """, (user_id, full_name, username))
        conn.commit()
    finally:
        conn.close()

def count_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def add_elon(user_id, name, category, price, status, image, phone):
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO elonlar (user_id, name, category, price, status, image, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, name, category, price, status, image, phone))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def get_elonlar_by_category(category):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, category, price, status, image, phone FROM elonlar 
        WHERE LOWER(category) = LOWER(?)
    """, (category.strip(),))
    rows = cursor.fetchall()
    conn.close()
    
    ads = []
    for row in rows:
        ads.append({
            "name": row[0],
            "category": row[1],
            "price": row[2],
            "status": row[3],
            "image": row[4],
            "phone": row[5]
        })
    return ads

def get_user_history(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, category, price, status, image, phone FROM elonlar 
        WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    ads = []
    for row in rows:
        ads.append({
            "name": row[0],
            "category": row[1],
            "price": row[2],
            "status": row[3],
            "image": row[4],
            "phone": row[5]
        })
    return ads


def set_elon_status(elon_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    query1 = "UPDATE elonlar SET is_active=1 WHERE id=?"
    query2 = "SELECT user_id FROM elonlar WHERE id = ?"
    cursor.execute(query1, (elon_id, ))
    conn.commit()
    return cursor.execute(query2, (elon_id, )).fetchone()[0]


def reject_elon(elon_id):
    """Rad etilgan e'lonni o'chiradi va egasining user_id sini qaytaradi."""
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        row = cursor.execute("SELECT user_id FROM elonlar WHERE id = ?", (elon_id,)).fetchone()
        if row is None:
            return None
        cursor.execute("DELETE FROM elonlar WHERE id = ?", (elon_id,))
        conn.commit()
        return row[0]
    finally:
        conn.close()


# def change_user_status(user_id):
#     pass
