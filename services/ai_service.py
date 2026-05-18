from anthropic import Anthropic

class Ai_service:
    def __init__(self)-> None:
        self.client = Anthropic()
    def generate_examples(self, word) -> str:
        prompt = "Generate 3 example sentences using the word " + word + ". Return only the 3 sentences, one per line, no headers, no numbering, no markdown formatting"
        print(prompt)
        result = self.client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        text = result.content[0].text
        sentences = [s.strip() for s in text.strip().split("\n") if s.strip()]
        #sentences.pop(0)
        return sentences
ai_service = Ai_service()