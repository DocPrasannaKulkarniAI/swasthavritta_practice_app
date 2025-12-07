import streamlit as st
import json
import random

# -------------------------------
# Load Question Bank
# -------------------------------
with open("question_bank.json", "r", encoding="utf-8") as f:
    qb = json.load(f)

# Track used questions (reset on topic change)
st.session_state.setdefault("used_saq", [])
st.session_state.setdefault("used_laq", [])

# -------------------------------
# Page Settings
# -------------------------------
st.set_page_config(page_title="Swasthavritta Question Practice", layout="wide")

st.title("📘 Swasthavritta Question Practice by PraKul")
st.caption("Department of Swasthavritta, SKAMCRC Bengaluru")

# -------------------------------
# Select Paper
# -------------------------------
paper_choice = st.radio(
    "Select Paper:",
    ["Paper 1: Principles of Swasthavritta, Yoga & Naturopathy",
     "Paper 2: Public Health"],
    horizontal=True
)

paper_key = "paper_1" if paper_choice.startswith("Paper 1") else "paper_2"
paper = qb[paper_key]

# -------------------------------
# Topic Selection
# -------------------------------
topic_keys = list(paper["topics"].keys())
topic_display = [
    f"{paper['topics'][k]['name']}  (Marks: {paper['topics'][k]['marks']})"
    for k in topic_keys
]

selected_topic_display = st.selectbox("Select Topic:", topic_display)
selected_key = topic_keys[topic_display.index(selected_topic_display)]

topic_info = paper["topics"][selected_key]
laq_allowed = topic_info["laq_eligible"]

# Reset used questions when topic changes
if st.session_state.get("last_topic") != selected_key:
    st.session_state["used_saq"] = []
    st.session_state["used_laq"] = []
    st.session_state["last_topic"] = selected_key

# -------------------------------
# Fetch Questions
# -------------------------------
saqs = paper["saq_pool"].get(selected_key, [])
laqs = paper["laq_pool"].get(selected_key, []) if laq_allowed else []

# -------------------------------
# Utility: Fetch Random Non-Repeating Question
# -------------------------------
def get_question(pool, used_list):
    available = [q for q in pool if q not in used_list]
    if not available:
        return None
    q = random.choice(available)
    used_list.append(q)
    return q

# -------------------------------
# Display Topic Heading
# -------------------------------
st.subheader(f"Topic: {topic_info['name']}  (Marks Allocated: {topic_info['marks']})")
st.markdown("---")

# -------------------------------
# SAQ Section
# -------------------------------
st.markdown("### ✍️ Short Answer Questions (5 Marks)")

q1 = get_question(saqs, st.session_state["used_saq"])
q2 = get_question(saqs, st.session_state["used_saq"])

if q1:
    st.write(f"- {q1}")
if q2:
    st.write(f"- {q2}")

if not saqs:
    st.info("No SAQs available for this topic.")

if st.button("🔄 Give More SAQs"):
    st.rerun()

st.markdown("---")

# -------------------------------
# LAQ Section (Only if Topic Eligible)
# -------------------------------
if laq_allowed:
    st.markdown("### 📝 Long Answer Questions (10 Marks)")

    ql = get_question(laqs, st.session_state["used_laq"])
    if ql:
        st.write(f"- {ql}")
    else:
        st.info("No more LAQs available for this topic.")

    if st.button("🔄 Give More LAQs"):
        st.rerun()

else:
    st.markdown("### 📝 Long Answer Questions (Not Applicable for This Topic)")
    st.info("This topic is NOT eligible for LAQs as per University rules.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Developed by **Prof. (Dr.) Prasanna Kulkarni** • Swasthavritta, SKAMCRC Bengaluru")
