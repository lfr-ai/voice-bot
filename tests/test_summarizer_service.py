from voice.application.services.summarizer_service import SummarizerService


class DummyGateway:
    def chat(self, *, system_prompt, user_prompt, model, temperature, max_completion_tokens):
        return "summary:" + user_prompt[:20]


def test_summarizer_basic():
    svc = SummarizerService(gateway=DummyGateway())
    chunks = ["This is a first chunk.", "Second chunk with more details."]
    s = svc.summarize(chunks)
    assert s.startswith("summary:")
