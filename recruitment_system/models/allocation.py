import numpy as np
from typing import List, Dict, Tuple

class TOPSIS:
    def __init__(self, criteria_weights: Dict[str, float]):
        """
        Initialize TOPSIS with criteria weights
        
        Parameters:
        - criteria_weights: Dictionary mapping criteria names to their weights
        """
        self.criteria_weights = criteria_weights
        self.normalized_matrix = None
        self.weighted_matrix = None
        self.ideal_solutions = None
        
    def normalize_matrix(self, decision_matrix: np.ndarray) -> np.ndarray:
        """Normalize the decision matrix"""
        # Tính tổng bình phương cho mỗi cột
        column_sums = np.sum(decision_matrix**2, axis=0)
        # Thay thế các giá trị 0 bằng 1 để tránh chia cho 0
        column_sums = np.where(column_sums == 0, 1, column_sums)
        return decision_matrix / np.sqrt(column_sums)
    
    def calculate_weighted_matrix(self, normalized_matrix: np.ndarray) -> np.ndarray:
        """Calculate weighted normalized matrix"""
        return normalized_matrix * np.array(list(self.criteria_weights.values()))
    
    def find_ideal_solutions(self, weighted_matrix: np.ndarray, benefit_criteria: List[str]) -> Tuple[np.ndarray, np.ndarray]:
        """Find ideal positive and negative solutions"""
        ideal_positive = np.zeros(len(self.criteria_weights))
        ideal_negative = np.zeros(len(self.criteria_weights))
        
        for i, criterion in enumerate(self.criteria_weights.keys()):
            if criterion in benefit_criteria:
                ideal_positive[i] = np.max(weighted_matrix[:, i])
                ideal_negative[i] = np.min(weighted_matrix[:, i])
            else:
                ideal_positive[i] = np.min(weighted_matrix[:, i])
                ideal_negative[i] = np.max(weighted_matrix[:, i])
                
        return ideal_positive, ideal_negative
    
    def calculate_distances(self, weighted_matrix: np.ndarray, 
                          ideal_positive: np.ndarray, 
                          ideal_negative: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate distances to ideal solutions"""
        d_positive = np.sqrt(np.sum((weighted_matrix - ideal_positive)**2, axis=1))
        d_negative = np.sqrt(np.sum((weighted_matrix - ideal_negative)**2, axis=1))
        return d_positive, d_negative
    
    def calculate_topsis_scores(self, d_positive: np.ndarray, d_negative: np.ndarray) -> np.ndarray:
        """Calculate TOPSIS scores"""
        # Tính tổng khoảng cách
        total_distance = d_positive + d_negative
        # Thay thế các giá trị 0 bằng 1 để tránh chia cho 0
        total_distance = np.where(total_distance == 0, 1, total_distance)
        return d_negative / total_distance
    
    def evaluate_candidates(self, candidates: List[Dict], job_requirements: Dict) -> List[Tuple[int, float]]:
        """
        Evaluate candidates using TOPSIS method
        
        Parameters:
        - candidates: List of candidate dictionaries
        - job_requirements: Dictionary containing job requirements
        
        Returns:
        - List of tuples (candidate_id, topsis_score)
        """
        if not candidates:
            return []
            
        # Convert qualitative criteria to numerical values
        decision_matrix = []
        for candidate in candidates:
            # Tính điểm kỹ năng trung bình
            skill_scores = self._normalize_skills(candidate['skills'], job_requirements['skills'])
            avg_skill_score = sum(skill_scores) / len(skill_scores) if skill_scores else 0
            
            # Tính tỷ lệ kinh nghiệm (0-1)
            experience_ratio = min(candidate['experience'] / max(job_requirements['required_experience'], 1), 1.0)
            
            # Tính tỷ lệ lương (0-1)
            salary_ratio = min(job_requirements['offered_salary'] / max(candidate['desired_salary'], 1), 1.0)
            
            # Tính điểm ngành nghề (0.5 hoặc 1)
            industry_score = 1.0 if candidate['industry'].lower() == job_requirements['industry'].lower() else 0.5
            
            row = [
                avg_skill_score,  # Kỹ năng (35%)
                experience_ratio,  # Kinh nghiệm (25%)
                industry_score,  # Ngành nghề (15%)
                salary_ratio  # Lương (25%)
            ]
            decision_matrix.append(row)
            
        decision_matrix = np.array(decision_matrix)
        
        # Normalize matrix
        self.normalized_matrix = self.normalize_matrix(decision_matrix)
        
        # Calculate weighted matrix
        self.weighted_matrix = self.calculate_weighted_matrix(self.normalized_matrix)
        
        # Find ideal solutions
        benefit_criteria = ['skills', 'experience', 'industry', 'salary']
        ideal_positive, ideal_negative = self.find_ideal_solutions(self.weighted_matrix, benefit_criteria)
        
        # Calculate distances
        d_positive, d_negative = self.calculate_distances(self.weighted_matrix, ideal_positive, ideal_negative)
        
        # Calculate TOPSIS scores
        topsis_scores = self.calculate_topsis_scores(d_positive, d_negative)
        
        # Return candidate IDs and their scores
        return [(candidate['id'], float(score)) for candidate, score in zip(candidates, topsis_scores)]
    
    def _normalize_skills(self, candidate_skills, required_skills):
        """Normalize skill levels between candidate and job requirements"""
        normalized_values = []
        for required_skill in required_skills:
            # Tìm kỹ năng tương ứng của ứng viên
            matching_skill = next(
                (skill for skill in candidate_skills if skill['name'].lower() == required_skill['name'].lower()),
                None
            )
            
            if matching_skill:
                # Tính tỷ lệ giữa level của ứng viên và yêu cầu
                ratio = min(matching_skill['level'] / max(required_skill['required_level'], 1), 1.0)
                normalized_values.append(ratio)
            else:
                normalized_values.append(0.0)
                
        return normalized_values

def calculate_match_score(job, applicant):
    """Tính điểm phù hợp giữa công việc và ứng viên"""
    # Tính điểm kỹ năng (40%)
    skill_score = 0
    if job['skills'] and applicant['skills']:
        total_skill_score = 0
        for job_skill in job['skills']:
            matching_skill = next(
                (skill for skill in applicant['skills'] 
                 if skill['name'].lower() == job_skill['name'].lower()),
                None
            )
            if matching_skill:
                # Nếu ứng viên có kỹ năng cao hơn hoặc bằng yêu cầu
                if matching_skill['level'] >= job_skill['required_level']:
                    total_skill_score += 1
                else:
                    # Nếu thấp hơn, tính tỷ lệ
                    total_skill_score += matching_skill['level'] / job_skill['required_level']
        skill_score = (total_skill_score / len(job['skills'])) * 0.4
    
    # Tính điểm kinh nghiệm (30%)
    exp_score = min(applicant['experience'] / job['required_experience'], 1.0) * 0.3
    
    # Tính điểm lương (30%)
    salary_score = 0
    if applicant['desired_salary'] <= job['offered_salary']:
        salary_ratio = applicant['desired_salary'] / job['offered_salary']
        salary_score = (1 - salary_ratio) * 0.3
    
    return skill_score + exp_score + salary_score

def allocate_candidates(applicants, jobs, applicant_skills_dict, job_skills_dict):
    """
    Phân bổ ứng viên cho công việc dựa trên điểm phù hợp
    """
    # Tính điểm cho tất cả cặp ứng viên-công việc
    match_scores = []
    for applicant in applicants:
        for job in jobs:
            # Bỏ qua nếu ứng viên yêu cầu lương cao hơn công việc
            if applicant['desired_salary'] > job['offered_salary']:
                continue
            
            # Tính điểm phù hợp
            score = calculate_match_score(job, applicant)
            match_scores.append((applicant['id'], job['id'], score))
    
    # Sắp xếp theo điểm giảm dần
    match_scores.sort(key=lambda x: x[2], reverse=True)
    
    # Phân bổ ứng viên
    assigned_applicants = set()
    job_allocations = {}
    
    for applicant_id, job_id, score in match_scores:
        # Bỏ qua nếu ứng viên đã được phân bổ hoặc công việc đã đủ
        if applicant_id in assigned_applicants:
            continue
        
        current_allocations = job_allocations.get(job_id, [])
        job = next((j for j in jobs if j['id'] == job_id), None)
        
        if len(current_allocations) >= job['max_candidates']:
            continue
        
        # Chỉ phân bổ nếu điểm >= 0.5
        if score >= 0.5:
            current_allocations.append((applicant_id, score * 100))  # Chuyển thành phần trăm
            job_allocations[job_id] = current_allocations
            assigned_applicants.add(applicant_id)
    
    return job_allocations 