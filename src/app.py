from .data.store import PostgresVectorStore
from .data.memory import ChatMessageHistoryStore
from random import randbytes

class App:
  def __init__(self,pgvector_uri,redis_uri,pg_collection_name="embedding",redis_sessionid=None) -> None:
    self.v_db = PostgresVectorStore(pgvector_uri,pg_collection_name)
    if redis_sessionid == None: redis_sessionid = randbytes(8).hex()
    self.m_db = ChatMessageHistoryStore(redis_uri,redis_sessionid)
    self.__app = 