import sqlite3
import random
from faker import Faker

def calculate_salary_range(experience):
    """Tính range lương dựa trên số năm kinh nghiệm"""
    base_range = 1200  # Mức lương cơ bản cho 1 năm kinh nghiệm (cao hơn mức ứng viên 20%)
    min_salary = experience * (base_range * 0.8)  # Giảm 20% cho mức thấp nhất
    max_salary = experience * (base_range * 1.2)  # Tăng 20% cho mức cao nhất
    return round(min_salary), round(max_salary)

def format_required_skills(selected_skills):
    """Format danh sách kỹ năng thành chuỗi text"""
    skill_texts = []
    for skill_id, skill_name, level in selected_skills:
        skill_texts.append(f"{skill_name}:{level}")
    return ", ".join(skill_texts)

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
cursor.execute('SELECT id, name FROM skills')
skills_data = cursor.fetchall()
skill_ids = [row[0] for row in skills_data]
skill_dict = {row[0]: row[1] for row in skills_data}

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
    try:
        # Tạo dữ liệu công việc
        title = random.choice(job_titles) + " " + str(i+1)
        required_experience = random.randint(1, 10)  # Kinh nghiệm yêu cầu từ 1-10 năm
        
        # Tính range lương dựa trên kinh nghiệm
        min_salary, max_salary = calculate_salary_range(required_experience)
        offered_salary = round(random.uniform(min_salary, max_salary), 2)
        
        industry = random.choice(industries)
        location = random.choice(locations)
        max_candidates = random.randint(1, 5)
        
        # Chọn và format kỹ năng yêu cầu
        num_skills = random.randint(1, 5)
        selected_skill_ids = random.sample(skill_ids, min(num_skills, len(skill_ids)))
        selected_skills = []
        
        for skill_id in selected_skill_ids:
            required_level = random.randint(1, 10)
            selected_skills.append((skill_id, skill_dict[skill_id], required_level))
        
        required_skills_text = format_required_skills(selected_skills)
        
        # Insert công việc vào database
        cursor.execute('''
            INSERT INTO jobs (title, required_experience, industry, location, 
                            offered_salary, max_candidates, required_skills) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, required_experience, industry, location, 
              offered_salary, max_candidates, required_skills_text))
        
        # Lấy ID của công việc vừa thêm
        job_id = cursor.lastrowid
        
        # Thêm kỹ năng cho công việc
        for skill_id, _, required_level in selected_skills:
            cursor.execute('''
                INSERT INTO job_skills (job_id, skill_id, required_level) 
                VALUES (?, ?, ?)
            ''', (job_id, skill_id, required_level))
            
    except sqlite3.IntegrityError as e:
        print(f"Lỗi khi thêm công việc {title}: {e}")
        continue

    # In tiến trình
    print(f"Đã tạo công việc {i + 1}/10: {title}")
    conn.commit()  # Commit sau mỗi công việc

# Lưu thay đổi cuối cùng và đóng kết nối
conn.commit()
conn.close()

print("Hoàn thành việc tạo 10 công việc ngẫu nhiên!") 