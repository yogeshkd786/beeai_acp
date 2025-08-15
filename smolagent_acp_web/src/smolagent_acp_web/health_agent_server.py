import os
import logging
import asyncio
import time
from typing import AsyncGenerator, List
from collections.abc import AsyncGenerator as AsyncGeneratorType
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# ACP SDK imports
from acp_sdk.server import Server
from acp_sdk.models import Message, MessagePart

# smolagents imports
from smolagents import CodeAgent, DuckDuckGoSearchTool, VisitWebpageTool, OpenAIServerModel

# Local imports
from .web_content_extractor import HealthContentExtractor

logger = logging.getLogger(__name__)

def create_health_agent_server() -> Server:
    """
    Create and configure the ACP health agent server.
    
    Returns:
        Server: Configured ACP server instance
    """
    # Initialize ACP server
    server = Server()
    
    

    gemini_api_key = getenv("GEMINI_API_KEY")

    # If the API key is not found, raise an exception
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set!")
    print(f"Gemini API Key loaded: {gemini_api_key[:5]}...") # Print first 5 chars for security

    # Initialize the Google Gemini LLM using OpenAIServerModel for smolagents compatibility.
    llm = OpenAIServerModel(
        model_id="gemini-2.5-pro",
        api_key=gemini_api_key,
        api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
        max_tokens=2000,  # Set maximum tokens for response generation
        temperature=0.7,  # Optional: control randomness (0.0-1.0)
        # Additional optional parameters:
        # top_p=0.9,      # Optional: nucleus sampling
        # frequency_penalty=0.0,  # Optional: reduce repetition
        # presence_penalty=0.0,   # Optional: encourage new topics
    )
    
    # Initialize content extractor
    content_extractor = HealthContentExtractor()
    
    @server.agent()
    async def health_agent(messages: List[Message]) -> AsyncGeneratorType[Message, None]:
        """
        Health-focused CodeAgent that supports hospitals in handling health-based questions for patients.
        
        Current or prospective patients can use it to find answers about their health and hospital treatments.
        The agent performs web searches using DuckDuckGo and extracts content from relevant web pages to provide
        accurate, up-to-date health information while maintaining patient privacy considerations.
        
        Args:
            messages: List of ACP-compliant messages from the client
            
        Yields:
            Message: ACP-compliant response messages with health information
        """
        try:
            # Extract user prompt from ACP message format
            if not messages:
                yield Message(
                    role="agent",
                    parts=[MessagePart(
                        content="Error: No input messages received.",
                        content_type="text/plain"
                    )]
                )
                return
            
            # Get the latest user message
            user_message = messages[-1]
            if not user_message.parts:
                yield Message(
                    role="agent",
                    parts=[MessagePart(
                        content="Error: Empty message received.",
                        content_type="text/plain"
                    )]
                )
                return
            
            prompt = user_message.parts[0].content if user_message.parts[0].content is not None else ""
            logger.info(f"Processing health query: {prompt[:100]}...")
            
            # Create enhanced health-focused prompt
            health_focused_prompt = f"""
            You are a health information assistant for a hospital. A patient has asked: "{prompt}"
            
            Please help by:
            1. Searching for reliable health information from reputable medical sources
            2. Visiting relevant web pages to get detailed, accurate information
            3. Providing a comprehensive but easy-to-understand response
            4. Including sources and disclaimers about consulting healthcare professionals
            5. Focusing on evidence-based medical information
            
            Important: Always remind users to consult with their healthcare provider for personalized medical advice.
            Search for information from reputable sources like Mayo Clinic, WebMD, NIH, CDC, or medical journals.
            """
            
            # Create smolagents CodeAgent with health-focused tools
            agent = CodeAgent(
                tools=[
                    DuckDuckGoSearchTool(),
                    VisitWebpageTool(),
                ],
                model=llm
            )
            
            # Run the agent with error handling and retry logic
            max_retries = 3
            retry_delay = 5  # Start with 5 seconds
            
            for attempt in range(max_retries):
                try:
                    response = agent.run(health_focused_prompt)
                    
                    # Process and enhance the response
                    enhanced_response = content_extractor.enhance_health_response(str(response))
                    
                    # Log successful processing
                    logger.info(f"Successfully processed health query, response length: {len(enhanced_response)}")
                    
                    # Return ACP-compliant response
                    yield Message(
                        role="agent",
                        parts=[MessagePart(
                            content=enhanced_response,
                            content_type="text/plain"
                        )]
                    )
                    break  # Success, exit retry loop
                    
                except Exception as agent_error:
                    error_str = str(agent_error)
                    logger.error(f"Agent execution error (attempt {attempt + 1}/{max_retries}): {agent_error}")
                    
                    # Check if it's a rate limit error
                    if "rate_limit" in error_str.lower() or "ratelimit" in error_str.lower():
                        if attempt < max_retries - 1:  # Not the last attempt
                            logger.info(f"Rate limit hit, waiting {retry_delay} seconds before retry...")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                            continue
                        else:
                            # Last attempt failed due to rate limit
                            error_response = f"""
                            I apologize, but I'm currently experiencing high demand and have hit rate limits while trying to search for health information about your question: "{prompt}"
                            
                            This is a temporary issue. Please try again in a few minutes, or contact your healthcare provider directly for immediate medical concerns.
                            
                            For general health information, you may also visit reputable sources like:
                            - Mayo Clinic (mayoclinic.org)
                            - WebMD (webmd.com)
                            - MedlinePlus (medlineplus.gov)
                            - CDC (cdc.gov)
                            """
                    else:
                        # Non-rate-limit error
                        error_response = f"""
                        I apologize, but I encountered an issue while searching for health information about your question: "{prompt}"
                        
                        Error details: {error_str}
                        
                        Please try rephrasing your question or contact your healthcare provider directly for immediate medical concerns.
                        
                        For general health information, you may also visit reputable sources like:
                        - Mayo Clinic (mayoclinic.org)
                        - WebMD (webmd.com)
                        - MedlinePlus (medlineplus.gov)
                        - CDC (cdc.gov)
                        """
                    
                    yield Message(
                        role="agent",
                        parts=[MessagePart(
                            content=error_response,
                            content_type="text/plain"
                        )]
                    )
                    break  # Exit retry loop for non-rate-limit errors
                
        except Exception as e:
            logger.error(f"Health agent error: {e}")
            yield Message(
                role="agent",
                parts=[MessagePart(
                    content=f"An unexpected error occurred while processing your health query. Please try again or contact technical support. Error: {str(e)}",
                    content_type="text/plain"
                )]
            )
    
    @server.agent()
    async def health_router_agent(messages: List[Message]) -> AsyncGeneratorType[Message, None]:
        """
        Router agent that categorizes health queries and routes them appropriately.
        
        This agent helps determine the urgency and type of health question to provide
        appropriate routing and response handling.
        """
        try:
            if not messages or not messages[-1].parts:
                yield Message(
                    role="agent",
                    parts=[MessagePart(
                        content="Error: No valid input received for health routing.",
                        content_type="text/plain"
                    )]
                )
                return
            
            prompt = messages[-1].parts[0].content if messages[-1].parts[0].content is not None else ""
            
            # Simple routing logic for health queries
            urgent_keywords = ['emergency', 'urgent', 'severe pain', 'chest pain', 'difficulty breathing', 'bleeding']
            general_keywords = ['symptoms', 'treatment', 'medication', 'prevention', 'diet', 'exercise']
            
            prompt_lower = prompt.lower() if prompt else ""
            is_urgent = any(keyword in prompt_lower for keyword in urgent_keywords)
            is_general = any(keyword in prompt_lower for keyword in general_keywords)
            
            if is_urgent:
                response = """
                ⚠️ URGENT HEALTH CONCERN DETECTED ⚠️
                
                Based on your query, this appears to be a potentially urgent health matter.
                
                IMMEDIATE ACTION REQUIRED:
                - If this is a medical emergency, call 911 or go to the nearest emergency room immediately
                - For urgent but non-emergency concerns, contact your healthcare provider or urgent care clinic
                - Do not delay seeking professional medical attention
                
                This AI system cannot provide emergency medical care or replace professional medical evaluation.
                """
            elif is_general:
                response = f"""
                I'll help you find reliable health information about: "{prompt}"
                
                Let me search for evidence-based information from reputable medical sources.
                This will include general health information, but remember that this is not a substitute for professional medical advice.
                
                Routing your query to our health information agent...
                """
                # In a real implementation, this would route to the health_agent
            else:
                response = f"""
                I've received your health-related query: "{prompt}"
                
                I'll search for general health information to help answer your question.
                Please note that this information is for educational purposes only and should not replace consultation with your healthcare provider.
                
                Searching for reliable health information...
                """
            
            yield Message(
                role="agent",
                parts=[MessagePart(
                    content=response,
                    content_type="text/plain"
                )]
            )
            
        except Exception as e:
            logger.error(f"Health router agent error: {e}")
            yield Message(
                role="agent",
                parts=[MessagePart(
                    content=f"Error in health query routing: {str(e)}. Please try again or contact support.",
                    content_type="text/plain"
                )]
            )
    
    return server

