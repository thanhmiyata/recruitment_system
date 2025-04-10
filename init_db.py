import sqlite3
import random
from datetime import datetime
import os

def init_db():
    # Xóa database cũ nếu tồn tại
    if os.path.exists('recruitment.db'):
        os.remove('recruitment.db')
        print("Old database deleted successfully!")
    
    # Kết nối database
    conn = sqlite3.connect('recruitment.db')
    cursor = conn.cursor()
    
    # Tạo bảng skills
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Tạo bảng jobs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            required_experience INTEGER,
            location TEXT,
            offered_salary INTEGER,
            max_candidates INTEGER
        )
    ''')
    
    # Tạo bảng applicants
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            experience INTEGER,
            location TEXT,
            desired_salary INTEGER
        )
    ''')
    
    # Tạo bảng job_skills
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_skills (
            job_id INTEGER,
            skill_id INTEGER,
            required_level INTEGER,
            FOREIGN KEY (job_id) REFERENCES jobs (id),
            FOREIGN KEY (skill_id) REFERENCES skills (id),
            PRIMARY KEY (job_id, skill_id)
        )
    ''')
    
    # Tạo bảng applicant_skills
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applicant_skills (
            applicant_id INTEGER,
            skill_id INTEGER,
            level INTEGER,
            FOREIGN KEY (applicant_id) REFERENCES applicants (id),
            FOREIGN KEY (skill_id) REFERENCES skills (id),
            PRIMARY KEY (applicant_id, skill_id)
        )
    ''')
    
    # Thêm các kỹ năng mẫu
    skills = [
        'Python', 'Java', 'JavaScript', 'SQL', 'HTML/CSS',
        'React', 'Node.js', 'Docker', 'AWS', 'Git'
    ]
    
    for skill in skills:
        try:
            cursor.execute('INSERT INTO skills (name) VALUES (?)', (skill,))
        except sqlite3.IntegrityError:
            pass  # Bỏ qua nếu kỹ năng đã tồn tại
    
    # Danh sách địa điểm
    locations = ['Ho Chi Minh City', 'Ha Noi', 'Da Nang', 'Hue', 'Can Tho']
    
    # Danh sách công ty
    companies = [
        'Tech Solutions Inc.', 'Digital Innovations Ltd.', 'Global Software Co.',
        'Future Systems', 'Smart Tech Solutions', 'Innovative Software',
        'Digital Dynamics', 'Tech Pioneers', 'Modern Solutions',
        'Advanced Systems'
    ]
    
    # Danh sách tiêu đề công việc
    job_titles = [
        'Python Developer', 'Java Developer', 'Frontend Developer',
        'Backend Developer', 'Full Stack Developer', 'DevOps Engineer',
        'Data Engineer', 'Mobile Developer', 'UI/UX Designer',
        'System Administrator'
    ]
    
    # Tạo 10 công việc ngẫu nhiên
    for i in range(10):
        # Tạo thông tin công việc
        title = random.choice(job_titles)
        company = random.choice(companies)
        required_experience = random.randint(1, 5)
        location = random.choice(locations)
        offered_salary = random.randint(1500, 3000)
        max_candidates = random.randint(1, 5)  # Chỉ từ 1-5 ứng viên tối đa
        
        # Thêm công việc vào database
        cursor.execute('''
            INSERT INTO jobs (title, company, required_experience, location, offered_salary, max_candidates)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, company, required_experience, location, offered_salary, max_candidates))
        
        job_id = cursor.lastrowid
        
        # Thêm kỹ năng cho công việc
        required_skills = random.sample(skills, random.randint(2, 4))
        for skill_name in required_skills:
            cursor.execute('SELECT id FROM skills WHERE name = ?', (skill_name,))
            skill_id = cursor.fetchone()[0]
            required_level = random.randint(2, 5)
            cursor.execute('''
                INSERT INTO job_skills (job_id, skill_id, required_level)
                VALUES (?, ?, ?)
            ''', (job_id, skill_id, required_level))
        
        # Tạo số lượng ứng viên ngẫu nhiên cho mỗi công việc (từ 1-5)
        num_applicants = random.randint(1, 5)
        for j in range(num_applicants):
            # Tạo thông tin ứng viên
            name = f"Applicant {i*10 + j + 1}"
            email = f"applicant{i*10 + j + 1}@example.com"
            experience = random.randint(1, 5)
            location = random.choice(locations)
            desired_salary = random.randint(1000, offered_salary)
            
            # Thêm ứng viên vào database
            cursor.execute('''
                INSERT INTO applicants (name, email, experience, location, desired_salary)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, email, experience, location, desired_salary))
            
            applicant_id = cursor.lastrowid
            
            # Thêm kỹ năng cho ứng viên
            for skill_name in required_skills:
                cursor.execute('SELECT id FROM skills WHERE name = ?', (skill_name,))
                skill_id = cursor.fetchone()[0]
                level = random.randint(1, 5)
                cursor.execute('''
                    INSERT INTO applicant_skills (applicant_id, skill_id, level)
                    VALUES (?, ?, ?)
                ''', (applicant_id, skill_id, level))
            
            # Thêm 1-2 kỹ năng ngẫu nhiên khác
            other_skills = [s for s in skills if s not in required_skills]
            additional_skills = random.sample(other_skills, random.randint(1, 2))
            for skill_name in additional_skills:
                cursor.execute('SELECT id FROM skills WHERE name = ?', (skill_name,))
                skill_id = cursor.fetchone()[0]
                level = random.randint(1, 3)
                cursor.execute('''
                    INSERT INTO applicant_skills (applicant_id, skill_id, level)
                    VALUES (?, ?, ?)
                ''', (applicant_id, skill_id, level))
    
    # Lưu thay đổi
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db() 