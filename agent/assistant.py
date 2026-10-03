from datetime import datetime
from config.llm import llm
from config.settings import OWNER_NAME
from agent.domains.calendar.tools import add_event
from langchain.agents import create_agent

tools = [add_event]

today = datetime.now().strftime("%Y-%m-%d")

agent = create_agent(
    llm,
    tools,
    system_prompt=f"You're {OWNER_NAME}'s personal assistant. Today is {today}.",
)

def handle_message(message: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": message}]})
    content = result["messages"][-1].content

    if isinstance(content, str):
        return content

    # Gemini 3.x returns a list of content blocks; pull out the text parts.
    return "".join(block.get("text", "") for block in content if isinstance(block, dict))
