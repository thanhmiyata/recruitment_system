import sqlite3
import random
from faker import Faker

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()

# Kết nối database
conn = sqlite3.connect('recruitment.db')
cursor = conn.cursor()

# Kiểm tra bảng skills có dữ liệu không
cursor.execute('SELECT COUNT(*) FROM skills')
skill_count = cursor.fetchone()[0]

# Nếu không có kỹ năng, thêm kỹ năng mẫu
if skill_count == 0:
    print("Không tìm thấy kỹ năng. Thêm kỹ năng mẫu...")
    skills = ['Python', 'Java', 'JavaScript', 'SQL', 'C++', 'Project Management', 
              'Data Analysis', 'Machine Learning', 'Communication', 'Leadership']
    for skill in skills:
        cursor.execute('INSERT INTO skills (name) VALUES (?)', (skill,))
    conn.commit()
    print(f"Đã thêm {len(skills)} kỹ năng mẫu.")

# Lấy danh sách các skill hiện có
cursor.execute('SELECT id FROM skills')
skill_ids = [row[0] for row in cursor.fetchall()]

# Danh sách ngành nghề
industries = ['IT', 'Finance', 'Healthcare', 'Education', 'Marketing', 'Engineering', 
              'Sales', 'Manufacturing', 'Retail', 'Consulting', 'Media', 'Construction']

# Danh sách địa điểm
locations = ['Hanoi', 'Ho Chi Minh City', 'Da Nang', 'Can Tho', 'Hai Phong', 
             'Nha Trang', 'Vung Tau', 'Hue', 'Vinh', 'Quy Nhon']

# Tạo 200 ứng viên
for i in range(200):
    # Tạo dữ liệu ứng viên
    name = fake.name()
    email = fake.email()
    experience = random.randint(1, 10)  # Kinh nghiệm từ 1-10 năm
    industry = random.choice(industries)
    location = random.choice(locations)
    desired_salary = random.randint(100, 10000)  # Lương mong muốn từ 100-10000
    
    # Insert ứng viên vào database
    cursor.execute('''
        INSERT INTO applicants (name, email, experience, industry, location, desired_salary) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, experience, industry, location, desired_salary))
    
    # Lấy ID của ứng viên vừa thêm
    applicant_id = cursor.lastrowid
    
    # Thêm từ 1-5 kỹ năng ngẫu nhiên cho ứng viên
    num_skills = random.randint(1, 5)
    selected_skills = random.sample(skill_ids, min(num_skills, len(skill_ids)))
    
    for skill_id in selected_skills:
        # Mức độ kỹ năng từ 1-10
        skill_level = random.randint(1, 10)
        
        try:
            cursor.execute('''
                INSERT INTO applicant_skills (applicant_id, skill_id, level) 
                VALUES (?, ?, ?)
            ''', (applicant_id, skill_id, skill_level))
        except sqlite3.IntegrityError:
            # Skip nếu đã tồn tại
            pass

    # In tiến trình
    if (i + 1) % 20 == 0:
        print(f"Đã tạo {i + 1} ứng viên")

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Hoàn thành việc tạo 200 ứng viên ngẫu nhiên!") 