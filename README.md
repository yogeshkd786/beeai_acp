# BeeAI ACP

BeeAI ACP (Agent Conversation Platform) is a framework that allows you to run AI agents built with different frameworks, such as CrewAI and Smolagents, and interact with them using a unified interface. This platform simplifies the process of managing and communicating with multiple agents, regardless of their underlying implementation.

## Running Agents from Different Frameworks

BeeAI ACP is designed to be framework-agnostic. It achieves this by using a standardized Agent Communication Protocol (ACP). As long as an agent can communicate using the ACP, it can be managed and run by the BeeAI platform.

This repository contains two examples of agents built with different frameworks:

*   **CrewAI RAG Agent:** An agent that uses the CrewAI framework for Retrieval-Augmented Generation.
*   **Smolagent Health Agent:** An agent that uses the Smolagents framework to answer health-related questions.

By examining these examples, you can learn how to integrate your own agents, built with any framework, into the BeeAI ACP.

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
 beeai list
    ```
    This command will show you a list of all the agents running on the platform.

2.  **Run the research agent:**
beeai run research_agent "Your question about hospital policy coverage"
    ```
    Replace `"Your question about hospital policy coverage"` with your actual question.

This will send the question to the `research_agent`, and you will see the agent's response in the console.



---

## Getting Started with the Smolagent Health Agent

This repository also contains an example of a health agent built with the Smolagents framework. This agent can answer health-related questions by searching the web and extracting relevant information.

### 1. Prerequisites

*   Python 3.11+
*   pip
*   virtualenv (recommended)
*   A Google Gemini API key

### 2. Setup

1.  **Navigate to the agent's directory:**
    ```bash
    cd smolagent_acp_web
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    The dependencies are listed in the `pyproject.toml` file. You can install them using `pip`:
    ```bash
    pip install "acp-sdk>=1.0.1" "asyncio>=4.0.0" "ddgs>=9.5.2" "duckduckgo-search>=8.1.1" "langchain-groq>=0.3.7" "litellm>=1.75.7" "markdownify>=1.2.0" "requests>=2.32.4" "smolagents>=1.21.1" "trafilatura>=2.0.0"
    ```

4.  **Set up your environment variables:**

    Create a `.env` file in the `smolagent_acp_web` directory and add your Gemini API key:
    ```
    GEMINI_API_KEY="your-gemini-api-key"
    ```

### 3. Run the Application

The Smolagent example consists of two parts: the agent server and a web interface. You need to run both in separate terminals.

**Step 1: Start the Health Agent Server**

1.  Open a new terminal or command prompt.
2.  Navigate to the source directory:
    ```bash
    cd src/smolagent_acp_web
    ```
3.  Run the `main.py` script to start the agent server. This will run on port 8000.
    ```bash
    python main.py
    ```
    OR
    uv run server

**Step 2: Start the Web Interface Server**

1.  Open a **new, separate** terminal or command prompt.
2.  Navigate to the same source directory:
    ```bash
    cd src/smolagent_acp_web
    ```
3.  Run the `web_interface.py` script to start the web server. This will run on port 5010.
    ```bash
    python web_interface.py
    ```

### 4. Interact with the Agent

1.  Open your web browser and navigate to the following URL:
    [http://localhost:5010](http://localhost:5010)

You can now ask health-related questions in the web interface and get answers from the Smolagent.

#### Using BeeAI Commands

BeeAI provides a command-line interface to interact with your agents. Here's how you can use it:

1.  **List available agents:**
 beeai list
    ```
    This command will show you a list of all the agents running on the platform.

2.  **Run the research agent:**
beeai run health_agent "what are symptoms of blood pressure?"
    ```
    Replace `"Your question about symptoms"` with your actual question.

This will send the question to the `health_agent`, and you will see the agent's response in the console.