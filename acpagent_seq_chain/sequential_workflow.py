
from acp_sdk.client import Client
import asyncio
import sys
import os
from colorama import Fore, Style, init

# --- Agent Server Endpoints ---
# URL for the RAG agent server
RAG_AGENT_URL = "http://localhost:8001"
# URL for the Web agent server
WEB_AGENT_URL = "http://localhost:8000"




async def run_rag_agent(question: str) -> str:
    """
    Running the RAG agent and returns a output.
    """
    print(f"{Fore.YELLOW}Invoking RAG agent with question: {question}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Connecting to RAG agent at: {RAG_AGENT_URL}{Style.RESET_ALL}")
    async with Client(base_url=RAG_AGENT_URL) as ragagent:
        run1 = await ragagent.run_sync(
            agent="rag_agent", input=f"Context: {question} What is the waiting period for rehabilitation?"
        )
        rag_agent_output = run1.output[0].parts[0].content
        print(Fore.LIGHTMAGENTA_EX+ rag_agent_output + Fore.RESET)
        print(f"{Fore.CYAN}RAG Agent Output: {rag_agent_output}{Style.RESET_ALL}")
        return rag_agent_output


async def run_research_agent(prompt: str) -> str:
    """
    Runs the research agent with the given prompt.
    """
    print(f"\n{Fore.YELLOW}Invoking research agent with prompt: {prompt[:100]}...{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Connecting to Research agent at: {WEB_AGENT_URL}{Style.RESET_ALL}")
    async with Client(base_url=WEB_AGENT_URL) as researchagent:
        
        run2 = await researchagent.run_sync(
            agent="health_agent", input=prompt
        )
        response = run2.output[0].parts[0].content
        print(Fore.YELLOW + run2.output[0].parts[0].content + Fore.RESET)
        return response


    return response

async def main():
    """
    Main function to run the sequential workflow.
    """
    init(autoreset=True)
    
    initial_question = "Do I need rehabilitation after a shoulder reconstruction?"
    
    print(f"{Style.BRIGHT}Starting sequential agent workflow...{Style.RESET_ALL}")
    
    # Step 1: Run the Research agent
    research_output = await run_research_agent(initial_question)

    # Step 2: Run the RAG agent with the output from the Research agent
    # This will fail if the RAG agent server is not running.
    try:
        final_answer = await run_rag_agent(research_output)
    except Exception as e:
        final_answer = f"{Fore.RED}Error connecting to the RAG agent: {e}\nPlease ensure the RAG Agent server is running at {RAG_AGENT_URL}{Style.RESET_ALL}"

    # Step 3: Print the final answer
    print(f"\n\n{Fore.GREEN}{Style.BRIGHT}==================== FINAL ANSWER ===================={Style.RESET_ALL}")
    print(final_answer)
    print(f"{Fore.GREEN}{Style.BRIGHT}===================================================={Style.RESET_ALL}")

if __name__ == "__main__":
    # Run the main function in an asyncio event loop
    asyncio.run(main())
