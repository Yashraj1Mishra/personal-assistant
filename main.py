from jarvis.memory import load_memory, save_memory
from jarvis.router import get_commands, handle_flexible_command

def main():
    memory = load_memory()
    commands = get_commands()

    if "user_name" in memory:
        print("Welcome back,", memory["user_name"] + "! I am Jarvis.")
    else:
        name = input("Enter your name: ").strip()
        memory["user_name"] = name
        save_memory(memory)
        print("Hello", name + "! I am Jarvis.")

    while True:
        command = input("What do you want me to do? ").strip().lower()

        if command in commands:
            result = commands[command](memory)
            if result == "exit":
                break
        else:
            result = handle_flexible_command(command, memory)
            if result == "exit":
                break

if __name__ == "__main__":
    main()