from langchain.memory.chat_message_histories import RedisChatMessageHistory


class ChatMessageHistoryStore:
  def __init__(self,redis_url,session_id="Default") -> None:
    self.__memstore = RedisChatMessageHistory(url=redis_url,session_id=session_id)

  def get_chat(self,chat_id):
    return self.__memstore.
  



  
# Retrieve a specific memory chat using userId and chatId
user_id = "user123"
chat_id = "chat456"
specific_chat = chat_history.get_chat(user_id=user_id, chat_id=chat_id)

# Process the specific chat as needed
print(specific_chat)