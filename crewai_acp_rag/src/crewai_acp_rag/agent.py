from pdb import run
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import PDFSearchTool
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from crewai.tools import tool
import os
from os import getenv
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq

from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from acp_sdk.models.platform import PlatformUIAnnotation, PlatformUIType
from acp_sdk import Annotations, MessagePart, Metadata




    # If you want to run a snippet of code before or after the crew starts,
    # you can use the @before_kickoff and @after_kickoff decorators
    # https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

groq_api_key = getenv("GROQ_API_KEY")

    # If the API key is not found, raise an exception
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set!")
print(f"Groq API Key loaded: {groq_api_key[:5]}...") # Print first 5 chars for security

    # Initialize the Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model="groq/llama-3.3-70b-versatile"
)

print(f"LLM initialized: {llm is not None}")

server=Server()

websearch_tool = SerperDevTool()


vectorstore_tool = PDFSearchTool(pdf='rbhs_info.pdf',
    config=dict(
        llm=dict(
            provider="groq", # or google, openai, anthropic, llama2, ...
            config=dict(
                model="llama-3.3-70b-versatile",
                # temperature=0.5,
                # top_p=1,
                # stream=true,
            ),
        ),
        embedder=dict(
            provider="huggingface", # or openai, ollama, ...
            config=dict(
                model="BAAI/bge-small-en-v1.5",
                #task_type="retrieval_document",
                # title="Embeddings",
            ),
        ),
    )
)


@server.agent(
    name="research_agent",
    description=(
        "This is an agent for questions around hospital policy coverage, it uses a RAG pattern to find answers based on policy documentation, "
        "Use it to help answer questions on coverage and waiting periods."
    ),
    metadata=Metadata(
        annotations=Annotations(
            beeai_ui=PlatformUIAnnotation(
                ui_type=PlatformUIType.CHAT,
                display_name="Research Agent",
                programming_language="Python",
                user_greeting="Hello! I'm your Research AI assistant. How can I help you today?",
                
            )
        ),
        framework="BeeAI",
        recommended_models=["llama-3.3-70b-versatile"],
        author={
            "name": "Yogesh Kadam",
            "email": "yogeshkadamcloud@gmail.com"
        }
    )
)




async def research_agent(input: list[Message]) -> AsyncGenerator[RunYield, RunYieldResume]:
    "This is an agent for questions around hospital policy coverage, it uses a RAG pattern to find answers based on policy documentation. Use it to help answer questions on coverage and waiting periods."

    rag_agent = Agent(
        role="Senior Insurance Coverage Assistant", 
        goal="Use the information retrieved from the vectorstore to answer the question",
        backstory="""You are an expert insurance agent designed to assist with coverage queries.
        You are an assistant for question-answering tasks.
        Use the information present in the retrieved context to answer the question.
        You have to provide a clear concise answer.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[vectorstore_tool], 
        max_retry_limit=5
    )
        
    task1 = Task(
        description=input[0].parts[0].content,
        expected_output = """Use the vectorstore_tool to retrieve information from the vectorstore.
        Return a clear and concise text as response.
        A comprehensive response as to the users question""",
        agent=rag_agent
    )

    crew = Crew(agents=[rag_agent], tasks=[task1], verbose=True)
        
    task_output = await crew.kickoff_async()
    yield Message(parts=[MessagePart(content=str(task_output))])


if __name__ == "__main__":
    server.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 8001)))
