import json
import asyncio
import os
import nest_asyncio
from acp_sdk.client import Client
from smolagents import LiteLLMModel
#from fastacp import AgentCollection, ACPCallingAgent
from colorama import Fore

#print(ACPCallingAgent.__doc__)

# --- Agent Server Endpoints ---
# URL for the RAG agent server
RAG_AGENT_URL = "http://localhost:8001"
# URL for the Web agent server
WEB_AGENT_URL = "http://localhost:8000"

model = LiteLLMModel(
    model_id="gemini/gemini-2.5-flash",
    api_key=os.environ.get("GEMINI_API_KEY")
)

async def run_hospital_workflow() -> None:
    # Discover agents dynamically from the agent servers
    agents = []
    async with Client(base_url=RAG_AGENT_URL) as rag_client, Client(base_url=WEB_AGENT_URL) as web_client:
        clients = [(rag_client, RAG_AGENT_URL), (web_client, WEB_AGENT_URL)]
        for client, base_url in clients:
            try:
                # The acp-sdk has an agents() method to discover agents.
                async for agent_meta in client.agents():
                    agents.append({
                        "name": agent_meta.name,
                        "desc": agent_meta.description,
                        "client": client,
                        "url": str(base_url)
                    })
                    print(f"Discovered agent: {agent_meta.name} at {agent_meta.description} at {base_url}")
            except Exception as e:
                print(f"Could not discover agents at {base_url}: {e}")

        if not agents:
            print("Could not discover any agents. Please ensure the agent servers are running.")
            return

        # Prepare agent/tool descriptions for Gemini
        agent_descriptions = [f'{a["name"]}: {a["desc"]}' for a in agents]
        agent_list_str = "\n".join(agent_descriptions)

        # User query
        user_query = "do i need to go for post medical checkups after a pregnancy and what is the waiting period from my insurance cover?"
        #user_query = "what is the waiting period from my insurance?"

        # Ask Gemini to create a plan
        orchestrator_prompt = f"""You are an orchestrator agent. Your job is to take a user's query and create a plan to answer it by using a set of available agents.

The user's query is: "{user_query}"

Here are the available agents:
{agent_list_str}

Your plan should be a JSON array of steps. Each step should have two keys: "agent_name" and "question". "agent_name" must be one of the available agent names. "question" should be the specific question to ask that agent.

Break down the user's query into smaller, logical questions that can be answered by the available agents. The order of the steps in the array matters.

For example, if the user asks "I have a broken leg, what should I do and what is my insurance coverage?", the plan could be:
[
    {{
        "agent_name": "health_agent",
        "question": "What should I do if I have a broken leg?"
    }},
    {{
        "agent_name": "rag_agent",
        "question": "What is my insurance coverage for a broken leg?"
    }}
]

Now, create a plan for the user's query.
"""
        # Call Gemini LLM (LiteLLMModel) correctly
        gemini_response_message = model.generate(messages=[{"role": "user", "content": orchestrator_prompt}])
        gemini_response = gemini_response_message.content
        
        print(Fore.CYAN + f"Gemini response: {gemini_response}" + Fore.RESET)

        try:
            # Extract the JSON part of the response
            json_part = gemini_response[gemini_response.find("[") : gemini_response.rfind("]") + 1]
            plan = json.loads(json_part)
        except (json.JSONDecodeError, IndexError) as e:
            print(Fore.RED + f"Error parsing plan from Gemini: {e}" + Fore.RESET)
            print(Fore.RED + f"Full response: {gemini_response}" + Fore.RESET)
            return

        # Execute the plan
        results = []
        for step in plan:
            agent_name = step["agent_name"]
            question = step["question"]
            print(Fore.CYAN + f"Executing step: call {agent_name} with question: {question}" + Fore.RESET)
            
            found_agent = False
            for agent in agents:
                if agent_name.lower() == agent["name"].lower():
                    try:
                        response = await agent["client"].run_sync(agent=agent_name, input=question)
                        result = response.output[0].parts[0].content
                        results.append(result)
                    except Exception as e:
                        result = f"Error calling agent: {e}"
                        results.append(result)
                    found_agent = True
                    break
            if not found_agent:
                results.append(f"Agent '{agent_name}' not found.")

        # Synthesize the final answer
        synthesis_prompt = f"""You are a helpful assistant. You have been given a user's original query and a series of answers from different agents. Your task is to synthesize these answers into a single, coherent response for the user.

User's original query: "{user_query}"

Here are the answers from the agents:
{" ".join(results)}

Please provide a final, synthesized answer to the user.
"""
        final_response_message = model.generate(messages=[{"role": "user", "content": synthesis_prompt}])
        final_response = final_response_message.content
        print(Fore.YELLOW + f"Final result: {final_response}" + Fore.RESET)


asyncio.run(run_hospital_workflow())
