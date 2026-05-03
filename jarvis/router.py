from jarvis.actions import (
    say_hello,
    tell_time,
    tell_name,
    how_are_you,
    introduce,
    favorite_color,
    open_google,
    open_youtube,
    open_github,
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
from jarvis.ai import ask_ai
from jarvis.utils import normalize_command, resolve_alias, fuzzy_match_command


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
        "remember my name": remember_name,
        "what is my name": recall_name,
        "remember my city": remember_city,
        "what is my city": recall_city,
        "help": show_help,
        "bye": exit_jarvis,
        "exit": exit_jarvis,
    }


BUILT_IN_COMMANDS = set(get_commands().keys())


def handle_flexible_command(command, memory):
    command = normalize_command(command)
    command = resolve_alias(command)

    commands = get_commands()

    if command in commands:
        return commands[command](memory)

    fuzzy_match = fuzzy_match_command(command, BUILT_IN_COMMANDS)
    if fuzzy_match and fuzzy_match in commands:
        print(f"Did you mean: {fuzzy_match}?")
        return commands[fuzzy_match](memory)

    if command.startswith("remember that "):
        return remember_fact(command, memory)

    if command.startswith("what is ") or command.startswith("who is "):
        return recall_fact(command, memory)

    if command.startswith("search google for "):
        return search_google(command, memory)

    if command.startswith("search youtube for "):
        return search_youtube(command, memory)

    answer = ask_ai(command)
    print(answer)