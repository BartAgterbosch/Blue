from util.res import *
import importlib
from locale import getlocale
from gtts import gTTS
from random import randint
from os import remove
import playsound
from difflib import SequenceMatcher
from util.translator import translate
from multiprocessing import Process
from functools import partial
from webbrowser import open as open_url

def starred_sentences_ratio(line,voice_command,sentence):
    """
a star [*] can be placed in sentence to mark where random words can appears.
I split the setences by * and return the average ratio of matching,
the voice command is considered as matching.
    """

    split = sentence.split("*")

    voice_command = voice_command.lower()

    ratio_l = []

    for line_part in split:
        if not line_part in voice_command :
            r = SequenceMatcher(None, voice_command, line_part).ratio()
            if r < 0.80:
                return {"module" : line.split(":")[0], "ratio" : r, "match" : False}
        else:
            r = 1.0

        ratio_l.append(r)

    av_r = 0.0

    av_r += sum(ratio_l)/len(ratio_l)

    return {"module" : line.split(":")[0], "ratio" : av_r, "match" : True}
        

def full_sentence_ratio(line,voice_command, sentence):
    """
    return a matching ratio between a trigger sentence from a skill and the voice_command
    
    """
    return {"module" : line.split(":")[0], "ratio": SequenceMatcher(None, voice_command, sentence).ratio()}



def check_user_custom_commands(voice_command):

    #custom websites part
    custom_websites = get_custom_websites_voice_commands()
    for website in custom_websites:
        if voice_command == website['voice_command'] :
            Process(target = open_url, args=(website['url'],) ).start()
            return True

    #coming soon : custom request to server part


    return False


def init_skill_call(module, ratio,final_sentences,voice_command):
    # correct module is now defined, display ratio in a human-friendly way 
    # and call the skill
    ratio = round(ratio,4)
    print(f"module : {module} | confidence : {ratio*100}%") 
    Process(target=call_skill,args=(module,voice_command,final_sentences.split("/"),)).start()


def check_skills(voice_command):

    pinfo("logging voice command...")
    with open("config/logs.txt","w") as f:
        f.write(voice_command)
        f.close()

    #check if a skill is waiting user to speak or not, if not we can begin the process
    if not is_waiting_user_command():
        pinfo("checking user custom commands...")

        if not check_user_custom_commands(voice_command):

            pinfo("checking skills...")
            with open("config/skills.blue","r",encoding="utf-8") as f:
                lines = f.read().splitlines()

                pinfo("trying starred sentences ratio...")
                for line in lines:

                    sentences = line.split(":")[1]
                    for sentence in sentences.split("/"):

                        result = starred_sentences_ratio(line,voice_command,sentence)
                        if result['match']:
                            init_skill_call(result['module'], result['ratio'],sentences,voice_command)
                            return True


                ratio = 0
                module = None
                final_sentences = ""
                pinfo("trying full sentences ratio...")
                for line in lines:

                    sentences = line.split(":")[1]
                    for sentence in sentences.split("/"):
                        final_sentences = sentences
                        #starred lines ratio didn't work, using full ratio to get the higher match
                        result = full_sentence_ratio(line,voice_command,sentence.strip("*"))
                        if result['ratio'] > ratio:
                            module = result['module']

                if ratio > 0.2:
                    #calling module on higher ratio obtained
                    init_skill_call(module, ratio,final_sentences,voice_command)
                else:
                    module = "open_website"
                    init_skill_call(module, ratio,"",voice_command)

                return True

    else:
        return True


def speak(text):
    try:
        tts = gTTS(text,lang=get_locale())
        sn = str(randint(1,100000))+".mp3"
        tts.save(sn)
        playsound.playsound(sn)
        remove(sn)
    except Exception as e:
        print(e)
        pass


def call_skill(module,voice_command,sentences):

    
    try:
        skill = importlib.import_module(f"skills_modules.{module}")
    except Exception as e:
        perror(f"Error while importing skill module : {e}")
        return

    ret, response = skill.initialize(voice_command,sentences)

    try:
        locale = get_locale()
        if locale != 'fr':
            response = translate(response,'fr',dest=locale)

    except Exception as e:
        perror(f"Error while translating Blue response to your language : {e}")
        return

    print(response)

    try:
        if response != "":
            speak(response)
    except Exception as e:
        perror(f"Error while trying to speak : {e}")
        return
    