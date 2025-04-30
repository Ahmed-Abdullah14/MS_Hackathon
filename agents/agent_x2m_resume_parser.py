import re
import pdfplumber
import spacy
from fuzzywuzzy import fuzz
from collections import defaultdict
import os  


nlp = spacy.load("en_core_web_sm")

# --- Sample JD Template (replace with actual job info dynamically) ---
job_description = {
    "title": "Data Analyst",
    "required_skills": {
        "Python": 5, "SQL": 5, "Power BI": 4, "Excel": 3, "Data Cleaning": 3
    },
    "skill_categories": {
        "Data Analysis": ["Python", "Power BI", "Excel"],
        "Database": ["SQL"],
        "Data Wrangling": ["Data Cleaning"]
    },
    "experience_keywords": ["data analysis", "reporting", "dashboards", "ETL", "KPIs"]
}

# --- PDF Text Extractor ---
def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        return ' '.join(page.extract_text() for page in pdf.pages if page.extract_text()).lower()

# --- Skill Match Engine ---
def skill_match(resume_text, required_skills, categories):
    matched_skills = defaultdict(int)
    score = 0

    for skill, weight in required_skills.items():
        if skill.lower() in resume_text:
            matched_skills[skill] += weight
            score += weight
        else:
            # Fuzzy match for typos, e.g., "Java Script"
            match_score = fuzz.partial_ratio(skill.lower(), resume_text)
            if match_score > 85:
                matched_skills[skill] += weight * 0.75  # penalized for fuzziness
                score += weight * 0.75

    # Skill Category Bonus
    for category, skills in categories.items():
        if any(s.lower() in resume_text for s in skills):
            score += 1  # minor bonus for category presence

    return dict(matched_skills), round(score, 2)

import re
from dateutil import parser
from datetime import datetime
from dateutil.relativedelta import relativedelta

def extract_experience_duration(resume_text: str) -> str:
    """
    Extracts date ranges from the resume and calculates total experience.
    Returns:
        - 'X months' if < 12 months
        - 'Y years' if ≥ 12 months
    """
    date_pattern = r"""
        (?P<start>
            (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*[\s\-.,]*\d{4} |
            \d{1,2}/\d{4} |
            \d{4}
        )
        \s*(?:to|–|-|—)\s*
        (?P<end>
            (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*[\s\-.,]*\d{4} |
            \d{1,2}/\d{4} |
            \d{4} |
            present|Present|Current
        )
    """
    matches = re.finditer(date_pattern, resume_text, re.IGNORECASE | re.VERBOSE)

    date_ranges = []
    for match in matches:
        start_text = match.group("start").strip().replace("–", "-").replace("—", "-")
        end_text = match.group("end").strip().replace("–", "-").replace("—", "-")
        date_ranges.append((start_text, end_text))

    parsed_ranges = []
    for start, end in date_ranges:
        try:
            start_date = parser.parse(start, default=datetime(1900, 1, 1))
        except:
            continue
        try:
            if re.search(r'present|current', end, re.IGNORECASE):
                end_date = datetime.today()
            else:
                end_date = parser.parse(end, default=datetime(1900, 1, 1))
        except:
            continue

        if start_date <= end_date:
            parsed_ranges.append((start_date, end_date))

    parsed_ranges.sort()
    merged_ranges = []
    for range in parsed_ranges:
        if not merged_ranges:
            merged_ranges.append(range)
        else:
            last_start, last_end = merged_ranges[-1]
            current_start, current_end = range
            if current_start <= last_end:
                merged_ranges[-1] = (last_start, max(last_end, current_end))
            else:
                merged_ranges.append(range)

    total_months = 0
    for start, end in merged_ranges:
        delta = relativedelta(end, start)
        months = delta.years * 12 + delta.months
        total_months += months

    if total_months < 12:
        return f"{total_months} months"
    else:
        years = total_months // 12
        return f"{years} years"



# --- Experience Relevance Engine ---
def experience_match(resume_text, title, exp_keywords):
    doc = nlp(resume_text)
    title_score = fuzz.partial_ratio(title.lower(), resume_text)

    keyword_score = sum(1 for kw in exp_keywords if kw.lower() in resume_text)

    # Get duration string like '6 months' or '2 years'
    experience_str = extract_experience_duration(resume_text)

    # Extract numeric part for scoring
    exp_value = int(re.search(r'\d+', experience_str).group())

    if "month" in experience_str.lower():
        exp_years = exp_value / 12  # Convert months to fraction of year
    else:
        exp_years = exp_value  # Already in years

    weighted_exp_score = (keyword_score * 2) + title_score + (exp_years * 3)

    return {
        "title_score": title_score,
        "keyword_score": keyword_score,
        "years_extracted": experience_str,
        "total_experience_score": round(weighted_exp_score, 2)
    }


# --- Main X2M Filtering Function ---
def run_x2m_resume_filter(resume_path, jd=job_description):
    resume_text = extract_text_from_pdf(resume_path)

    skill_results, skill_score = skill_match(
        resume_text, jd["required_skills"], jd["skill_categories"])

    exp_results = experience_match(
        resume_text, jd["title"], jd["experience_keywords"])

    total_score = round((0.6 * skill_score) + (0.4 * exp_results["total_experience_score"]), 2)

    return {
        "Skill Match Score": skill_score,
        "Experience Relevance Score": exp_results["total_experience_score"],
        "Matched Skills": skill_results,
        "Years of Experience": exp_results["years_extracted"],
        "Job Title Score": exp_results["title_score"],
        "Responsibility Keyword Score": exp_results["keyword_score"],
        "Final Weighted Score": total_score
    }

def process_cv_files(directory_path):
    """
    Processes all PDF CV files in the given directory.

    Args:
        directory_path (str): The path to the directory containing the CV files.
    """
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            print(f"\nProcessing CV: {filename}")
            results = run_x2m_resume_filter(file_path)
            if results:
                if "error" in results:
                    print(f"  Error: {results['error']}")
                else:
                    print("  Skill Match Score:", results["Skill Match Score"])
                    print("  Experience Relevance Score:", results["Experience Relevance Score"])
                    print("  Matched Skills:", results["Matched Skills"])
                    print("  Experience Duration:", results["Years of Experience"])
                    print("  Job Title Score:", results["Job Title Score"])
                    print("  Responsibility Keyword Score:", results["Responsibility Keyword Score"])
                    print("  Final Weighted Score:", results["Final Weighted Score"])
            else:
                print(f"  Skipped processing {filename} due to errors.")

if __name__ == "__main__":
    # Use the directory where your CV files are located
    cv_directory = "data/resumes"  # Enter relative path to the CV directory here 

    # Get the directory of the root workspace
    root_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(root_dir)  # Move up one level to the root workspace

    # Construct the absolute path to the CV directory
    cv_directory = os.path.normpath(os.path.join(root_dir, cv_directory))

    # Debug code to check the directory path
    if not os.path.exists(cv_directory):
        print(f"Error: Directory does not exist: {cv_directory}")
    else:
        process_cv_files(cv_directory)
