import json
from colorama import Fore, Style

from .llm import *
from researcher.prompts.prompts import *



async def get_sub_queries(query, role, cfg):
    
    messages = [
        {"role": "system" , "content" : role },
        {"role": "user" , "content" : generate_search_queries_prompt(query) }
    ]
    
    response = await create_chat_completion(messages, temperature=cfg.temperature, model=cfg.llm)
    response = json.loads(response)
    
    return response



async def choose_agent(query, model):
    
    try:
        
        response = await create_chat_completion(
            messages = [
                    {"role": "system", "content": f"{auto_agent_instructions()}"},
                    {"role": "user", "content": f"task: {query}"}], 
            model=model
        )
        
        agent = json.loads(response)
        return agent['server'], agent['agent_role_prompt']
    
    except Exception as e:

        print(f"{Fore.RED} Error in choose_agent: {e}{Style.RESET_ALL}")
        return { "server": "Default Agent",
                "agent_role_prompt": "You are an AI critical thinker research assistant. Your sole purpose is to write well written, critically acclaimed, objective and structured reports on given text."}


async def generate_report(context, question, agent_role, cfg):
    
    # try and except block remaining
    response = await create_chat_completion(
            messages = [
                    {"role": "system", "content": f"{agent_role}"},
                    {"role": "user", "content": f"task: {generate_report_prompt(question, context)}"}], 
#             model=cfg.llm
              model= cfg.llm
    )
    
    return response
