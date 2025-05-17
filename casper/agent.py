class CasperAgent:
    """A minimal AI agent using the OpenAI API."""

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model

    def respond(self, prompt: str) -> str:
        """Generate a response for the given prompt.

        This method requires the ``openai`` package and the ``OPENAI_API_KEY``
        environment variable to be set. It returns the generated text or raises
        an exception if the API call fails.
        """
        try:
            import os
            import openai

            openai.api_key = os.environ["OPENAI_API_KEY"]
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            raise RuntimeError("Failed to generate response") from exc
