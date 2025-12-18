from typing import Any, List

from langchain.agents import create_agent


class AgentService:
    def __init__(self, tools: List[Any]):
        self.model = "openai:gpt-4o-mini"
        self.tools = tools
        self.agent = create_agent(self.model, self.tools)

    async def ask_agent(self, payload: str) -> str:
        if not self.agent:
            raise RuntimeError("Agent not initialized. Call start() first.")

        try:
            result = await self.agent.ainvoke({"messages": payload})

            messages = result["messages"]

            for message in messages:
                message.pretty_print()

            return messages[-1].content
        except Exception as e:
            print(e)
            raise RuntimeError("Request to model provider failed")
