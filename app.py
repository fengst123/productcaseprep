
import streamlit as st
import openai

# Set page config
st.set_page_config(page_title="Product Case Prep Buddy", page_icon="🤖")

# Title
st.title("🤖 Product Case Prep Buddy")
st.write("Practice product management cases and get instant AI feedback.")

# Sidebar inputs
case_type = st.sidebar.selectbox("Select Case Type", [
    "Design a New Feature",
    "Improve a Metric",
    "Evaluate a Product",
    "Prioritize Roadmap",
    "Launch Strategy"
])

hint_mode = st.sidebar.checkbox("Hint Mode")

# Example prompts per case type
example_prompts = {
    "Design a New Feature": "Design a new feature for Airbnb to help solo travelers.",
    "Improve a Metric": "Instagram engagement is down 20% among Gen Z. What would you do?",
    "Evaluate a Product": "Evaluate the success of Google Pixel phones.",
    "Prioritize Roadmap": "You’re a PM at Spotify. You have limited dev resources. How do you prioritize between lyrics, AI DJ, and social listening features?",
    "Launch Strategy": "How would you launch a new grocery delivery app in a mid-sized U.S. city?"
}

st.subheader("🧠 Case Prompt")
st.write(f"**Prompt:** {example_prompts[case_type]}")

user_response = st.text_area("Your Answer", height=250)

if st.button("Submit Answer") and user_response:
    with st.spinner("Evaluating your answer..."):
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

        messages = [
            {"role": "system", "content": f"You are an expert product management interview coach. You are helping a student prepare for a case interview. Provide structured, rubric-based feedback on their response to this {case_type} case."},
            {"role": "user", "content": f"Case Prompt: {example_prompts[case_type]}\n\nAnswer: {user_response}"}
        ]

        if hint_mode:
            messages.append({
                "role": "system",
                "content": "If possible, give constructive hints or reframe the problem to help the user improve, based on frameworks like CIRCLES, AARM, or PRD templates."
            })

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )

        st.subheader("📋 Feedback")
        st.markdown(response.choices[0].message.content)

st.markdown("---")
st.markdown("_Tip: You can change case type or turn on Hint Mode from the sidebar._")
