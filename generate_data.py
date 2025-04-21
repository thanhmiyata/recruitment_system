import sqlite3
import os
from datetime import datetime

# Xóa database cũ nếu tồn tại
if os.path.exists('recruitment.db'):
    os.remove('recruitment.db')

# Kết nối database
conn = sqlite3.connect('recruitment.db')
cursor = conn.cursor()

# Tạo bảng
cursor.execute('''
    CREATE TABLE jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT NOT NULL,
        required_experience INTEGER NOT NULL,
        offered_salary INTEGER NOT NULL,
        max_candidates INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE applicants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        experience INTEGER NOT NULL,
        industry TEXT NOT NULL,
        location TEXT NOT NULL,
        desired_salary INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
''')

cursor.execute('''
    CREATE TABLE job_skills (
        job_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        required_level INTEGER NOT NULL,
        PRIMARY KEY (job_id, skill_id),
        FOREIGN KEY (job_id) REFERENCES jobs (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id)
    )
''')

cursor.execute('''
    CREATE TABLE applicant_skills (
        applicant_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        level INTEGER NOT NULL,
        PRIMARY KEY (applicant_id, skill_id),
        FOREIGN KEY (applicant_id) REFERENCES applicants (id),
        FOREIGN KEY (skill_id) REFERENCES skills (id)
    )
''')

# Thêm các kỹ năng
skills = [
    'Python', 'Java', 'C#', 'SQL', 'HTML', 'CSS', 'JavaScript',
    'Django', 'Spring', '.NET', 'Git', 'Docker', 'AWS',
    'RESTful API', 'Microservices', 'Agile', 'Scrum'
]

for skill in skills:
    cursor.execute('INSERT INTO skills (name) VALUES (?)', (skill,))

# Thêm công việc
jobs = [
    {
        'title': 'Senior Python Developer',
        'company': 'Tech Solutions Inc',
        'location': 'Ho Chi Minh City',
        'required_experience': 3,
        'offered_salary': 2500,
        'max_candidates': 2,
        'required_skills': [
            ('Python', 4),
            ('Django', 3),
            ('SQL', 3),
            ('Git', 3),
            ('AWS', 2)
        ]
    },
    {
        'title': 'Java Backend Developer',
        'company': 'Enterprise Systems',
        'location': 'Ha Noi',
        'required_experience': 4,
        'offered_salary': 2800,
        'max_candidates': 3,
        'required_skills': [
            ('Java', 4),
            ('Spring', 3),
            ('SQL', 3),
            ('Microservices', 3),
            ('Docker', 2)
        ]
    },
    {
        'title': 'C# Full Stack Developer',
        'company': 'Software Innovations',
        'location': 'Da Nang',
        'required_experience': 3,
        'offered_salary': 2300,
        'max_candidates': 4,
        'required_skills': [
            ('C#', 4),
            ('.NET', 3),
            ('SQL', 3),
            ('JavaScript', 3),
            ('HTML', 2),
            ('CSS', 2)
        ]
    }
]

