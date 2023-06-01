import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.qa import RetrievalQA
from langchain.llms import OpenAI

st.title('🦜🔗 Ask the Doc App')
st.set_page_config(page_title='🦜🔗 Ask the Doc App')
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# File upload
uploaded_file = st.file_uploader('Upload an article', type='txt')
if uploaded_file is not None:
    documents = [uploaded_file.read().decode('utf-8')]
else:
    documents = []

# Split documents into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Select embeddings
embeddings = OpenAIEmbeddings()

# Create vectorstore index
db = Chroma.from_documents(texts, embeddings)

# Create retriever interface
retriever = db.as_retriever()

# Create QA chain
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=retriever)

# Form input and query
with st.form('myform'):
    query_text = st.text_input('Enter your question:', '')
    submitted = st.form_submit_button('Submit')
    if not openai_api_key.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and openai_api_key.startswith('sk-'):
        response = qa.run(query_text)
        st.info(response)
