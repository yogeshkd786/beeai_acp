import asyncio
from acp_sdk.client import Client
from colorama import Fore 
import nest_asyncio

nest_asyncio.apply()

async def run_doctor_workflow() -> None:
    async with Client(base_url="http://localhost:8000") as hospital:
        run1 = await hospital.run_sync(
            agent="doctor_agent", input="I'm based in Jurong East. Are there any doctors near me?"
        )
        content = run1.output[0].parts[0].content
        print(Fore.LIGHTMAGENTA_EX+ content + Fore.RESET)

asyncio.run(run_doctor_workflow())