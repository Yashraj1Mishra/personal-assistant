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
    exit_jarvis
)

BUILT_IN_COMMANDS = {
    "hello",
    "time",
    "your name",
    "name",
    "how are you",
    "tell me about yourself",
    "favorite color",
    "open google",
    "open youtube",
    "open github",
    "remember my name",
    "what is my name",
    "remember my city",
    "what is my city",
    "bye",
    "exit"
}

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
        "bye": exit_jarvis,
        "exit": exit_jarvis
    }

def handle_flexible_command(command, memory):
    if command.startswith("remember that "):
        remember_fact(command, memory)
    elif command.startswith("what is ") or command.startswith("who is "):
        recall_fact(command, memory)
    elif command.startswith("search google for "):
        search_google(command, memory)
    elif command.startswith("search youtube for "):
        search_youtube(command, memory)
    elif "hello" in command:
        say_hello(memory)
    elif "time" in command:
        tell_time(memory)
    elif "your name" in command or "who are you" in command:
        tell_name(memory)
    elif "how are you" in command:
        how_are_you(memory)
    elif "about yourself" in command:
        introduce(memory)
    elif "favorite color" in command:
        favorite_color(memory)
    elif "open" in command and "google" in command:
        open_google(memory)
    elif "open" in command and "youtube" in command:
        open_youtube(memory)
    elif "open" in command and "github" in command:
        open_github(memory)
    elif "remember my name" in command:
        remember_name(memory)
    elif "what is my name" in command or command == "my name":
        recall_name(memory)
    elif "remember my city" in command:
        remember_city(memory)
    elif "what is my city" in command or command == "my city":
        recall_city(memory)
    elif "bye" in command or "exit" in command:
        return exit_jarvis(memory)
    else:
        print("Sorry, I don't understand that command.")