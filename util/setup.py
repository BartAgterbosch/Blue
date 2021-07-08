from os import path,mkdir
from util.res import *
from locale import getlocale


def get_hot_word():

    if not path.exists("config/assistant_name.blue"):
        hot_word = input("\nplease select a word/sentence to trigger your assistant\n-->")
        psuccess(f"Congratulations ! Your assistant is now called {hot_word} !")
        with open("config/assistant_name.blue","w") as f:
            f.write(hot_word)

        return hot_word
    else:
        with open("config/assistant_name.blue","r") as f:
            return f.read()


def check_files_integrity():
    
    if not path.exists("config/"):
        mkdir("config")
        hot_word = input("\nplease select a word/sentence to trigger your assistant\n-->")
        psuccess(f"Congratulations ! Your assistant is now called {hot_word} !")
        with open("config/assistant_name.blue","w") as f:
            f.write(hot_word)
    
    if not path.exists("skills_modules/"):
        mkdir("skills_modules")
    
    
    if not path.exists("config/custom_websites.blue"):
        open("config/custom_websites.blue","w")
    
    
    if not path.exists("config/custom_servers.blue"):
        open("config/custom_servers.blue","w")
    
    if not path.exists("config/irobot_cleaners.blue"):
        open("config/irobot_cleaners.blue","w")
    
    
    if not path.exists("config/custom_rss_feed.blue"):
        open("config/custom_rss_feed.blue","w")


    locale = getlocale()[0][2:]
    if locale not in get("https://raw.githubusercontent.com/ThaaoBlues/Blue/main/language-files/supported_languages.txt").text:
        locale = "fr"


    if not path.exists("config/skills.blue"):
        with open("config/skills.blue","w",encoding="utf-8") as f:
            f.write(get(f"https://raw.githubusercontent.com/ThaaoBlues/Blue/main/language-files/{locale}/skills.blue").text)
            f.close()

    if not path.exists("config/unnecessary.blue"):
        with open("config/unnecessary.blue","w",encoding="utf-8") as f:
            f.write(get(f"https://raw.githubusercontent.com/ThaaoBlues/Blue/main/language-files/{locale}/unnecessary.blue").text)
            f.close()
