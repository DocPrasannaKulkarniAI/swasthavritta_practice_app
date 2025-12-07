import streamlit as st
import json
import random

# ---------------------------------------------------------
# 📌 PAGE CONFIG (Mobile friendly)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Swasthavritta Question Practice by PraKul",
    layout="wide"
)

# ---------------------------------------------------------
# 📌 CUSTOM CSS FOR MOBILE-FRIENDLY UI
# ---------------------------------------------------------
st.markdown("""
<style>
    body, p, div, span {
        font-size: 1.05rem !important;
    }
    .stButton>button {
        font-size: 1.1rem !important;
        padding: 0.6rem 1.2rem !important;
    }
    .question-box {
        padding: 0.8rem;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 4px solid #4a90e2;
    }
    .footer {
        text-align: center;
        padding: 15px;
        margin-top: 40px;
        color: #666;
        font-size: 0.9rem;
    }
    .quote-box {
        background: #fff7e6;
        padding: 12px;
        border-left: 4px solid #ffa500;
        border-radius: 5px;
        font-style: italic;
        font-size: 1.15rem;
        margin-bottom: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 📌 ROTATING INSPIRATIONAL QUOTES
# ---------------------------------------------------------
quotes = [
    "Success begins with preparation. Preparation begins with practice.",
    "Consistency beats intensity — small steps daily ensure big results.",
    "A disciplined student becomes an exceptional physician.",
    "Learning Ayurveda is tapas — steady effort brings mastery."
]
st.markdown(f"<div class='quote-box'>{random.choice(quotes)}</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 📌 SIDEBAR INFORMATION
# ---------------------------------------------------------
st.sidebar.title("Swasthavritta Question Practice by PraKul")

st.sidebar.markdown("""
**Prof. (Dr.) Prasanna Kulkarni**  
Healthcare AI-GPT Developer  
Department of Swasthavritta  
SKAMCRC Bengaluru  

🌐 [Visit Website](https://atharvaayurtech.com)

📝 [MCQ Practice – AyurKrida AI](https://atharvaayurtech.com/AI/tools/ayurkrida-ai-quiz-simulation/2)
""")

# ---------------------------------------------------------
# 📌 LOAD QUESTION BANK
# ---------------------------------------------------------
with open("question_bank.json", "r") as f:
    data = json.load(f)

topic_groups = data["topic_groups"]
saq_pool = data["saq_pool"]
laq_pool = data["laq_pool"]

# ---------------------------------------------------------
# 📌 MODE SELECTION
# ---------------------------------------------------------
mode = st.radio(
    "Choose Mode",
    ["Topic-Wise Practice", "Generate Paper-1 (80 Marks)", "Generate Paper-2 (80 Marks)"]
)

# ---------------------------------------------------------
# 📌 TOPIC-WISE MODE
# ---------------------------------------------------------
if mode == "Topic-Wise Practice":

    topics = {k: v["name"] for k, v in topic_groups.items()}
    selected = st.selectbox("Select Topic:", list(topics.keys()), format_func=lambda x: topics[x])

    marks = topic_groups[selected]["marks"]

    st.subheader(f"Topic: {topics[selected]} ({marks} Marks)")

    # SAQs
    if selected in saq_pool:
        st.markdown("### Short Answer Questions (5 Marks)")
        qlist = saq_pool[selected]
        q1, q2 = random.sample(qlist, 2)
        st.markdown(f"<div class='question-box'>• {q1}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='question-box'>• {q2}</div>", unsafe_allow_html=True)

    # LAQs
    if topic_groups[selected]["laq_eligible"] and selected in laq_pool:
        st.markdown("### Long Answer Question (10 Marks)")
        ql = random.choice(laq_pool[selected])
        st.markdown(f"<div class='question-box'>• {ql}</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 📌 PAPER-WISE GENERATOR FUNCTION
# ---------------------------------------------------------
def generate_paper(paper_type):

    if paper_type == 1:  # PAPER 1 LAQs
        laq_topics = ["2_3_4", "ritucharya", "7", "9_10"]
        saq_topics = ["1", "2_3_4", "ratricharya", "ritucharya", "5_6", "7", "8", "9", "10"]

    elif paper_type == 2:  # PAPER 2 LAQs
        laq_topics = ["11", "12_13", "17_18_19_20", "24_25"]
        saq_topics = ["11", "12_13", "14_15_16", "17_18_19_20"]

    # Generate 4 LAQs
    final_laqs = []
    for t in laq_topics:
        if t in laq_pool:
            final_laqs.append(random.choice(laq_pool[t]))
        if len(final_laqs) == 4:
            break

    # Generate 8 SAQs
    final_saqs = []
    all_saq_list = []
    for t in saq_topics:
        if t in saq_pool:
            all_saq_list.extend(saq_pool[t])

    final_saqs = random.sample(all_saq_list, 8)

    # DISPLAY RESULTS
    st.header("80-Marks Question Paper")
    st.markdown("### **SECTION A — Long Answer Questions (10 Marks × 4 = 40 Marks)**")

    for i, q in enumerate(final_laqs, start=1):
        st.markdown(f"<div class='question-box'><b>Q{i}.</b> {q}</div>", unsafe_allow_html=True)

    st.markdown("### **SECTION B — Short Answer Questions (5 Marks × 8 = 40 Marks)**")

    for i, q in enumerate(final_saqs, start=1):
        st.markdown(f"<div class='question-box'><b>Q{i}.</b> {q}</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 📌 HANDLE PAPER-WISE MODE
# ---------------------------------------------------------
if mode == "Generate Paper-1 (80 Marks)":
    generate_paper(1)

elif mode == "Generate Paper-2 (80 Marks)":
    generate_paper(2)

# ---------------------------------------------------------
# 📌 FOOTER
# ---------------------------------------------------------
st.markdown("""
<div class='footer'>
Concept and App Developed by <b>Prof. (Dr.) Prasanna Kulkarni</b> • Swasthavritta, SKAMCRC Bengaluru
</div>
""", unsafe_allow_html=True)
