# 📚 Smart Study Assistant

<div align="center">

An AI-powered learning application that transforms lecture notes and PDF documents into structured study materials and supports document-based question answering using a complete Retrieval-Augmented Generation pipeline.

Built with **Python**, **Streamlit**, **OpenRouter**, **Pydantic**, **Sentence Transformers**, and **NumPy**.

</div>

---

## 🚀 Project Overview

Smart Study Assistant is a modular AI application designed to help students study more effectively.

Users can paste lecture notes, upload a PDF, or use both together to generate:

- Summaries
- Key concepts
- Flashcards
- Multiple-choice questions
- Mock exams

The application also includes a working Retrieval-Augmented Generation feature that allows users to upload a PDF, index its content, and ask questions based on the information inside the document.

This project was built as an AI engineering learning project. The focus is not only on calling an LLM, but also on understanding:

- Software architecture
- Service boundaries
- Structured outputs
- Input validation
- Document processing
- Embeddings
- Semantic retrieval
- Retrieval-Augmented Generation
- Provider abstraction
- Maintainable AI application design

> **Current Status:** Core application and basic end-to-end RAG pipeline completed ✅  
> **Current Stage:** Improving retrieval reliability, citations, testing, interface design, and deployment

---

## ✨ Features

### Study Material Generation

The application can generate:

- 📄 Concise lecture summaries
- 🧠 Important concepts with explanations
- 📝 Question-and-answer flashcards
- ❓ Multiple-choice questions with explanations
- 🎓 Mock exam questions with model answers

Users can provide:

- Typed lecture notes
- An uploaded PDF
- Typed notes and a PDF together

---

### Structured AI Outputs

The application does not depend on loosely formatted LLM responses.

Each feature requests structured JSON output and validates the response using Pydantic.

Implemented response models include:

- `SummaryResponse`
- `ConceptResponse`
- `FlashcardResponse`
- `MCQResponse`
- `MockExamResponse`

The processing flow is:

```text
LLM response
      ↓
JSON parsing
      ↓
Pydantic validation
      ↓
Typed Python objects
      ↓
Streamlit display
```

This makes the application safer, more predictable, and easier to maintain.

---

### PDF Ingestion

The application supports PDF upload and text extraction.

Current PDF capabilities include:

- Uploading PDFs through Streamlit
- Extracting text using `pypdf`
- Skipping empty pages
- Detecting documents with no extractable text
- Supporting typed notes, PDF text, or both
- Keeping document-processing logic outside the UI layer

The study service always receives a plain string, regardless of where the content came from.

```text
Typed notes ───────────────┐
                           ├──→ Plain text → Study service
Uploaded PDF → Extraction ─┘
```

---

### Retrieval-Augmented Generation

The application includes a working RAG pipeline for asking questions about uploaded PDF documents.

The current RAG system supports:

- PDF text extraction
- Word-based chunking
- Configurable chunk size
- Configurable overlap
- Local embedding generation
- Query embedding generation
- Cosine similarity
- Top-K retrieval
- Context augmentation
- Document-grounded LLM answers
- Retrieved chunk display
- Similarity score display
- Streamlit session-state indexing

The complete pipeline is:

```text
Uploaded PDF
      ↓
Text extraction
      ↓
Text chunking
      ↓
Chunk embeddings
      ↓
Chunk records stored in session state
      ↓
User question
      ↓
Question embedding
      ↓
Cosine similarity
      ↓
Top-K chunk retrieval
      ↓
Retrieved context + question
      ↓
RAG prompt
      ↓
LLM answer
```

---

### Provider Abstraction

The application supports interchangeable LLM providers.

Current providers:

- Mock provider
- OpenRouter provider

The rest of the application communicates with a generic LLM service instead of calling a provider directly.

```python
ask_llm(prompt)
```

This makes it possible to add providers such as OpenAI, Gemini, or Anthropic without rewriting the study features or RAG pipeline.

---

## 🧠 RAG Architecture

### Indexing Pipeline

The indexing pipeline runs when a PDF is prepared for document question answering.

