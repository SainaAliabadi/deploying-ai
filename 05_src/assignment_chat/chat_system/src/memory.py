from typing import List
from langchain_core.messages import HumanMessage, AIMessage

class ConversationMemory:
    def __init__(self, max_messages: int = 12):
        self.messages: List = []
        self.max_messages = max_messages

    def add_user(self, text: str):
        self.messages.append(HumanMessage(content=text))
        self._trim()

    def add_ai(self, text: str):
        self.messages.append(AIMessage(content=text))
        self._trim()

    def get_history(self):
        return self.messages

    def clear(self):
        self.messages = []

    def _trim(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
