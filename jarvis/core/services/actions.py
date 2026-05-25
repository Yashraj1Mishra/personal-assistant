import webbrowser
from datetime import datetime
from urllib.parse import quote

from jarvis.core.memory import save_memory


def say_hello(memory):
    return "Hello! Nice to talk to you."


def tell_time(memory):
    current_time = datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}."


def tell_name(memory):
    return "My name is Jarvis."


def how_are_you(memory):
    return "I am working perfectly."


def introduce(memory):
    return "I am Jarvis, your beginner AI assistant."


def favorite_color(memory):
    return "I like blue because it feels futuristic."


def open_google(memory):
    webbrowser.open_new_tab("https://www.google.com")
    return "Opening Google..."


def open_youtube(memory):
    webbrowser.open_new_tab("https://www.youtube.com")
    return "Opening YouTube..."


def open_github(memory):
    webbrowser.open_new_tab("https://github.com")
    return "Opening GitHub..."


def open_live_news(memory):
    url = "https://news.google.com/search?q=geopolitics"
    webbrowser.open_new_tab(url)
    return "Opening live geopolitics news..."


def remember_name(memory, value=None):
    if value:
        memory["user_name"] = value.strip()
        save_memory(memory)
        return "Okay, I will remember your name."
    return "Please use: remember that my name is YOUR_NAME"


def recall_name(memory):
    if "user_name" in memory and str(memory["user_name"]).strip():
        return f"Your name is {memory['user_name']}."
    return "I don't know your name yet."


def remember_city(memory, value=None):
    if value:
        memory["city"] = value.strip()
        save_memory(memory)
        return "Okay, I will remember your city."
    return "Please use: remember that my city is YOUR_CITY"


def recall_city(memory):
    if "city" in memory and str(memory["city"]).strip():
        return f"You live in {memory['city']}."
    return "I don't know your city yet."


def exit_jarvis(memory):
    return "exit"


def remember_fact(command, memory):
    prefix = "remember that "
    fact = command[len(prefix):].strip()

    if " is " in fact:
        key, value = fact.split(" is ", 1)
        key = key.strip()
        value = value.strip()

        if key and value:
            memory[key] = value
            save_memory(memory)
            return f"Okay, I will remember that {key} is {value}."
        return "Please use this format: remember that something is something"

    return "Please use this format: remember that something is something"


def recall_fact(command, memory):
    prefixes = ["what is ", "who is "]

    for prefix in prefixes:
        if command.startswith(prefix):
            key = command[len(prefix):].strip()
            if key in memory:
                return f"{key} is {memory[key]}"
            return f"I don't know what {key} is yet."

    return "Please ask in a format like: what is my favorite food"


def search_google(command, memory):
    prefix = "search google for "
    topic = command[len(prefix):].strip()

    if topic:
        url = "https://www.google.com/search?q=" + quote(topic)
        webbrowser.open_new_tab(url)
        return f"Searching Google for {topic}..."

    return "Please tell me what to search for."


def search_youtube(command, memory):
    prefix = "search youtube for "
    topic = command[len(prefix):].strip()

    if topic:
        url = "https://www.youtube.com/results?search_query=" + quote(topic)
        webbrowser.open_new_tab(url)
        return f"Searching YouTube for {topic}..."

    return "Please tell me what to search for."


def show_help(memory):
    return (
        "Here are some things I can do:\n"
        "- hello\n"
        "- time\n"
        "- your name\n"
        "- how are you\n"
        "- tell me about yourself\n"
        "- favorite color\n"
        "- open google\n"
        "- open youtube\n"
        "- open github\n"
        "- open live news\n"
        "- help\n\n"
        "Memory commands:\n"
        "- remember that my name is Aman\n"
        "- what is my name\n"
        "- remember that my city is Gaya\n"
        "- what is my city\n"
        "- remember that sky is blue\n"
        "- what is sky\n"
        "- who is sky\n\n"
        "Search commands:\n"
        "- search google for Python tutorials\n"
        "- search youtube for Python projects\n\n"
        "AI commands:\n"
        "- ask normal questions like: write a poem\n"
        "- ask normal questions like: what is python\n\n"
        "Exit commands:\n"
        "- bye\n"
        "- exit"
    )