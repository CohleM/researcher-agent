
from researcher.config import Config
from researcher.search.duckduckgo import Duckduckgo
from researcher.utils.functions import * 


class Researcher:
    def __init__(self, query ):
        self.query = query
        self.cfg = Config()
        self.agent = None
        self.role = None
        
    async def run(self):
        """
        Run the researcher
        """
        if self.cfg.search_engine == 'Duckduckgo':
            retriever = Duckduckgo()
            
        print(f'Running research for query: {self.query}')
        self.agent, self.role = await choose_agent(self.query, self.cfg.llm )
        print(f'Running {self.agent} ...')
        
        #query modification
        sub_queries = await get_sub_queries(self.query, self.role, self.cfg) + [self.query]
        
        return sub_queries
        

        
        
        
        
        
