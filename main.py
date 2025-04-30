import asyncio
from typing import Annotated
from semantic_kernel import Kernel
from kernel_config import kernel_init
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents import ChatHistory
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread


kernel = kernel_init()

manager_agent  = ChatCompletionAgent(
    service = kernel.get_service(type=ChatCompletionClientBase),
    name = "Manager_Agent",
    instructions = (
        """
        You are the Manager Agent, a helpful and intelligent AI responsible for engaging with users and routing their requests to the most appropriate specialized AI agents.

        Your responsibilities:
        1. Greet the user and maintain a friendly, natural conversation.
        2. Actively listen to the user's query and analyze their intent.
        3. Based on the intent, select the correct specialized agent (e.g., JD_Agent, RP_Agent, CM_Agent, etc.).
        4. If the intent is unclear, ask one clarifying follow-up question.
        5. Once the intent is understood, respond with a brief explanation of which agent will handle the task and why.
        6. Forward the query to the appropriate agent and return the agent's response to the user.
        7. If no suitable agent is available, explain this politely and ask if the user would like to rephrase or get a general response.

        Your tone should be friendly, professional, and confident. Make the user feel supported throughout the interaction.
        """
    )
)

chat_history = ChatHistory()
thread = ChatHistoryAgentThread(chat_history=chat_history)

async def chat() -> bool:
    """
    Answer the user query and keep prompting user for input"
    Type 'exit' to exit.
    """

    try: 
        user_input = input("User:> ")
    except (KeyboardInterrupt,EOFError):
        print("\n\nExiting chat...")
        return False
    
    if user_input.lower().strip() == 'exit':
        print("\n\nExiting chat...")
        return False
    
    thread._chat_history.add_user_message(user_input)
    
    request_settings = OpenAIChatPromptExecutionSettings(function_choice_behavior=FunctionChoiceBehavior.Auto())
    

    response = await manager_agent.get_response(
        message = user_input,
        thread = thread,
        settings=request_settings
    )

    if response:
        print(f"Agent:> {response}")


    return True


async def main() -> None:
    
    print("Welcome to the chat bot!\n Type 'exit' to exit.\n ")
    chatting = True
    while chatting:
        chatting = await chat()

if __name__ == "__main__":
    asyncio.run(main())



    