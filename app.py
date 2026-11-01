import streamlit as st
from pypdf import PdfReader
import plotly.graph_objects as go
import re

# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# CUSTOM DESIGN
st.markdown("""
<style>
.stApp {
    background-color: #f4f6ff;
}
h1, h2, h3 {
    color: #4b0082;
}
.stButton>button {
    background-color: #6c42d8;
    color: white;
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# SKILLS DATABASE
job_skills = {
    "Software Developer": [
        "Python", "Java", "C", "C++", "SQL",
        "Data Structures", "Algorithms",
        "HTML", "CSS", "JavaScript",
        "Git", "OOP", "Problem Solving"
    ],

    "Web Developer": [
        "HTML", "CSS", "JavaScript",
        "React", "Node.js", "Python",
        "SQL", "Git", "REST API"
    ],

    "Data Analyst": [
        "Python", "SQL", "Excel",
        "Power BI", "Tableau",
        "Statistics", "Pandas",
        "NumPy", "Data Visualization"
    ],

    "Cybersecurity Analyst": [
        "Python", "Linux", "Networking",
        "Cryptography", "Ethical Hacking",
        "Wireshark", "SQL", "Cybersecurity"
    ],

    "AI/ML Engineer": [
        "Python", "Machine Learning",
        "Deep Learning", "NumPy",
        "Pandas", "TensorFlow",
        "Scikit-learn", "Statistics"
    ]
}

# LEARNING RESOURCES
learning_links = {
    "Python": "https://www.python.org/about/gettingstarted/",
    "Java": "https://www.w3schools.com/java/",
    "C": "https://www.learn-c.org/",
    "C++": "https://www.learncpp.com/",
    "SQL": "https://www.w3schools.com/sql/",
    "HTML": "https://www.w3schools.com/html/",
    "CSS": "https://www.w3schools.com/css/",
    "JavaScript": "https://www.w3schools.com/js/",
    "React": "https://react.dev/learn",
    "Node.js": "https://nodejs.org/en/learn",
    "Git": "https://git-scm.com/doc",
    "Data Structures": "https://www.geeksforgeeks.org/data-structures/",
    "Algorithms": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/",
    "Machine Learning": "https://www.coursera.org/learn/machine-learning",
    "Deep Learning": "https://www.deeplearning.ai/",
    "TensorFlow": "https://www.tensorflow.org/tutorials",
    "Scikit-learn": "https://scikit-learn.org/stable/tutorial/index.html",
    "NumPy": "https://numpy.org/learn/",
    "Pandas": "https://pandas.pydata.org/docs/getting_started/",
    "Excel": "https://support.microsoft.com/excel",
    "Power BI": "https://learn.microsoft.com/en-us/power-bi/",
    "Tableau": "https://www.tableau.com/learn/training",
    "Statistics": "https://www.khanacademy.org/math/statistics-probability",
    "Linux": "https://ubuntu.com/tutorials",
    "Networking": "https://www.cisco.com/",
    "Cryptography": "https://www.coursera.org/learn/crypto",
    "Ethical Hacking": "https://www.netacad.com/",
    "Wireshark": "https://www.wireshark.org/docs/",
    "Cybersecurity": "https://www.cisa.gov/cybersecurity",
    "REST API": "https://www.postman.com/api-platform/api-documentation/",
    "Problem Solving": "https://www.hackerrank.com/",
    "OOP": "https://www.geeksforgeeks.org/object-oriented-programming-oops-concept-in-java/"
}

# EXTRACT RESUME TEXT
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# DETECT SKILLS
def detect_skills(text, skill_list):
    found = []

    for skill in skill_list:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            found.append(skill)

    return found


# LEARNING ROADMAP
def create_roadmap(missing_skills):

    roadmap = []

    for index, skill in enumerate(missing_skills, 1):

        link = learning_links.get(
            skill,
            "https://www.google.com/search?q=" + skill + "+tutorial"
        )

        roadmap.append({
            "week": index,
            "skill": skill,
            "link": link
        })

    return roadmap


# MAIN APPLICATION
st.title("📄 AI Resume Analyzer & Skill Gap Detector")

st.write(
    "Analyze your resume, identify missing skills, "
    "and discover what you need to learn for your dream job."
)

st.info(
    "This application uses keyword-based resume analysis "
    "to provide skill recommendations."
)

# USER INPUT
st.subheader("👤 Personal Information")

name = st.text_input("Enter your name")

role = st.selectbox(
    "Select your target job role",
    list(job_skills.keys())
)

st.subheader("📋 Job Description")

job_description = st.text_area(
    "Paste the job description here (optional)",
    height=150,
    placeholder="Paste the company's required skills and job description..."
)

st.subheader("📁 Upload Resume")

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)

# ANALYSIS BUTTON
if st.button("🚀 Analyze My Resume"):

    if not name.strip():
        st.warning("Please enter your name.")

    elif not uploaded_file:
        st.warning("Please upload your resume PDF.")

    else:

        try:
            resume_text = extract_text(uploaded_file)

            if not resume_text.strip():
                st.error(
                    "No readable text found. Please upload a text-based PDF."
                )

            else:

                # GET REQUIRED SKILLS
                if job_description.strip():
                    required_skills = detect_skills(
                        job_description,
                        list(learning_links.keys())
                    )

                    if not required_skills:
                        required_skills = job_skills[role]

                        st.warning(
                            "No recognized skills found in the job description. "
                            "Using the selected job role instead."
                        )
                else:
                    required_skills = job_skills[role]

                # RESUME SKILLS
                resume_skills = detect_skills(
                    resume_text,
                    list(learning_links.keys())
                )

                # MATCHING
                matched = [
                    skill for skill in required_skills
                    if skill in resume_skills
                ]

                missing = [
                    skill for skill in required_skills
                    if skill not in resume_skills
                ]

                total = len(required_skills)

                percentage = (
                    (len(matched) / total) * 100
                    if total > 0 else 0
                )

                # RESULTS
                st.divider()

                st.header("📊 Resume Analysis Results")

                st.write("Candidate:", name)
                st.write("Target Role:", role)

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Skill Match",
                    f"{percentage:.1f}%"
                )

                col2.metric(
                    "Matched Skills",
                    len(matched)
                )

                col3.metric(
                    "Missing Skills",
                    len(missing)
                )

                # PROGRESS BAR
                st.subheader("🎯 Job Readiness")

                st.progress(int(percentage))

                if percentage >= 75:
                    st.success(
                        "Excellent! Your resume matches many of the required skills."
                    )

                elif percentage >= 40:
                    st.warning(
                        "Good start! Work on your missing skills to improve your profile."
                    )

                else:
                    st.info(
                        "Keep learning! Focus on building the important skills for this role."
                    )

                # MATCHED SKILLS
                st.subheader("✅ Matched Skills")

                if matched:
                    st.write(", ".join(matched))
                else:
                    st.write("No matching skills detected.")

                # MISSING SKILLS
                st.subheader("❌ Missing Skills")

                if missing:
                    st.write(", ".join(missing))
                else:
                    st.success("You have all the detected required skills!")

                # CHART
                st.subheader("📈 Skill Match Analysis")

                fig = go.Figure(data=[
                    go.Pie(
                        labels=["Matched Skills", "Missing Skills"],
                        values=[len(matched), len(missing)],
                        hole=0.55
                    )
                ])

                fig.update_layout(
                    title="Resume Skill Analysis",
                    showlegend=True
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                # LEARNING ROADMAP
                st.divider()

                st.header("📚 Personalized Learning Roadmap")

                if missing:

                    st.write(
                        "Follow this suggested learning order "
                        "to improve your job readiness."
                    )

                    roadmap = create_roadmap(missing)

                    for item in roadmap:

                        st.markdown(
                            f"### Week {item['week']}: {item['skill']}"
                        )

                        st.markdown(
                            f"[Start Learning]({item['link']})"
                        )

                else:
                    st.success(
                        "Great! No missing skills were detected "
                        "from the selected requirements."
                    )

                # RECOMMENDATIONS
                st.divider()

                st.header("💡 Career Recommendations")

                if missing:
                    st.write(
                        "1. Start learning the missing skills."
                    )
                    st.write(
                        "2. Build practical projects using those skills."
                    )
                    st.write(
                        "3. Add your projects and achievements to your resume."
                    )
                    st.write(
                        "4. Practice technical and interview questions."
                    )

                else:
                    st.write(
                        "Continue building projects and preparing for interviews."
                    )

                # DOWNLOAD REPORT
                report = f"""
AI RESUME ANALYZER REPORT

Candidate Name: {name}
Target Job Role: {role}

SKILL MATCH: {percentage:.2f}%

MATCHED SKILLS:
{', '.join(matched)}

MISSING SKILLS:
{', '.join(missing)}

RECOMMENDATIONS:
Build your missing skills and work on practical projects.

Note: This is a basic keyword-based resume analysis.
It is not a complete AI assessment.
"""

                st.download_button(
                    label="📥 Download Analysis Report",
                    data=report,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error(
                f"Something went wrong while analyzing your resume: {e}"
            )


# FOOTER
st.divider()

st.markdown(
    "Developed with ❤️ | AI Resume Analyzer & Skill Gap Detector"
)
