import webbrowser
from datetime import datetime
from jarvis.memory import save_memory

def say_hello(memory):
    print("Hello! Nice to talk to you.")

def tell_time(memory):
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    print("The current time is", current_time)

def tell_name(memory):
    print("My name is Jarvis.")

def how_are_you(memory):
    print("I am working perfectly.")

def introduce(memory):
    print("I am Jarvis, your beginner AI assistant.")

def favorite_color(memory):
    print("I like blue because it feels futuristic.")

def open_google(memory):
    webbrowser.open("https://www.google.com")
    print("Opening Google...")

def open_youtube(memory):
    webbrowser.open("https://www.youtube.com")
    print("Opening YouTube...")

def open_github(memory):
    webbrowser.open("https://github.com")
    print("Opening GitHub...")

def remember_name(memory):
    user_name = input("What should I remember as your name? ").strip()
    memory["user_name"] = user_name
    save_memory(memory)
    print("Okay, I will remember your name.")

def recall_name(memory):
    if "user_name" in memory:
        print("Your name is", memory["user_name"])
    else:
        print("I don't know your name yet.")

def remember_city(memory):
    city = input("Which city should I remember? ").strip()
    memory["city"] = city
    save_memory(memory)
    print("Okay, I will remember your city.")

def recall_city(memory):
    if "city" in memory:
        print("You live in", memory["city"])
    else:
        print("I don't know your city yet.")

def exit_jarvis(memory):
    print("Goodbye! Shutting down.")
    return "exit"

from urllib.parse import quote

def remember_fact(command, memory):
    prefix = "remember that "
    fact = command[len(prefix):]

    if " is " in fact:
        key, value = fact.split(" is ", 1)
        key = key.strip()
        value = value.strip()
        memory[key] = value
        save_memory(memory)
        print(f"Okay, I will remember that {key} is {value}.")
    else:
        print("Please use this format: remember that something is something")

def recall_fact(command, memory):
    prefixes = ["what is ", "who is "]

    for prefix in prefixes:
        if command.startswith(prefix):
            key = command[len(prefix):].strip()
            if key in memory:
                print(f"{key} is {memory[key]}")
            else:
                print(f"I don't know what {key} is yet.")
            return

    print("Please ask in a format like: what is my favorite food")

def search_google(command, memory):
    prefix = "search google for "
    topic = command[len(prefix):].strip()

    if topic:
        url = "https://www.google.com/search?q=" + quote(topic)
        webbrowser.open(url)
        print(f"Searching Google for {topic}...")
    else:
        print("Please tell me what to search for.")

def search_youtube(command, memory):
    prefix = "search youtube for "
    topic = command[len(prefix):].strip()

    if topic:
        url = "https://www.youtube.com/results?search_query=" + quote(topic)
        webbrowser.open(url)
        print(f"Searching YouTube for {topic}...")
    else:
        print("Please tell me what to search for.")