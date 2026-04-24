from datetime import datetime
from config.llm import llm
from agent.domains.calendar.tools import add_event
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

tools = [add_event]

today = datetime.now().strftime("%Y-%m-%d")

prompt = ChatPromptTemplate.from_messages([
    ("system", f"You're Ben Carmel's personal assistant. Today is {today}."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

def run(message: str) -> str:
    result = executor.invoke({"input": message})
    return result["output"]
