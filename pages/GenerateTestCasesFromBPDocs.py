import streamlit as st
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate

from utils import read_pdf, read_docx, read_txt

def upload_document(label, file_types):
   uploaded_file = st.file_uploader(label, type=file_types)
   if uploaded_file is not None:
       if uploaded_file.type == "application/pdf":
           content = read_pdf(uploaded_file)
       elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
           content = read_docx(uploaded_file)
       else:  # Assuming text file
           content = read_txt(uploaded_file)
       return content
   return None

#def generate_test_cases(business_process_doc, detailed_steps_docs, openai_api_key):
   
def generate_test_cases(business_process_doc, detailed_steps_docs, openai_api_key):
    # Initialize LangChain with OpenAI's GPT-3.5-turbo as the backend
    llm = OpenAI(api_key=openai_api_key, model="gpt-3.5-turbo")
    
    combined_documents = f"Business Process Document:\n{business_process_doc}\n\n"
    for name, doc in detailed_steps_docs.items():
        combined_documents += f"{name}:\n{doc}\n\n"
    
    prompt = "Why are there so many songs about rainbows?" 
    #PromptTemplate(combined_documents,template="Generate test cases using the following documents:\n\n{combined_documents}")
    response = llm(prompt)
    st.write(response)
 
def main():
   st.title("Test Case Generator for Business Processes")
   with st.sidebar:
       openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
       "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
   business_process_doc = upload_document("Upload your business process document", ['txt', 'pdf', 'docx'])
   detailed_steps_docs = {}
   if business_process_doc:
       num_detailed_docs = st.number_input("Number of detailed steps documents", min_value=1, value=1, step=1)
       for i in range(num_detailed_docs):
           detailed_doc = upload_document(f"Upload detailed steps document {i+1}", ['txt', 'pdf', 'docx'])
           if detailed_doc:
               detailed_steps_docs[f"Detailed Steps Document {i+1}"] = detailed_doc
   if st.button("Generate Test Cases") and business_process_doc and detailed_steps_docs and openai_api_key:
       test_cases = generate_test_cases(business_process_doc, detailed_steps_docs, openai_api_key)
       st.subheader("Generated Test Cases")
       st.write(test_cases)
if __name__ == "__main__":
   main()