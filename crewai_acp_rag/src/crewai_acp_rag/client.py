import nest_asyncio
nest_asyncio.apply()
from acp_sdk.client import Client
import asyncio
#from colorama import Fore 

question=input("Enter your question: ")

async def acp_client() -> None:
    async with Client(base_url="http://localhost:8001") as client:
        run = await client.run_sync(
                        
            agent="rag_agent", input=question
                  
        )
        print("Response:\n" + run.output[0].parts[0].content)

asyncio.run(acp_client())