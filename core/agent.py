from researcher.config import Config
from researcher.search.duckduckgo import Duckduckgo
from researcher.utils.functions import * 
from researcher.retriever.langchain_hybrid_retriever import HybridRetriever
from researcher.scraping.scrape import Scraper
from researcher.context.chunking import Chunking


class Researcher:
    def __init__(self, query ):
        self.query = query
        self.cfg = Config()
        self.agent = None
        self.role = None
        self.visited_urls = set()
        self.context = []
        
    async def run(self):
        """
        Run the researcher
        """
        if self.cfg.search_engine == 'Duckduckgo':
            retriever = Duckduckgo()
            
        print(f'📘 Starting research for query: {self.query}')
        self.agent, self.role = await choose_agent(self.query, self.cfg.llm )
        print(f'Running {self.agent} ...')
        
        #query modification
        sub_queries = await get_sub_queries(self.query, self.role, self.cfg) + [self.query]
        
        for each_query in sub_queries:
            
            print(f'🔍 Searching web with query: {each_query}')
            content = await self.get_content_using_query(each_query)
            context = await self.get_similar_context(each_query, content)
            self.context.append(context)
            
        
        return self.context    

    async def get_content_using_query(self,query):

        search_engine = Duckduckgo(query = query)
        search_urls = search_engine.search(max_results = self.cfg.max_search_results_per_query)

        search_urls = [url.get('href') for url in search_urls]

        new_search_urls = await self.get_unique_urls(search_urls) #filter out the same urls 

        content_scraper = Scraper(new_search_urls)
        content = content_scraper.run()

        return content
    
    async def get_chunks(self, content):
        
        chunks = []
        chunking = Chunking(self.cfg.chunk_size ,self.cfg.chunk_overlap)

        for each_content in content:
            chunks += chunking.run(content=each_content['raw_content'], metadatas= {'url': each_content['url'] })
            
        return chunks
    
    async def get_unique_urls(self, urls):
        
        new_urls = []
        for url in urls:
            if url not in self.visited_urls:
                
                print(f'✅ Adding url {url} to our research')
                
                new_urls.append(url)
                self.visited_urls.add(url)
                
        return new_urls
                
    
    async def get_similar_context(self, query, content):
        
        #chunk where?
        chunks = await self.get_chunks(content)
        hybrid_retriever = HybridRetriever(chunks ,max_results = self.cfg.max_chunks_per_query)
        similar_context = hybrid_retriever.get_context(query)

        return similar_context       
