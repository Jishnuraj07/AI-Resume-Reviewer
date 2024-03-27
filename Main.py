import streamlit as st
from PyPDF2 import PdfReader
from openai import AzureOpenAI


# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint="your end point",
    api_key="your key",
    api_version="version"
)

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    text = ''
    with uploaded_file as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Main function
def main():
    st.title("Resume Reviewer")

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

    if uploaded_file is not None:
        # Display uploaded file
        st.write("Uploaded resume:")
        st.write(uploaded_file.name)

        # Extract text from PDF
        resume_text = extract_text_from_pdf(uploaded_file)
        
        # Perform completion request
        completion = client.chat.completions.create(
            model="gpt-35-turbo",
            messages=[
                {"role": "user", "content": resume_text},
                {"role": "assistant", "content": "Give review on the resume uploaded by analyzing various aspects such as grammar, key skills, job responsibilities, etc."}
            ],
            temperature=0.7,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        # Display assistant's response
        st.write("Assistant's Review:")
        st.write(completion.choices[0].message['content'])

if __name__ == "__main__":
    main()
