from langchain.vectorstores import VectorStore
class DocumentSearchAgent:
    def __init__(self, vector_store: VectorStore):
        self.__vector_store = vector_store
        self.__metadata = {}

    def search(self,query):
        # Perform the search query
        # if metadata_filter_threshold > 0.8:
        #     # Apply metadata filter based on the metadata_filter_threshold
        #     return self.__vector_store.search(query, 'similarity', filter=self.__metadata)
        # else:
            return self.__vector_store.search(query,'similarity')

    def set_metadata_filter(self,metadata):
        self.__metadata = metadata