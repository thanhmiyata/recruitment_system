import sqlite3
import random
from faker import Faker

# Khởi tạo Faker để tạo dữ liệu giả
fake = Faker()

def calculate_salary_range(experience):
    """Tính range lương dựa trên số năm kinh nghiệm"""
    base_range = 1000  # Mức lương cơ bản cho 1 năm kinh nghiệm
    min_salary = experience * (base_range * 0.8)  # Giảm 20% cho mức thấp nhất
    max_salary = experience * (base_range * 1.2)  # Tăng 20% cho mức cao nhất
    return round(min_salary), round(max_salary)

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
    
    # Tính range lương dựa trên kinh nghiệm
    min_salary, max_salary = calculate_salary_range(experience)
    desired_salary = round(random.uniform(min_salary, max_salary), 2)
    
    industry = random.choice(industries)
    location = random.choice(locations)
    
    try:
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
            
            cursor.execute('''
                INSERT INTO applicant_skills (applicant_id, skill_id, level) 
                VALUES (?, ?, ?)
            ''', (applicant_id, skill_id, skill_level))
            
    except sqlite3.IntegrityError as e:
        print(f"Lỗi khi thêm ứng viên {name}: {e}")
        continue

    # In tiến trình
    if (i + 1) % 20 == 0:
        print(f"Đã tạo {i + 1} ứng viên")
        conn.commit()  # Commit sau mỗi 20 bản ghi

# Lưu thay đổi cuối cùng và đóng kết nối
conn.commit()
conn.close()

print("Hoàn thành việc tạo 200 ứng viên ngẫu nhiên!") 