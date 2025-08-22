# ACP-Compliant Health Agent

An Agent Communication Protocol (ACP) compliant health agent using the smolagent library that helps hospitals answer patient health questions through web search and content extraction.

## Overview

This application implements a hospital health agent system that:

- Uses **smolagents** framework for code-based AI agents
- Implements **ACP (Agent Communication Protocol)** for standardized agent communication
- Provides health-focused question answering for hospital patients
- Performs web searches using **DuckDuckGoSearchTool**
- Extracts content from web pages using **VisitWebpageTool**
- Maintains patient privacy considerations and medical disclaimers

## Features

### Core Capabilities
- **ACP Server Wrapper**: Standardized communication protocol for multi-agent systems
- **Health-Focused Agent**: Specialized for medical and hospital-related questions
- **Web Search Integration**: DuckDuckGo search for reliable health information
- **Content Extraction**: Enhanced web page content processing for health information
- **Asynchronous Processing**: Non-blocking agent communication
- **Error Handling**: Robust error handling for web search failures
- **Medical Disclaimers**: Automatic inclusion of appropriate medical disclaimers

### Safety Features
- **Trusted Source Validation**: Prioritizes reputable medical sources
- **Emergency Detection**: Identifies potential emergency situations
- **Privacy Considerations**: Designed with patient privacy in mind
- **Professional Disclaimers**: Always recommends consulting healthcare providers

## Agents

This application includes three distinct agents, each with a specific role:

### Health Agent (`health_agent`)

This is the primary agent for answering health-related questions. It takes a user's query, searches the web for relevant and reliable information, and provides a comprehensive, easy-to-understand response.

- **Tools**: `DuckDuckGoSearchTool`, `VisitWebpageTool`
- **Functionality**:
    - Searches for health information from reputable sources.
    - Extracts and summarizes content from web pages.
    - Enhances the response with medical disclaimers and formatting.

### Health Router Agent (`health_router_agent`)

This agent acts as a preliminary triage for incoming health queries. It categorizes questions to determine their urgency and provides an appropriate initial response.

- **Functionality**:
    - Identifies urgent queries based on keywords (e.g., "emergency," "chest pain").
    - Provides immediate guidance for urgent situations, advising users to contact emergency services.
    - For general queries, it confirms that the request is being processed.

### Doctor Agent (`doctor_agent`)

This agent helps users find doctors in their vicinity. It leverages an external MCP (Multi-Agent Communication Protocol) server to access a database of doctors.

- **Tools**: `ToolCollection` from an MCP server.
- **Functionality**:
    - Takes a user's location as input.
    - Queries an external service to find nearby doctors.
    - Returns a list of doctors to the user.

## Important Considerations

### Trusted Sources

The `HealthContentExtractor` class includes a list of trusted health sources (e.g., Mayo Clinic, WebMD, NIH). When the `health_agent` retrieves information, it prioritizes these sources to ensure the information is reliable and evidence-based.

### Medical Disclaimer

All responses from the `health_agent` are appended with a medical disclaimer. This is to ensure that users understand that the information provided is for educational purposes only and not a substitute for professional medical advice.

## Installation

### Prerequisites
```bash
# Install required Python packages
pip install smolagents acp-sdk trafilatura asyncio fastapi uvicorn python-multipart
```

## Running the Application

There are two methods to run the application. Method 1 is recommended as it is more straightforward.

### Method 1: Using Python Directly (Recommended)

This method involves running the agent server and the web interface in two separate terminals.

**Step 1: Start the Health Agent Server**

1.  Open a new terminal or command prompt.
2.  Navigate to the source directory:
    ```bash
    cd <path_to_project>\smolagent_acp_web\src\smolagent_acp_web
    ```
3.  Run the `main.py` script to start the agent server. This will run on port 8000.
    ```bash
    python main.py
    ```
    You should see output indicating the server has started.

**Step 2: Start the Web Interface Server**

1.  Open a **new, separate** terminal or command prompt.
2.  Navigate to the same source directory:
    ```bash
    cd <path_to_project>\smolagent_acp_web\src\smolagent_acp_web
    ```
3.  Run the `web_interface.py` script to start the web server. This will run on port 5010.
    ```bash
    python web_interface.py
    ```
    You should see output indicating the server has started.

**Step 3: Access the Web Interface**

1.  Open your web browser and navigate to the following URL:
    [http://localhost:5010](http://localhost:5010)

### Method 2: Using the `uv` command

This method uses the `uv` command to run the agent server as an installed script.

**Step 1: Install the project in editable mode**

1.  Open a terminal or command prompt.
2.  Navigate to the project's root directory:
    ```bash
    cd <path_to_project>\smolagent_acp_web
    ```
3.  Install the project in editable mode. This will create the `server` script in your virtual environment.
    ```bash
    pip install -e .
    ```

**Step 2: Start the Health Agent Server**

1.  From the same terminal, run the `server` script using `uv`. This will run on port 8000.
    ```bash
    uv run server
    ```
    Alternatively, you can run the script directly:
    ```bash
    server
    ```

**Step 3: Start the Web Interface Server**

1.  Open a **new, separate** terminal or command prompt.
2.  Navigate to the source directory:
    ```bash
    cd <path_to_project>\smolagent_acp_web\src\smolagent_acp_web
    ```
3.  Run the `web_interface.py` script to start the web server. This will run on port 5010.
    ```bash
    python web_interface.py
    ```

**Step 4: Access the Web Interface**

1.  Open your web browser and navigate to the following URL:
    [http://localhost:5010](http://localhost:5010)

## Interacting with the Agents

### Web Interface

The simplest way to interact with the `health_agent` is through the web interface. Open [http://localhost:5010](http://localhost:5010) in your browser, type your health question in the text area, and click "Get Health Information."

### Command-line Client

You can use the `client_example.py` script to interact with the `health_agent` and `health_router_agent` from the command line.

-   **Run example queries:**
    ```bash
    python smolagent_acp_web/src/smolagent_acp_web/client_example.py
    ```
-   **Run in interactive mode:**
    ```bash
    python smolagent_acp_web/src/smolagent_acp_web/client_example.py --interactive
    ```
    In interactive mode, you can prefix your query with `router:` to use the `health_router_agent`.

### Programmatic Client

You can also interact with the agents programmatically using the `acp-sdk`.

-   **Health Agent Example**: See `client_example.py` for how to create a `HealthAgentClient` to interact with the `health_agent` and `health_router_agent`.
-   **Doctor Agent Example**: See `client_acp_mcp_call.py` for an example of how to call the `doctor_agent`.
