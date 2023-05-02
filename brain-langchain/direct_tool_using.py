import os
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = "168e6559f58d9fc00b4a924f52788e2cdebb8f9c6cb78c942753e2b9af845329"


from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper
search = SerpAPIWrapper()

llm_math = LLMMathChain(llm=OpenAI(temperature=0))


tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or things you don't know about"
    ),
    Tool(
        name = "Math",
        func=llm_math.run,
        description="useful for when you need to answer questions about math"
    )
]

agent = initialize_agent(tools, OpenAI(temperature=0), agent="zero-shot-react-description", verbose=True)


while True:
    response = agent.run(input("Enter a question: "))

    print(response)
    if response == "exit":
        break