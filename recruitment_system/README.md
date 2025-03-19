# Recruitment System

A web-based system for managing job applicants and matching them with suitable positions using a greedy allocation algorithm.

## Features

- Manage job applicants and their profiles
- Manage job postings and requirements
- Track skills and skill levels
- Automatically match applicants with jobs based on:
  - Required skills and skill levels
  - Years of experience
  - Industry match
  - Location match
  - Salary expectations

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd recruitment_system
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the navigation menu to:
   - Add/view applicants
   - Add/view jobs
   - Add/view skills
   - Run the allocation algorithm to match applicants with jobs

## Database Schema

The system uses SQLite with the following tables:

- `applicants`: Stores applicant information
- `jobs`: Stores job postings
- `skills`: Stores available skills
- `applicant_skills`: Links applicants with their skills and skill levels
- `job_skills`: Links jobs with required skills and required levels

## Allocation Algorithm

The system uses a greedy algorithm to match applicants with jobs based on:

1. Skill match score (60% weight):
   - Compares applicant's skill levels with job requirements
   - Normalizes scores between 0 and 1

2. Other factors (40% weight):
   - Experience match
   - Industry match
   - Location match
   - Salary expectations

The algorithm:
1. Calculates match scores for all applicant-job pairs
2. Sorts pairs by score in descending order
3. Greedily assigns applicants to jobs while respecting:
   - Maximum number of candidates per job
   - Minimum match score threshold (50%)
   - One job per applicant

## Contributing

Feel free to submit issues and enhancement requests! 