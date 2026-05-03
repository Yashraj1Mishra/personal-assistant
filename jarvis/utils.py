from rapidfuzz import process, fuzz


ALIASES = {
    "hi": "hello",
    "hey": "hello",
    "hello jarvis": "hello",
    "what time is it": "time",
    "tell me the time": "time",
    "who are you": "your name",
    "what is your name": "your name",
    "open up google": "open google",
    "open up youtube": "open youtube",
    "open up github": "open github",
    "quit": "exit",
    "help me": "help",
    "what can you do": "help",
}


def normalize_command(command):
    return " ".join(command.lower().strip().split())


def resolve_alias(command):
    return ALIASES.get(command, command)


def fuzzy_match_command(command, command_choices, cutoff=75):
    match = process.extractOne(
        command,
        command_choices,
        scorer=fuzz.WRatio,
        score_cutoff=cutoff,
    )

    if match:
        return match[0]

    return None