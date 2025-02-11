# -*- coding: utf-8 -*-
from keyring import get_password
from util.res import get_assistant_name, is_service_registered, is_user_account_for_service, get_username_for_service, register_service
import simplenote

def initialize(voice_command,sentences):

    #remove trigger words to get only the valuable data
    for sentence in sentences:
        for part in sentence.split("*"):
            voice_command = voice_command.replace(part,"",1)


    #check if the external service "simplenote" has been registered
    if not is_service_registered("simplenote"):
        register_service("simplenote")


    #check if user has registered an simplenote account    
    if is_user_account_for_service("simplenote"):
       #an account has been registered, getting his username
        ac_username = get_username_for_service("simplenote")

    # no account available for this service, returning some sentences to guide him
    else:
        return False, "Vous n'avez pas encore enregistré votre compte simplenote.com"

    #getting password from secure keyring
    ac_password = get_password("simplenote",ac_username)
    #connecting to simplenote
    sn = simplenote.Simplenote(ac_username,ac_password )
    #trying to get assistant default note page
    found = False
    for note in sn.get_note_list():
        if note == 0:
            break
        if get_assistant_name() in note[0]['tags']:
            note_key = note[0]['key']
            content = note[0]['content']
            sn.update_note({'key':note_key,'tags':[get_assistant_name()],'content':content+"\n"+voice_command}) 
            found = True
            break

    if not found:
        # note page of your assistant doesn't exists, creating one
        sn.add_note({'tags':[get_assistant_name()],'content':voice_command})


    return True, f"J'ai ajouté {voice_command} à vos notes."