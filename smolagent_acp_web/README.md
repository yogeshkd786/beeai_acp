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

## Installation

### Prerequisites
```bash
# Install required Python packages
pip install smolagents acp-sdk trafilatura asyncio

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