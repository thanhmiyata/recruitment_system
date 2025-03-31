import sqlite3
import random

def get_db_connection():
    conn = sqlite3.connect('recruitment.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_skills():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # List of common programming and technical skills
    skills = [
        "Python",
        "JavaScript",
        "Java",
        "C++",
        "SQL",
        "React",
        "Node.js",
        "Docker",
        "AWS",
        "Machine Learning"
    ]
    
    # Insert skills
    for skill in skills:
        cursor.execute('''
            INSERT INTO skills (name)
            VALUES (?)
        ''', (skill,))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    generate_skills()
    print("Skills generated successfully!") 