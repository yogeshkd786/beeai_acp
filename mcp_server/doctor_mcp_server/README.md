# Doctor Information MCP Server

This project implements a Multi-Agent Communication Protocol (MCP) server that exposes a tool to retrieve doctor information based on a user-provided location in Singapore. The information is loaded from a local JSON file (`doctor_list_sg.json`).

## Importance and Benefits of an MCP Server

An MCP server, built using frameworks like `FastMCP`, provides a standardized way for different agents or services to communicate and expose their functionalities as "tools." This architecture offers several benefits:

*   **Interoperability:** Agents written in different languages or using different internal logic can seamlessly interact by calling each other's exposed tools.
*   **Modularity:** Complex systems can be broken down into smaller, independent agents, each responsible for a specific task. This improves maintainability and scalability.
*   **Reusability:** Tools exposed by an MCP server can be reused across various applications or agent workflows without needing to reimplement the underlying logic.
*   **Scalability:** Individual agents can be scaled independently based on their load, optimizing resource utilization.
*   **Dynamic Tool Discovery:** Agents can dynamically discover and utilize tools exposed by other MCP servers, enabling flexible and adaptive systems.

## Project Structure

```
doctor_mcp_server/
├── doctor_info_server.py
├── doctor_list_sg.json
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Prerequisites

Before running this server, ensure you have the following:

*   **Python 3.9+:** Installed on your system.
*   **`doctor_list_sg.json`:** A JSON file containing doctor information. A sample file is provided in this directory.

## Setup

1.  **Navigate to the Project Directory:**
    ```bash
    cd <path>\doctor_mcp_server
    ```

2.  **Install Dependencies:**
    It is recommended to use `uv` for dependency management if you have it, otherwise `pip`.
    ```bash
    # Using uv (recommended)
    uv pip install -r requirements.txt

    # Or using pip
    pip install -r requirements.txt
    ```

## How to Run

1.  **Start the MCP Server:**
    From within the `doctor_mcp_server` directory, run the following command:
    ```bash
    uvicorn doctor_info_server:app --host 0.0.0.0 --port 8002
    OR uv run doctor_info_server.py
    ```
    This will start the server, typically accessible at `http://localhost:8002`.

2.  **Verify the Server (Optional):**
    You can open your web browser and navigate to `http://localhost:8002/docs` to see the FastAPI interactive API documentation (Swagger UI), which lists the exposed `doctor_info_tool`.

## Using the `doctor_info_tool`

Once the server is running, any MCP-compatible client (or even a simple HTTP client) can call the `doctor_info_tool`.

**Example (Conceptual MCP Client Call):**

A client would typically send a POST request to `http://localhost:8002/call/doctor_info_tool` with a JSON payload specifying the `location`.

```json
{
    "location": "Orchard"
}
```

The server would then return a response containing doctor information for "Orchard".
