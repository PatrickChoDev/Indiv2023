from .data.store import PostgresVectorStore
from .data.memory import 


class App:
  def __init__(self,pgvector_uri,pg_collection_name="embedding") -> None:
    self.v_db = PostgresVectorStore(pgvector_uri,pg_collection_name)
    self.m_db = 