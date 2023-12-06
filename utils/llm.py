from openai import OpenAI
import logging
from langsmith.run_helpers import traceable


#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

async def create_chat_completion(messages,cfg, stream=False ):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        #     api_key= oai_key,
    )

    if not stream:

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=cfg.llm,
            temperature=cfg.temperature
        )

        print(f'Token Usage: {chat_completion.usage}')

        return chat_completion.choices[0].message.content


