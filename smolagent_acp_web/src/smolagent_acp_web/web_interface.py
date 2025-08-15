#!/usr/bin/env python3
"""
Web Interface for ACP Health Agent
Provides a simple web interface to interact with the health agent.
"""

import asyncio
import logging
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Hospital Health Agent Web Interface")

def get_html_template(response_html=""):
    """Generate HTML template with response content."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospital Health Agent</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f7fa;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        label {{
            display: block;
            margin-bottom: 8px;
            color: #34495e;
            font-weight: 500;
        }}
        textarea {{
            width: 100%;
            padding: 12px;
            border: 2px solid #ecf0f1;
            border-radius: 6px;
            font-size: 16px;
            resize: vertical;
            min-height: 100px;
            box-sizing: border-box;
        }}
        textarea:focus {{
            outline: none;
            border-color: #3498db;
        }}
        button {{
            background-color: #27ae60;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
        }}
        button:hover {{
            background-color: #229954;
        }}
        .response {{
            background-color: #ecf8ff;
            border-left: 4px solid #3498db;
            padding: 20px;
            margin-top: 20px;
            border-radius: 6px;
            white-space: pre-wrap;
            font-family: Georgia, serif;
            line-height: 1.6;
        }}
        .error {{
            background-color: #fee;
            border-left: 4px solid #e74c3c;
            color: #c0392b;
        }}
        .disclaimer {{
            background-color: #fff9e6;
            border: 1px solid #f39c12;
            padding: 15px;
            margin: 20px 0;
            border-radius: 6px;
            font-size: 14px;
            color: #d68910;
        }}
        .examples {{
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 6px;
        }}
        .example-question {{
            cursor: pointer;
            color: #3498db;
            text-decoration: underline;
            margin: 5px 0;
        }}
        .example-question:hover {{
            color: #2980b9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Hospital Health Agent</h1>
        <p class="subtitle">Ask health questions and get evidence-based information from trusted medical sources</p>
        
        <div class="disclaimer">
            <strong>Medical Disclaimer:</strong> This tool provides general health information for educational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always consult with your healthcare provider for personalized medical guidance.
        </div>
        
        <form method="post" action="/ask">
            <div class="form-group">
                <label for="question">Your Health Question:</label>
                <textarea name="question" id="question" placeholder="Example: What are the symptoms of diabetes?" required></textarea>
            </div>
            <button type="submit">Get Health Information</button>
        </form>
        
        <div class="examples">
            <strong>Example Questions:</strong><br>
            <div class="example-question" onclick="document.getElementById('question').value='What are the symptoms of diabetes?'">• What are the symptoms of diabetes?</div>
            <div class="example-question" onclick="document.getElementById('question').value='How can I prevent heart disease?'">• How can I prevent heart disease?</div>
            <div class="example-question" onclick="document.getElementById('question').value='What are the benefits of regular exercise?'">• What are the benefits of regular exercise?</div>
            <div class="example-question" onclick="document.getElementById('question').value='How much sleep do adults need?'">• How much sleep do adults need?</div>
        </div>
        
        {response_html}
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main web interface."""
    return get_html_template()

@app.post("/ask", response_class=HTMLResponse)
async def ask_health_question(question: str = Form(...)):
    """Process health questions through the ACP health agent."""
    if not question.strip():
        error_html = '<div class="response error">Please enter a health question.</div>'
        return get_html_template(error_html)
    
    try:
        # Connect to the ACP health agent
        async with Client(base_url="http://localhost:8000") as client:
            message = Message(
                role="user",
                parts=[MessagePart(
                    content=question.strip(),
                    content_type="text/plain"
                )]
            )
            
            logger.info(f"Processing health question: {question[:50]}...")
            
            # Send request to health agent
            run = await client.run_sync(
                agent="health_agent",
                input=[message]
            )
            
            if run.output and run.output[0].parts:
                response = run.output[0].parts[0].content
                response_html = f'<div class="response">{response}</div>'
                logger.info(f"Successfully received response ({len(response)} chars)")
            else:
                response_html = '<div class="response error">No response received from health agent.</div>'
                
    except Exception as e:
        logger.error(f"Error communicating with health agent: {e}")
        error_message = f"Unable to connect to health agent: {str(e)}"
        response_html = f'<div class="response error">{error_message}</div>'
    
    return get_html_template(response_html)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Health Agent Web Interface"}

def main():
    """Start the web interface server."""
    logger.info("Starting Health Agent Web Interface on port 5000")
    logger.info("Connect to the health agent at http://localhost:5000")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5010,
        log_level="info"
    )

if __name__ == "__main__":
    main()