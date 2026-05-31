
import streamlit as st
import joblib
import pdfplumber
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time


st.set_page_config(
    page_title="TalentLens AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');


html, body, [class*="css"], .stApp, .stMarkdown, p, div, label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.12), transparent 40%),
        radial-gradient(circle at 90% 20%, rgba(236,72,153,0.10), transparent 45%),
        radial-gradient(circle at 50% 90%, rgba(14,165,233,0.10), transparent 45%),
        linear-gradient(180deg, #F8FAFF 0%, #EEF2FF 100%);
    background-attachment: fixed;
    color: #0F172A;
}

#MainMenu, footer, header {visibility: hidden;}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}


@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes floatY {
    0%,100% { transform: translateY(0); }
    50%     { transform: translateY(-6px); }
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
}
@keyframes pulseGlow {
    0%,100% { box-shadow: 0 0 0 0 rgba(99,102,241,0.35); }
    50%     { box-shadow: 0 0 0 14px rgba(99,102,241,0); }
}
@keyframes popIn {
    0%   { opacity: 0; transform: scale(0.85); }
    100% { opacity: 1; transform: scale(1); }
}


.hero {
    text-align: center;
    padding: 38px 20px 28px;
    animation: fadeUp 0.9s ease both;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    color: #4338CA;
    margin-bottom: 18px;
    animation: floatY 4s ease-in-out infinite;
}
.hero-badge .dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #10B981;
    box-shadow: 0 0 10px #10B981;
    animation: pulseGlow 2s infinite;
}
.main-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: clamp(40px, 6vw, 64px);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.05;
    background: linear-gradient(120deg, #4F46E5 0%, #7C3AED 35%, #EC4899 70%, #F59E0B 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 8s ease infinite;
    margin: 0 0 12px;
}
.sub-title {
    font-size: 18px;
    color: #475569;
    max-width: 620px;
    margin: 0 auto 8px;
    font-weight: 500;
}


.metric-card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.9);
    padding: 22px 18px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 8px 30px rgba(15,23,42,0.06);
    transition: all .35s cubic-bezier(.2,.8,.2,1);
    animation: fadeUp 0.8s ease both;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(236,72,153,0.06));
    opacity: 0;
    transition: opacity .35s ease;
}
.metric-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 18px 45px rgba(79,70,229,0.18);
    border-color: rgba(99,102,241,0.35);
}
.metric-card:hover::before { opacity: 1; }
.metric-card h2 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 34px;
    font-weight: 700;
    margin: 0 0 4px;
    background: linear-gradient(135deg, #4F46E5, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
}
.metric-card p {
    color: #64748B;
    font-size: 14px;
    font-weight: 500;
    margin: 0;
    position: relative;
}
.metric-card .icon {
    font-size: 26px;
    margin-bottom: 8px;
    display: inline-block;
    animation: floatY 3.5s ease-in-out infinite;
}


.card {
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.9);
    padding: 28px 30px;
    border-radius: 22px;
    box-shadow: 0 10px 40px rgba(15,23,42,0.06);
    margin-bottom: 22px;
    animation: fadeUp 0.7s ease both;
    transition: transform .3s ease, box-shadow .3s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 50px rgba(79,70,229,0.12);
}
.card h3, .card .stSubheader {
    margin-top: 0 !important;
}


