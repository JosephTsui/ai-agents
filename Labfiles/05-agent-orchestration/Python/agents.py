# Add references
import asyncio
from typing import cast
from agent_framework import ChatMessage, Role, SequentialBuilder, WorkflowOutputEvent
from agent_framework.azure import AzureAIAgentClient
from azure.identity import AzureCliCredential

async def main():
    # Agent instructions
    # Summarize the customer's feedback in one short sentence. Keep it neutral and concise.
    # Example output:
    # App crashes during photo upload.
    # User praises dark mode feature.
    summarizer_instructions="""
    用一句簡短的話總結客戶的回饋，保持中立和簡潔。
    輸出範例：
    上傳照片時應用程式崩潰。
    用戶讚揚深色模式功能。
    """


    # Classify the feedback as one of the following: Positive, Negative, or Feature request.
    classifier_instructions="""
    將回饋區分成以下三類之一：正面、負面或功能請求
    """


    # Based on the summary and classification, suggest the next action in one short sentence.
    # Example output:
    # Escalate as a high-priority bug for the mobile team.
    # Log as positive feedback to share with design and marketing.
    # Log as enhancement request for product backlog.
    action_instructions="""
    根據摘要和分類，用一句話建議下一步行動。
    輸出範例：
    升級為 mobile 團隊的高優先層級的 bug。
    分享給設計團隊和行銷團隊的正面回饋紀錄。
    作為產品待辦清單的功能請求紀錄。
    """

    # Create the chat client
    credential = AzureCliCredential()
    async with (
        AzureAIAgentClient(
            async_credential=credential) as chat_client
        ):

        # Create agents
        summarizer = chat_client.create_agent(
            instructions=summarizer_instructions,
            name="summarizer"
        )

        classifier = chat_client.create_agent(
            instructions=classifier_instructions,
            name="classifier"
        )

        action = chat_client.create_agent(
            instructions=action_instructions,
            name="action"
        )

        # Initialize the current feedback
        feedback = """
        我每天都會用儀表板來監控各項指標，整體來說效果不錯。
        但是，當我深夜工作時，明亮的螢幕確實會刺眼。
        如果能加入暗黑模式選項，體驗會更加舒適。
        """

        # Build sequential orchestration
        workflow = SequentialBuilder().participants(
            [summarizer, classifier, action]
        ).build()
    
        # Run and collect outputs
        outputs: list[list[ChatMessage]] = []
        async for event in workflow.run_stream(f"Customer feedback: {feedback}"):
            if isinstance(event, WorkflowOutputEvent):
                outputs.append(cast(list[ChatMessage], event.data))
                
        # Display outputs
        if outputs:
            for i, msg in enumerate(outputs[-1], start=1):
                name = msg.author_name or ("assistant" if msg.role == Role.ASSISTANT else "user")
                print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
    
    
if __name__ == "__main__":
    asyncio.run(main())