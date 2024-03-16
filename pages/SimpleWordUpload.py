import streamlit as st
import langchain

# Create a title for the app
st.title("Word Document Parser")

# Add a file uploader widget
uploaded_file = st.file_uploader("Upload a Word document")

# Use LangChain to parse the document
if uploaded_file is not None:
    document = langchain.Document.from_file(uploaded_file)
    text = document.text
    sentences = text.split(".")

    # Print the sentences
    for sentence in sentences:
        st.write(sentence)

# If no file is uploaded, print a message
else:
    st.write("Please upload a Word document")
