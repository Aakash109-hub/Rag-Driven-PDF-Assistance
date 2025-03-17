import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import base64


# Check if running locally or on Render
if os.getenv("RENDER") is None:
    from dotenv import load_dotenv
    load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.warning("⚠️ Groq API key is missing! Set it in a `.env` file.")
    st.stop()

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Function to extract text from PDFs
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text() or ""  # Avoid NoneType errors
            text += page_text
    return text

# Split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return text_splitter.split_text(text)

# Store text embeddings in FAISS
def get_vector_store(text_chunks):
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

# Create the conversational chain
def get_conversational_chain(vector_store):
    prompt_template = """
    Answer the question using the provided context. If the answer isn't available, say 
    "The answer is not available in the context." Do NOT attempt to answer incorrectly.\n\n
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """

    llm = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    return RetrievalQA.from_chain_type(llm=llm, retriever=vector_store.as_retriever(), chain_type="stuff", chain_type_kwargs={"prompt": prompt})

# Handle user queries and store chat history
def user_input(user_question, chain):
    response = chain.run(user_question)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    st.session_state.chat_history.append({"user": user_question, "bot": response})
    st.session_state.last_user_input = ""  # Clear input after response
    st.session_state.response_generated = True  # Flag to indicate response generated



def display_pdf(file):
    # Opening file from file path

    base64_pdf = base64.b64encode(file.read()).decode("utf-8")

    # Embedding PDF in HTML
    pdf_display = f"""<iframe src="data:application/pdf;base64,{base64_pdf}" width="400" height="100%" type="application/pdf"
                        style="height:100vh; width:100%"
                    >
                    </iframe>"""

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)    

# Main App
def main():
    st.set_page_config(page_title="SmartPDF AI")
    st.header("📄 SmartPDF AI: Your Personal Document Assistant")

    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    
    if "last_user_input" not in st.session_state:
        st.session_state.last_user_input = ""
    
    if "response_generated" not in st.session_state:
        st.session_state.response_generated = False

    with st.sidebar:
        st.title("📂 Upload PDFs")
        pdf_docs = st.file_uploader("Upload PDFs", accept_multiple_files=True)
        
        if st.button("📥 Process Documents"):
            if pdf_docs:
                with st.spinner("Processing PDFs..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vector_store = get_vector_store(text_chunks)
                    st.session_state.vector_store = vector_store
                    st.success("✅ PDF Processing Complete!")
        
        # Display PDF preview (full page view)
        if pdf_docs:
            st.subheader("📑 PDF Preview")
            for pdf in pdf_docs:
                display_pdf(pdf)

    
    # Display chat history
    st.subheader("💬 Chat History")
    for chat in st.session_state.chat_history:
        st.markdown(f"👤 **You:** {chat['user']}")
        st.markdown(f"🤖 **AI:** {chat['bot']}")
        st.markdown("---")
    
    # User input field
    user_question = st.text_input("💬 Ask a Question from the PDFs:", key="user_input", value=st.session_state.last_user_input)
    
    if user_question and st.session_state.vector_store and not st.session_state.response_generated:
        st.session_state.response_generated = True  # Prevent multiple runs
        chain = get_conversational_chain(st.session_state.vector_store)
        user_input(user_question, chain)
        st.rerun()
    else:
        st.session_state.response_generated = False  # Reset flag for next input

if __name__ == "__main__":
    main()





