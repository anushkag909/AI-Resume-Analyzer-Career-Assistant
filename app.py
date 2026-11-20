import streamlit as st
import fitz
import re

st.set_page_config(
    page_title="CareerCompass AI",
    page_icon="🎯",
    layout="wide"
)

# ---------- PDF TEXT EXTRACTION ----------
def extract_text_from_pdf(pdf_file):
    document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""

    for page in document:
        text += page.get_text()

    document.close()
    return text


# ---------- INFORMATION EXTRACTION ----------
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return match.group(0) if match else "Not found"


def extract_phone(text):
    match = re.search(r'(\+91[\s-]?)?[6-9]\d{9}', text)
    return match.group(0) if match else "Not found"


def extract_skills(text):
    skill_list = [
        "Python", "Machine Learning", "Deep Learning", "NLP",
        "Artificial Intelligence", "Data Science", "SQL",
        "Streamlit", "OpenAI", "PyTorch", "TensorFlow",
        "Pandas", "NumPy", "Matplotlib", "Seaborn",
        "Git", "GitHub", "Jupyter Notebook", "Excel",
        "PowerPoint", "HTML", "CSS", "JavaScript",
        "Java", "C++", "R", "Flask", "Django"
    ]

    found = []

    for skill in skill_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found.append(skill)

    return found

def extract_section(text, headings):
    if isinstance(headings, str):
        headings = [headings]

    lines = text.splitlines()
    collected = []
    collecting = False

    for line in lines:
        clean = line.strip()

        if not clean:
            continue

        if any(re.fullmatch(h, clean, re.IGNORECASE) for h in headings):
            collecting = True
            continue

        if collecting:
            if any(
                re.fullmatch(h, clean, re.IGNORECASE)
                for h in [
                    "Skills", "Education", "Experience",
                    "Projects", "Certifications",
                    "Achievements", "Summary", "Objective"
                ]
            ):
                break

            collected.append(clean)

    return collected


# ---------- HEADER ----------
st.title("🎯 CareerCompass AI")
st.subheader("Intelligent Resume Analysis & Career Readiness Assessment")

st.write(
    "Upload your resume to extract candidate information, "
    "identify skills and analyze career readiness."
)

st.divider()


# ---------- UPLOAD ----------
uploaded_file = st.file_uploader(
    "📄 Upload your Resume (PDF)",
    type=["pdf"]
)


