from typing import Any, List

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage

TASK_SYSTEM_PROMPT = """
You are a Task Management Agent that interacts exclusively via MCP tools.

Rules:
- Use MCP tools for all task operations.
- Do not fabricate data.
- Do not call tools with missing or invalid arguments.
- Do not ask follow-up questions.
- If no filters are provided for listing tasks, call list_tasks with an empty object.

You are responsible for selecting the correct tool and arguments.
Be concise, correct, and deterministic.
"""


class AgentService:
    def __init__(self, tools: List[Any]):
        self.model = "openai:gpt-4o-mini"
        self.tools = tools
        self.agent = create_agent(self.model, self.tools)

    async def ask_agent(self, payload: str) -> str:
        if not self.agent:
            raise RuntimeError("Agent not initialized.")

        try:
            result = await self.agent.ainvoke(
                {"messages": [SystemMessage(content=TASK_SYSTEM_PROMPT), HumanMessage(content=payload), ]})

            messages = result["messages"]

            for message in messages:
                message.pretty_print()

            return messages[-1].content
        except Exception as e:
            print(e)
            raise RuntimeError("Request to model provider failed")
