import os, time
import asyncio
import json
from dotenv import load_dotenv
from contextlib import AsyncExitStack
# Add references


# Clear the console
os.system('cls' if os.name=='nt' else 'clear')

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

async def connect_to_server(exit_stack: AsyncExitStack):
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )

    # Start the MCP server
    
    # Create an MCP client session

    # List available tools

    return session

async def chat_loop(session):

    # Connect to the agents client
    

    # List tools available on the server
    

    # Build a function for each tool
    

    # Create the agent
    

    # Enable auto function calling
    

    # Create a thread for the chat session
    

    while True:
        user_input = input("Enter a prompt for the inventory agent. Use 'quit' to exit.\nUSER: ").strip()
        if user_input.lower() == "quit":
            print("Exiting chat.")
            break

        # Invoke the prompt


        # Monitor the run status
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
            tool_outputs = []

            if run.status == "requires_action":

                tool_calls = run.required_action.submit_tool_outputs.tool_calls

                for tool_call in tool_calls:

                    # Retrieve the matching function tool
                    

                    # Append the output text
                    
                
                # Submit the tool call output
                
        # Check for failure
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

        # Display the response
        

    # Delete the agent when done
    print("Cleaning up agents:")
    agents_client.delete_agent(agent.id)
    print("Deleted inventory agent.")


async def main():
    import sys
    exit_stack = AsyncExitStack()
    try:
        session = await connect_to_server(exit_stack)
        await chat_loop(session)
    finally:
        await exit_stack.aclose()

if __name__ == "__main__":
    asyncio.run(main())
