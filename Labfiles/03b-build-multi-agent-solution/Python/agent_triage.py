import os
from dotenv import load_dotenv

# Add references
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ConnectedAgentTool, MessageRole, ListSortOrder, ToolSet, FunctionTool


# Clear the console
os.system('cls' if os.name=='nt' else 'clear')

# Load environment variables from .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")


# Connect to the agents client
agents_client = AgentsClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
)

with agents_client:


    # Create an agent to prioritize support tickets
    # priority_agent_instructions
    # Assess how urgent a ticket is based on its description.
    #
    # Respond with one of the following levels:
    # - High: User-facing or blocking issues
    # - Medium: Time-sensitive but not breaking anything
    # - Low: Cosmetic or non-urgent tasks
    #
    # Only output the urgency level and a very brief explanation.
    priority_agent_name="priority_agent"
    priority_agent_instructions="""
    根據工單描述，評估其緊急程度。

    使用以下等級回應：
    - 高：直接影響用戶或直接無法使用系統的問題
    - 中：時間緊迫，但不會造成系統中斷的問題
    - 低：外觀問題或非緊急任務

    只輸出緊急程度和簡短說明。    
"""
    priority_agent = agents_client.create_agent(
        model=model_deployment,
        name=priority_agent_name,
        instructions=priority_agent_instructions
    )

    # Create an agent to assign tickets to the appropriate team
    # team_agent_instructions
    # Decide which team should own each ticket.
    #
    # Choose from the following teams:
    # - Frontend
    # - Backend
    # - Infrastructure
    # - Marketing
    #
    # Base your answer on the content of the ticket. Respond with the team name and a very brief explanation.
    team_agent_name="team_agent"
    team_agent_instructions="""
    決定哪個團隊應該要負責這張工單。

    由以下團隊中選擇：
    - 前端團隊
    - 後端團隊
    - 基礎設施(Infrastructure)團隊
    - 行銷團隊

    根據工單內容回答，只輸出團隊名稱和簡短說明。
"""

    team_agent = agents_client.create_agent(
        model=model_deployment,
        name=team_agent_name,
        instructions=team_agent_instructions
    )

    # Create an agent to estimate effort for a support ticket
    # effort_agent_instructions
    # Estimate how much work each ticket will require.
    #
    # Use the following scale:
    # - Small: Can be completed in a day
    # - Medium: 2-3 days of work
    # - Large: Multi-day or cross-team effort
    #
    # Base your estimate on the complexity implied by the ticket. Respond with the effort level and a brief justification.
    effort_agent_name="effort_agent"
    effort_agent_instructions="""
    估算每張工單所需的工作量。

    使用以下標準：
    - 小：一天內可以完成
    - 中：2-3天的工作
    - 大：多天或跨團隊的工作

    根據工單所暗示的複雜性來進行你的估算。回應時請提供工作量等級和簡要說明。
    """

    effort_agent = agents_client.create_agent(
        model=model_deployment,
        name=effort_agent_name,
        instructions=effort_agent_instructions
    )

    # Create connected agent tools for the support agents
    priority_agent_tool= ConnectedAgentTool(
        id=priority_agent.id,
        name=priority_agent_name,
        description="取得工單的優先級"
    )
    
    team_agent_tool = ConnectedAgentTool(
        id=team_agent.id,
        name=team_agent_name,
        description="決定負責工單的團隊"
    )

    effort_agent_tool = ConnectedAgentTool(
        id=effort_agent.id,
        name=effort_agent_name,
        description="估算工單的工作量等級"
    )



    # Create an agent to triage support ticket processing by using connected agents
    # triage_agent_instructions
    # Triage the given ticket. Use the connected tools to determine the ticket's priority, 
    # which team it should be assigned to, and how much effort it may take.
    triage_agent_name="triage_agent"
    triage_agent_instructions="""
    分流給定的工單。
    使用連接的工具來決定工單的優先級、應分配給哪個團隊，以及可能需要多少工作量。
"""
    triage_agent = agents_client.create_agent(
        model=model_deployment,
        name=triage_agent_name,
        instructions=triage_agent_instructions,
        tools=[
            priority_agent_tool.definitions[0],
            team_agent_tool.definitions[0],
            effort_agent_tool.definitions[0]
        ]
    )

    # Use the agents to triage a support issue
    print("Createing agent thread.")
    thread=agents_client.threads.create()

    # Create the ticket prompt
    prompt = input("\nWhat's the support problem you need to resolve?:")

    # Send the prompt to the agent
    message = agents_client.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content=prompt
    )

    # Run the thread using the primary agent
    print("\nProcessing agent thread. Please wait.")
    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=triage_agent.id
    )

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch and display messages
    messages = agents_client.messages.list(
        thread_id=thread.id,
        order=ListSortOrder.ASCENDING
    )

    for message in messages:
        if message.text_messages:
            last_msg = message.text_messages[-1]
            print(f"{message.role}:\n{last_msg.text.value}\n")


    # Clean up
    print("Cleaning up agents:")
    agents_client.delete_agent(triage_agent.id)
    print("Deleted triage agent.")
    agents_client.delete_agent(priority_agent.id)
    print("Deleted priority agent.")
    agents_client.delete_agent(team_agent.id)
    print("Deleted team agent.")
    agents_client.delete_agent(effort_agent.id)
    print("Deleted effort agent.")
