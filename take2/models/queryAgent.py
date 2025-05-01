import requests

SYSTEM_PROMPT = (
    "You are an AI assistant that helps verify the truthfulness of news articles. "
    "Given a paragraph of news content, generate a short and precise web search query that someone could use "
    "to fact-check the main claim in the text.\n\n"
    "Respond only with the search query, no extra text or formatting.\n"
)

class QueryAgent:
    def __init__(self, model="llama3"):
        self.model = model

    def generate_query(self, paragraph: str):
        prompt = f"{SYSTEM_PROMPT}\n\nParagraph:\n\"\"\"\n{paragraph}\n\"\"\"\n"
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            reply = response.json()["response"].strip()
            return reply
        except Exception as e:
            return f"[QueryAgent Error: {str(e)}]"
