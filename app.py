import streamlit as st
import pandas as pd
import json
from modules import agent_logic

# --- Page Configuration ---
st.set_page_config(
    page_title="Terrier Career Agent",
    page_icon="🤖",
    layout="wide"
)

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads all necessary data from the /data directory."""
    try:
        with open('data/student_data.json', 'r') as f:
            student_data = json.load(f)
        with open('data/job_requirements.json', 'r') as f:
            job_requirements = json.load(f)
        with open('data/course_catalog.json', 'r') as f:
            course_catalog = json.load(f)
        alumni_df = pd.read_csv('data/alumni_database.csv')
        return student_data, job_requirements, course_catalog, alumni_df
    except FileNotFoundError as e:
        st.error(f"Error: A required data file was not found. Please make sure the `data` directory is correct. Details: {e}")
        return None, None, None, None

student_data, job_requirements, course_catalog, alumni_df = load_data()

# --- Main Application ---
if student_data:
    st.title("🤖 Terrier Career Agent")
    st.markdown("Your personal AI career coach, powered by AI.")

    # --- Sidebar for Profile and User Input ---
    with st.sidebar:
        st.header("Your Profile")
        st.markdown(f"**Name:** {student_data.get('student_name', 'N/A')}")
        st.markdown(f"**Major:** {student_data.get('major', 'N/A')}")
        st.divider()
        st.subheader("Add Your Skills")
        user_skills_input = st.text_area(
            "List skills from projects or experience (comma-separated):",
            "Git, Public Speaking, Agile"
        )
        user_skills_list = [skill.strip() for skill in user_skills_input.split(',') if skill.strip()]

    # --- Main Interaction Logic ---
    if 'analysis' not in st.session_state:
        st.session_state.analysis = None

    if st.button("🚀 Analyze My Career Profile", type="primary", use_container_width=True):
        with st.spinner("AI is analyzing your profile... This may take a moment."):
            st.session_state.analysis = agent_logic.get_profile_analysis(student_data)

    if st.session_state.analysis:
        if "error" in st.session_state.analysis:
            st.error(f"An error occurred during analysis: {st.session_state.analysis['error']}")
        else:
            # --- 1. AI-Powered Profile Analysis ---
            st.header("1. AI-Powered Profile Analysis")
            strengths = st.session_state.analysis.get('strengths', [])
            if strengths:
                for strength in strengths:
                    st.success(f"✓ {strength}")
            else:
                st.info("No specific strengths were identified in this analysis.")
            st.divider()

            # --- 2. Career Path Exploration ---
            st.header("2. Career Path Exploration")
            job_paths = st.session_state.analysis.get('suggested_paths', [])

            if not job_paths:
                st.warning("The AI did not suggest specific career paths in this run. You can try analyzing your profile again.")
            else:
                selected_path = st.selectbox("Select a path to explore further:", options=job_paths)

                if selected_path:
                    # --- Skill Gap Analysis ---
                    gap_analysis = agent_logic.perform_skill_gap_analysis(student_data, user_skills_list, selected_path, job_requirements)
                    st.subheader(f"Visual Skill Analysis for a {selected_path}")
                    
                    chart_data = pd.DataFrame({
                        'Count': [len(gap_analysis['skills_have']), len(gap_analysis['skills_needed'])]
                    }, index=['Skills You Have', 'Skills You Need'])
                    st.bar_chart(chart_data)

                    # --- Course Recommendations ---
                    st.subheader("📚 Recommended BU Courses to Fill Gaps")
                    recommended_courses = agent_logic.recommend_courses(gap_analysis['skills_needed'], course_catalog)
                    if recommended_courses:
                        for course in recommended_courses:
                            st.info(f"**{course['course_code']}: {course['course_name']}** → Teaches: {', '.join(course['provides_skills'])}")
                    else:
                        st.warning("No specific courses found in our catalog for your needed skills.")
                    st.divider()

                    # --- Alumni Connector ---
                    st.header("3. The Alumni Network")
                    st.markdown(f"Find Terriers working as a **{selected_path}**")
                    relevant_alumni = agent_logic.find_relevant_alumni(selected_path, alumni_df)
                    if not relevant_alumni.empty:
                        st.dataframe(relevant_alumni)
                    else:
                        st.info("No alumni found for this role in our mock database.")
