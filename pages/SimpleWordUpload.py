import streamlit as st
from langchain.document_loaders import UnstructuredWordDocumentLoader
import tempfile

def load_word_document(doc_file):
    # Create a temporary file to save the uploaded document
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
        tmp_file.write(doc_file.getbuffer())
        tmp_filename = tmp_file.name
    
    # Load the document using UnstructuredWordDocumentLoader
    loader = UnstructuredWordDocumentLoader(tmp_filename)
    document = loader.load()
    
    # Concatenate all the text from the document
    full_text = "\n".join([element.text for element in document if element.text])
    
    return full_text

def main():
    st.title("Word Document Loader")
    
    # File uploader allows the user to upload a Word document
    doc_file = st.file_uploader("Upload a Word document", type=["docx"])
    
    if doc_file is not None:
        # Load and display the document
        document_text = load_word_document(doc_file)
        st.write("Document Content:")
        st.text_area("Content", value=document_text, height=300)

if __name__ == "__main__":
    main()
