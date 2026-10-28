import streamlit as st
from pypdf import PdfReader
import re
import plotly.graph_objects as go
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄"
)
st.markdown("""
<style>
 stApp {
    background-color: #f4f6ff;
}
h1 {
    color: #4b0082;
    text-align: center;
}
h2, h3 {
    color: #673ab7;
}
.stButton > button {
    background-color: #673ab7;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
}
.stButton > button:hover {
    background-color: #512da8;
    color: white;
}

/* Website Background */
stApp {
 background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
}


    color: #4527a0;
    text-align: center;
    font-weight: bold;


/* Buttons */
 stButton > button {
    background-color: #673ab7;
    color: white;
    border-radius: 12px;
    padding: 10px 25px;
    font-weight: bold;
}

/* Button Hover Effect */
.stButton > button:hover {
    background-color: #512da8;
    color: white;
}

/* Section Headings */
h2, h3 {
    color: #283593;
}

</style>
""", unsafe_allow_html=True)
st.title("🤖 AI Resume Analyzer")
st.write("Upload your resume and discover your skill gaps!")

# Job roles and required skills
job_skills = {
    "Software Developer": [
        "python", "java", "sql", "html",
        "git", "javascript", "data structures"
    ],
    "Web Developer": [
        "html", "css", "javascript",
        "python", "git"
    ],
    "Data Analyst": [
        "python", "sql", "excel",
        "power bi", "statistics"
    ],
    "Cybersecurity Analyst": [
        "python", "linux", "networking",
        "cybersecurity", "sql"
    ]
}

# Get user details
name = st.text_input("Enter your name")

role = st.selectbox(
    "Select your target job role",
    list(job_skills.keys())
)

# Resume upload
uploaded_file = st.file_uploader(
    "📄 Upload your Resume (PDF)",
    type=["pdf"]
)

# Extract text from PDF
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text.lower()

# Detect skills
def detect_skills(text, skills):
    detected = []

    for skill in skills:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            detected.append(skill)

    return detected

# Analyze resume
if st.button("🔍 Analyze My Resume"):

    if not name.strip():
        st.warning("Please enter your name.")

    elif uploaded_file is None:
        st.warning("Please upload your PDF resume.")

    else:
        try:
            resume_text = extract_text(uploaded_file)

            if not resume_text.strip():
                st.error(
                    "Could not read the PDF text. "
                    "Please upload a text-based PDF."
                )

            else:
                required_skills = job_skills[role]

                matched = detect_skills(
                    resume_text,
                    required_skills
                )

                missing = [
                    skill for skill in required_skills
                    if skill not in matched
                ]

                percentage = (
                    len(matched) / len(required_skills)
                ) * 100
                # Skill Match Donut Chart
                fig = go.Figure(data=[go.Pie(
    labels=["Matched Skills", "Missing Skills"],
    values=[len(matched), len(missing)],
    hole=0.6,
    marker=dict(colors=["#4CAF50", "#FF5252"])
)])

                fig.update_layout(
    title="Skill Match Analysis",
    title_x=0.5
)

                st.plotly_chart(fig, use_container_width=True)

                st.success(
                    f"Resume Analysis for {name}"
                )

                st.subheader("📊 Skill Match")
                st.progress(percentage / 100)
                st.write(f"{percentage:.2f}% Match")

                st.subheader("✅ Skills Found")
                if matched:
                    for skill in matched:
                        st.write("✔", skill.title())
                else:
                    st.write("No required skills detected.")

                st.subheader("📚 Skills to Improve")
                if missing:
                    for skill in missing:
                        st.write("➜", skill.title())
                else:
                    st.write("All listed skills detected!")
# Skill Analysis Chart
                st.subheader("📊 Skill Analysis Chart")

                fig = go.Figure(data=[
                    go.Bar(
                        x=["Matched Skills", "Missing Skills"],
                        y=[len(matched), len(missing)],
                        marker_color=["#673AB7", "#FF9800"],
                        text=[len(matched), len(missing)],
                        textposition="auto"
                    )
                ])

                fig.update_layout(
                    title="Your Skill Gap Analysis",
                    xaxis_title="Skill Category",
                    yaxis_title="Number of Skills",
                    template="plotly_white"
                )

                st.plotly_chart(fig, use_container_width=True)
                st.subheader("💡 Recommendations")

                if percentage >= 80:
                    st.success(
                        "Great skill match! "
                        "Keep improving your knowledge."
                    )
                elif percentage >= 50:
                    st.info(
                        "Good progress! Focus on missing skills."
                    )
                else:
                    st.warning(
                        "Build your skills step by step."
                    )

                st.caption(
                    "This is a basic keyword-based resume "
                    "analyzer, not a full AI assessment. "
                    "Missing skills mean they were not "
                    "detected in the resume."
                )
                st.caption(
                    "This is a basic keyword-based resume "
                    "analyzer, not a full AI assessment. "
                    "Missing skills mean they were not "
                    "detected in the resume."
                )

                # Learning Resources code ಇಲ್ಲಿ

                # Download Report code ಇಲ್ಲಿ

        except Exception as e:
            st.error(
                "Unable to read this PDF. "
                "Please try another valid PDF."
            )

                # ಇಲ್ಲಿ ಹೊಸ code paste ಮಾಡು

        except Exception as e:
            st.error(
                "Unable to read this PDF. "
                "Please try another valid PDF."
            )
      # Learning Resources
st.subheader("📚 Learning Resources")

learning_links = {
    "python": "https://www.learnpython.org/",
    "java": "https://www.w3schools.com/java/",
    "sql": "https://www.w3schools.com/sql/",
    "html": "https://www.w3schools.com/html/",
    "css": "https://www.w3schools.com/css/",
    "javascript": "https://www.w3schools.com/js/",
    "react": "https://react.dev/learn",
    "machine learning": "https://developers.google.com/machine-learning/crash-course"
}

if "missing" in locals():
    for skill in missing:
        link = learning_links.get(skill.lower())
        if link:
            st.markdown(f"📖 [{skill.title()}]({link})")
        else:
            st.write(f"📖 Learn more about {skill.title()}")

# Career Recommendations
st.subheader("💡 Career Recommendations")

if "percentage" in locals():
    if percentage >= 80:
        st.success("Excellent skill match! You are well prepared.")
    elif percentage >= 50:
        st.info("Good progress! Improve your missing skills.")
    else:
        st.warning("Focus on learning missing skills to improve your job readiness.")

# Download Report
st.subheader("📄 Download Analysis Report")

if all(name in locals() for name in ["matched", "missing", "percentage"]):
    report = f"""
AI RESUME ANALYZER REPORT

Skill Match: {percentage:.2f}%

Matched Skills:
{', '.join(matched)}

Missing Skills:
{', '.join(missing)}

Recommendation:
Improve missing skills to increase your job readiness.
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain"
    )      