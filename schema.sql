-- Drop existing tables if they exist
DROP TABLE IF EXISTS applicant_skills;
DROP TABLE IF EXISTS job_skills;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS applicants;
DROP TABLE IF EXISTS jobs;

-- Create jobs table
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    required_experience INTEGER NOT NULL,
    offered_salary INTEGER NOT NULL,
    max_candidates INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create applicants table
CREATE TABLE applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    experience INTEGER NOT NULL,
    location TEXT NOT NULL,
    desired_salary INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create skills table
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Create job_skills table
CREATE TABLE job_skills (
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    required_level INTEGER NOT NULL,
    PRIMARY KEY (job_id, skill_id),
    FOREIGN KEY (job_id) REFERENCES jobs (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id)
);

-- Create applicant_skills table
CREATE TABLE applicant_skills (
    applicant_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    level INTEGER NOT NULL,
    PRIMARY KEY (applicant_id, skill_id),
    FOREIGN KEY (applicant_id) REFERENCES applicants (id),
    FOREIGN KEY (skill_id) REFERENCES skills (id)
);

-- Insert sample skills
INSERT INTO skills (name) VALUES 
    ('Python'),
    ('Java'),
    ('JavaScript'),
    ('SQL'),
    ('HTML'),
    ('CSS'),
    ('React'),
    ('Node.js'),
    ('Git'),
    ('Docker');

-- Insert sample jobs
INSERT INTO jobs (title, company, location, required_experience, offered_salary, max_candidates) VALUES 
    ('Python Developer', 'Tech Corp', 'Ho Chi Minh City', 2, 2000, 3),
    ('Frontend Developer', 'Web Solutions', 'Ha Noi', 1, 1500, 2),
    ('Backend Developer', 'Data Systems', 'Da Nang', 3, 2500, 2);

-- Insert sample applicants
INSERT INTO applicants (name, email, experience, location, desired_salary) VALUES 
    ('John Doe', 'john@example.com', 3, 'Ho Chi Minh City', 1800),
    ('Jane Smith', 'jane@example.com', 2, 'Ha Noi', 1400),
    ('Mike Johnson', 'mike@example.com', 1, 'Da Nang', 1200),
    ('Sarah Wilson', 'sarah@example.com', 4, 'Ho Chi Minh City', 2200);

-- Insert job skills
INSERT INTO job_skills (job_id, skill_id, required_level) VALUES 
    (1, 1, 3),  -- Python Developer requires Python level 3
    (1, 4, 2),  -- Python Developer requires SQL level 2
    (2, 5, 2),  -- Frontend Developer requires HTML level 2
    (2, 6, 2),  -- Frontend Developer requires CSS level 2
    (3, 2, 3),  -- Backend Developer requires Java level 3
    (3, 4, 3);  -- Backend Developer requires SQL level 3

-- Insert applicant skills
INSERT INTO applicant_skills (applicant_id, skill_id, level) VALUES 
    (1, 1, 4),  -- John has Python level 4
    (1, 4, 3),  -- John has SQL level 3
    (2, 5, 3),  -- Jane has HTML level 3
    (2, 6, 3),  -- Jane has CSS level 3
    (3, 2, 2),  -- Mike has Java level 2
    (3, 4, 2),  -- Mike has SQL level 2
    (4, 1, 5),  -- Sarah has Python level 5
    (4, 4, 4);  -- Sarah has SQL level 4 