# Thêm ứng viên
applicants = [
    # Python Developers
    {
        'name': 'Nguyen Van A',
        'email': 'nguyenvana@example.com',
        'experience': 4,
        'industry': 'Software Development',
        'location': 'Ho Chi Minh City',
        'desired_salary': 2200,
        'skills': [
            ('Python', 4),
            ('Django', 3),
            ('SQL', 3),
            ('Git', 2),
            ('AWS', 2)
        ]
    },
    {
        'name': 'Tran Thi B',
        'email': 'tranthib@example.com',
        'experience': 3,
        'industry': 'Software Development',
        'location': 'Ho Chi Minh City',
        'desired_salary': 2000,
        'skills': [
            ('Python', 3),
            ('Django', 3),
            ('SQL', 2),
            ('Git', 2),
            ('AWS', 1)
        ]
    },
    # Java Developers
    {
        'name': 'Le Van C',
        'email': 'levanc@example.com',
        'experience': 5,
        'industry': 'Software Development',
        'location': 'Ha Noi',
        'desired_salary': 2500,
        'skills': [
            ('Java', 4),
            ('Spring', 3),
            ('SQL', 3),
            ('Microservices', 2),
            ('Docker', 2)
        ]
    },
    {
        'name': 'Pham Thi D',
        'email': 'phamthid@example.com',
        'experience': 4,
        'industry': 'Software Development',
        'location': 'Ha Noi',
        'desired_salary': 2300,
        'skills': [
            ('Java', 3),
            ('Spring', 3),
            ('SQL', 2),
            ('Microservices', 2),
            ('Docker', 1)
        ]
    },
    {
        'name': 'Hoang Van E',
        'email': 'hoangvane@example.com',
        'experience': 3,
        'industry': 'Software Development',
        'location': 'Ha Noi',
        'desired_salary': 2100,
        'skills': [
            ('Java', 3),
            ('Spring', 2),
            ('SQL', 2),
            ('Microservices', 1),
            ('Docker', 1)
        ]
    },
    # C# Developers
    {
        'name': 'Vu Thi F',
        'email': 'vuthif@example.com',
        'experience': 4,
        'industry': 'Software Development',
        'location': 'Da Nang',
        'desired_salary': 2000,
        'skills': [
            ('C#', 4),
            ('.NET', 3),
            ('SQL', 2),
            ('JavaScript', 2),
            ('HTML', 2),
            ('CSS', 1)
        ]
    },
    {
        'name': 'Do Van G',
        'email': 'dovang@example.com',
        'experience': 3,
        'industry': 'Software Development',
        'location': 'Da Nang',
        'desired_salary': 1900,
        'skills': [
            ('C#', 3),
            ('.NET', 2),
            ('SQL', 2),
            ('JavaScript', 2),
            ('HTML', 1),
            ('CSS', 1)
        ]
    },
    {
        'name': 'Nguyen Thi H',
        'email': 'nguyenthih@example.com',
        'experience': 3,
        'industry': 'Software Development',
        'location': 'Da Nang',
        'desired_salary': 1800,
        'skills': [
            ('C#', 3),
            ('.NET', 2),
            ('SQL', 1),
            ('JavaScript', 2),
            ('HTML', 1),
            ('CSS', 1)
        ]
    },
    {
        'name': 'Tran Van I',
        'email': 'tranvani@example.com',
        'experience': 2,
        'industry': 'Software Development',
        'location': 'Da Nang',
        'desired_salary': 1700,
        'skills': [
            ('C#', 2),
            ('.NET', 2),
            ('SQL', 1),
            ('JavaScript', 1),
            ('HTML', 1),
            ('CSS', 1)
        ]
    }
]

# Thêm công việc và kỹ năng yêu cầu
for job in jobs:
    cursor.execute('''
        INSERT INTO jobs (title, company, location, required_experience, offered_salary, max_candidates)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        job['title'],
        job['company'],
        job['location'],
        job['required_experience'],
        job['offered_salary'],
        job['max_candidates']
    ))
    
    job_id = cursor.lastrowid
    
    for skill_name, required_level in job['required_skills']:
        cursor.execute('SELECT id FROM skills WHERE name = ?', (skill_name,))
        skill_id = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO job_skills (job_id, skill_id, required_level)
            VALUES (?, ?, ?)
        ''', (job_id, skill_id, required_level))

# Thêm ứng viên và kỹ năng
for applicant in applicants:
    cursor.execute('''
        INSERT INTO applicants (name, email, experience, industry, location, desired_salary)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        applicant['name'],
        applicant['email'],
        applicant['experience'],
        applicant['industry'],
        applicant['location'],
        applicant['desired_salary']
    ))
    
    applicant_id = cursor.lastrowid
    
    for skill_name, level in applicant['skills']:
        cursor.execute('SELECT id FROM skills WHERE name = ?', (skill_name,))
        skill_id = cursor.fetchone()[0]
        
        cursor.execute('''
            INSERT INTO applicant_skills (applicant_id, skill_id, level)
            VALUES (?, ?, ?)
        ''', (applicant_id, skill_id, level))

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Dữ liệu đã được tạo thành công!") 