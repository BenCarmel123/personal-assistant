from config.llm import llm
from langchain_core.messages import HumanMessage


def test_agent():
    print("Testing agent (OpenAI LLM)...")
    response = llm.invoke([HumanMessage(content="Say 'agent is working' and nothing else.")])
    print(f"Agent response: {response.content}")


if __name__ == "__main__":
    test_agent()
