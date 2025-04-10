import sqlite3
import random
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('recruitment.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_skills(cursor):
    # Define 10 common programming and technical skills
    skills = [
        "Python", "JavaScript", "Java", "C++", "SQL",
        "React", "Node.js", "Docker", "AWS", "Machine Learning"
    ]
    
    # Insert skills into database
    for skill in skills:
        cursor.execute('INSERT INTO skills (name) VALUES (?)', (skill,))

def generate_test_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Generate skills first
    generate_skills(cursor)
    
    # Create a job
    job_data = {
        'title': 'aaa job',
        'company': 'Test Company',
        'required_experience': 2,
        'location': 'Ho Chi Minh City',
        'offered_salary': 2000,
        'max_candidates': 2
    }
    
    cursor.execute('''
        INSERT INTO jobs (title, company, required_experience, location, offered_salary, max_candidates)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (job_data['title'], job_data['company'], job_data['required_experience'],
          job_data['location'], job_data['offered_salary'], job_data['max_candidates']))
    
    job_id = cursor.lastrowid
    
    # Get all skills
    cursor.execute('SELECT id FROM skills')
    skill_ids = [row[0] for row in cursor.fetchall()]
    
    # Select 3 random skills for the job
    job_skills = random.sample(skill_ids, min(3, len(skill_ids)))
    
    # Add skills to the job
    for skill_id in job_skills:
        required_level = random.randint(3, 5)
        cursor.execute('''
            INSERT INTO job_skills (job_id, skill_id, required_level)
            VALUES (?, ?, ?)
        ''', (job_id, skill_id, required_level))
    
    # Create two identical applicants with different salaries
    base_applicant = {
        'name': 'Identical Applicant',
        'experience': 2,
        'location': 'Ho Chi Minh City',
        'skills': job_skills  # Use the same skills as the job
    }
    
    # First applicant with lower salary
    cursor.execute('''
        INSERT INTO applicants (name, email, experience, location, desired_salary)
        VALUES (?, ?, ?, ?, ?)
    ''', (base_applicant['name'], 'identical1@example.com', base_applicant['experience'],
          base_applicant['location'], 1500))
    
    applicant1_id = cursor.lastrowid
    
    # Add skills for first applicant
    for skill_id in base_applicant['skills']:
        level = random.randint(3, 5)
        cursor.execute('''
            INSERT INTO applicant_skills (applicant_id, skill_id, level)
            VALUES (?, ?, ?)
        ''', (applicant1_id, skill_id, level))
    
    # Second applicant with higher salary (but still <= job salary)
    cursor.execute('''
        INSERT INTO applicants (name, email, experience, location, desired_salary)
        VALUES (?, ?, ?, ?, ?)
    ''', (base_applicant['name'], 'identical2@example.com', base_applicant['experience'],
          base_applicant['location'], 1800))
    
    applicant2_id = cursor.lastrowid
    
    # Add skills for second applicant
    for skill_id in base_applicant['skills']:
        level = random.randint(3, 5)
        cursor.execute('''
            INSERT INTO applicant_skills (applicant_id, skill_id, level)
            VALUES (?, ?, ?)
        ''', (applicant2_id, skill_id, level))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    generate_test_data()
    print("Test data generated successfully!") 