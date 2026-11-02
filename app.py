
import streamlit as st
from openai import OpenAI
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Learning Roadmap Generator",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #10172a, #172554, #312e81);
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #93c5fd;
}
.subtitle {
    text-align: center;
    font-size: 17px;
    color: #cbd5e1;
}
div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #9333ea);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px 25px;
    font-weight: bold;
    width: 100%;
}
div.stButton > button:hover {
    border: 1px solid white;
    color: white;
}
.result-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #475569;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🎓 AI Learning Roadmap Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal AI-powered learning journey starts here.</div>',
    unsafe_allow_html=True
)

st.write("")
st.divider()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🚀 About Project")
    st.write(
        "This application uses Grok AI to generate "
        "personalized learning roadmaps."
    )
    st.info("Enter your learning goals to get started.")

# ---------------- USER INPUT ----------------
st.subheader("📝 Enter Your Learning Requirements")

col1, col2 = st.columns(2)

with col1:
    field = st.text_input(
        "🎯 Learning Field",
        placeholder="e.g. Cybersecurity, Python, Artificial Intelligence"
    )

    level = st.selectbox(
        "📊 Current Skill Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

with col2:
    duration = st.selectbox(
        "⏳ Time to Learn",
        ["1 Month", "3 Months", "6 Months", "9 Months", "1 Year"]
    )

    daily_hours = st.selectbox(
        "⏰ Daily Study Time",
        ["1 Hour", "2 Hours", "3 Hours", "4 Hours", "5+ Hours"]
    )

st.write("")
generate = st.button("✨ Generate My Learning Roadmap")

# ---------------- API FUNCTION ----------------
def generate_roadmap(field, level, duration, daily_hours):

    client = OpenAI(
        api_key=st.secrets["XAI_API_KEY"],
        base_url="https://api.x.ai/v1"
    )

    prompt = f"""
    Act as an expert learning roadmap designer.

    Create a detailed and practical learning roadmap.

    Learning field: {field}
    Current skill level: {level}
    Learning duration: {duration}
    Daily study time: {daily_hours}

    Include:

    1. Introduction and learning objectives.
    2. A structured weekly or monthly learning plan.
    3. Topics in the correct learning order.
    4. Tools and technologies to learn.
    5. Hands-on practical exercises.
    6. Real-world projects.
    7. Free learning resources and documentation.
    8. Assessment and progress checkpoints.
    9. Final skills the learner should achieve.
    10. Career opportunities where relevant.

    Make the roadmap realistic for the available time.
    Use clear headings, numbered steps and simple English.
    Do not invent specific URLs.
    """

    response = client.chat.completions.create(
        model="grok-4.6",
        messages=[
            {
                "role": "system",
                "content": "You are an expert AI learning advisor."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


# ---------------- GENERATE RESULT ----------------
if generate:

    if not field.strip():
        st.warning("Please enter your learning field.")
    else:
        try:
            with st.spinner("🤖 Grok AI is creating your roadmap..."):
                roadmap = generate_roadmap(
                    field,
                    level,
                    duration,
                    daily_hours
                )

            st.success("Your learning roadmap is ready!")

            st.divider()

            st.subheader(f"🎯 Your {field} Learning Roadmap")

            with st.container(border=True):
                st.markdown(roadmap)

            st.download_button(
                "📥 Download Roadmap",
                data=roadmap,
                file_name="learning_roadmap.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    "<center>🚀 Powered by Python, Streamlit and Grok AI</center>",
    unsafe_allow_html=True
)
