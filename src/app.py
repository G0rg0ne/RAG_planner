# Importing dependencies
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import faiss
from langchain.prompts import PromptTemplate
from htmlTemplates import css, bot_template, user_template
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.llms import HuggingFacePipeline
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from transformers import pipeline
import torch
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers.utils.generic")

# Custom prompt template
custom_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

# Extract text from PDF
def get_pdf_text(docs):
    text = ""
    for pdf in docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception as e:
            st.warning(f"Error reading {pdf.name}: {e}")
    return text

# Split text into chunks
def get_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    return text_splitter.split_text(raw_text)

# Generate vectorstore using embeddings
def get_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cuda'}
    )
    return faiss.FAISS.from_texts(texts=chunks, embedding=embeddings)

# Initialize conversation chain with a HuggingFace LLM pipeline
def get_conversationchain(vectorstore):
    model_name = "TheBloke/Llama-2-7B-Chat-GPTQ"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map={"": "cuda:0"} if device == "cuda" else None
    )
    model.to(device)

    # Hugging Face pipeline
    hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=1024, temperature=0.2,do_sample=True )
    
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # Memory for conversation history
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")
    
    # Conversational retrieval chain
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        condense_question_prompt=CUSTOM_QUESTION_PROMPT,
        memory=memory
    )

# Generate and display response
def handle_question(question):
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    response = st.session_state.conversation({'question': question})
    st.session_state.chat_history = response["chat_history"]
    for i, msg in enumerate(st.session_state.chat_history):
        template = user_template if i % 2 == 0 else bot_template
        st.write(template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="PDF Info Extraction Engine", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("An Engine to Extract Information From PDF :books:")
    question = st.text_input("Ask a question from your document:")
    if question and st.session_state.conversation:
        handle_question(question)

    with st.sidebar:
        st.subheader("Upload PDF Documents")
        docs = st.file_uploader("Upload your PDF here", accept_multiple_files=True)
        if docs and st.button("Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(docs)
                if raw_text:
                    text_chunks = get_chunks(raw_text)
                    vectorstore = get_vectorstore(text_chunks)
                    st.session_state.conversation = get_conversationchain(vectorstore)
                else:
                    st.warning("No text found in the uploaded PDF(s).")

if __name__ == '__main__':
    main()