```text
PDF
 ↓
Document Service
 ↓
Extracted Text
 ↓
Chunking Service
 ↓
Text Chunks
 ↓
Embedding Service
 ↓
Chunk Embeddings
 ↓
Chunk Records
 ↓
Streamlit Session State
```

Each chunk record currently contains:

```python
{
    "text": "Chunk content...",
    "embedding": [0.12, -0.44, 0.81, ...],
    "chunk_index": 0
}
```

---

### Query Pipeline

The query pipeline runs whenever the user asks a question.

```text
User Question
      ↓
Embedding Service
      ↓
Question Vector
      ↓
Retrieval Service
      ↓
Cosine Similarity
      ↓
Top-K Relevant Chunks
      ↓
RAG Prompt Builder
      ↓
LLM Service
      ↓
Grounded Answer
```

The embedding model finds semantically related chunks even when the user does not use the exact words found in the document.

---

## 🏗️ Application Architecture

```text
                         Streamlit UI
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
      Study Material Flow               Document Q&A Flow
              │                               │
              ▼                               ▼
       Study Service                     RAG Service
              │                               │
              ▼                  ┌────────────┼────────────┐
       Prompt Builders           ▼            ▼            ▼
              │          Chunking Service  Embedding   Retrieval
              ▼                            Service      Service
         LLM Service                          │            │
              │                               └─────┬──────┘
      ┌───────┴────────┐                            ▼
      ▼                ▼                      Retrieved Context
Mock Provider    OpenRouter Provider                 │
      │                │                             ▼
      └───────┬────────┘                       RAG Prompt
              ▼                                      │
         LLM Response                                 ▼
              │                                 LLM Service
              ▼                                      │
      JSON + Pydantic                                ▼
              │                              Grounded Answer
              ▼
      Typed Python Objects
              │
              ▼
       Streamlit Display
```

---

## 🗂️ Project Structure

```text
SmartStudyAssistant/

├── app.py
│
├── models/
│   ├── summary.py
│   ├── concept.py
│   ├── flashcard.py
│   ├── mcq.py
│   └── exam.py
│
├── prompts/
│   ├── summary_prompt.py
│   ├── concept_prompt.py
│   ├── flashcard_prompt.py
│   ├── mcq_prompt.py
│   ├── exam_prompt.py
│   └── rag_prompt.py
│
├── providers/
│   ├── mock_provider.py
│   └── openrouter_provider.py
│
├── services/
│   ├── chunking_service.py
│   ├── document_service.py
│   ├── embedding_service.py
│   ├── llm_service.py
│   ├── rag_service.py
│   ├── retrieval_service.py
│   └── study_service.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## ⚙️ Main Components

### `app.py`

Responsible for:

- Rendering the Streamlit interface
- Collecting typed notes
- Handling PDF uploads
- Calling application services
- Saving the RAG index in session state
- Displaying generated study material
- Displaying RAG answers
- Displaying retrieved chunks and similarity scores

The UI does not perform PDF parsing, embedding generation, retrieval, or provider selection.

---

### `study_service.py`

Contains the business logic for generating structured study materials.

Its flow is:

```text
Notes
  ↓
Feature Prompt
  ↓
LLM Response
  ↓
JSON Parsing
  ↓
Pydantic Validation
  ↓
