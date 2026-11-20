import re
import fitz


# -----------------------------
# Predefined skill dictionary
# -----------------------------
SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "machine learning",
    "deep learning",
    "data analysis",
    "data science",
    "nlp",
    "excel",
    "power bi",
    "tableau",
    "git",
    "github",
    "docker",
    "aws",
    "communication",
    "leadership",
    "project management"
]


# -----------------------------
# PDF text extraction
# -----------------------------
def extract_text_from_pdf(pdf_path):
    text = ""

    document = fitz.open(pdf_path)

    for page in document:
        text += page.get_text("text") + "\n"

    document.close()

    return text


# -----------------------------
# Basic text normalization
# -----------------------------
def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# -----------------------------
# Skill extraction
# Case-insensitive keyword matching
# -----------------------------
def extract_skills(text):
    normalized_text = normalize_text(text)

    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return sorted(set(found_skills))


# -----------------------------
# Section extraction
# -----------------------------
def extract_section(text, section_name):
    pattern = (
        r"(?i)\b"
        + re.escape(section_name)
        + r"\b"
        r"\s*:?\s*"
        r"(.*?)"
          r"(?=\n\s*(?:education|experience|technical skills|skills|projects|certifications|achievements|references)\b|\Z)"
    )

    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1).strip()

    return ""


# -----------------------------
# Email extraction
# -----------------------------
def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    return match.group(0) if match else ""


# -----------------------------
# Phone extraction
# -----------------------------
def extract_phone(text):
    pattern = r"(?:\+91[\s-]?)?[6-9]\d{9}"

    match = re.search(pattern, text)

    return match.group(0) if match else ""


# -----------------------------
# Main resume parser
# -----------------------------
def parse_resume(pdf_path):

    text = extract_text_from_pdf(pdf_path)

    skills = extract_skills(text)

    resume_data = {
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": skills,
        "education": extract_section(text, "education"),
        "experience": extract_section(text, "experience"),
        "projects": extract_section(text, "projects"),
        "certifications": extract_section(text, "certifications")
    }

    return resume_data


# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":

    pdf_file = input("Enter resume PDF path: ")

    result = parse_resume(pdf_file)

    print("\n========== RESUME ANALYSIS ==========")

    print("\nEmail:")
    print(result["email"])

    print("\nPhone:")
    print(result["phone"])

    print("\nSkills:")
    print(", ".join(result["skills"]))

    print("\nEducation:")
    print(result["education"])

    print("\nExperience:")
    print(result["experience"])

    print("\nProjects:")
    print(result["projects"])

    print("\nCertifications:")
    print(result["certifications"])

