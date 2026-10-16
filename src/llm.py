"""GROOT-01 local language model interface."""

from llama_cpp import Llama



class LocalLLM:
    """Interface for GROOT's local language model."""

    SYSTEM_PROMPT = ""

    def __init__(
        self,
        model_path: str,
        context_size: int,
        threads: int,
        temperature: float = 0.7,
        max_tokens: int = 256,
    ):
        self.model_path = model_path
        self.context_size = context_size
        self.threads = threads
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = None
        self.history = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT,
            }
        ]

    def load(self):
        """Load the local GGUF model."""
        self.model = Llama(
            model_path=self.model_path,
            n_ctx=self.context_size,
            n_threads=self.threads,
            verbose=False,
        )

    def generate(self, prompt: str) -> str:
        """Generate a response while maintaining conversation history."""
        if self.model is None:
            raise RuntimeError("Model is not loaded.")

        self.history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        response = self.model.create_chat_completion(
            messages=self.history,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        answer = response["choices"][0]["message"]["content"].strip()

        self.history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        return answer

    def clear_history(self):
        """Clear conversation history while preserving system instructions."""
        self.history = [
            {
                "role": "system",
                "content": self.SYSTEM_PROMPT,
            }
        ]

    def unload(self):
        """Unload the local model and clear conversation history."""
        self.history = []
        self.model = None
