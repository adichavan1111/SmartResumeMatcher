import streamlit as st
from transformers import pipeline

# Load model (free small model)
generator = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
st.title("Cover Letter Generator")
job_title = st.text_input("Job Title")
skills = st.text_area("Skills (comma separated)")
experience = st.text_area("Experience Summary")
company = st.text_input("Job Description")
generate_btn = st.button("Generate Resume")

if generate_btn:
    with st.spinner("Generating... please wait ⏳"):
        prompt = f"""
        Create a professional resume summary and cover letter for:
        Job: {job_title}
        Skills: {skills}
        Experience: {experience}
        Company: {company}
        """
        result = generator(prompt, max_new_tokens=300)
        output = result[0]["generated_text"]
    st.subheader("📝 Generated Resume & Cover Letter")
    st.write(output)




