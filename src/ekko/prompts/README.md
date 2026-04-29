# Prompts directory

This folder contains canonical prompt templates and supporting guidance for
the voice-bot project. Use these prompts as the golden standard for any LLM
interactions, especially for RAG (retrieval-augmented generation) and
transcript summarization.

Files:

- `prompt.txt` — primary, versioned prompt template and instructions.

Guidance:

- Keep prompts simple and declarative. Place long policies in separate
  markdown files and reference them by name.
- Do not commit secrets. Use placeholders and `.env` for runtime secrets.

Usage examples:

```py
from pathlib import Path

prompt = Path("src/voice/prompts/prompt.txt").read_text()
filled = prompt.replace("{context}", doc_text).replace("{user_request}", user_text)
# send `filled` to LLM
```
