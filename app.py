from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.llms.openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain import hub
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
from langchain.agents import AgentExecutor
from langchain.agents import Tool
from langchain.chains import RetrievalQA
import chainlit as cl


text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=100)

websites = [
    "https://www.cp.eng.chula.ac.th/about/faculty",
    "https://www.cp.eng.chula.ac.th/future/bachelor"
]


# for website in websites:
loader = WebBaseLoader(websites)
loader.requests_kwargs  = {"verify":False}
data = loader.load()
texts = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

db = FAISS.from_documents(texts, embeddings)

@cl.on_chat_start
def start():
    llm = OpenAI(temperature=0)
    llm_with_stop = llm.bind(stop=["\nObservation"])
    retriever = db.as_retriever()
    tools = [
      Tool(
        name="DocumentSearch",
        description="This tool can search and information. Useful for when you need to answer questions",
        func=RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever).run
      ),
    ]
    prompt = hub.pull("hwchase17/react-chat")

    prompt = prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm_with_stop
        | ReActSingleInputOutputParser()
    )
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)
    return cl.user_session.set("agent",agent_executor)


@cl.on_message
async def main(message):
    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)
    res = await agent.acall({"input":message.content}, callbacks=[cl.AsyncLangchainCallbackHandler()])
    print(res)
    await cl.Message(content=res['output']).send()
