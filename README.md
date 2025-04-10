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

## Database Initialization and Demo Data

Before running the application for the first time, or if you want to reset the data, you need to initialize the database and optionally populate it with demo data.

*(Make sure your virtual environment is activated before running these scripts)*

1.  **(Optional) Clear existing database:** If you want a completely fresh start, run:
    ```bash
    python clear_database.py
    ```

2.  **Initialize the database schema:** This creates the necessary tables.
    ```bash
    python init_db.py
    ```

3.  **Generate initial skills:** This populates the `skills` table.
    ```bash
    python generate_skills.py
    ```

4.  **Generate test applicants and jobs:** This adds demo data for testing.
    ```bash
    python generate_test_data.py
    ```

## Usage

1. **Set the Flask application environment variable:**
   *(This tells Flask where your application file is)*
   ```bash
   export FLASK_APP=app.py  # On Windows, use: set FLASK_APP=app.py
   ```

2. **Run the Flask development server:**
   ```bash
   flask run
   ```
   *(The server will typically start on http://127.0.0.1:5000)*

3. **Open your web browser** and navigate to the address provided (e.g., `http://127.0.0.1:5000`).

4. Use the navigation menu to:
   - Add/view applicants
   - Add/view jobs
   - Add/view skills
   - Run the allocation algorithm to match applicants with jobs

## Database Schema

The system uses SQLite with the following tables:

- `