-- Xóa các bảng cũ nếu tồn tại
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS applicant_skills;
DROP TABLE IF EXISTS job_skills;
DROP TABLE IF EXISTS applicants;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS skills;

-- Tạo bảng applicants
CREATE TABLE applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    experience INTEGER NOT NULL CHECK (experience >= 0),
    industry TEXT NOT NULL,
    location TEXT NOT NULL,
    desired_salary REAL NOT NULL CHECK (desired_salary >= 0)
);

-- Tạo bảng jobs (đã bổ sung required_skills)
CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    required_experience INTEGER NOT NULL CHECK (required_experience >= 0),
    industry TEXT NOT NULL,
    location TEXT NOT NULL,
    offered_salary REAL NOT NULL CHECK (offered_salary >= 0),
    max_candidates INTEGER NOT NULL DEFAULT 1 CHECK (max_candidates >= 1),
    required_skills TEXT -- Thông tin kỹ năng dạng văn bản
);

-- Tạo bảng skills
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Tạo bảng applicant_skills
CREATE TABLE applicant_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applicant_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    level INTEGER NOT NULL CHECK (level BETWEEN 1 AND 10),
    FOREIGN KEY (applicant_id) REFERENCES applicants (id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
    UNIQUE (applicant_id, skill_id)
);

-- Tạo bảng job_skills
CREATE TABLE job_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    required_level INTEGER NOT NULL CHECK (required_level BETWEEN 1 AND 10),
    FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
    UNIQUE (job_id, skill_id)
);

-- Tạo bảng applications
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applicant_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    application_date TEXT NOT NULL DEFAULT (datetime('now')),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    FOREIGN KEY (applicant_id) REFERENCES applicants (id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE,
    UNIQUE (applicant_id, job_id)
);

-- Thêm chỉ số để tối ưu truy vấn
CREATE INDEX idx_applicants_industry_location ON applicants (industry, location);
CREATE INDEX idx_jobs_industry_location ON jobs (industry, location);
CREATE INDEX idx_applicant_skills_applicant_id ON applicant_skills (applicant_id);
CREATE INDEX idx_job_skills_job_id ON job_skills (job_id);

-- Chèn dữ liệu mẫu
-- Skills
INSERT INTO skills (name) VALUES ('Python');
INSERT INTO skills (name) VALUES ('Java');
INSERT INTO skills (name) VALUES ('JavaScript');
INSERT INTO skills (name) VALUES ('SQL');
INSERT INTO skills (name) VALUES ('C++');
INSERT INTO skills (name) VALUES ('Project Management');
INSERT INTO skills (name) VALUES ('Data Analysis');
INSERT INTO skills (name) VALUES ('Machine Learning');
INSERT INTO skills (name) VALUES ('Communication');
INSERT INTO skills (name) VALUES ('Leadership');

-- Applicants
INSERT INTO applicants (name, email, experience, industry, location, desired_salary) VALUES 
    ('Nguyen Van A', 'nguyenvana@example.com', 5, 'IT', 'Hanoi', 2000.0),
    ('Tran Thi B', 'tranthib@example.com', 3, 'IT', 'Ho Chi Minh', 1500.0),
    ('Le Van C', 'levanc@example.com', 7, 'Finance', 'Hanoi', 2500.0);

-- Jobs (đã bổ sung required_skills)
INSERT INTO jobs (title, required_experience, industry, location, offered_salary, max_candidates, required_skills) VALUES 
    ('Senior Developer', 5, 'IT', 'Hanoi', 2200.0, 1, 'Python:7, SQL:6'),
    ('Data Analyst', 3, 'IT', 'Ho Chi Minh', 1600.0, 2, 'Data Analysis:5, SQL:4'),
    ('Finance Manager', 6, 'Finance', 'Hanoi', 2600.0, 1, 'Project Management:8');

-- Applicant_skills
INSERT INTO applicant_skills (applicant_id, skill_id, level) VALUES 
    (1, 1, 8), -- Nguyen Van A: Python level 8
    (1, 4, 7), -- Nguyen Van A: SQL level 7
    (2, 7, 6), -- Tran Thi B: Data Analysis level 6
    (2, 4, 5), -- Tran Thi B: SQL level 5
    (3, 6, 9); -- Le Van C: Project Management level 9

-- Job_skills
INSERT INTO job_skills (job_id, skill_id, required_level) VALUES 
    (1, 1, 7), -- Senior Developer: Python level 7
    (1, 4, 6), -- Senior Developer: SQL level 6
    (2, 7, 5), -- Data Analyst: Data Analysis level 5
    (2, 4, 4), -- Data Analyst: SQL level 4
    (3, 6, 8); -- Finance Manager: Project Management level 8

-- Applications
INSERT INTO applications (applicant_id, job_id, status) VALUES 
    (1, 1, 'pending'),
    (2, 2, 'approved'),
    (3, 3, 'pending'); 