Typed Response Object
```

The service uses a generic structured-output helper so JSON parsing and validation are not repeated for every feature.

---

### `document_service.py`

Responsible for document ingestion.

Current responsibilities:

- Read uploaded PDFs
- Extract page text
- Skip empty content
- Detect PDFs with no extractable text
- Return plain text

The service does not know anything about prompts, LLMs, flashcards, summaries, or retrieval.

---

### `chunking_service.py`

Responsible for dividing large text into smaller retrieval units.

Current implementation:

- Word-based chunking
- Configurable chunk size
- Configurable overlap
- Input validation

Example:

```text
Chunk 1: words 1–300
Chunk 2: words 251–550
Chunk 3: words 501–800
```

The overlap helps preserve meaning when an important idea crosses a chunk boundary.

---

### `embedding_service.py`

Uses Sentence Transformers with:

```text
all-MiniLM-L6-v2
```

Responsibilities:

- Load the embedding model
- Cache the model as a reusable resource
- Convert chunks into vectors
- Convert questions into vectors
- Return standard Python lists

The same embedding model is used for document chunks and user questions so both exist in the same vector space.

---

### `retrieval_service.py`

Responsible for semantic retrieval.

Current implementation includes:

- NumPy vector operations
- Cosine similarity
- Brute-force comparison
- Similarity ranking
- Top-K retrieval
- Metadata preservation
- Similarity score attachment

The current implementation is intentionally manual so the retrieval process is fully understood before introducing a vector database.

---

### `rag_service.py`

Coordinates the complete RAG workflow.

Responsibilities:

- Build a document index
- Generate chunk embeddings
- Pair chunks with vectors and metadata
- Embed the user question
- Retrieve relevant chunks
- Build the final context
- Create the RAG prompt
- Send the prompt through the LLM service
- Return the answer and supporting chunks

---

### `llm_service.py`

Provides a stable interface between application services and LLM providers.

The rest of the application calls:

```python
ask_llm(prompt)
```

The study and RAG services do not communicate directly with OpenRouter.

---

### `providers/`

Current providers:

- Mock Provider
- OpenRouter Provider

The provider architecture makes it possible to add:

- OpenAI
- Gemini
- Anthropic
- Local models

without changing the rest of the application.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| Streamlit | Web interface |
| OpenRouter | LLM access |
| Pydantic | Structured-output validation |
| pypdf | PDF text extraction |
| Sentence Transformers | Local embedding generation |
| all-MiniLM-L6-v2 | Semantic embedding model |
| NumPy | Cosine similarity and vector operations |
| Requests | API communication |
| python-dotenv | Environment variable management |
| uv | Dependency and environment management |

---

## 📦 Installation

Clone the repository:

```bash
git clone <repository-url>
cd SmartStudyAssistant
```

Install the dependencies:

```bash
uv sync
```

If Sentence Transformers is not installed:

```bash
uv add sentence-transformers
```

---

## 🔐 Environment Configuration

Create a `.env` file based on `.env.example`.

### Mock provider

Use the application without real API requests:

```env
LLM_PROVIDER=mock
```

### OpenRouter provider

Use a real LLM through OpenRouter:

```env
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_api_key_here
```

Never commit the real `.env` file.

The repository should contain only:

```text
.env.example
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
uv run streamlit run app.py
```

The application will open in the browser.

---

## 📖 How to Use

### Generate Study Materials

1. Paste lecture notes, upload a PDF, or use both.
2. Select a study feature.
3. The application creates a prompt.
4. The LLM returns structured JSON.
5. Pydantic validates the response.
6. The result is displayed in the interface.

Available features:

- Generate Summary
- Extract Concepts
- Generate Flashcards
- Generate MCQs
- Generate Mock Exam

---

### Ask Questions About a PDF

1. Upload a PDF in the document-question section.
2. Click **Index Document**.
3. Wait while the application:
   - extracts the text,
   - splits it into chunks,
   - generates embeddings,
   - stores the chunk records.
4. Enter a question.
5. Click **Ask Document**.
6. Review:
   - the generated answer,
   - retrieved chunks,
   - similarity scores.

---

## 🧪 Example RAG Flow

Document chunk:

```text
Overfitting occurs when a model learns the training data too closely,
including noise, and performs poorly on unseen examples.
```

User question:

```text
Why does my model perform badly on new data?
```

The user question does not contain the exact word `overfitting`, but the embedding model recognizes the semantic relationship.

The retrieval service ranks the overfitting chunk highly and sends it to the LLM as context.

---

## 🎓 What I Learned

### Software Engineering

- Layered application architecture
- Separation of concerns
- Single Responsibility Principle
- Stable interfaces between services
- Provider abstraction
- Refactoring duplicated code
- Reusable business logic
- Session state
- Resource caching
- Environment management
- Secret protection

### Structured AI Applications

- JSON-based LLM responses
- Pydantic models
- `model_validate()`
- Nested schemas
- Required fields
- Type-safe response access
- Validation of untrusted AI output

### Document Processing

- Streamlit file uploads
- `UploadedFile`
- PDF extraction
- Empty-page handling
- Scanned-document limitations
- Combining multiple input sources
- Keeping document logic outside the UI

### Retrieval-Augmented Generation

- Indexing pipeline
- Query pipeline
- Chunk size
- Chunk overlap
- Semantic embeddings
- Shared vector spaces
- Cosine similarity
- Top-K retrieval
- Context augmentation
- Grounded generation
- Retrieval metadata
- Difference between RAG and fine-tuning

---

## ✅ Completed

- Modular architecture
- Prompt separation
- Provider abstraction
- Mock provider
- OpenRouter provider
- Structured JSON outputs
- Pydantic validation
- Generic structured-output helper
- Summary generation
- Concept extraction
- Flashcard generation
- MCQ generation
- Mock exam generation
- PDF upload
- PDF text extraction
- Typed notes and PDF combination
- Word-based chunking
- Chunk overlap
- Local embedding generation
- Query embedding generation
- Cosine similarity
- Top-K retrieval
- Basic RAG document question answering
- Streamlit session-state indexing
- Retrieved source display
- Similarity score display

---

## 🚧 Current Limitations

The current version is a functional learning prototype.

Known limitations:

- Retrieval uses brute-force NumPy comparison
- Only one RAG document is indexed at a time
- The index is stored only in Streamlit session state
- The index is lost when the session ends
- Page numbers are not preserved yet
- Retrieved chunks may contain duplicated overlapping content
- Similarity thresholds still need improvement
- Unsupported-question fallback behavior needs stronger handling
- Chunking is word-based rather than semantic
- Large document collections are not supported yet
- Automated testing is still limited
- The application is not deployed yet

---

## 🗺️ Next Steps

Immediate next steps:

- Add a minimum similarity threshold
- Improve unsupported-question handling
- Preserve filename metadata
- Preserve page-number metadata
- Improve answer conciseness
- Reduce duplicate retrieved chunks
- Organize the Streamlit interface using tabs
- Add unit tests
- Add logging
- Add clearer custom exceptions
- Prepare deployment configuration
- Deploy the application
- Add interface screenshots
- Add a visual architecture diagram

Possible future improvements:

- Multiple-document ingestion
- FAISS vector indexing
- Persistent vector storage
- Chroma, Qdrant, or pgvector integration
- Recursive chunking
- Semantic chunking
- Saved study sessions
- SQLite integration
- Authentication
- Retrieval evaluation
- Answer faithfulness evaluation
- RAG-based flashcards
- RAG-based MCQs
- RAG-based summaries
- RAG-based mock exams

---

## 🎯 Project Goal

The goal of this project is to demonstrate the ability to design and build an AI application with:

- Clean architecture
- Structured LLM output
- Input validation
- Document ingestion
- Semantic search
- Retrieval-Augmented Generation
- Provider-independent LLM access
- Maintainable Python services

The project is being developed step by step to understand the engineering decisions behind AI systems rather than relying entirely on high-level frameworks.

---

## 📌 Current Project Status

```text
Core study application        ✅ Complete
Structured outputs            ✅ Complete
Pydantic validation           ✅ Complete
PDF ingestion                 ✅ Complete
Basic chunking                ✅ Complete
Local embeddings              ✅ Complete
Cosine similarity retrieval   ✅ Complete
Basic RAG pipeline            ✅ Complete
Retrieval reliability         🚧 In progress
Source citations              🚧 In progress
Testing                       🚧 In progress
UI improvements               🚧 In progress
Deployment                    ⏳ Planned
```

---

## 📄 License

This project was created as a learning and portfolio project for exploring AI engineering, LLM application architecture, document processing, semantic search, and Retrieval-Augmented Generation.
