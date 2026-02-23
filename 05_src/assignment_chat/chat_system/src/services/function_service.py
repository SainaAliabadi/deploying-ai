import statistics
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from chat_system.src.config import settings


# ----------------------------
# Define Tool Function
# ----------------------------

@tool
def statistical_calculator(numbers: List[float], operation: str) -> str:
    """
    Perform a statistical calculation on a list of numbers.
    Supported operations:
    - mean
    - sum
    - median
    - stdev
    """

    if not numbers:
        return "No numbers provided."

    if operation == "mean":
        result = statistics.mean(numbers)
    elif operation == "sum":
        result = sum(numbers)
    elif operation == "median":
        result = statistics.median(numbers)
    elif operation == "stdev":
        if len(numbers) < 2:
            return "Standard deviation requires at least two numbers."
        result = statistics.stdev(numbers)
    else:
        return "Unsupported operation."

    return f"The {operation} of {numbers} is {result:.4f}."


# ----------------------------
# Service Class
# ----------------------------

class FunctionCallingService:

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=0
        ).bind_tools([statistical_calculator])

    def handle(self, user_input: str):

        response = self.llm.invoke(user_input)

        # If tool was called
        if response.tool_calls:
            tool_call = response.tool_calls[0]
            tool_name = tool_call["name"]
            args = tool_call["args"]

            if tool_name == "statistical_calculator":
                return statistical_calculator.invoke(args)

        # If model did not call tool
        return "I can help compute statistics like mean, sum, median, or standard deviation. Try asking!"
