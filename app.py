from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from dotenv import load_dotenv
from typing import Dict, Optional
import chainlit as cl
from src.data.store import ChromaVectorStore
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents import Tool
from langchain import OpenAI
from langchain.chains import RetrievalQA
from src.data.user import AuthenticationDatabase
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor,AgentOutputParser
from langchain.memory import ConversationBufferMemory, ReadOnlySharedMemory
from langchain.schema import StrOutputParser


load_dotenv()

embed = OpenAIEmbeddings()
llm = OpenAI(model_name='text-davinci-003',streaming=True, temperature=0)

auth_db = AuthenticationDatabase()
chula_vectorstore =  ChromaVectorStore("chula",embed).get_store()
course_vectorstore =  ChromaVectorStore("course",embed).get_store()
memory = ConversationBufferMemory(memory_key="chat_history")

tools = [
  Tool(
    name="DocumentSearch",
    description="This tool can search and information from database which can be called DB or documents. Useful for when you need to answer questions",
    func=RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=chula_vectorstore.as_retriever()).run
  ),
]

class ChatRunnable(Runnable):
    def __init__(self,agent):
        self.agent = agent
    def invoke(self, input_data,a):
        print(input_data,a)
        # Pass the input data to the agent
        output = self.agent.invoke(input_data)
        return output


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Optional[cl.AppUser]:
  # Fetch the user matching username from your database
  # and compare the hashed password with the value stored in the database
  user = auth_db.login(username,password)
  print(user)
  if user:
    cl.user_session.set('user_id',user[0])
    return cl.AppUser(username=user[1], role=user[2], provider="credentials")
  else:
    return cl.AppUser(username="Anonymous",role="ANONYMOUS", provider="credentials")

@cl.oauth_callback
def oauth_callback(
  provider_id: str,
  token: str,
  raw_user_data: Dict[str, str],
  default_app_user: cl.AppUser,
) -> Optional[cl.AppUser]:
  return default_app_user


@cl.on_chat_start
async def on_chat_start():
    

    prefix = """Have a conversation with a human, answering the following questions as best you can. If you don't know please reply to inform user, 
    don't make up any answer. You have access to the following tools:"""
    suffix = """Begin!"

    {chat_history}
    Question: {input}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "chat_history", "agent_scratchpad"]
    )

    print(prompt)

    from langchain import OpenAI, LLMChain, PromptTemplate

    llm_chain = LLMChain(llm=llm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools[:auth_db.getRoleLevel(cl.user_session.get("user_id"))+1], verbose=True)
    agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools[:auth_db.getRoleLevel(cl.user_session.get("user_id"))+1],memory=memory)
    runnable = ChatRunnable(agent_chain)
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"input": message.content},
        config=RunnableConfig(callbacks=[cl.AsyncLangchainCallbackHandler()]),
    ):
        print(chunk)
        await msg.stream_token(chunk['output'])

    await msg.send()