# Health-specific utility functions
def validate_health_query(query: str) -> tuple[bool, str]:
    """
    Validate health queries for safety and appropriateness.
    
    Args:
        query: User's health question
        
    Returns:
        tuple: (is_valid, message)
    """
    if not query or len(query.strip()) < 3:
        return False, "Please provide a more detailed health question."
    
    # Check for emergency indicators
    emergency_terms = [
        'suicide', 'kill myself', 'overdose', 'poisoning',
        'severe chest pain', 'can\'t breathe', 'unconscious'
    ]
    
    if any(term in query.lower() for term in emergency_terms):
        return False, "This appears to be a medical emergency. Please call 911 or contact emergency services immediately."
    
    return True, "Query is valid for health information search."

def sanitize_health_response(response: str) -> str:
    """
    Sanitize health response to ensure appropriate disclaimers and safety.
    
    Args:
        response: Raw response from the agent
        
    Returns:
        str: Sanitized response with appropriate disclaimers
    """
    disclaimer = """

⚕️ IMPORTANT MEDICAL DISCLAIMER:
This information is for educational purposes only and is not intended to replace professional medical advice, diagnosis, or treatment. Always consult with your healthcare provider for personalized medical guidance. If you have a medical emergency, call 911 immediately.
"""
    
    # Ensure the response includes proper medical disclaimers
    if "disclaimer" not in response.lower() and "consult" not in response.lower():
        response += disclaimer
    
    return response
