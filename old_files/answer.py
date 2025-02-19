from chatterbot import ChatBot, filters
from chatterbot.trainers import ChatterBotCorpusTrainer
import wikipedia
import pyttsx3
import socket
import platform
from time import sleep
from googlesearch import search
import speedtest
from youtube_search import YoutubeSearch
from googletrans import  Translator
from random import randint
import pywhatkit
import multiprocessing
import webbrowser
from locale import getdefaultlocale
import subprocess
from gtts import gTTS
import feedparser
import playsound
import os
import pafy
class answer():
    def __init__(self):

        # Create a new chat bot named  Blue
        self.chatbot = ChatBot('Blue',
        filters=[filters.get_recent_repeated_responses],
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database='sqlite:///db.sqlite3')

        #get default system language
        self.lang = str(getdefaultlocale()[0])

        #init tts offline engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 110)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty("voice", voices[26].id)  

        #init translator to support others languages
        self.gtl = Translator(service_urls=['translate.googleapis.com'])

        #set wikipedia language      
        wikipedia.set_lang(str(getdefaultlocale()[0][0]+getdefaultlocale()[0][1]))

    def speak(self,text):
        try:
            tts = gTTS(text,lang=self.lang[0]+self.lang[1])
            sn = str(randint(1,100000))+".mp3"
            tts.save(sn)
            playsound.playsound(sn)
            os.remove(sn)
        except:
            self.engine.say(text)
            self.engine.runAndWait()
            
            
            
            
            


    #to send custom message to a server
    def interact_with_server(self,ip,port,message):
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.connect((ip,int(port)))
            s.send(bytes(message))
            s.close()
            return True, response
        except:
            return False


    #to interact with a irobot cleaner
    def interact_with_cleaner(self,ip,password):
        robot = Robot(ip,password)
        ms = robot.GetMission()
        if not "cleaning" in str(ms):
            robot.StartCleaning()
        else:
            robot.StopCleaning()
            robot.ReturnHome()

    #to basically call the module and display a website by his url
    def display_website(self,ws):
        subprocess.run(["python3","websearch.py",ws])


    def end_video(self,time):
        time = time.split(":")
        time = int(time[0])*60 + int(time[1])
        sleep(time)
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            print(line)
            if 'midori' in str(line).lower():
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)
        sleep(1)


    def check_commands_files(self,message):
        response = ""
        #checking custom files
        with open("irobot_cleaners.blue","r") as f:
            while(True):
                try:
                    if f.readline() in message:
                        password = f.readline()
                        ip = f.readline()
                        self.interact_with_cleaner(ip,password)
                        f.close()
                        break
                except:
                    f.close()
                    break
                
        with open("skills.blue","r") as f:
            for line in f:
                line = line.split(":")
                if (message in line[0]):
                    subprocess.run(["python3","/skills/"+line[1],message],shell=True)


        with open("custom_rss_feed.blue","r") as f:
            while(True):
                try:
                    l = f.readline().lower()
                    if message.lower() in l:
                        url = f.readline()
                        feed = feedparser.parse(url)
                        self.speak("Voici les deux derniers articles publiés :")
                        for entry in feed.entries[:2]:
                            self.speak(entry.title)
                            sleep(1)
                            self.speak("voici donc le contenu de l'article :")
                            sleep(0.5)
                            self.speak(entry.summary)

                        f.close()
                        return True, response
                        break

                    elif l.strip("\n").strip("\r") == "":
                        return False, response
                except:
                    print(e)
                    f.close()
                    return False,response
                    break

        with open("custom_servers.blue","r") as f:
            while(True):
                try:
                    l =  f.readline()
                    if message in l:
                        ip = f.readline()
                        port = f.readline()
                        command = f.readline().replace("[NL]","\n")
                        res = self.interact_with_server(ip,port,command)
                        if not res:
                            self.speak("Erreur lors de l'envoi du message au serveur")
                            response = ("Erreur lors de l'envoi du message au serveur")
                        else:
                            self.speak("Message bien envoyé au serveur")
                            response = ("Message bien envoyé au serveur")
                        f.close()
                        return True, response
                        break
                    elif l.strip("\n").strip("\r") == "":
                        return False, response
                except:
                    f.close()
                    return False,response
                    break


        with open("custom_websites.blue","r") as f:
            while(True):
                try:
                    if message in f.readline():
                        url = f.readline()
                        print(url)
                        self.display_website(url)
                        f.close()
                        return True, response
                        break
                    elif l.strip("\n").strip("\r") == "":
                        return False, response
                except:
                    f.close()
                    break
        

    def check_commands(self,message):
        response = ""
        
        checked, response = self.check_commands_files(message=message)
        if checked:
            return checked, response
        
        else:
            print(2)
            if "va sur" in message:

                #check if the domain name is complete
                if "." in message:
                    self.display_website("http://www."+message.strip("va sur").replace(' ','').replace('blue',"").lower())
                    response = (f"j'ai affiché {message.strip('va sur').replace(' ','').lower()} sur la base BLUE")
                    self.speak(f"j'ai affiché {message.strip('va sur').replace(' ','').lower()} sur la base BLUE")
                else:
                    #if not, get the first result on a google search
                    self.display_website(str(list(search(message.strip('va sur').replace(' ','').lower(),num=1,start=0,stop=1))[0]))
                    response = (f"j'ai affiché {message.strip('va sur').replace(' ','').lower()} sur la base BLUE")
                    self.speak(f"j'ai affiché {message.strip('va sur').replace(' ','').lower()} sur la base BLUE")
                return True, response



            elif "cherche" in message:
                response = GoogleSearch().search(message.replace("cherche","",1))
                result1 = response.results[0]
                self.speak(f"selon {result1.title}, {result1.getText()}")

                return True, response


            elif ("mets la" in message or "mets le clip" in message) and not message.startswith("mets de"):
                message = message.replace("mets la","",1).replace("mets le clip","",1).replace("la video de","",1).replace("la chanson de","",1).replace("la musique de","",1).replace("une video de","",1).replace("une chanson de","",1).replace("une musique de","",1)
                results = YoutubeSearch(message, max_results=10).to_dict()
                url = "https://youtube.com" + results[0]['url_suffix']
                vid = pafy.new(url)
                best = vid.getbest()
                self.speak(f"j'ai affiché {message.lower()} sur la base BLUE")
                self.display_website(best.url)
                print(f"j'ai affiché {message.lower()} sur la base BLUE")
                if results[0]['duration'] != 0:
                    proc = multiprocessing.Process(target=self.end_video,args=(results[i]['duration'],))  
                    proc.start()
                    proc.join()
                else:
                    proc = multiprocessing.Process(target=self.end_video,args=("20:0",))
                    proc.start()
                    proc.join()
                return True, response

            elif (message in "quelle heure est-il") or (message in "quelle heure il est") or (message in "donne moi l'heure s'il te plais"):
                date = datetime.datetime.now()
                response = (str(date.hour) + ':' + str(date.minute) +"et"+ str(date.second) + " secondes")
                self.speak("Il est " + response)
                return True, response

            elif message in "quel jour sommes-nous quel jour on est quel jour est-on donne moi le jour":
                d = datetime.date.today().strftime("%d %B %Y")
                response = (str(d))
                print(response)
                self.speak("Nous sommes le" + response)
                return True, response

            elif message in "adieu goodbye exit aurevoir au revoir tais toi shut-up au-revoir ta gueule ferme-la chut":
                response = ("bonne journée !")
                self.run_cmd("xset dpms force off")
                return True, response


            elif message.startswith("dis"):
                response = (message[3:])
                self.speak(message[3:])
                return True, response

            elif message in "ouvre youtube":
                self.display_website("https://www.youtube.com")
                response = ("j'ai ouvert youtube dans votre navigateur")
                return True, response

            elif message in "ouvre google":
                self.display_website("https://www.google.com")
                response = ("j'ai ouvert google dans votre navigateur")
                return True, response

            elif message in "ouvre drive ouvre le drive ouvre google drive ouvre mon drive":
                self.display_website("https://drive.google.com/drive/my-drive")            
                response = ("j'ai ouvert google drive dans votre navigateur")
                return True, response

            elif message in "ouvre classroom ouvre google classroom":
                self.display_website("https://classroom.google.com/u/0/h")            
                response = ("j'ai ouvert google classroom dans votre navigateur")
                return True, response

            elif message in "ouvre Gmail ouvre gmail ouvre mes mails ouvre mail ouvre ma boite mail ouvre ma boite gmail":
                self.display_website("https://mail.google.com/mail/u/0/#inbox")
                response = ("j'ai ouvert votre boite mail dans votre navigateur")
                return True, response

            elif message in "effectue  un speedtest effectue un test de vitesse fais un speedtest s'il te plaît fais un test de vitesse s'il te plaît c'est un speedtest s'il te plaît":
                response = ("Mise en route d'un speedtest..")
                s = speedtest.Speedtest()
                s.get_servers()
                s.get_best_server()
                s.download()
                s.upload()
                res = s.results.dict()
                d = (float(res["download"]) / 1024)/1000
                u = (float(res["upload"]) / 1024)/1000
                p = float(res["ping"])
                d = round(d,3)
                u = round(u,3)
                p = round(p,3)
                d = str(d)
                u = str(u)
                p = str(p)
                d = d.replace(".",",")
                u = u.replace(".",",")
                p = p.replace(".",",")
                response = ("Vous êtes actuellement à {} Mb/s download et {} Mb/s upload, avec un ping de {} millisecondes".format(d,u,p))
                return True, response

            elif message in "éteins toi éteins-toi extinction shutdown":
                try:
                    self.run_cmd("shutdown now")
                except:
                    response = ("Désolé, l'exécution de la commande a foirée")
                return True, response

            elif message in "redémarre toi redémarre-toi redémarrage reboot":
                try:
                    self.run_cmd("reboot")
                except:
                    response = ("Désolé, l'exécution de la commande a foirée")
                return True, response


            elif message in "joue de la musique" or "mets de la musique" in message or "top 50" in message or "top 100" in message:
                results = YoutubeSearch('top trending world music', max_results=10).to_dict()
                print("[+] Searching \"top trending world music\" on Youtube and getting you the best stream url... ")
                url = "https://youtube.com" + results[0]['url_suffix']
                vid = pafy.new(url)
                best = vid.getbest()
                self.display_website(best.url)
                return True, response

            elif message in "ifconfig ipconfig quelle est mon adresse IP locale mon IP locale":
                print(self.run_cmd("ifconfig"))
                self.speak("Voici votre configuration IP")
                response = ("Voici votre configuration IP")
                return True, response

            if ("ferme Google" in message) or ("ferme Internet" in message) or ("ferme la fenêtre" in message) or (message == "stop") or ("arrête" in message):
                #get default browser name
                sDefault_Browser= self.run_cmd("sensible-browser -V").split('\n')[0].split(' ')[0]
                #kill it by name
                self.run_cmd("killall " + sDefault_Browser)
                self.speak("j'ai fermé ton navigateur internet")
                response = "j'ai fermé ton navigateur internet"
                return True, response

            elif "ferme" in message:
                message = message.split(sep= " ")
                process_name = " ".join(message[1:])
                self.run_cmd(f"killall {process_name}")
                self.speak("j'ai fermé {}".format(process_name))
                response = ("j'ai fermé {}".format(process_name))

                return True, response

                

            elif message in "quelle est mon adresse IP routeur mon IP routeur":
                self.speak("voici votre IP routeur " + socket.gethostbyname(socket.gethostname()))
                response = ("Voici votre IP routeur" + socket.gethostbyname(socket.gethostname()))
                return True, response

            elif message in "quel temps fait-il dehors donnes moi la météo":
                self.display_website("https://www.google.com/search?q=meteo")         
                client.send("j'ai ouvert la météo dans votre navigateur")
                return True, response

            elif "wikipédia" in message:
                message = message.split()
                message = message[-1]
                self.display_website("https://fr.wikipedia.org/wiki/{}".format(message))            
                response = ("voici la page wikipédia de {}".format(message))
                return True, response

            elif "comment" in message and "faire" in message or "how to" in message:
                message = message.split()

                if len(message[-2]) <= 2:
                    message = message[-2] + message[-1]
                else:
                    message = message[-1]

                self.display_website("https://fr.wikipedia.org/wiki/{}".format(message))    
                response = ("voici la page wikipédia de {}".format(message))
                return True, response



            elif ("définition" in message) or ("qui est" in message) or ("qui était" in message) or ("c'est quoi" in message) or ("qu'est-ce qu" in message):
                message = message.split()
                message = message[-1]
                try:
                    print("[+] Searching on wikipedia...")
                    res = wikipedia.summary(message,sentences=1)
                    response = str(res)
                    print(response)
                    self.speak(res)
                    return True, response
                except:
                    response = "Auncun article sur wikipedia correspond à ce nom."
                    self.speak("Auncun article sur wikipedia correspond à ce nom.")
                    return True, response
                
                
                

            elif message in "fait un compte à rebours":
                #pas finis
                return True, response


            elif message == "test":
                self.display_website("www.google.com")
                print("in test")
            
            elif "informations" in message or "info" in message or "nouvelles" in message:
                self.speak("d'après le journal Le monde, ")

            else:
                return False, response
        


    def run_cmd(self,sCommand):
        """
            run command line
            :sCommand: String parameter containing the command to run
            :returns: A string containing the stdout
        """
        return subprocess.run([sCommand],shell=True,capture_output=True).stdout.decode("utf-8")


    def get_answer(self,message,client):
        print("[+] Translating...")
        message = self.gtl.translate(message,dest="fr")
        if not client == None:

            if message.lower() == "merci":
                self.speak("Avec plaisir !")

            checked, response = self.check_commands(message)
            response = self.gtl.translate(response,dest=self.lang[0]+self.lang[1])
            if not checked:
                response = str(self.chatbot.get_response(message))
                response = self.gtl.translate(response,dest=self.lang[0]+self.lang[1])
                print(f"BLUE:{response}")
                client.send(bytes(response,'utf-8'))
            else:
                print(f"BLUE:{response}")
                client.send(bytes(response,'utf-8'))

        else:
            print(3)
            checked, response = self.check_commands(message)
            response = self.gtl.translate(response,dest=self.lang[0]+self.lang[1])
            print(response)
            if not checked:
                print(message)
                response = str(self.chatbot.get_response(message))
                response = self.gtl.translate(response,dest=self.lang[0]+self.lang[1])
                print(f"BLUE:{response}")
                self.speak(response)
            else:
                
                print(response)

