import os

from dotenv import load_dotenv

from openai import AsyncOpenAI

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion


def kernel_init():
    kernel = Kernel()

    load_dotenv()

    client = AsyncOpenAI(
        api_key=os.environ.get("OPEN_AI_API_KEY")
        #api_key=os.environ.get("GITHUB_TOKEN"), 
        #base_url="https://models.inference.ai.azure.com/",
    )

# Create an AI Service that will be used by the `ChatCompletionAgent`
    chat_completion_service = OpenAIChatCompletion(
        ai_model_id="gpt-4o-mini",
        async_client=client,
    )

    kernel.add_service(chat_completion_service)

    return kernel