section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #F1F5FF 100%);
    border-right: 1px solid rgba(99,102,241,0.12);
    box-shadow: 4px 0 30px rgba(15,23,42,0.04);
}
section[data-testid="stSidebar"] * { color: #0F172A !important; }
section[data-testid="stSidebar"] .stAlert {
    background: rgba(99,102,241,0.08) !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    border-radius: 14px !important;
}


[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(14px);
    border: 2px dashed rgba(99,102,241,0.4);
    border-radius: 20px;
    padding: 28px;
    transition: all .3s ease;
    animation: fadeUp 0.8s ease both;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6366F1;
    background: rgba(238,242,255,0.8);
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(99,102,241,0.15);
}
[data-testid="stFileUploader"] section { color: #0F172A !important; font-size: 16px; font-weight: 500; }
[data-testid="stFileUploader"] small { color: #475569 !important; }
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #4F46E5, #7C3AED) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
    transition: all .25s ease;
}
[data-testid="stFileUploader"] button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(79,70,229,0.35);
}


.stButton > button {
    width: 100%;
    height: 3.2em;
    border-radius: 14px;
    background: linear-gradient(120deg, #4F46E5, #7C3AED, #EC4899);
    background-size: 200% 200%;
    color: white;
    font-size: 16px;
    font-weight: 700;
    border: none;
    transition: all .3s ease;
    box-shadow: 0 10px 25px rgba(79,70,229,0.30);
}
.stButton > button:hover {
    transform: translateY(-2px);
    background-position: 100% 0;
    box-shadow: 0 15px 35px rgba(124,58,237,0.40);
}


.skill-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(236,72,153,0.10));
    color: #4338CA;
    padding: 8px 16px;
    border-radius: 999px;
    display: inline-block;
    margin: 5px;
    font-weight: 600;
    font-size: 14px;
    border: 1px solid rgba(99,102,241,0.25);
    transition: all .25s ease;
    animation: popIn 0.5s ease both;
}
.skill-box:hover {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 8px 18px rgba(99,102,241,0.25);
    background: linear-gradient(135deg, #4F46E5, #7C3AED);
    color: white;
}
.skill-missing {
    background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(239,68,68,0.10));
    color: #B45309;
    border-color: rgba(245,158,11,0.30);
}
.skill-missing:hover {
    background: linear-gradient(135deg, #F59E0B, #EF4444);
    color: white;
    box-shadow: 0 8px 18px rgba(245,158,11,0.30);
}


.result-headline {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 30px;
    font-weight: 700;
    background: linear-gradient(120deg, #4F46E5, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 6px 0 0;
}
.card-eyebrow {
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 12px;
    font-weight: 700;
    color: #6366F1;
    margin-bottom: 6px;
}

h1,h2,h3,h4,h5,h6 {
    color: #0F172A !important;
    font-family: 'Space Grotesk', sans-serif !important;
}


textarea {
    background-color: white !important;
    color: #0F172A !important;
    border-radius: 12px !important;
}
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.7) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}
.stAlert {
    border-radius: 14px !important;
    backdrop-filter: blur(10px);
    animation: fadeIn 0.5s ease both;
}


.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #4F46E5, #7C3AED, #EC4899);
    background-size: 200% 100%;
    animation: shimmer 1.6s linear infinite;
}


