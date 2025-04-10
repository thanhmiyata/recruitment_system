import sqlite3
import os

def get_db_connection():
    """Tạo kết nối đến database"""
    conn = sqlite3.connect('recruitment_system/recruitment.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_app(app):
    """Khởi tạo database cho ứng dụng"""
    if not os.path.exists('recruitment_system'):
        os.makedirs('recruitment_system')
    
    conn = get_db_connection()
    with app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close() 