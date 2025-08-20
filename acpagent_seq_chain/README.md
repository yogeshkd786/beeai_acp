# Sequential Agent Chaining with ACP

This project demonstrates a sequential workflow where two different agent frameworks, wrapped in the Agent Control Protocol (ACP), are chained together. The output of the first agent is used as the input for the second agent, creating a simple yet powerful pipeline.

## How it Works

The `sequential_workflow.py` script orchestrates the chaining of two agents:

1.  **Research Agent (`health_agent`):** This agent is running on `http://localhost:8000`. It takes an initial question and performs research to gather information.

2.  **RAG Agent (`rag_agent`):** This agent is running on `http://localhost:8001`. It's a Retrieval-Augmented Generation (RAG) agent that answers questions based on a specific knowledge base.

The workflow is as follows:

1.  An initial question is posed to the **Research Agent**.
2.  The output from the **Research Agent** is then passed as input to the **RAG Agent**.
3.  The final answer from the **RAG Agent** is then printed to the console.

This demonstrates how you can create more complex workflows by composing specialized agents, each excelling at a specific task.

## Prerequisites

*   Python 3.8+
*   `uv` (or `pip` and `virtualenv`)
*   The two agent servers (`health_agent` and `rag_agent`) must be running at their respective endpoints.

## Step-by-Step Guide to Run

1.  **Clone the repository and navigate to the project directory:**
    ```bash
    # (Assuming you have already cloned the repository)
    cd acpagent_seq_chain
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment.
    ```bash
    # Create and activate a virtual environment
    python -m venv .venv or uv venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

    # Install dependencies using uv
    uv sync
    ```
    Alternatively, you can use `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ensure the Agent Servers are Running:**
    Before running the script, you need to start the two agent servers in separate terminals:

    *   **Start the Research Agent (`health_agent`):**
        Navigate to the `smolagent_acp_web` directory and run the server (typically on port 8000).
        ```bash
        # In a new terminal
        cd ../smolagent_acp_web
        uv run server
        ```

    *   **Start the RAG Agent (`rag_agent`):**
        Navigate to the `crewai_acp_rag` directory and run the server (typically on port 8001).
        ```bash
        # In another new terminal
        cd ../crewai_acp_rag
        uv run server
        ```

4.  **Run the Sequential Workflow:**
    Once the two agent servers are running, you can execute the `sequential_workflow.py` script from the `acpagent_seq_chain` directory:
    ```bash
    # In the acpagent_seq_chain directory
    python sequential_workflow.py
    ```

The script will then execute the sequential workflow, and you will see the output from both agents, followed by the final answer.
