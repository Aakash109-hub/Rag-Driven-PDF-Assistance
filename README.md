# 📚 SmartPDF AI: A RAG-based PDF Assistant

SmartPDF AI is a **Retrieval-Augmented Generation (RAG)** application that allows users to interact with PDF documents by asking questions and receiving context-based answers. This project combines 🔍 **Google Generative AI's** powerful embeddings and conversational AI with ⚡ **FAISS vector search** for efficient and accurate information retrieval

![Screenshot 2024-12-30 121437](https://github.com/user-attachments/assets/68388f77-8fc7-4542-8f55-03b0f454d12a)


---

## 🚀 Features
- 📂 **PDF Upload**: Upload multiple PDF documents for analysis.
- ❓ **Contextual Q&A**: Ask questions and get detailed answers based on the content of the uploaded PDFs.
- 🤖 **Advanced Embeddings**: Leverages Google Generative AI for high-quality embeddings and responses.
- ⚡ **Efficient Retrieval**: Uses FAISS for fast and accurate similarity search.
- 🖥️ **User-Friendly Interface**: Built with Streamlit for an interactive and seamless experience.

---

## 🌐 Live Demo
The application is deployed on Render and is accessible online:

👉 SmartPDF AI Live Application : https://smartai-pdfassist-ak19.onrender.com/

---

## 🛠️ How It Works

### 🗂️ **Indexing (Offline Process)**
1. **📥 Load**: Extract text from uploaded PDFs using `PdfReader`.
2. **✂️ Split**: Divide the extracted text into manageable chunks for better search efficiency.
3. **💾 Store**: Generate embeddings using `GoogleGenerativeAIEmbeddings` and store them in a **FAISS VectorStore**.

**📊 Workflow Visualization**:
```
Raw Data (PDFs) --> Text Extraction --> Text Chunking --> Embedding Generation --> FAISS VectorStore
```

### ⚙️ **Retrieval and Generation (Run-Time Process)**
1. **🔎 Retrieve**: Find relevant text chunks using a similarity search on the FAISS index.
2. **🧠 Generate**: Use `ChatGoogleGenerativeAI` to generate answers based on the user’s query and the retrieved text context.

**📊 Workflow Visualization**:
```
User Query --> Similarity Search (FAISS) --> Relevant Text Chunks --> Conversational Chain (LLM) --> Answer
```
---

## 📂 Project Structure
```
📂 SmartPDF AI
├── app.py                     # Main application code
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not included in the repo)
├── faiss_index/               # FAISS index files (auto-generated)
└── README.md                  # Project documentation
```

---

## 💡 Use Cases
- ⚖️ **Legal Research**: Extract specific clauses or details from contracts and legal documents.
- 🎓 **Academic Research**: Summarize and query information from research papers and theses.
- 📈 **Business Analysis**: Search through reports, proposals, and presentations.
- 📖 **Personal Use**: Quickly retrieve information from eBooks or personal documents.

---

## ⚠️ Limitations
- 📄 **Document Type**: Currently supports only PDF files.
- 🧾 **Answer Accuracy**: Limited to the context available in the uploaded PDFs.
- 🏋️ **Large Files**: Performance may degrade with very large documents.

---

## 🤝 Contributions
Contributions are welcome! If you have ideas for improvements or want to add features:
1. 🍴 Fork this repository.
2. 🌿 Create a feature branch (`git checkout -b feature-name`).
3. 💾 Commit your changes (`git commit -m 'Add feature-name'`).
4. 🚀 Push to the branch (`git push origin feature-name`).
5. 📝 Open a pull request.

---

## 🌟 Acknowledgments
- 🔗 [LangChain](https://github.com/hwchase17/langchain) for its modular framework.
- 🤖 [Google Generative AI](https://cloud.google.com/vertex-ai) for embeddings and conversational AI.
- 🖥️ [Streamlit](https://streamlit.io/) for a seamless user interface.
- ⚡ [FAISS](https://github.com/facebookresearch/faiss) for efficient vector search.

---

If you find this project helpful, please consider giving it a ⭐ on GitHub!
