# Overview

This is a fully functional ACP-compliant health agent system designed to help hospitals answer patient health questions. The application uses the smolagents framework to create a code-based AI agent that performs web searches and extracts health information from trusted medical sources. The system implements the Agent Communication Protocol (ACP) for standardized agent communication, making it suitable for integration into larger multi-agent hospital systems.

## Status: FULLY FUNCTIONAL ✅
- Server running on port 8000
- Health agent responding with accurate medical information
- Web search and content extraction working
- Medical disclaimers and trusted sources integrated
- Example client applications tested successfully

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Framework Architecture
The system is built around the **smolagents** framework, which provides a code-based AI agent architecture. The main components include:

- **ACP Server Wrapper**: Implements Agent Communication Protocol for standardized multi-agent communication
- **Health-Focused CodeAgent**: Specialized agent designed for medical and hospital-related question answering
- **Asynchronous Processing**: Built on asyncio for non-blocking agent communication and concurrent request handling

## Agent Communication Protocol (ACP) Integration
The application implements ACP compliance through:

- **Standardized Message Format**: Uses ACP SDK models for Message and MessagePart structures
- **Server-Client Architecture**: ACP server hosts the health agent, clients connect via standardized protocol
- **Multiple Agent Support**: Architecture supports multiple agents (health_agent, health_router_agent)

## Large Language Model Integration
- **LiteLLM Model**: Uses GPT-4o-mini for cost-effective health question processing
- **Configurable API Integration**: Supports OpenAI API with fallback mechanisms
- **Token Management**: Configured with 2048 max tokens for balanced response length

## Web Search and Content Processing
- **DuckDuckGoSearchTool**: Integrated search capability for finding reliable health information
- **VisitWebpageTool**: Web page content extraction for detailed health information
- **Enhanced Content Extraction**: Custom HealthContentExtractor class using trafilatura library

## Safety and Trust Architecture
- **Trusted Source Validation**: Hardcoded list of reputable medical sources (Mayo Clinic, WebMD, NIH, CDC, etc.)
- **Medical Disclaimer System**: Automatic inclusion of appropriate medical disclaimers in responses
- **Emergency Detection**: Built-in capability to identify potential emergency situations
- **Privacy Considerations**: Designed with patient privacy protection in mind

# External Dependencies

## Core Frameworks
- **smolagents**: Primary framework for code-based AI agents and tool integration
- **acp-sdk**: Agent Communication Protocol implementation for standardized agent communication

## Language Model Services
- **OpenAI API**: GPT-4o-mini model access via LiteLLM
- **LiteLLM**: Unified interface for multiple LLM providers

## Web Processing Tools
- **trafilatura**: Web content extraction and text processing
- **DuckDuckGo Search API**: Web search functionality through smolagents integration

## Python Runtime Dependencies
- **asyncio**: Asynchronous programming support for concurrent operations
- **logging**: Comprehensive logging and error tracking
- **typing**: Type hints and enhanced code documentation

## Configuration Requirements
- **Environment Variables**: OPENAI_API_KEY for LLM access
- **Network Access**: Required for web search and content extraction operations
- **Port Configuration**: Default server deployment on port 8000