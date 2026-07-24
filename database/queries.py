import sqlite3

DB_NAME = "mars_shop_clone.db"


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
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]
    finally:
        conn.close()


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
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, category, price, status, image, phone FROM elonlar
            WHERE LOWER(category) = LOWER(?) AND is_active = 1
        """, (category.strip(),))
        rows = cursor.fetchall()
    finally:
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
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, category, price, status, image, phone FROM elonlar
            WHERE user_id = ?
        """, (user_id,))
        rows = cursor.fetchall()
    finally:
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


def get_pending_elonlar():
    """Tasdiq kutayotgan (is_active=0) e'lonlar ro'yxatini qaytaradi."""
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, name, category, price, status, image, phone FROM elonlar
            WHERE is_active = 0
        """)
        rows = cursor.fetchall()
    finally:
        conn.close()

    ads = []
    for row in rows:
        ads.append({
            "id": row[0],
            "user_id": row[1],
            "name": row[2],
            "category": row[3],
            "price": row[4],
            "status": row[5],
            "image": row[6],
            "phone": row[7]
        })
    return ads


def set_elon_status(elon_id):
    """E'lonni tasdiqlaydi (is_active=1) va egasining user_id sini qaytaradi."""
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE elonlar SET is_active=1 WHERE id=?", (elon_id,))
        conn.commit()
        row = cursor.execute("SELECT user_id FROM elonlar WHERE id = ?", (elon_id,)).fetchone()
        return row[0] if row else None
    finally:
        conn.close()


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


def get_user_status(user_id):
    """(full_name, is_active, username) qaytaradi, topilmasa None."""
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        query = "SELECT full_name, is_active, username FROM users WHERE user_id=?"
        return cursor.execute(query, (user_id,)).fetchone()
    finally:
        conn.close()


def change_user_status(status, user_id):
    """Foydalanuvchini ban (0) yoki bandan chiqarish (1)."""
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_active=? WHERE user_id=?", (status, user_id))
        conn.commit()
    finally:
        conn.close()
