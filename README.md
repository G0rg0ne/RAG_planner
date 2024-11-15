# RAG_planner: RAG-based Chatbot

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** chatbot designed to answer questions based on specific documents. The chatbot retrieves relevant information from the provided documents and generates responses using a language model. This approach ensures accurate, contextually relevant answers, making it suitable for applications in customer support, knowledge management, and more.

## Features

- **Document Retrieval**: Retrieves documents relevant to user queries using semantic search.
- **Answer Generation**: Generates responses using a language model, contextualizing answers based on retrieved information.
- **Multi-Document Support**: Allows querying across multiple documents, enabling comprehensive information retrieval.
- **Real-Time Interaction**: Provides quick responses, suitable for interactive applications.

## Project Structure

```
📂 project-name
├── 📁 data
│   └── documents/          # Folder containing source documents
├── 📁 src
│   ├── app.py          # Chatbot interface
│   ├── main.py        # Process that uses Replicate to load LLM
│   └── replicate_test.py            # Test replicate
├── 📁 configs
│   └── config.yaml         # Configuration file with model settings and paths
├── 📄 README.md            # Project documentation
├── Dockerfile              # Docker setup
└── pyproject.toml          # Poetry project configuration
```

## Getting Started

### Prerequisites

- **Docker** >= 20.10
- **Poetry** >= 1.1

### Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd project-name
   ```



3. **Build and Run with Docker Compose**:

   Build the Docker image and start the services with Docker Compose:

   ```bash
   docker build -t rag_planner/latest .
   ```

   ```bash
   docker run -it --rm --name rag_planner --gpus all -p 8501:8501 -v $(pwd):/workdir rag_test /bin/bash
   ```
### Model and Data Setup

1. **Data Preparation**:
   - Place the documents to be used by the chatbot in the `data/documents` directory.
   - Supported formats: `.txt`, `.pdf`, `.docx`, etc.
   
2. **Model Selection**:
   - This project uses a language model for response generation. Configure model details in `config.yaml`.
   - Common choices include OpenAI’s GPT, Hugging Face models, or custom-trained models.

### Configuration

- Configure paths, model parameters, and retrieval settings in `configs/config.yaml`.

### Running the Chatbot

1. **Start the Chatbot RAG Module**:
   - Run `retriever.py` to index documents in `data/documents`.

   ```bash
   streamlit run src/app.py
   ```

2. **Start Replicate LLM module**:
   - Execute `chatbot.py` to initiate the chatbot interface.

   ```bash
   python src/main.py
   ```

3. **Interacting with the Chatbot**:
   - Enter your query in the chatbot interface. The chatbot will retrieve relevant document information and generate a response.


## License

This project is licensed under the MIT License.



