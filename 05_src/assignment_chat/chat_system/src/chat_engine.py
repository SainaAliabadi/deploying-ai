from langchain_openai import ChatOpenAI
from chat_system.src.config import settings
from chat_system.src.prompting import build_prompt
from chat_system.src.guardrails import check_guardrails
from chat_system.src.memory import ConversationMemory
from chat_system.src.logging_utils import log_info

from chat_system.src.services.api_service import CountryAPIService
from chat_system.src.services.semantic_service import SemanticSearchService
from chat_system.src.services.function_service import FunctionCallingService


class ChatEngine:

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
        )

        self.prompt = build_prompt()
        self.memory = ConversationMemory()

        self.api_service = CountryAPIService()
        self.semantic_service = SemanticSearchService()
        self.function_service = FunctionCallingService()

    def route(self, user_input: str):

        lower = user_input.lower()

        semantic_keywords = [
            "machine learning",
            "deep learning",
            "embeddings",
            "vector database",
            "llm",
            "reinforcement learning",
            "natural language processing"
        ]

        function_keywords = [
            "mean",
            "sum",
            "median",
            "standard deviation",
            "stdev"
        ]

        if any(keyword in lower for keyword in function_keywords):
            log_info("Routing → Function Service")
            return "function"

        if any(keyword in lower for keyword in semantic_keywords):
            log_info("Routing → Semantic Service")
            return "semantic"

        if "tell me about" in lower or "country" in lower:
            log_info("Routing → API Service")
            return "api"

        return "default"

    def chat(self, user_input: str) -> str:

        allowed, message = check_guardrails(user_input)
        if not allowed:
            return message

        route = self.route(user_input)

        if route == "api":
            return self.api_service.handle(user_input)

        if route == "semantic":
            return self.semantic_service.handle(user_input)

        if route == "function":
            return self.function_service.handle(user_input)

        self.memory.add_user(user_input)

        chain = self.prompt | self.llm

        response = chain.invoke({
            "input": user_input,
            "history": self.memory.get_history()
        })

        output_text = response.content

        self.memory.add_ai(output_text)

        return output_text
