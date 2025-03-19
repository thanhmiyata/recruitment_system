from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
import os
from models.allocation import allocate_candidates, calculate_total_match_score

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
    return render_template('index.html')

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

@app.route('/api/job/<int:job_id>/top_candidates')
def top_candidates(job_id):
    conn = get_db_connection()
    
    # Get job information
    job = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    
    if not job:
        conn.close()
        return jsonify({"error": "Job not found"}), 404
    
    # Get all applicants
    applicants = conn.execute('SELECT * FROM applicants').fetchall()
    
    # Get job skills
    job_skills = conn.execute(
        'SELECT s.id, s.name, js.required_level FROM job_skills js '
        'JOIN skills s ON js.skill_id = s.id '
        'WHERE js.job_id = ?',
        (job_id,)
    ).fetchall()
    
    # Calculate match scores for all candidates
    candidate_scores = []
    
    for applicant in applicants:
        # Get applicant skills
        applicant_skills = conn.execute(
            'SELECT s.id, s.name, aps.level FROM applicant_skills aps '
            'JOIN skills s ON aps.skill_id = s.id '
            'WHERE aps.applicant_id = ?',
            (applicant['id'],)
        ).fetchall()
        
        # Calculate match score
        score = calculate_total_match_score(applicant, job, applicant_skills, job_skills)
        
        candidate_scores.append({
            "id": applicant['id'],
            "name": applicant['name'],
            "email": applicant['email'],
            "experience": applicant['experience'],
            "desired_salary": applicant['desired_salary'],
            "match_score": score
        })
    
    # Sort by score in descending order and limit to max_candidates
    candidate_scores.sort(key=lambda x: x['match_score'], reverse=True)
    top_candidates = candidate_scores[:job['max_candidates']]
    
    conn.close()
    return jsonify(top_candidates)

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True) 