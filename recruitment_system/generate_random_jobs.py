import sqlite3
import random
from faker import Faker

# Khởi tạo Faker
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

# Danh sách tên công việc
job_titles = [
    'Software Engineer', 'Data Analyst', 'Project Manager', 'Product Manager',
    'Business Analyst', 'UX Designer', 'UI Designer', 'DevOps Engineer',
    'System Administrator', 'Network Engineer', 'Database Administrator',
    'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
    'Mobile Developer', 'AI Engineer', 'Data Scientist', 'QA Engineer'
]

# Danh sách ngành nghề
industries = ['IT', 'Finance', 'Healthcare', 'Education', 'Marketing', 'Engineering', 
              'Sales', 'Manufacturing', 'Retail', 'Consulting', 'Media', 'Construction']

# Danh sách địa điểm
locations = ['Hanoi', 'Ho Chi Minh City', 'Da Nang', 'Can Tho', 'Hai Phong', 
             'Nha Trang', 'Vung Tau', 'Hue', 'Vinh', 'Quy Nhon']

# Tạo 10 công việc ngẫu nhiên
for i in range(10):
    # Tạo dữ liệu công việc
    title = random.choice(job_titles) + " " + str(i+1)
    required_experience = random.randint(1, 10)  # Kinh nghiệm yêu cầu từ 1-10 năm
    industry = random.choice(industries)
    location = random.choice(locations)
    offered_salary = random.randint(100, 10000)  # Lương đề xuất từ 100-10000
    max_candidates = random.randint(1, 10)
    
    # Insert công việc vào database
    cursor.execute('''
        INSERT INTO jobs (title, required_experience, industry, location, offered_salary, max_candidates) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, required_experience, industry, location, offered_salary, max_candidates))
    
    # Lấy ID của công việc vừa thêm
    job_id = cursor.lastrowid
    
    # Thêm từ 1-5 kỹ năng ngẫu nhiên cho công việc
    num_skills = random.randint(1, 5)
    selected_skills = random.sample(skill_ids, min(num_skills, len(skill_ids)))
    
    for skill_id in selected_skills:
        # Mức độ kỹ năng yêu cầu từ 1-10
        required_level = random.randint(1, 8)
        
        try:
            cursor.execute('''
                INSERT INTO job_skills (job_id, skill_id, required_level) 
                VALUES (?, ?, ?)
            ''', (job_id, skill_id, required_level))
        except sqlite3.IntegrityError:
            # Skip nếu đã tồn tại
            pass

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Hoàn thành việc tạo 10 công việc ngẫu nhiên!") 