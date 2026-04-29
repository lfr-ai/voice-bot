# LangChain Chat Adapter

Location: `src/voice/infrastructure/llm/chat_adapter.py`

This adapter provides a provider-agnostic interface to LangChain chat models.

Usage (example):

```python
from voice.infrastructure.llm.chat_adapter import ChatModelAdapter
from voice.config.settings import get_settings

settings = get_settings()
adapter = ChatModelAdapter.from_settings(settings)
resp = adapter.chat(
    system_prompt="You are a helpful assistant.",
    user_prompt="Hello, what is RAG?",
    deployment_name=settings.llm_default_deployment or "gpt-4",
)
```

Supports both synchronous (`chat`) and asynchronous (`async_chat`) methods.

Adapter details

The LangChain-based adapter implementation lives at:

```text
src/voice/infrastructure/llm/langchain_adapter.py
```

The adapter implements a provider-agnostic interface (see `ChatPort` in
`src/voice/core/protocols.py`) and follows the composition pattern used in the
repository.

Design notes

- Provider selection is driven from `Settings` (configured via environment
  variables).
- The adapter lazily initializes model clients and caches them per deployment.
- OpenAI and Azure OpenAI are supported. API keys are expected in environment
  variables; Key Vault is not used by default.

How to use

1. Configure API credentials and model/deployment settings via environment
   variables or CI secrets.
2. Create the adapter from settings and call `chat`/`async_chat` as required.

```python
from voice.config.settings import get_settings
from voice.infrastructure.llm.langchain_adapter import LangChainChatAdapter

settings = get_settings()
adapter = LangChainChatAdapter.from_settings(settings)
resp = await adapter.async_chat(
    system_prompt="system",
    user_prompt="hello",
    deployment_name=settings.llm_model,
    max_completion_tokens=256,
    temperature=0.0,
)
```
