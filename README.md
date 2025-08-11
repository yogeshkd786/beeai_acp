# BeeAI ACP

BeeAI ACP (Agent Conversation Platform) is a framework that allows you to run AI agents built with different frameworks, such as CrewAI, and interact with them using a unified interface. This platform simplifies the process of managing and communicating with multiple agents, regardless of their underlying implementation.

## Key Features

*   **Framework Agnostic:** Run agents built with various frameworks, including CrewAI.
*   **Unified Interface:** Interact with all your agents using a consistent set of commands.
*   **Simplified Agent Management:** Easily start, stop, and manage your agents.

## Getting Started with the CrewAI RAG Agent

This repository contains an example of a CrewAI RAG (Retrieval-Augmented Generation) agent that can answer questions about hospital policy coverage. Here's how to run it:

### 1. Prerequisites

*   Python 3.8+
*   pip
*   virtualenv (recommended)
*   A Groq API key

### 2. Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Navigate to the agent's directory:**
    ```bash
    cd crewai_acp_rag
    ```

3.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

4.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt 
    OR 
    uv sync
    ```

5.  **Set up your environment variables:**

    Create a `.env` file in the `crewai_acp_rag` directory and add your Groq API key:
    ```
    GROQ_API_KEY="your-groq-api-key"
    ```

### 3. Run the Agent

1.  **Start the agent server:**
    ```bash
    python src/crewai_acp_rag/agent.py 
    OR
    uv run server
    ```
    The server will start on `http://localhost:8001` by default.

### 4. Interact with the Agent

Once the agent is running, you can interact with it using the provided client or BeeAI commands.

#### Using the Client

In a separate terminal, run the client script:

```bash
python src/crewai_acp_rag/client.py
```

The client will prompt you to enter your question. Type your question and press Enter to get a response from the agent.

#### Using BeeAI Commands

BeeAI provides a command-line interface to interact with your agents. Here's how you can use it:

1.  **List available agents:**
    ```bash
    beeai list
    ```
    This command will show you a list of all the agents running on the platform.

2.  **Run the research agent:**
    ```bash
    beeai run research_agent "Your question about hospital policy coverage"
    ```
    Replace `"Your question about hospital policy coverage"` with your actual question.

This will send the question to the `research_agent`, and you will see the agent's response in the console.
