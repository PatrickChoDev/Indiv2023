from langchain.vectorstores import VectorStore
class DocumentSearchAgent:
    def __init__(self, vector_store: VectorStore):
        self.__vector_store = vector_store
        self.__metadata = {}

    def search(self,query, metadata_filter_enabled=False, metadata_filter_threshold=0.5):
        # Perform the search query
        if metadata_filter_enabled:
            # Apply metadata filter based on the metadata_filter_threshold
            return self.__vector_store.search(query, filter=self.__metadata)
        else:
            return self.__vector_store.search(query)

    def set_metadata_filter(self,metadata):
        self.__metadata = metadata