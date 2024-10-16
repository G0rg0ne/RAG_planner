# importing dependencies

import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import faiss
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFacePipeline
from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel
from master_planner.htmlTemplates import css, bot_template, user_template

# creating custom template to guide llm model
custom_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CUSTOM_QUESTION_PROMPT = PromptTemplate.from_template(custom_template)

# extracting text from pdf
def get_pdf_text(docs):
    text = ""
    for pdf in docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# converting text to chunks
def get_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks

# using all-MiniLm embeddings model and faiss to get vectorstore
def get_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': 'cpu'}
    )
    vectorstore = faiss.FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

# Replace ChatOpenAI with a HuggingFace LLM model pipeline
def get_conversationchain(vectorstore):
    # Load the GPT-2 model and tokenizer for local use
    model_name = "gpt2"  # You can replace this with other local models (bigger or more specific models)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Create a Hugging Face pipeline for text generation
    hf_pipeline = pipeline(
        "text-generation", model=model, tokenizer=tokenizer, max_length=100
    )

    # Use HuggingFacePipeline with Langchain
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # Set up conversation buffer memory
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True, output_key="answer"
    )

    # Create the conversational retrieval chain using the Hugging Face model
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        condense_question_prompt=CUSTOM_QUESTION_PROMPT,
        memory=memory,
    )

    return conversation_chain

# generating response from user queries and displaying them accordingly
def handle_question(question):
    response = st.session_state.conversation({'question': question})
    st.session_state.chat_history = response["chat_history"]
    for i, msg in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="An Engine you can use to Extract informations From PDF", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("An Engine you can use to Extract informations From PDF :books:")
    question = st.text_input("Ask question from your document:")
    if question:
        handle_question(question)

    with st.sidebar:
        st.subheader("Your documents")
        docs = st.file_uploader("Upload your PDF here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # Get the PDF text
                raw_text = get_pdf_text(docs)

                # Get the text chunks
                text_chunks = get_chunks(raw_text)

                # Create vectorstore
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain
                st.session_state.conversation = get_conversationchain(vectorstore)

if __name__ == '__main__':
    main()
