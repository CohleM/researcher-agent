from openai import OpenAI



async def create_chat_completion(messages, temperature=0, stream=False, model='gpt-3.5-turbo'):
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        #     api_key= oai_key,
    )

    if not stream:

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=temperature
        )

        return chat_completion.choices[0].message.content


