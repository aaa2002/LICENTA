import requests

SYSTEM_PROMPT = (
    "You are a helpful assistant that evaluates text for coherence. "
    "When given a paragraph, your task is to determine if the ideas flow logically, are well-connected, and make sense overall.\n\n"
    # This was added for context. otherwise it was marking single sentences as incoherent. TODO: mention in documentation
    "It is not important if the text is short or long, but rather if it has good sentence structure. If there is a singular sentence/question, that can be marked as coherent if it makes sense.\n\n"
    "Respond in json format:\n"
    "{\n"
    "   label: 'real' or 'fake',\n"
    "   confidence: <float>,\n"
    "   explanation: <string>\n"
    "}\n"
)

class CoherenceAgent:
    def __init__(self, model="llama3"):
        self.model = model

    def analyze(self, paragraph: str, web_text: str = None):
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

            import json
            result = json.loads(reply)
            return result
        except Exception as e:
            return {"error": str(e), "raw_response": reply if 'reply' in locals() else "No response"}
