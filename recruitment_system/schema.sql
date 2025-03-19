DROP TABLE IF EXISTS applicants;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS applicant_skills;
DROP TABLE IF EXISTS job_skills;

CREATE TABLE applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    experience INTEGER NOT NULL, -- in years
    industry TEXT NOT NULL,
    location TEXT NOT NULL,
    desired_salary REAL NOT NULL
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    required_experience INTEGER NOT NULL, -- in years
    industry TEXT NOT NULL,
    location TEXT NOT NULL,
    offered_salary REAL NOT NULL,
    max_candidates INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE applicant_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applicant_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    level INTEGER NOT NULL, -- 1-10 rating
    FOREIGN KEY (applicant_id) REFERENCES applicants (id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
    UNIQUE(applicant_id, skill_id)
);

CREATE TABLE job_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    required_level INTEGER NOT NULL, -- 1-10 rating
    FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skills (id) ON DELETE CASCADE,
    UNIQUE(job_id, skill_id)
);

-- Insert some sample skills
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