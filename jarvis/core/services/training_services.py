from jarvis.core.memory import save_memory


class TrainingService:
    def __init__(self, memory: dict):
        self.memory = memory
        self.memory.setdefault("training_notes", [])
        self.memory.setdefault("aliases", {})

    def add_training_note(self, note: str):
        note = note.strip()
        if not note:
            return False, "Training note is empty."

        self.memory["training_notes"].append(note)
        save_memory(self.memory)
        return True, "Training note saved."

    def list_training_notes(self):
        return self.memory.get("training_notes", [])

    def add_alias(self, alias: str, actual_command: str):
        alias = alias.strip().lower()
        actual_command = actual_command.strip().lower()

        if not alias or not actual_command:
            return False, "Alias or command cannot be empty."

        self.memory["aliases"][alias] = actual_command
        save_memory(self.memory)
        return True, f"Alias '{alias}' saved for '{actual_command}'."

    def resolve_alias(self, command: str):
        return self.memory.get("aliases", {}).get(command.strip().lower(), command)

    def get_summary(self):
        notes = len(self.memory.get("training_notes", []))
        aliases = len(self.memory.get("aliases", {}))
        return f"Training notes: {notes} | Aliases: {aliases}"