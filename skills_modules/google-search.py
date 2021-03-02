from platform import system
from webbrowser import open as display_website

def initialize(voice_command,sentences):
    for sentence in sentences:
        voice_command = voice_command.replace(sentence,"",1)

    display_website(f"https://www.google.com/search?q={voice_command}")


    response = "J'ai ouvert les résultats de ta recherche dans ton navigateur"

    return True, response