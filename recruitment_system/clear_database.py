import sqlite3
import os

DATABASE = 'recruitment.db'

def clear_database():
    # Kiểm tra xem file database có tồn tại không
    if not os.path.exists(DATABASE):
        print(f"Database file {DATABASE} không tồn tại.")
        return
    
    # Kết nối với database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tắt tạm thời foreign key constraints để tránh lỗi khi xóa
    cursor.execute('PRAGMA foreign_keys = OFF')
    
    try:
        # Lấy danh sách tất cả các bảng
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        # Xóa dữ liệu từ tất cả các bảng
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':  # Bỏ qua bảng hệ thống
                print(f"Đang xóa dữ liệu từ bảng {table_name}...")
                cursor.execute(f"DELETE FROM {table_name}")
        
        # Reset các auto-increment counter
        cursor.execute("DELETE FROM sqlite_sequence")
        
        # Lưu thay đổi
        conn.commit()
        print("Đã xóa toàn bộ dữ liệu trong database thành công.")
    
    except Exception as e:
        print(f"Lỗi khi xóa dữ liệu: {e}")
        conn.rollback()
    
    finally:
        # Bật lại foreign key constraints
        cursor.execute('PRAGMA foreign_keys = ON')
        conn.close()

if __name__ == "__main__":
    clear_database() 