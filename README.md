# 📚 Smart Study Assistant

A modular AI-powered study assistant built with **Python**, **Streamlit**, and **OpenRouter**. This project demonstrates how to design maintainable AI applications by separating the user interface, business logic, prompt engineering, and LLM providers.

> **Project Status:** Phase 1 Complete ✅

---

# Features

Current capabilities include:

* 📄 Generate lecture summaries
* 🧠 Extract key concepts
* 📝 Generate flashcards
* ❓ Generate multiple-choice questions (MCQs)
* 🎓 Generate mock exams
* 🔄 Switch between LLM providers without changing application logic
* 🧪 Mock provider for offline development and testing

---

# Tech Stack

* Python 3.11
* Streamlit
* OpenRouter API
* Requests
* python-dotenv
* uv (package manager)

---

# Project Structure

```text
SmartStudyAssistant/

├── app.py
│
├── prompts/
│   ├── summary_prompt.py
│   ├── concept_prompt.py
│   ├── flashcard_prompt.py
│   ├── mcq_prompt.py
│   └── exam_prompt.py
│
├── services/
│   ├── llm_service.py
│   ├── study_service.py
│   └── providers/
│       ├── mock_provider.py
│       └── openrouter_provider.py
│
├── data/
├── utils/
├── .env
├── pyproject.toml
├── uv.lock
└── README.md
```

---

# Architecture

```
                Streamlit UI
                     │
                     ▼
             Study Service Layer
                     │
                     ▼
             Prompt Builders
                     │
                     ▼
               LLM Service
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 Mock Provider           OpenRouter Provider
```

The architecture follows a layered design where each component has a single responsibility.

---

# Responsibilities

## app.py

Responsible for:

* Displaying the Streamlit interface
* Collecting user input
* Displaying AI-generated results

The UI never communicates directly with an LLM provider.

---

## study_service.py

Contains the application's business logic.

Responsible for:

* Generating summaries
* Extracting concepts
* Creating flashcards
* Creating MCQs
* Creating mock exams

It coordinates prompt generation and LLM communication.

---

## prompts/

Each prompt lives in its own module.

Examples:

* summary_prompt.py
* concept_prompt.py
* flashcard_prompt.py
* mcq_prompt.py
* exam_prompt.py

Keeping prompts separate makes them easier to improve and maintain.

---

## llm_service.py

Acts as the abstraction layer between the application and any LLM provider.

The rest of the application only calls:

```python
ask_llm(prompt)
```

The UI never depends on a specific provider.

---

## providers/

Each provider implements a common interface for generating responses.

Current providers:

* Mock Provider
* OpenRouter Provider

Additional providers (Gemini, OpenAI, Anthropic, etc.) can be added without changing the rest of the application.

---

# Development Workflow

During development, the application can run entirely without an internet connection using the mock provider.

```env
LLM_PROVIDER=mock
```

To use a real LLM:

```env
LLM_PROVIDER=openrouter
```

No Python code needs to change.

---

# Running the Project

Install dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run streamlit run app.py
```

---

# What I Learned

This phase focused on software architecture rather than simply calling an LLM.

Key concepts learned:

* Modular application design
* Separation of concerns
* Single Responsibility Principle (SRP)
* Provider abstraction
* Prompt engineering organization
* Environment variable management
* API integration
* Basic AI application architecture

---

# Future Improvements

The next development phases include:

* Structured JSON outputs
* Pydantic validation
* PDF and DOCX support
* Streaming responses
* Retrieval-Augmented Generation (RAG)
* Conversation memory
* User authentication
* Database integration
* Deployment to the cloud

---

# License

This project was built as a learning project for exploring AI application development and software engineering best practices.
