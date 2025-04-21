from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
from models.allocation import allocate_candidates, calculate_match_score
from models.database import get_db_connection
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

DATABASE = 'recruitment.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        with open('schema.sql') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Lấy danh sách công việc
    cursor.execute('''
        SELECT j.*, GROUP_CONCAT(s.name || ':' || js.required_level) as skills
        FROM jobs j
        LEFT JOIN job_skills js ON j.id = js.job_id
        LEFT JOIN skills s ON js.skill_id = s.id
        GROUP BY j.id
    ''')
    jobs = cursor.fetchall()
    
    # Chuyển đổi jobs thành list of dictionaries
    jobs_list = []
    for job in jobs:
        job_dict = dict(job)
        # Chuyển đổi chuỗi skills thành list
        if job_dict['skills']:
            job_dict['skills'] = [
                {'name': skill.split(':')[0], 'required_level': int(skill.split(':')[1])}
                for skill in job_dict['skills'].split(',')
            ]
        else:
            job_dict['skills'] = []
        jobs_list.append(job_dict)
    
    conn.close()
    return render_template('jobs.html', jobs=jobs_list)

@app.route('/applicants')
def applicants():
    conn = get_db_connection()
    applicants = conn.execute('SELECT * FROM applicants').fetchall()
    conn.close()
    return render_template('applicants.html', applicants=applicants)

@app.route('/add_applicant', methods=['GET', 'POST'])
def add_applicant():
    conn = get_db_connection()
    skills = conn.execute('SELECT * FROM skills').fetchall()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        experience = request.form['experience']
        industry = request.form['industry']
        location = request.form['location']
        desired_salary = request.form['desired_salary']
        
        conn.execute(
            'INSERT INTO applicants (name, email, experience, industry, location, desired_salary) VALUES (?, ?, ?, ?, ?, ?)',
            (name, email, experience, industry, location, desired_salary)
        )
        
        applicant_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # Add skills for the applicant
        for skill_id in request.form.getlist('skills'):
            skill_level = request.form.get(f'skill_level_{skill_id}', 1)
            conn.execute(
                'INSERT INTO applicant_skills (applicant_id, skill_id, level) VALUES (?, ?, ?)',
                (applicant_id, skill_id, skill_level)
            )
        
        conn.commit()
        flash('Applicant added successfully!')
        return redirect(url_for('applicants'))
    
    conn.close()
    return render_template('add_applicant.html', skills=skills)

@app.route('/jobs')
def jobs():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return render_template('jobs.html', jobs=jobs)

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    conn = get_db_connection()
    skills = conn.execute('SELECT * FROM skills').fetchall()
    
    if request.method == 'POST':
        title = request.form['title']
        required_experience = request.form['required_experience']
        industry = request.form['industry']
        location = request.form['location']
        offered_salary = request.form['offered_salary']
        max_candidates = request.form['max_candidates']
        
        conn.execute(
            'INSERT INTO jobs (title, required_experience, industry, location, offered_salary, max_candidates) VALUES (?, ?, ?, ?, ?, ?)',
            (title, required_experience, industry, location, offered_salary, max_candidates)
        )
        
        job_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        
        # Add required skills for the job
        for skill_id in request.form.getlist('skills'):
            required_level = request.form.get(f'required_level_{skill_id}', 1)
            conn.execute(
                'INSERT INTO job_skills (job_id, skill_id, required_level) VALUES (?, ?, ?)',
                (job_id, skill_id, required_level)
            )
        
        conn.commit()
        flash('Job added successfully!')
        return redirect(url_for('jobs'))
    
    conn.close()
    return render_template('add_job.html', skills=skills)

@app.route('/allocate')
def allocate():
    conn = get_db_connection()
    
    # Get all applicants and jobs
    applicants = conn.execute('SELECT * FROM applicants').fetchall()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    
    # Get skills for applicants and jobs
    applicant_skills = {}
    for applicant in applicants:
        skills = conn.execute(
            'SELECT s.id, s.name, aps.level FROM applicant_skills aps '
            'JOIN skills s ON aps.skill_id = s.id '
            'WHERE aps.applicant_id = ?',
            (applicant['id'],)
        ).fetchall()
        applicant_skills[applicant['id']] = skills
    
    job_skills = {}
    for job in jobs:
        skills = conn.execute(
            'SELECT s.id, s.name, js.required_level FROM job_skills js '
            'JOIN skills s ON js.skill_id = s.id '
            'WHERE js.job_id = ?',
            (job['id'],)
        ).fetchall()
        job_skills[job['id']] = skills
    
    # Run allocation algorithm
    allocations = allocate_candidates(applicants, jobs, applicant_skills, job_skills)
    
    conn.close()
    return render_template('allocations.html', allocations=allocations, jobs=jobs, applicants=applicants)

