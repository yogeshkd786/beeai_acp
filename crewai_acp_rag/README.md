# CrewAI RAG Agent

This project implements a Research Agent using the CrewAI framework. The agent is designed to answer questions about hospital policy coverage by leveraging a Retrieval-Augmented Generation (RAG) pattern. It uses a Large Language Model (LLM) to understand user queries and a PDF search tool to find relevant information within a policy document.

## Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.8+
*   pip
*   virtualenv (recommended)

You will also need a Groq API key to use the Llama-3.3-70b-versatile model.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>/crewai_acp_rag
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    OR
    uv sync
    ```

4.  **Set up your environment variables:**

    Create a `.env` file in the `crewai_acp_rag` directory and add your Groq API key:
    ```
    GROQ_API_KEY="your-groq-api-key"
    ```

5.  **Run the agent server:**
    ```bash
    python src/crewai_acp_rag/agent.py
    OR 
    uv run server
    ```
    The server will start on `http://localhost:8001` by default.

6.  **Run the client:**

    In a separate terminal, run the client to ask questions:
    ```bash
    python src/crewai_acp_rag/client.py
    ```

## How it Works

The project consists of two main components:

*   **`agent.py`**: This script defines the `research_agent`. The agent is configured with a specific role, goal, and backstory to guide its behavior. It uses the `PDFSearchTool` to search for information in the `rbhs_info.pdf` document and the `SerperDevTool` for web searches. The agent is powered by the `llama-3.3-70b-versatile` model from Groq.

*   **`client.py`**: This script provides a simple command-line interface to interact with the `research_agent`. It takes user input, sends it to the agent server, and prints the response.

The core of the project is the RAG pattern, which allows the agent to provide answers based on the content of the provided PDF document. When a user asks a question, the agent retrieves relevant text from the PDF and then uses the LLM to generate a human-like answer based on the retrieved context.
