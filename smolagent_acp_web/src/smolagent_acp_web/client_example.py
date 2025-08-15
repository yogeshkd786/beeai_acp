"""
Example ACP Client for Health Agent
Demonstrates how to interact with the ACP-compliant health agent server.
"""

import asyncio
import logging
import sys
from typing import List

# ACP SDK imports
from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart

logger = logging.getLogger(__name__)

class HealthAgentClient:
    """
    Client for interacting with the ACP health agent server.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the health agent client.
        
        Args:
            base_url: Base URL of the ACP health agent server
        """
        self.base_url = base_url
        logger.info(f"Initialized Health Agent Client for {base_url}")
    
    async def ask_health_question(self, question: str, agent_name: str = "health_agent") -> str:
        """
        Ask a health question to the ACP agent.
        
        Args:
            question: Health question to ask
            agent_name: Name of the agent to query (health_agent or health_router_agent)
            
        Returns:
            str: Response from the health agent
        """
        try:
            async with Client(base_url=self.base_url) as client:
                logger.info(f"Sending health question to {agent_name}: {question[:50]}...")
                
                # Create ACP-compliant message
                message = Message(
                    role="user",
                    parts=[MessagePart(
                        content=question,
                        content_type="text/plain"
                    )]
                )
                
                # Send request to the health agent
                run = await client.run_sync(
                    agent=agent_name,
                    input=[message]
                )
                
                # Extract response
                if run.output and run.output[0].parts:
                    response = run.output[0].parts[0].content
                    logger.info(f"Received response with {len(response)} characters")
                    return response
                else:
                    return "No response received from the health agent."
                    
        except Exception as e:
            logger.error(f"Error communicating with health agent: {e}")
            return f"Error: Unable to get response from health agent. {str(e)}"
    
    async def batch_health_questions(self, questions: List[str]) -> List[str]:
        """
        Ask multiple health questions in sequence.
        
        Args:
            questions: List of health questions
            
        Returns:
            List[str]: List of responses from the health agent
        """
        responses = []
        
        for i, question in enumerate(questions, 1):
            logger.info(f"Processing question {i}/{len(questions)}")
            response = await self.ask_health_question(question)
            responses.append(response)
            
            # Small delay between requests to be respectful
            await asyncio.sleep(1)
        
        return responses
    
    async def interactive_session(self):
        """
        Start an interactive session with the health agent.
        """
        print("🏥 Hospital Health Agent - Interactive Session")
        print("=" * 50)
        print("Ask health questions and get evidence-based information.")
        print("Type 'quit', 'exit', or 'bye' to end the session.")
        print("Type 'router:' before your question to use the router agent.")
        print("=" * 50)
        
        while True:
            try:
                # Get user input
                user_input = input("\n💬 Your health question: ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye', '']:
                    print("👋 Thank you for using the Hospital Health Agent. Stay healthy!")
                    break
                
                # Check for router agent usage
                agent_name = "health_agent"
                if user_input.startswith("router:"):
                    agent_name = "health_router_agent"
                    user_input = user_input[7:].strip()
                
                # Validate input
                if len(user_input) < 3:
                    print("⚠️ Please provide a more detailed health question.")
                    continue
                
                print(f"\n🔍 Searching for health information about: {user_input}")
                print("⏳ Please wait while I search reputable medical sources...")
                
                # Get response from health agent
                response = await self.ask_health_question(user_input, agent_name)
                
                # Display response
                print("\n" + "=" * 70)
                print("🩺 HEALTH INFORMATION RESPONSE:")
                print("=" * 70)
                print(response)
                print("=" * 70)
                
            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Thank you for using the Hospital Health Agent!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or contact technical support.")

async def main():
    """
    Main function demonstrating various health agent interactions.
    """
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Initialize client
    client = HealthAgentClient()
    
    # Check if server is running
    try:
        test_response = await client.ask_health_question("Test connection", "health_agent")
        if "Error:" in test_response:
            print("❌ Could not connect to health agent server.")
            print("Please ensure the server is running on http://localhost:8000")
            print("Run: python main.py")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        print("Please ensure the health agent server is running.")
        sys.exit(1)
    
    print("✅ Connected to Health Agent Server")
    
    # Run interactive session or example queries based on command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        await client.interactive_session()
    else:
        # Run example health queries
        print("\n🧪 Running example health queries...")
        
        example_questions = [
            "What are the symptoms of high blood pressure?"        ]
        
        for question in example_questions:
            print(f"\n📋 Example Question: {question}")
            print("-" * 50)
            
            response = await client.ask_health_question(question)
            print("🩺 Response:")
            print(response[:500] + "..." if len(response) > 500 else response)
            print("-" * 50)
            
            # Small delay between questions
            await asyncio.sleep(2)
        
        print("\n✨ Example queries completed!")
        print("Run with --interactive flag for interactive mode:")
        print("python client_example.py --interactive")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Client session ended.")
    except Exception as e:
        print(f"❌ Client error: {e}")
        sys.exit(1)
