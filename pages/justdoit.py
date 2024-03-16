import streamlit as st
from langchain.chains import DocumentChain
from langchain.llms import OpenAI

# Initialize the OpenAI model with GPT-3
with st.sidebar:
       openai_api_key = st.text_input("OpenAI API Key", key="openai_api_key", type="password")
       "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

openai_model = OpenAI(model="gpt-3", api_key = openai_api_key)

# Initialize the DocumentChain with the OpenAI model
document_chain = DocumentChain(llm=openai_model)

# Streamlit app interface
st.title('GPT-3 DocumentChain Generator')

# Text input for the user prompt
user_prompt = st.text_area("Enter your prompt:", value="", max_chars=500)

if st.button('Generate'):
    if user_prompt:
        # Generating the response using DocumentChain
        response = document_chain.generate(user_prompt)
        st.text_area("Response:", value=response, height=250, max_chars=None)
    else:
        st.warning('Please enter a prompt.')