redis_url = "redis://localhost:6379/0"
session_id = "my-session"
chat_history = RedisChatMessageHistory(url=redis_url, session_id=session_id)

# Retrieve a specific memory chat using userId and chatId
user_id = "user123"
chat_id = "chat456"
specific_chat = chat_history.get_chat(user_id=user_id, chat_id=chat_id)

# Process the specific chat as needed
print(specific_chat)