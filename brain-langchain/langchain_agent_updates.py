"""# Tool Priority
An example of giving a tool more/less priority than other ones.
"""

import os
os.environ["OPENAI_API_KEY"] = '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'
os.environ["SERPAPI_API_KEY"] = "168e6559f58d9fc00b4a924f52788e2cdebb8f9c6cb78c942753e2b9af845329"

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain import LLMMathChain, SerpAPIWrapper
search = SerpAPIWrapper()

tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ),
    Tool(
        name="Music Search",
        func=lambda x: "'This is the custom function.", #Mock Function
        description="A Music search engine. Use this more than the normal search if the question is about Music, like 'who is the singer of yesterday?' or 'what is the most popular song in 2022?'",
    )
]

agent = initialize_agent(tools, OpenAI(temperature=0), agent="zero-shot-react-description", verbose=True)

agent.run("what is the most famous song of christmas")