.app-footer {
    text-align: center;
    padding: 24px 0 8px;
    color: #64748B;
    font-size: 14px;
}
.app-footer .heart {
    background: linear-gradient(135deg, #EC4899, #F43F5E);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


model = joblib.load("model.pkl")
tfidf = joblib.load("tfidf.pkl")
le = joblib.load("encoder.pkl")


category_skills = {
    "INFORMATION-TECHNOLOGY": [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "power bi",
    "tableau",
    "git",
    "github",
    "streamlit",
    "flask",
    "tensorflow",
    "pytorch",
    "deep learning",
    "nlp",
    "statistics"

    ],
    "DESIGNER": [
        "photoshop", "illustrator", "figma", "canva",
        "ui ux", "branding", "wireframing", "html", "css"
    ],
    "FINANCE": [
        "excel", "financial analysis", "forecasting", "budgeting",
        "power bi", "tableau", "leadership", "communication", "data analysis"
    ],
    "AVIATION": [
        "communication", "leadership", "teamwork", "airport operations",
        "problem solving", "time management", "safety procedures"
    ],
    "BUSINESS-DEVELOPMENT": [
        "sales", "marketing", "negotiation", "communication",
        "leadership", "project management", "business strategy"
    ],
    "ENGINEERING": [
        "autocad", "solidworks", "matlab", "problem solving",
        "project management", "leadership", "communication"
    ],
    "HEALTHCARE": [
        "patient care", "medical terminology", "communication",
        "teamwork", "leadership", "time management"
    ],
    "DATA SCIENCE & AI": [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "power bi",
    "tableau",
    "git",
    "github",
    "streamlit",
    "flask",
    "tensorflow",
    "pytorch",
    "deep learning",
    "nlp",
    "statistics"

]
}


all_skills = []
for skill_list in category_skills.values():
    all_skills.extend(skill_list)
all_skills = list(set(all_skills))


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text
    return text.strip()


def predict_category(resume_text):
    resume_tfidf = tfidf.transform([resume_text])
    prediction = model.predict(resume_tfidf)
    category = le.inverse_transform(prediction)[0]
    return category


def extract_skills(text):
    text = text.lower()
    found_skills = []
    for skill in all_skills:
        if skill.lower() in text:
            found_skills.append(skill)
    return found_skills


def missing_skills(found_skills, category):
    recommended_skills = category_skills.get(category, [])
    missing = []
    for skill in recommended_skills:
        if skill not in found_skills:
            missing.append(skill)
    return missing[:6]




def ats_score(found_skills, category, text):
    recommended_skills = category_skills.get(category, [])
    if len(recommended_skills) == 0:
        return 35
    matched = 0
    for skill in recommended_skills:
        if skill in found_skills:
            matched += 1
    skill_score = (matched / len(recommended_skills)) * 70
    word_count = len(text.split())
    if word_count > 350:
        length_score = 20
    elif word_count > 200:
        length_score = 15
    elif word_count > 100:
        length_score = 10
    else:
        length_score = 5
    bonus = 0
    if matched >= 6:
        bonus = 5
    final_score = skill_score + length_score + bonus
    final_score = min(final_score, 96)
    return int(final_score)


def resume_strength(score):
    if score >= 80:
        return "Excellent Resume 🚀"
    elif score >= 65:
        return "Strong Resume 💪"
    elif score >= 45:
        return "Average Resume 🙂"
    else:
        return "Needs Improvement ⚠️"


def analyze_resume(resume_text):
    category = predict_category(resume_text)

    found_skills = extract_skills(resume_text)

    if (
        "python" in found_skills
        and "machine learning" in found_skills
    ):
        category = "DATA SCIENCE & AI"

    missing = missing_skills(found_skills, category)

    score = ats_score(found_skills, category, resume_text)

    strength = resume_strength(score)

    return {
        "Suggested Career Domain": category,
        "Skills Found": found_skills,
        "Missing Skills": missing,
        "ATS Score": score,
        "Resume Strength": strength
    }


st.markdown("""
<div class="hero">
    <div class="hero-badge"><span class="dot"></span> AI-Powered Resume Intelligence</div>
    <div class="main-title">TalentLens AI</div>
    <div class="sub-title">Premium AI Resume Analyzer & ATS Scanner — uncover your strengths, fix the gaps, land the role.</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
metrics = [
    ("⚡", "95%", "Prediction Accuracy"),
    ("🎯", "ATS", "Resume Scoring"),
    ("🧠", "AI", "Skill Intelligence"),
    ("📊", "NLP", "Resume Classification"),
]
for col, (icon, value, label) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="icon">{icon}</div>
            <h2>{value}</h2>
            <p>{label}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.sidebar.markdown("### 🚀 TalentLens AI")
st.sidebar.markdown("##### Your career co-pilot")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 About")
st.sidebar.info("""
**TalentLens AI** uses:

✔ Machine Learning  
✔ Natural Language Processing  
✔ TF-IDF Vectorization  
✔ ATS Scoring Engine  
✔ Smart Skill Extraction  
✔ Career Domain Prediction  
""")
st.sidebar.markdown("### 💡 How it works")
st.sidebar.markdown("""
1. Upload your resume PDF  
2. AI extracts text & skills  
3. Predicts best career domain  
4. Scores your resume for ATS  
5. Recommends missing skills  
""")
st.sidebar.markdown("---")
st.sidebar.caption("v2.0 · Premium Edition")

st.markdown("### 📄 Upload Your Resume")
st.caption("Drop a PDF below — we'll do the rest in seconds.")
uploaded_file = st.file_uploader(" ", type=["pdf"], label_visibility="collapsed")

if uploaded_file is not None:
    with st.spinner("🔎 Analyzing your resume with AI..."):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)
        resume_text = extract_text_from_pdf(uploaded_file)

    if len(resume_text) < 50:
        st.error("⚠️ Could not extract proper text from this PDF.")
        st.stop()

    result = analyze_resume(resume_text)
    st.success("✅ Resume Analysis Completed Successfully")

    

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-eyebrow">🎯 Suggested Career Domain</div>
            <div class="result-headline">{result['Suggested Career Domain']}</div>
            <p style="color:#64748B;margin-top:10px;">Best-matched industry based on your resume content.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="card-eyebrow">💡 Resume Strength</div>
            <div class="result-headline">{result['Resume Strength']}</div>
            <p style="color:#64748B;margin-top:10px;">Overall quality signal derived from skills, length & ATS score.</p>
        </div>
        """, unsafe_allow_html=True)

    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-eyebrow">📊 ATS Resume Score</div>', unsafe_allow_html=True)
    score = result["ATS Score"]
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'font': {'size': 54, 'color': '#0F172A', 'family': 'Space Grotesk'}},
        title={'text': "<b>ATS Compatibility</b>", 'font': {'size': 18, 'color': '#475569'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#CBD5E1'},
            'bar': {'color': "#4F46E5", 'thickness': 0.28},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50],   'color': "rgba(239,68,68,0.25)"},
                {'range': [50, 75],  'color': "rgba(245,158,11,0.25)"},
                {'range': [75, 100], 'color': "rgba(16,185,129,0.30)"},
            ],
            'threshold': {
                'line': {'color': "#EC4899", 'width': 4},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    gauge.update_layout(
        height=360,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Plus Jakarta Sans'}
    )
    st.plotly_chart(gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-eyebrow">✅ Skills Detected</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='margin:0 0 14px;'>What you already bring to the table</h3>", unsafe_allow_html=True)
    if len(result["Skills Found"]) == 0:
        st.warning("No major skills detected. Try adding more keywords to your resume.")
    else:
        chips_html = "".join(
            f'<span class="skill-box" style="animation-delay:{i*0.05}s">{skill}</span>'
            for i, skill in enumerate(result["Skills Found"])
        )
        st.markdown(f"<div>{chips_html}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

        

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="card-eyebrow">⚠️ Recommended Skills</div>',
        unsafe_allow_html=True
    )

    

    if len(result["Missing Skills"]) == 0:

        st.markdown("""
        <div style="
            background:rgba(16,185,129,0.12);
            border:1px solid rgba(16,185,129,0.25);
            padding:18px;
            border-radius:14px;
            color:#059669;
            font-weight:600;
            margin-top:15px;
        ">
            🎉 Your resume already has strong skill alignment.
            No additional skills are currently recommended.
        </div>
        """, unsafe_allow_html=True)

    

    else:

        st.markdown("""
        <h3 style='margin-top:10px; margin-bottom:20px;'>
            Add these skills to boost your ATS score
        </h3>
        """, unsafe_allow_html=True)

        skills_html = ""

        for i, skill in enumerate(result["Missing Skills"]):

            skills_html += f"""
            <span class="skill-box skill-missing"
            style="
                animation-delay:{i*0.05}s;
                margin-right:10px;
                margin-bottom:12px;
                display:inline-block;
            ">
                {skill}
            </span>
            """

        st.markdown(skills_html, unsafe_allow_html=True)

    st.markdown(
        """
        <div style='margin-bottom:25px;'></div>
        """,
        unsafe_allow_html=True
    )

   

    with st.expander("📑 View Extracted Resume Text"):

        st.text_area(
            "Resume Text",
            resume_text,
            height=320
        )

        st.download_button(
            label="⬇ Download Resume Text",
            data=resume_text,
            file_name="resume_text.txt",
            mime="text/plain"
        )

else:

    st.markdown("""
    <div class="card" style="text-align:center;">
        <div style="font-size:46px;animation:floatY 3s ease-in-out infinite;">📤</div>
        <h3 style="margin:8px 0 6px;">Upload a resume to begin</h3>
        <p style="color:#64748B;margin:0;">Your analysis, ATS score and personalized skill recommendations will appear here.</p>
    </div>
    """, unsafe_allow_html=True)
     