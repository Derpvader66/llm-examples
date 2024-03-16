import streamlit as st
import os
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
# Set page title
st.set_page_config(page_title="Test Case Generator", page_icon=":memo:")
# App title and description
st.title("Test Case Generator")
st.markdown("Upload your business process documents and user documentation files to generate test cases.")
# Create file uploader widgets
uploaded_business_files = st.file_uploader("Choose business process documents", accept_multiple_files=True)
uploaded_user_files = st.file_uploader("Choose user documentation files", accept_multiple_files=True)
# Process uploaded files
def process_files(uploaded_files, directory):
   if uploaded_files:
       for uploaded_file in uploaded_files:
           if not os.path.exists(directory):
               os.makedirs(directory)
           with open(os.path.join(directory, uploaded_file.name), "wb") as f:
               f.write(uploaded_file.getbuffer())
       st.success(f"{len(uploaded_files)} file(s) uploaded successfully to {directory}!")
# Generate test cases
def generate_test_cases():
   # Load and process the documents
   business_docs = UnstructuredFileLoader(["business_process_docs/" + f for f in os.listdir("business_process_docs")]).load()
   user_docs = UnstructuredFileLoader(["user_documentation/" + f for f in os.listdir("user_documentation")]).load()
   docs = business_docs + user_docs
   # Split the documents into chunks
   text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
   texts = text_splitter.split_documents(docs)
   # Create embeddings and vector store
   embeddings = OpenAIEmbeddings()
   db = FAISS.from_documents(texts, embeddings)
   # Initialize the question-answering chain
   chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
   # Generate test cases
   query = "Generate detailed test cases based on the provided business process and user documentation."
   test_cases = chain.run(input_documents=db.similarity_search(query), question=query)
   st.header("Generated Test Cases")
   st.write(test_cases)
# Process uploaded files
process_files(uploaded_business_files, "business_process_docs")
process_files(uploaded_user_files, "user_documentation")
# Generate test cases button
if st.button("Generate Test Cases"):
   generate_test_cases()
