from abc import ABC, abstractmethod
from langchain.vectorstores import VectorStore
from langchain.vectorstores.pgvector import PGVector



class BaseVectorStore(ABC):
  def __init__(self) -> None:
    self.__store = self.init_connection()

  @abstractmethod
  def init_connection(self) -> VectorStore:
    raise NotImplementedError

  def get_store(self):
    return self.__store
  
  def clean(self,ids):
    return self.__store.delete(ids)


class PostgresVectorStore(BaseVectorStore):
  def __init__(self,connection: str,collection_name: str,embedding_fn) -> None:
    self.__connection = connection
    self.__collection_name = collection_name
    self.__emb_fn = embedding_fn
    super().__init__()

  def init_connection(self):
    return PGVector(collection_name=self.__collection_name,connection_string=self.__connection,embedding_function=self.__emb_fn)