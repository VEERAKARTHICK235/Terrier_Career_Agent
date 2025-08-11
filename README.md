# 🤖 Terrier Career Agent

This project is an AI-powered career coach designed for the HackBU hackathon. It analyzes a student's academic profile, performs a skill-gap analysis for potential careers, recommends courses, and helps find relevant alumni. This version uses the Google Gemini REST API.

## ✨ Features

- **Dynamic AI Analysis:** Uses the Gemini API for real-time career suggestions.
- **Interactive Skill Input:** Allows users to add skills from outside their coursework.
- **Visual Skill-Gap Analysis:** Displays a chart comparing existing skills to required skills.
- **Course Recommendations:** Suggests specific courses to fill identified skill gaps.
- **Secure API Key Handling:** Uses a `.env` file to keep secrets safe.

## 🚀 How to Run

1.  **Clone the Repository:**
    ```bash
    git clone <https://github.com/VEERAKARTHICK235/Terrier_Career_Agent.git>
    cd terrier_career_agent
    ```

2.  **Create the Environment File:**
    -   Create a file named `.env` in the root directory.
    -   Add your API key to it: `GEMINI_API_KEY="YOUR_API_KEY_HERE"`

3.  **Install Dependencies:**
    -   It's recommended to use a virtual environment.
    -   Run: `pip install -r requirements.txt`

4.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```

The application will open in your web browser. Enjoy!
