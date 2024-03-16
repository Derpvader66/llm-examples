import streamlit as st
from langchain.document_loaders import UnstructuredWordDocumentLoader, UnstructuredPDFLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
def load_documents(files):
   loaders = []
   for file in files:
       if file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
           loader = UnstructuredWordDocumentLoader(file)
       elif file.type == "application/pdf":
           loader = UnstructuredPDFLoader(file)
       elif file.type == "application/vnd.ms-excel" or file.type == "text/csv":
           loader = CSVLoader(file)
       else:
           raise ValueError(f"Unsupported file type: {file.type}")
       loaders.append(loader)
   documents = []
   for loader in loaders:
       documents.extend(loader.load())
   text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
   docs = text_splitter.split_documents(documents)
   return docs
def generate_test_cases(business_docs, user_docs, test_case_sample, openai_api_key):
   embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
   business_db = FAISS.from_documents(business_docs, embeddings)
   user_db = FAISS.from_documents(user_docs, embeddings)
   llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
   prompt = PromptTemplate(
       input_variables=["test_case_sample"],
       template="""
       Test Case Sample:
       {test_case_sample}
       Generate test cases based on the provided business process documents, user documentation, and the test case sample:
       """
   )
   chain = LLMChain(llm=llm, prompt=prompt)
   generated_test_cases = chain.run(test_case_sample=test_case_sample)
   return generated_test_cases.strip()
def main():
   st.set_page_config(page_title="Test Case Generator", layout="wide")
   st.title("Test Case Generator")
   openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
   business_process_files = st.file_uploader("Upload Business Process Documents", type=["docx", "pdf", "csv"], accept_multiple_files=True)
   user_docs_files = st.file_uploader("Upload User Documentation Files", type=["docx", "pdf"], accept_multiple_files=True)
   test_case_sample_file = st.file_uploader("Upload Test Case Sample Document", type=["docx"])
   if openai_api_key and business_process_files and user_docs_files and test_case_sample_file:
       business_docs = load_documents(business_process_files)
       user_docs = load_documents(user_docs_files)
       test_case_sample = test_case_sample_file.read().decode("utf-8")
       st.subheader("Business Process Documents")
       for doc in business_docs:
           st.write(doc.page_content)
       st.subheader("User Documentation Files")
       for doc in user_docs:
           st.write(doc.page_content)
       st.subheader("Test Case Sample")
       st.write(test_case_sample)
       if st.button("Generate Test Cases"):
           generated_test_cases = generate_test_cases(business_docs, user_docs, test_case_sample, openai_api_key)
           st.subheader("Generated Test Cases")
           st.write(generated_test_cases)
   else:
       st.warning("Please provide the OpenAI API key and upload the necessary documents.")
if __name__ == "__main__":
   main()