if uploaded_file:

    with st.spinner("Analyzing your resume..."):
        text = extract_text_from_pdf(uploaded_file)

        email = extract_email(text)
        phone = extract_phone(text)
        skills = extract_skills(text)

        education = extract_section(text, "Education")

        experience = extract_section(text, "Experience")

        projects = extract_section(text, "Projects")

    certifications = extract_section(text, "Certifications")
    # -------- SKILL GAP ANALYSIS --------
    st.subheader("🎯 Skill Gap Analysis")

    role_skills = {
        "Data Scientist": [
            "Python", "Pandas", "NumPy", "Machine Learning",
            "SQL", "Data Science", "Matplotlib"
        ],
        "Machine Learning Engineer": [
            "Python", "Machine Learning", "Deep Learning",
            "PyTorch", "TensorFlow", "SQL"
        ],
        "AI / NLP Engineer": [
            "Python", "NLP", "Machine Learning",
            "Deep Learning", "OpenAI", "PyTorch"
        ],
        "Data Analyst": [
            "Python", "Pandas", "NumPy",
            "SQL", "Excel", "PowerPoint"
        ]
    }

    selected_role = st.selectbox(
        "Select your target career role:",
        list(role_skills.keys())
    )

    required_skills = role_skills[selected_role]

    matched_skills = [
        skill for skill in required_skills
        if any(skill.lower() == s.lower() for s in skills)
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in matched_skills
    ]

    gap_percentage = (
        len(matched_skills) / len(required_skills) * 100
        if required_skills else 0
    )

    st.write(f"**Role:** {selected_role}")
    st.write(f"**Skill Match:** {gap_percentage:.0f}%")

    if matched_skills:
        st.success(
            "✅ Skills you already have: "
            + ", ".join(matched_skills)
        )

    if missing_skills:
        st.warning(
            "📚 Skills you should develop: "
            + ", ".join(missing_skills)
        )
        st.markdown("### 📌 Skill Development Priorities")

        skill_actions = {
            "SQL": "Learn joins, subqueries, CTEs, and window functions.",
            "Machine Learning": "Practice supervised learning, model evaluation, and feature engineering.",
            "Deep Learning": "Build projects using neural networks and compare model performance.",
            "PyTorch": "Implement and train basic neural-network models.",
            "TensorFlow": "Practice model building, training, and evaluation workflows.",
            "Data Science": "Work on end-to-end projects using real-world datasets.",
            "NLP": "Practice text preprocessing, embeddings, and NLP model building.",
            "Python": "Strengthen problem-solving, data structures, and clean coding.",
            "Matplotlib": "Create clear analytical plots and explain key trends.",
            "Power BI": "Build dashboards and practice data-driven reporting."
        }

        for i, skill in enumerate(missing_skills):
            priority = "High" if i < 2 else "Medium"

            st.markdown(
                f"**{i + 1}. {skill} — {priority} Priority**"
            )

            st.write(
                skill_actions.get(
                    skill,
                    f"Build practical projects and strengthen your knowledge of {skill}."
                )
            )
    else:
        st.success("🎉 You have all the core skills for this role!")
    # -------- CAREER RECOMMENDATIONS --------
    st.subheader("🚀 Career Recommendations")

    career_recommendations = {
        "Data Scientist": {
            "summary": "Your profile is well aligned with Data Science. Focus on strengthening practical SQL, advanced statistics, and real-world machine learning projects.",
            "next_steps": [
                "Strengthen SQL and advanced querying",
                "Build an end-to-end machine learning project",
                "Practice model evaluation and feature engineering",
                "Create data science projects using real-world datasets"
            ]
        },
        "Machine Learning Engineer": {
            "summary": "Your profile has a strong foundation for Machine Learning Engineering. Focus on deep learning, deployment, and production-ready ML systems.",
            "next_steps": [
                "Strengthen Deep Learning fundamentals",
                "Build and deploy ML models",
                "Learn model serving and APIs",
                "Work on an end-to-end ML pipeline"
            ]
        },
        "AI Engineer": {
            "summary": "Your profile can progress toward AI Engineering by combining machine learning with NLP, LLMs, and practical AI applications.",
            "next_steps": [
                "Strengthen NLP and LLM concepts",
                "Build an AI-powered application",
                "Learn prompt engineering and RAG",
                "Deploy an AI application using an API"
            ]
        }
    }

    recommendation = career_recommendations.get(
        selected_role,
        {
            "summary": "Continue strengthening your technical skills and build practical projects aligned with your target career.",
            "next_steps": [
                "Identify important missing skills",
                "Build practical projects",
                "Strengthen problem-solving skills",
                "Create a portfolio demonstrating your work"
            ]
        }
    )

    st.info(recommendation["summary"])

    st.markdown("### 📌 Recommended Next Steps")

    for step in recommendation["next_steps"]:
        st.write("• " + step)

    # -------- PERSONALIZED SKILL ROADMAP --------
    st.subheader("🗺️ Personalized Skill Roadmap")

    if missing_skills:
        st.write("Based on your current resume, prioritize these skills:")

        for i, skill in enumerate(missing_skills, 1):
            st.write(f"**{i}. {skill}**")
    else:
        st.success("🎯 You already cover the core skills for this career role.")

    st.markdown("### 📈 Suggested Learning Path")
    st.write("**Phase 1:** Strengthen missing technical skills")
    st.write("**Phase 2:** Build a practical project")
    st.write("**Phase 3:** Deploy and document the project")
    st.write("**Phase 4:** Add the project to your portfolio/GitHub")
    # -------- CAREER ROLE COMPARISON --------
    st.subheader("📊 Career Role Comparison")

    resume_skills_lower = {skill.lower() for skill in skills}

    role_comparison = []

    for role, required_skills in role_skills.items():
        matched = [
            skill for skill in required_skills
            if skill.lower() in resume_skills_lower
        ]

        match_percentage = (len(matched) / len(required_skills)) * 100

        role_comparison.append({
            "Career Role": role,
            "Skill Match": f"{match_percentage:.0f}%",
            "Matched Skills": len(matched),
            "Required Skills": len(required_skills)
        })

    st.dataframe(
        role_comparison,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Compare your current resume skills against the core skills required for each career role."
    )
    # -------- SKILL MATCH VISUALIZATION --------
    st.markdown("### 📈 Skill Match Visualization")

    for item in role_comparison:
        match_value = int(item["Skill Match"].replace("%", ""))

        st.write(
            f"**{item['Career Role']} — {item['Skill Match']}**"
        )

        st.progress(match_value / 100)
    # -------- CAREER READINESS SCORE --------

    score = 0

    if email:
        score += 10

    if phone:
        score += 10

    if skills:
        score += 30

    if education:
        score += 15

    if experience:
        score += 15

    if projects:
        score += 10

    if certifications:
        score += 10

    score = min(score, 100)

    st.header("🎯 Career Readiness Score")
    st.progress(score / 100)
    st.metric("Readiness Score", f"{score}/100")

    st.success("✅ Resume analyzed successfully!")
    # -------- WHAT-IF CAREER ANALYSIS --------
    st.subheader("🔮 What-If Career Analysis")

    if missing_skills:
        st.write(
            "See how improving missing skills could strengthen your fit for the selected career role."
        )

        selected_improvements = st.multiselect(
            "Select skills you plan to develop:",
            missing_skills
        )

        if selected_improvements:
            projected_match = min(
                100,
                gap_percentage + (
                        len(selected_improvements) / len(missing_skills)
                ) * (100 - gap_percentage)
            )

            st.metric(
                "Projected Skill Match",
                f"{projected_match:.0f}%",
                f"+{projected_match - gap_percentage:.0f}%"
            )

            st.progress(projected_match / 100)

            st.success(
                "Great! Improving these skills can strengthen your alignment "
                "with the selected career role."
            )
    else:
        st.success(
            "🎯 No major skill gaps detected. You are already well aligned "
            "with this career role."
        )
    # ---------- CONTACT ----------
    st.header("👤 Candidate Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Email", email)

    with col2:
        st.metric("Phone", phone)


    # ---------- SKILLS ----------
    st.header("🧠 Extracted Skills")

    if skills:
        cols = st.columns(4)

        for i, skill in enumerate(skills):
            cols[i % 4].success(skill)
    else:
        st.info("No predefined skills detected.")


    # ---------- EDUCATION ----------
    st.header("🎓 Education")

    if education:
        for item in education:
            st.write("•", item)
    else:
        st.info("Education information could not be automatically identified.")


    # ---------- EXPERIENCE ----------
    st.header("💼 Experience")

    if experience:
        for item in experience:
            st.write("•", item)
    else:
        st.info("Experience information could not be automatically identified.")


    # ---------- PROJECTS ----------
    st.header("🚀 Projects")

    if projects:
        for item in projects:
            st.write("•", item)
    else:
        st.info("Project information could not be automatically identified.")


    # ---------- CERTIFICATIONS ----------
    st.header("📜 Certifications")

    if certifications:
        for item in certifications:
            st.write("•", item)
    else:
        st.info("Certification information could not be automatically identified.")


    # ---------- RAW TEXT ----------
    with st.expander("🔍 View Extracted Resume Text"):
        st.text_area(
            "Resume Text",
            text,
            height=300
        )


    st.divider()

    st.success(
        "CareerCompass AI has completed the initial resume analysis."
    )
    # -------- AI CAREER ASSISTANT --------
    st.header("🤖 AI Career Assistant")

    question = st.text_input(
        "Ask something about your career:",
        placeholder="e.g. What skills should I improve for Data Science?"
    )

    if question:
        st.info(
            f"Based on your resume, your current readiness score is {score}/100. "
            f"Your detected skills include: {', '.join(skills)}."
        )
else:
    st.info("👆 Please upload a PDF resume to begin analysis.")
