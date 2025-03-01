# my_tavily_model.py
import requests
import re

class ChatTavily:
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        self.base_url = "https://api.tavily.com"  # Base URL from Tavily

    def extract_sql(self, text: str) -> str:
        """
        Extracts a complete SQL query from text.
        Looks for a pattern that starts with SELECT, contains a FROM clause,
        and optionally stops at a semicolon.
        """
        # This regex looks for "SELECT" followed by any characters (non-greedy) up to a semicolon
        # or until the end of the string, ensuring there is a FROM clause somewhere.
        print(f"TEXT:{text}")
        pattern = re.compile(r"(SELECT\s+.*?FROM\s+.*?;)", re.IGNORECASE | re.DOTALL)
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
        # Fallback: if no semicolon, try to capture from SELECT to end.
        pattern = re.compile(r"(SELECT\s+.*)", re.IGNORECASE | re.DOTALL)
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
        return ""

    def generate(self, prompt: str, max_tokens: int = 150) -> str:
        url = f"{self.base_url}/search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "query": prompt
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            json_response = response.json()
            # Uncomment the next line if you need to debug the raw response:
            #print("Raw Response:", json_response)
            # Try to get the direct answer first.
            generated_text = json_response.get("answer")
            if not generated_text:
                # If "answer" is empty, look through the results.
                results = json_response.get("results", [])
                for res in results:
                    content = res.get("content", "")
                    if "SELECT" in content.upper():
                        generated_text = content
                        break
            # Now extract a clean SQL query from the generated_text.
            sql_query = self.extract_sql(generated_text) if generated_text else ""
            return sql_query
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return ""
