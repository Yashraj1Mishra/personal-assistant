from jarvis.core.services.actions import (
    say_hello,
    tell_time,
    tell_name,
    how_are_you,
    introduce,
    favorite_color,
    open_google,
    open_youtube,
    open_github,
    open_live_news,
    remember_name,
    recall_name,
    remember_city,
    recall_city,
    remember_fact,
    recall_fact,
    search_google,
    search_youtube,
    show_help,
    exit_jarvis,
)
from jarvis.core.services.ai import ask_ai
from jarvis.core.services.training_services import TrainingService
from jarvis.core.services.utils import normalize_command, fuzzy_match_command


def get_commands():
    return {
        "hello": say_hello,
        "time": tell_time,
        "your name": tell_name,
        "name": tell_name,
        "how are you": how_are_you,
        "tell me about yourself": introduce,
        "favorite color": favorite_color,
        "open google": open_google,
        "open youtube": open_youtube,
        "open github": open_github,
        "open live news": open_live_news,
        "what is my name": recall_name,
        "what is my city": recall_city,
        "help": show_help,
        "bye": exit_jarvis,
        "exit": exit_jarvis,
    }


BUILT_IN_COMMANDS = set(get_commands().keys())


def handle_flexible_command(command, memory):
    trainer = TrainingService(memory)

    raw_command = command.strip()
    command = normalize_command(command)
    command = trainer.resolve_alias(command)

    commands = get_commands()

    if command in commands:
        return commands[command](memory)

    if command.startswith("remember that my name is "):
        value = raw_command[len("remember that my name is "):].strip()
        return remember_name(memory, value)

    if command.startswith("remember that my city is "):
        value = raw_command[len("remember that my city is "):].strip()
        return remember_city(memory, value)

    if command.startswith("alias "):
        raw = command.replace("alias ", "", 1).strip()
        if " as " in raw:
            actual, alias = raw.split(" as ", 1)
            ok, msg = trainer.add_alias(alias.strip(), actual.strip())
            return msg
        return "Use alias like: alias open google as google"

    if command.startswith("remember that "):
        return remember_fact(command, memory)

    if command.startswith("what is ") or command.startswith("who is "):
        return recall_fact(command, memory)

    if command.startswith("search google for "):
        return search_google(command, memory)

    if command.startswith("search youtube for "):
        return search_youtube(command, memory)

    if "live news" in command or "geopolitics" in command:
        return open_live_news(memory)

    fuzzy_match = fuzzy_match_command(command, BUILT_IN_COMMANDS)
    if fuzzy_match and fuzzy_match in commands:
        return f"Did you mean: {fuzzy_match}?\n{commands[fuzzy_match](memory)}"

    return ask_ai(command)