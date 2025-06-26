import traceback

def log_error(e: Exception, context: str = "") -> str:
    """
    Logolja a hibát konzolra, opcionálisan egy kontextus szöveggel.
    Visszatér egy rövidített, felhasználónak szánt üzenettel.
    """
    print(f"\n[HIBA] {context}")
    print(traceback.format_exc())
    return f"{context} Hiba történt, részletek a naplóban."
