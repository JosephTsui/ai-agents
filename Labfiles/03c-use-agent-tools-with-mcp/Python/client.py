import os
from dotenv import load_dotenv

# Add references


# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

# Connect to the agents client


# MCP server configuration
mcp_server_url = "https://learn.microsoft.com/api/mcp"
mcp_server_label = "mslearn"

# Initialize agent MCP tool


# Create agent with MCP tool and process agent run
with agents_client:

    # Create a new agent
    

    # Log info
    print(f"Created agent, ID: {agent.id}")
    print(f"MCP Server: {mcp_tool.server_label} at {mcp_tool.server_url}")

    # Create thread for communication
    

    # Create a message on the thread
    

    # Set approval mode


    # Create and process agent run in thread with MCP tools
    
    
    # Check run status
    print(f"Run completed with status: {run.status}")
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Display run steps and tool calls
    run_steps = agents_client.run_steps.list(thread_id=thread.id, run_id=run.id)
    for step in run_steps:
        print(f"Step {step['id']} status: {step['status']}")

        # Check if there are tool calls in the step details
        step_details = step.get("step_details", {})
        tool_calls = step_details.get("tool_calls", [])

        if tool_calls:
            # Display the MCP tool call details
            print("  MCP Tool calls:")
            for call in tool_calls:
                print(f"    Tool Call ID: {call.get('id')}")
                print(f"    Type: {call.get('type')}")
                print(f"    Type: {call.get('name')}")

        print()  # add an extra newline between steps

    # Fetch and log all messages
    messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    print("\nConversation:")
    print("-" * 50)
    for msg in messages:
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role.upper()}: {last_text.text.value}")
            print("-" * 50)

    # Clean-up and delete the agent once the run is finished.
    agents_client.delete_agent(agent.id)
    print("Deleted agent")