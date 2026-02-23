import requests
from chat_system.src.logging_utils import log_info, log_err
from langchain_openai import ChatOpenAI
from chat_system.src.config import settings


class CountryAPIService:

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=0.2
        )

    def fetch_country_data(self, country_name: str):
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()[0]
        except Exception as e:
            log_err(f"API error: {e}")
            return None

    def transform_response(self, raw_data: dict) -> str:
        """
        Transform structured API data into natural explanation.
        Not allowed to return raw JSON.
        """

        if not raw_data:
            return "I couldn't retrieve data for that country."

        structured_summary = {
            "name": raw_data.get("name", {}).get("common"),
            "capital": raw_data.get("capital", ["Unknown"])[0],
            "population": raw_data.get("population"),
            "region": raw_data.get("region"),
            "area_km2": raw_data.get("area"),
            "currencies": list(raw_data.get("currencies", {}).keys())
        }

        prompt = f"""
        Rewrite the following country data into a clear, engaging paragraph.

        Data:
        {structured_summary}
        """

        response = self.llm.invoke(prompt)
        return response.content

    def handle(self, user_input: str) -> str:
        """
        Extract country name heuristically from user input.
        (Simplified implementation first — can improve later)
        """

        words = user_input.strip().split()
        country_guess = words[-1]

        log_info(f"API Service triggered for country: {country_guess}")

        raw_data = self.fetch_country_data(country_guess)
        return self.transform_response(raw_data)
