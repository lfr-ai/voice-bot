from ekko.application.services.chat_service import ChatService


class DummyGateway:
    def chat(self, *, system_prompt, user_prompt, model, temperature, max_completion_tokens):
        return f"echo:{user_prompt}"


def test_chat_service_basic():
    svc = ChatService(gateway=DummyGateway())
    resp = svc.chat(system_prompt="sys", user_prompt="hello", model="m", temperature=0.1, max_completion_tokens=10)
    assert resp == "echo:hello"
