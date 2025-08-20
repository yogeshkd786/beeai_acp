# `hierarchically_chaining.py`

This script demonstrates a sophisticated hierarchical agent orchestration pattern. It's designed to handle complex user queries by dynamically discovering available agents, leveraging a large language model (LLM) like Gemini to formulate a multi-step execution plan, executing that plan by calling multiple agents sequentially, and finally synthesizing the individual results into a single, coherent answer.

## Features

*   **Dynamic Agent Discovery:** Automatically identifies and registers agents from specified endpoints.
*   **LLM-powered Orchestration (Plan Generation):** Uses Gemini to break down complex user queries into a structured, executable plan, determining which agents to call and in what order.
*   **Sequential Agent Execution:** Executes the generated plan by invoking agents one after another, passing relevant sub-questions.
*   **Result Synthesis:** Combines the answers from various agents into a comprehensive and unified final response to the user.

## Prerequisites

Before running this script, ensure you have the following:

*   **Python 3.x:** Installed on your system.
*   **Required Python Packages:** These are listed in `requirements.txt`.
*   **`uv` (Recommended) or `pip`:** A Python package installer.
*   **`GEMINI_API_KEY`:** An environment variable set with your Gemini API key.
*   **Running RAG Agent Server:** An agent server accessible at `http://localhost:8001` (as configured by `RAG_AGENT_URL` in the script).
*   **Running Web Agent Server:** An agent server accessible at `http://localhost:8000` (as configured by `WEB_AGENT_URL` in the script).

## Setup

1.  **Navigate to the Directory:**
    ```bash
    cd <script-path>\acpagent_hierarchy_chain
    ```

2.  **Install Dependencies:**
    It is recommended to use `uv` for dependency management, as specified by `uv.lock`.
    ```bash
    uv pip install -r requirements.txt
    ```
    Alternatively, you can use `pip`:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Gemini API Key:**
    Set your Gemini API key as an environment variable. Replace `YOUR_GEMINI_API_KEY` with your actual key.

    *   **Windows (Command Prompt):**
        ```bash
        set GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        ```
    *   **Windows (PowerShell):**
        ```powershell
        $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
        ```
    *   **Linux/macOS:**
        ```bash
        export GEMINI_API_KEY=YOUR_GEMINI_API_KEY
        ```

## How to Run

1.  **Ensure Agent Servers are Running:** Make sure your RAG Agent Server (e.g., `crewai_acp_rag`) and Web Agent Server (e.g., `smolagent_acp_web`) are active and accessible at their configured URLs (`http://localhost:8001` and `http://localhost:8000` respectively).

2.  **Execute the Script:**
    ```bash
    python hierarchically_chaining.py
    ```

## Example Usage (Console Output)

Upon execution, the script will:

1.  Print messages indicating the discovery of available agents from the configured servers.
2.  Display Gemini's generated execution plan (a JSON array) for the predefined user query.
3.  Show the execution steps as it calls each agent with its specific sub-question.
4.  Finally, present the synthesized answer, combining the information gathered from all agents, as the `Final result`.