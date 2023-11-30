class Config:
    def __init__(self):

        self.retriever = "Weaviate"
        self.search_engine = "duckduckgo"
        self.llm = "gpt-3.5-turbo"
        self.max_search_query = 3
        self.max_search_results_per_query = 5
        self.total_words = 1000
        self.temperature = 0
        
        

