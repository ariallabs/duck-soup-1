import os
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = "168e6559f58d9fc00b4a924f52788e2cdebb8f9c6cb78c942753e2b9af845329"

# find  a way to store the mamory in a file
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain import LLMMathChain

search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=OpenAI(temperature=0.9))
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math",
        return_direct=True
    )
]
memory = ConversationBufferMemory(memory_key="chat_history")

llm=OpenAI(temperature=0.9)
agent_chain = initialize_agent(tools, llm, agent="conversational-react-description", verbose=True, memory=memory)

while True:
    user_input = input('Human: ')
    if user_input == "quit":
        break
    agent_chain.run(input=user_input)
