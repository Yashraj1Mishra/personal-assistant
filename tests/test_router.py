import pytest

from jarvis.core.agents.router import handle_flexible_command


def test_hello_command():
    memory = {}
    result = handle_flexible_command("hello", memory)
    assert result == "Hello! Nice to talk to you."


def test_name_memory_save_and_recall():
    memory = {}

    save_result = handle_flexible_command("remember that my name is Yash", memory)
    recall_result = handle_flexible_command("what is my name", memory)

    assert save_result == "Okay, I will remember your name."
    assert memory["user_name"] == "Yash"
    assert recall_result == "Your name is Yash."


def test_city_memory_save_and_recall():
    memory = {}

    save_result = handle_flexible_command("remember that my city is Pune", memory)
    recall_result = handle_flexible_command("what is my city", memory)

    assert save_result == "Okay, I will remember your city."
    assert memory["city"] == "Pune"
    assert recall_result == "You live in Pune."


def test_generic_fact_save_and_recall():
    memory = {}

    save_result = handle_flexible_command("remember that sky is blue", memory)
    recall_result = handle_flexible_command("what is sky", memory)

    assert save_result == "Okay, I will remember that sky is blue."
    assert memory["sky"] == "blue"
    assert recall_result == "sky is blue"


def test_open_google(monkeypatch):
    opened_urls = []

    def fake_open(url):
        opened_urls.append(url)

    monkeypatch.setattr("jarvis.core.services.actions.webbrowser.open_new_tab", fake_open)

    memory = {}
    result = handle_flexible_command("open google", memory)

    assert result == "Opening Google..."
    assert opened_urls == ["https://www.google.com"]


def test_search_google(monkeypatch):
    opened_urls = []

    def fake_open(url):
        opened_urls.append(url)

    monkeypatch.setattr("jarvis.core.services.actions.webbrowser.open_new_tab", fake_open)

    memory = {}
    result = handle_flexible_command("search google for python tutorials", memory)

    assert result == "Searching Google for python tutorials..."
    assert opened_urls
    assert "https://www.google.com/search?q=python%20tutorials" in opened_urls[0]


def test_search_youtube(monkeypatch):
    opened_urls = []

    def fake_open(url):
        opened_urls.append(url)

    monkeypatch.setattr("jarvis.core.services.actions.webbrowser.open_new_tab", fake_open)

    memory = {}
    result = handle_flexible_command("search youtube for pyqt6", memory)

    assert result == "Searching YouTube for pyqt6..."
    assert opened_urls
    assert "https://www.youtube.com/results?search_query=pyqt6" in opened_urls[0]


def test_unknown_command_falls_back_to_ai(monkeypatch):
    def fake_ask_ai(command):
        return f"AI response for: {command}"

    monkeypatch.setattr("jarvis.core.agents.router.ask_ai", fake_ask_ai)

    memory = {}
    result = handle_flexible_command("tell me a story", memory)

    assert result == "AI response for: tell me a story"


def test_exit_command():
    memory = {}
    result = handle_flexible_command("exit", memory)
    assert result == "exit"