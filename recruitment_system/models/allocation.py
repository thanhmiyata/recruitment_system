def calculate_skill_match_score(applicant_skills, job_skills):
    """
    Calculate a skill match score between an applicant and a job.
    
    Parameters:
    - applicant_skills: List of (skill_id, skill_name, level) tuples
    - job_skills: List of (skill_id, skill_name, required_level) tuples
    
    Returns:
    - score: A normalized score between 0 and 1
    """
    if not job_skills:
        return 1.0  # If job requires no skills, any applicant is a perfect match
    
    # Convert to dictionaries for easy lookup
    applicant_skill_dict = {skill[0]: skill[2] for skill in applicant_skills}
    job_skill_dict = {skill[0]: skill[2] for skill in job_skills}
    
    total_score = 0
    max_possible_score = 0
    
    # Check each skill required for the job
    for skill_id, required_level in job_skill_dict.items():
        max_possible_score += 10  # Maximum level is 10
        
        if skill_id in applicant_skill_dict:
            applicant_level = applicant_skill_dict[skill_id]
            
            # If applicant meets or exceeds required level
            if applicant_level >= required_level:
                total_score += required_level
            else:
                # Partial credit for having the skill but not at required level
                total_score += (applicant_level / required_level) * required_level
    
    # Normalize score between 0 and 1
    if max_possible_score == 0:
        return 1.0
    return total_score / max_possible_score

def calculate_other_match_factors(applicant, job):
    """
    Calculate match score based on factors other than skills:
    - Experience
    - Industry
    - Location
    - Salary
    
    Parameters:
    - applicant: Applicant record
    - job: Job record
    
    Returns:
    - score: A score between 0 and 1
    """
    # Experience match (1.0 if applicant meets or exceeds, otherwise partial credit)
    if applicant['experience'] >= job['required_experience']:
        experience_score = 1.0
    else:
        experience_score = applicant['experience'] / job['required_experience']
    
    # Industry match (1.0 if exact match, 0.5 otherwise)
    industry_score = 1.0 if applicant['industry'].lower() == job['industry'].lower() else 0.5
    
    # Location match (1.0 if exact match, 0.5 otherwise)
    location_score = 1.0 if applicant['location'].lower() == job['location'].lower() else 0.5
    
    # Salary match (1.0 if job offers at least what applicant wants, otherwise partial credit)
    if job['offered_salary'] >= applicant['desired_salary']:
        salary_score = 1.0
    else:
        # How close is the job's salary to applicant's desired salary
        salary_score = job['offered_salary'] / applicant['desired_salary']
    
    # Combine scores with weights
    weights = {
        'experience': 0.3,
        'industry': 0.2,
        'location': 0.2,
        'salary': 0.3
    }
    
    combined_score = (
        weights['experience'] * experience_score +
        weights['industry'] * industry_score +
        weights['location'] * location_score +
        weights['salary'] * salary_score
    )
    
    return combined_score

def calculate_total_match_score(applicant, job, applicant_skills, job_skills):
    """
    Calculate the overall match score between an applicant and a job.
    
    Parameters:
    - applicant: Applicant record
    - job: Job record
    - applicant_skills: List of skills for the applicant
    - job_skills: List of skills required for the job
    
    Returns:
    - score: A score between 0 and 100
    """
    skill_score = calculate_skill_match_score(applicant_skills, job_skills)
    other_score = calculate_other_match_factors(applicant, job)
    
    # Weight skills a bit higher than other factors
    total_score = (skill_score * 0.6) + (other_score * 0.4)
    
    # Convert to a 0-100 scale
    return total_score * 100

def allocate_candidates(applicants, jobs, applicant_skills_dict, job_skills_dict):
    """
    Allocate candidates to jobs using a greedy approach.
    
    Parameters:
    - applicants: List of applicant records
    - jobs: List of job records
    - applicant_skills_dict: Dictionary mapping applicant_id to their skills
    - job_skills_dict: Dictionary mapping job_id to required skills
    
    Returns:
    - allocations: Dictionary mapping job_id to list of (applicant_id, score) tuples
    """
    # Calculate match scores for all applicant-job pairs
    match_scores = []
    for applicant in applicants:
        for job in jobs:
            applicant_id = applicant['id']
            job_id = job['id']
            
            applicant_skills = applicant_skills_dict.get(applicant_id, [])
            job_skills = job_skills_dict.get(job_id, [])
            
            score = calculate_total_match_score(applicant, job, applicant_skills, job_skills)
            
            match_scores.append((applicant_id, job_id, score))
    
    # Sort by score in descending order
    match_scores.sort(key=lambda x: x[2], reverse=True)
    
    # Perform greedy allocation
    assigned_applicants = set()
    job_allocations = {}
    
    for applicant_id, job_id, score in match_scores:
        # Skip if applicant already assigned or job is full
        if applicant_id in assigned_applicants:
            continue
        
        current_allocations = job_allocations.get(job_id, [])
        job = next((j for j in jobs if j['id'] == job_id), None)
        
        if len(current_allocations) >= job['max_candidates']:
            continue
        
        # Minimum score threshold (e.g., 50 out of 100)
        if score >= 50:
            current_allocations.append((applicant_id, score))
            job_allocations[job_id] = current_allocations
            assigned_applicants.add(applicant_id)
    
    return job_allocations 