from datetime import datetime
from config.llm import llm
from config.settings import OWNER_NAME
from agent.domains.calendar.tools import add_event, find_events, update_event, delete_event
from langchain.agents import create_agent

tools = [add_event, find_events, update_event, delete_event]

today = datetime.now().strftime("%Y-%m-%d")

agent = create_agent(
    llm,
    tools,
    system_prompt=(
        f"You're {OWNER_NAME}'s personal assistant. Today is {today}. "
        "To update or delete a calendar event, always call find_events first "
        "to get its ID — never guess one. If find_events returns more than "
        "one plausible match, ask which one before acting. If the user "
        "clearly asked for an event to be deleted, delete it directly — do "
        "not ask for confirmation first."
    ),
)

def handle_message(message: str) -> str:
    result = agent.invoke({"messages": [{"role": "user", "content": message}]})
    content = result["messages"][-1].content

    if isinstance(content, str):
        return content

    # Gemini 3.x returns a list of content blocks; pull out the text parts.
    return "".join(block.get("text", "") for block in content if isinstance(block, dict))
