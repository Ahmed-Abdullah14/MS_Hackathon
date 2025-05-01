import asyncio
import os
import chainlit as cl
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents import ChatHistory
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from kernel_config import kernel_init
from jd_matcher_tools import JDMatcherTools


kernel = kernel_init()
kernel.add_plugin(JDMatcherTools(), plugin_name="JDMatcherTools")

jd_agent = ChatCompletionAgent(
    service = kernel.get_service(type=ChatCompletionClientBase),
    name = "Job_Description_Agent",
    instructions= (
        """
        You are Agent X1M – a professional Job Description Assistant. Your goal is to generate or improve job descriptions based on user input.

        Begin by asking the following required information, if missing:
        1. Company name
        2. Job title
        3. Company description and values
        4. Must-have skills or qualifications

        You may also ask for optional information to enhance the JD, such as:
        - Department or team
        - Location (remote/hybrid/onsite)
        - Job level (entry/mid/senior)
        - Tools or technologies used
        - Salary range
        - Preferred qualifications
        - Security/clearance requirements

        Once you have the required information, generate a clear, professional, and inclusive job description. Use the following format:

        ### Overview
        [Write a compelling paragraph about the company's mission and culture. Then describe the department and the role. Include what the team is working on and how the candidate will contribute.]

        ### Responsibilities
        - [List 4-6 core duties using action verbs]
        - [Make sure responsibilities show ownership and impact]

        ### Qualifications

        **Required**
        - [4-6 must-have skills, degrees, or experience]

        **Preferred**
        - [Any nice-to-have skills or traits]

        ### Culture and Values
        [End with 2-3 sentences highlighting the company's commitment to diversity, inclusion, innovation, and continuous learning.]

        Guidelines:
        - Use inclusive, bias-free language
        - Write clearly at a 10th-12th grade reading level
        - Use relevant keywords for applicant tracking systems (ATS)
        - Reflect the company's tone and professionalism
        """
    )
)

jd_matcher_agent = ChatCompletionAgent(
    service = kernel.get_service(type=ChatCompletionClientBase),
    name = "Job_Description_Matcher_Agent",
    instructions= (
        """
        You match resumes to job descriptions by:
        1. Asking the user if they would like to match candidates from the `data/resume` directory or provide their own resumes.
        2. If they choose the directory option, process resumes from the `data/resume` folder and extract the text.
        3. If they choose to provide their own resumes, accept resume uploads from the user and extract the text.
        4. Compare the job description with each resume text and return the best-fit candidate based on textual relevance.
        """
    ),
    plugins=[JDMatcherTools()]
)


manager_agent  = ChatCompletionAgent(
    service = kernel.get_service(type=ChatCompletionClientBase),
    name = "Manager_Agent",
    instructions = (
        """
        You are the Manager Agent, a helpful and intelligent AI responsible for engaging with users and routing their requests to the most appropriate specialized AI agents.

        Your responsibilities:
        1. Greet the user and maintain a friendly, natural conversation.
        2. If the user says "hi", "hello", or anything similar without a clear task, greet them warmly AND briefly explain what you can do, such as:
            - Write job descriptions
            - Match resumes to job descriptions
        3. If the user provides a specific request, analyze their intent.
        4. Based on the intent, select the correct specialized agent (e.g., JD_Agent, JD_Matcher_Agent, etc.).
        5. If the intent is unclear, ask one clarifying follow-up question.
        6. Once the intent is understood, respond with a brief explanation of which agent will handle the task and why.
        7. Forward the query to the appropriate agent and return the agent's response to the user.
        8. If no suitable agent is available, explain this politely and ask if the user would like to rephrase or get a general response.

        Your tone should be friendly, professional, and confident. Make the user feel supported throughout the interaction.
        """
    ),
    plugins=[jd_agent, jd_matcher_agent],
)

chat_history = ChatHistory()
thread = ChatHistoryAgentThread(chat_history=chat_history)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content="""
        👋 Welcome to **RecruitEdge AI** 🤖 — Your AI Hiring Assistant!
        """).send()

    sk_filter = cl.SemanticKernelFilter(kernel=kernel)
    cl.user_session.set("agent", manager_agent)
    cl.user_session.set("thread", thread)

@cl.on_message
async def on_message(message: cl.Message):

    cl.user_session.get("agent", manager_agent)
    cl.user_session.get("thread", thread)
    
    user_input = message.content

    thread._chat_history.add_user_message(user_input)
    
    request_settings = OpenAIChatPromptExecutionSettings(function_choice_behavior=FunctionChoiceBehavior.Auto())
    
    answer = cl.Message(content="")
    response = await manager_agent.get_response(
        message = user_input,
        thread = thread,
        settings=request_settings
    )

    if response.content:
        await answer.stream_token(str(response.content))
    

    await answer.send()


if __name__ == "__main__":
    os.system("chainlit run main.py -w")
    