@app.route('/add_skill', methods=['GET', 'POST'])
def add_skill():
    if request.method == 'POST':
        skill_name = request.form['name']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO skills (name) VALUES (?)', (skill_name,))
        conn.commit()
        conn.close()
        
        flash('Skill added successfully!')
        return redirect(url_for('index'))
    
    return render_template('add_skill.html')

@app.route('/skills')
def skills():
    conn = get_db_connection()
    skills = conn.execute('SELECT * FROM skills').fetchall()
    conn.close()
    return render_template('skills.html', skills=skills)

@app.route('/api/top_candidates/<int:job_id>')
def top_candidates(job_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Lấy thông tin công việc
    cursor.execute('''
        SELECT j.*, GROUP_CONCAT(s.name || ':' || js.required_level) as skills
        FROM jobs j
        LEFT JOIN job_skills js ON j.id = js.job_id
        LEFT JOIN skills s ON js.skill_id = s.id
        WHERE j.id = ?
        GROUP BY j.id
    ''', (job_id,))
    job = cursor.fetchone()
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    # Chuyển đổi job thành dictionary
    job_dict = dict(job)
    if job_dict['skills']:
        job_dict['skills'] = [
            {'name': skill.split(':')[0], 'required_level': int(skill.split(':')[1])}
            for skill in job_dict['skills'].split(',')
        ]
    else:
        job_dict['skills'] = []
    
    # Lấy danh sách ứng viên với điều kiện lọc
    cursor.execute('''
        SELECT a.*, GROUP_CONCAT(s.name || ':' || as2.level) as skills
        FROM applicants a
        LEFT JOIN applicant_skills as2 ON a.id = as2.applicant_id
        LEFT JOIN skills s ON as2.skill_id = s.id
        GROUP BY a.id
    ''')
    applicants = cursor.fetchall()
    
    if not applicants:
        conn.close()
        return jsonify({
            'job': job_dict,
            'candidates': []
        })
    
    # Chuyển đổi applicants thành list of dictionaries
    applicants_list = []
    for applicant in applicants:
        applicant_dict = dict(applicant)
        if applicant_dict['skills']:
            applicant_dict['skills'] = [
                {'name': skill.split(':')[0], 'level': int(skill.split(':')[1])}
                for skill in applicant_dict['skills'].split(',')
            ]
        else:
            applicant_dict['skills'] = []
        applicants_list.append(applicant_dict)
    
    # Tính điểm cho từng ứng viên
    candidates_list = []
    for applicant in applicants_list:
        # Parse skills
        applicant_skills = {}
        if applicant['skills']:
            for skill in applicant['skills']:
                applicant_skills[skill['name']] = skill['level']
                
        job_skills = {}
        if job_dict['skills']:
            for skill in job_dict['skills']:
                job_skills[skill['name']] = skill['required_level']
        
        # Calculate individual scores
        experience_score = min(100, (applicant['experience'] / job_dict['required_experience']) * 100)
        location_match = 100 if applicant['location'] == job_dict['location'] else 0
        salary_score = min(100, (job_dict['offered_salary'] / applicant['desired_salary']) * 100)
        
        # Calculate skill scores
        skill_scores = []
        for skill_name, required_level in job_skills.items():
            applicant_level = applicant_skills.get(skill_name, 0)
            skill_score = min(100, (applicant_level / required_level) * 100)
            skill_scores.append({
                'name': skill_name,
                'applicant_level': applicant_level,
                'required_level': required_level,
                'score': skill_score
            })
        
        total_skill_score = sum(skill['score'] for skill in skill_scores) / len(skill_scores) if skill_scores else 0
        
        # Calculate overall score
        match_score = (experience_score * 0.3 + 
                      location_match * 0.2 + 
                      salary_score * 0.3 + 
                      total_skill_score * 0.2)
        
        candidates_list.append({
            'id': applicant['id'],
            'name': applicant['name'],
            'experience': applicant['experience'],
            'desired_salary': applicant['desired_salary'],
            'location': applicant['location'],
            'skills': applicant['skills'],
            'match_score': match_score
        })
    
    # Sắp xếp ứng viên theo điểm số giảm dần
    candidates_list.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Bỏ giới hạn số lượng ứng viên
    # candidates_list = candidates_list[:job_dict['max_candidates']]
    
    conn.close()
    return jsonify({
        'job': job_dict,
        'candidates': candidates_list
    })

@app.route('/api/applicant_details/<int:applicant_id>/<int:job_id>')
def applicant_details(applicant_id, job_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get applicant details
        cursor.execute('''
            SELECT a.*, GROUP_CONCAT(DISTINCT s.name || ':' || aps.level) as skills
            FROM applicants a
            LEFT JOIN applicant_skills aps ON a.id = aps.applicant_id
            LEFT JOIN skills s ON aps.skill_id = s.id
            WHERE a.id = ?
            GROUP BY a.id
        ''', (applicant_id,))
        applicant = cursor.fetchone()
        
        if not applicant:
            return jsonify({'error': 'Applicant not found'}), 404
            
        # Convert sqlite3.Row to dictionary immediately
        applicant = dict(applicant)
        
        # Get job details
        cursor.execute('''
            SELECT j.*, GROUP_CONCAT(DISTINCT s.name || ':' || js.required_level) as skills
            FROM jobs j
            LEFT JOIN job_skills js ON j.id = js.job_id
            LEFT JOIN skills s ON js.skill_id = s.id
            WHERE j.id = ?
            GROUP BY j.id
        ''', (job_id,))
        job = cursor.fetchone()
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
            
        # Convert sqlite3.Row to dictionary immediately
        job = dict(job)
        
        # Parse skills
        applicant_skills = {}
        if applicant['skills']:
            for skill in applicant['skills'].split(','):
                name, level = skill.split(':')
                applicant_skills[name] = int(level)
                
        job_skills = {}
        if job['skills']:
            for skill in job['skills'].split(','):
                name, level = skill.split(':')
                job_skills[name] = int(level)
        
        # Calculate individual scores for display
        experience_score = min(100, (applicant['experience'] / job['required_experience']) * 100)
        location_match = 100 if applicant['location'] == job['location'] else 0
        salary_score = min(100, (job['offered_salary'] / applicant['desired_salary']) * 100)
        
        # Calculate skill scores
        skill_scores = []
        for skill_name, required_level in job_skills.items():
            applicant_level = applicant_skills.get(skill_name, 0)
            skill_score = min(100, (applicant_level / required_level) * 100)
            skill_scores.append({
                'name': skill_name,
                'applicant_level': applicant_level,
                'required_level': required_level,
                'score': skill_score
            })
        
        total_skill_score = sum(skill['score'] for skill in skill_scores) / len(skill_scores) if skill_scores else 0
        
        # Calculate overall score using the same formula as top_candidates
        overall_score = (experience_score * 0.3 + 
                        location_match * 0.2 + 
                        salary_score * 0.3 + 
                        total_skill_score * 0.2)
        
        return jsonify({
            'applicant': applicant,
            'job': job,
            'comparison': {
                'experience_score': experience_score,
                'location_match': location_match,
                'salary_score': salary_score,
                'skill_scores': skill_scores,
                'total_skill_score': total_skill_score,
                'overall_score': overall_score
            }
        })
        
    except Exception as e:
        print(f"Error in applicant_details: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

# API endpoint để lấy thông tin chi tiết của một applicant
@app.route('/api/applicant/<int:applicant_id>')
def get_applicant_details(applicant_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Lấy thông tin cơ bản của applicant
        cursor.execute('SELECT * FROM applicants WHERE id = ?', (applicant_id,))
        applicant = cursor.fetchone()
        
        if not applicant:
            return jsonify({'error': 'Applicant not found'}), 404
        
        applicant_dict = dict(applicant)
        
        # Lấy danh sách kỹ năng của applicant
        cursor.execute('''
            SELECT s.name, ask.level
            FROM applicant_skills ask
            JOIN skills s ON ask.skill_id = s.id
            WHERE ask.applicant_id = ?
            ORDER BY s.name
        ''', (applicant_id,))
        skills = cursor.fetchall()
        
        applicant_dict['skills'] = [{'name': row['name'], 'level': row['level']} for row in skills]
        
        return jsonify(applicant_dict)
        
    except Exception as e:
        print(f"Error getting applicant details: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True) 