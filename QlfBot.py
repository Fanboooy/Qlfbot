import socket

### Options TU NE TOUCHE PAS A CA
SERVER = "irc.twitch.tv"  # server
PORT = 6667  # port
### Options Tu peut toucher a ca
PASS = "oauth:hdlndotbg9ul01juh6e24sx912jkgp"  #https://twitchapps.com/tmi/
BOT = "QlfBot"  #Nom du bot [SEULEMENT EN MINUSCULE]
CHANNEL = "merizium"  #Nom de la chaine twitch [SEULEMENT EN MINUSCULE]
OWNER = "merizium"  #Nom de l'admin de la chaine [SEULEMENT EN MINUSCULE]

### Tu ne touche rien ici eventuellement tu pourra en ajouter
def resetjoueur(joueur) :
    if joueur != []:
        joueur = []
    return joueur

def createbanword ():
    mon_fichier = open("liste.txt", "r")
    contenue = mon_fichier.read()
    j = contenue.replace('\n',';')
    j = j + ";"
    mon_fichier.close()
    banword = []
    while j != "":
        mot = j.split(";",1)[0]
        banword.append(mot)
        dltmot = mot + ";"
        j = j.replace(dltmot,"")
    return banword
	
def resettickets(tickets):
    if tickets != 1 :
        tickets = 1
    return tickets
#10
def resetuserlist(userlist):
    if userlist != []:
        userlist = []
    return userlist

def resetnumero(numero):
    if numero != []:
        numero = []
    return numero
	
def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send((messageTemp + "\r\n").encode())

def getUser(line):
    #user = line.split(">", 1)[0]
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user
def getMessage(line):
	#user = line.split(">", 1)[1]
    global message
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message
def joinchat():
    readbuffer_join = "".encode()
    Loading = True
    while Loading:
        readbuffer_join = s.recv(1024)
        readbuffer_join = readbuffer_join.decode()
        temp = readbuffer_join.split("\n")
        readbuffer_join = readbuffer_join.encode()
        readbuffer_join = temp.pop()
        for line in temp:
            Loading = loadingCompleted(line)
    sendMessage(s, "Salut a tous les pixels, c'est le bot de MeriGameuse")
    print("Bot has joined " + CHANNEL + " Channel!")

def loadingCompleted(line):
    if ("End of /NAMES list" in line):
        return False
    else:
        return True
### Connection a l'IRC encore une fois tu ne touche a rien là
s_prep = socket.socket()
s_prep.connect((SERVER, PORT))
s_prep.send(("PASS " + PASS + "\r\n").encode())
s_prep.send(("NICK " + BOT + "\r\n").encode())
s_prep.send(("JOIN #" + CHANNEL + "\r\n").encode())
s = s_prep
joinchat()
readbuffer = ""

def Console(line):
    if "PRIVMSG" in line:
        return False
    else:
        return True

joueur = list()
joueur = []
numero = list()
numero = []
userlist = list()
userlist = []
tickets = 1
lstbanwords = createbanword()
trusted = ["Merizium","fanboooy_"]
while True: #La boucle lecture commence ici
        try:
            readbuffer = s.recv(1024)
            readbuffer = readbuffer.decode()
            temp = readbuffer.split("\n")
            readbuffer = readbuffer.encode()
            readbuffer = temp.pop()
        except:
            temp = ""
        for line in temp:
            if line == "":
                break
            #Anti TO de twitch (stv faire des viewsbot il te faudra ce "if"
            if "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                s.send(msgg)
                print(msgg)
                break
            user = getUser(line)
            message = getMessage(line)
            #Pour avoir un retour sur le CMD ou python
            print(user + " > " + message)
            #pour envoyer un mp
            PMSG = "/w " + user + " "

############################################################################
############################  Commandes ####################################
############################################################################
#!cassio
            #print(message)
            if user == OWNER and message =="!cassio":
                sendMessage(s, PMSG + "Bonjour meri AKA je max le q sur cassio")				
				
            if message.startswith("!commande"):
                sendMessage(s, "Commandes: !join PseudoInGame, !leave")
                #print("Commandes : !join PseudoInGame, !leave")
#!join                 
            if  message.startswith("!join"):
                m=message.strip()
                if m == "!join":
                    sendMessage(s,PMSG + "Lis bien la commande !join TonPseudo  <--")
                else :					
                    pseudo = m.split("n",1)[1]
                    if pseudo in lstbanwords :
                        sendMessage(s, PMSG + "Pas d'insulte avec moi !")					
                    if user in userlist or pseudo in joueur :
                        sendMessage(s,PMSG + "Une insciption par personne!")
                    else:
                        ticket = tickets
                        tickets = tickets + 1
                        joueur.append(pseudo) 
                        numero.append(str(ticket))
                        userlist.append(user) 
                        sendMessage(s, PMSG + "Tu a bien été inscrit dans la liste des joueurs") 

						
						
#!edit
            if message.startswith("!edit"):
                m = message.strip()
                if m == "!edit":
                    sendMessage(s, PMSG + "Lis bien la commande, !edit TonNouveauPseudo  <--")
                else :					
                    pseudo = message.split("t",1)[1]
                    if pseudo in lstbanwords :
                        sendMessage(s, PMSG + "Pas d'insulte avec moi !")
                    elif user in userlist :
                        x = -1
                        for i in userlist:
                            x+=1           
                            if i == (user) :
                                joueur[x]=pseudo
                                sendMessage(s, PMSG + "Ton pseudo a bien été changé par "+ pseudo)
                    else :
                        sendMessage(s, PMSG + "Tu n'es pas inscrit a la liste des joueurs, utilise la commande !join pour t'inscrire")
#!new game ,
            if user == OWNER and message.startswith("!new game") :
                joueur = resetjoueur(joueur)
                tickets = resettickets(tickets)
                userlist = resetuserlist(userlist)
                sendMessage(s, PMSG + "Game reset")
                print("game reset")
#!inv 
            if user == OWNER and message.startswith("!inv"):
                if tickets == 1 :
                    sendMessage(s, "Personne n'es inscrit, !join VotrePseudo pour vous inscrire")
                else :
                    nbj=len(joueur)
                    phr=""
                    for i in range (0,nbj) :
                        if joueur[i] != "":
                            phr = phr + joueur[i] + ","
                    sendMessage(s, phr)
#!Sarcasme		
            if user == "fanboooy_" and message.startswith("!Sarcasme"):
                    sendMessage(s, "DON'T MIND US WE'RE JUST SPLILLING OUR GUTS")
                    sendMessage(s, "IF THIS IS LOVE I DON'T WANNA BE LOVED")
                    sendMessage(s, "YOU POLLUTE THE ROOM WITH A FILTHY TONGUE")
                    sendMessage(s, "WATCH ME CHOKE IT DOWN SO I CAN THROW IT UP")

#!leave	
            if  message.startswith("!leave"):
                if user in userlist :
                    tjoueur = len(joueur)
                    x = -1
                    for i in userlist:
                        x+=1           
                        if i == (user) : #user quitte la room
                            userlist.remove(i)
                            joueur.remove(joueur[x])
                            t=len(numero) - 1
                            delet=numero[int(t)]
                            numero.remove(delet)
                            tickets = tickets - 1
                            sendMessage(s, PMSG + "Tu t'es bien déinscrit(e) de la prochaine game")
                            #print("Tu es déinscrit")
                else :
                    sendMessage(s, "Tu n'es pas dans la liste des joueurs, !join pour s'inscrire")
                    #print("tu ne peut pas")
#!!report
            if message.startswith("!report"):
                if user in trusted :
                    banadd = msg.split(" ",1)[1]
                    mon_fichier = open("liste.txt", "a")
                    mon_fichier.writelines("\n" + banadd)
                    mon_fichier.close()
                else :
                    sendMessage(s, PMSG + "Tu n'a pas le droit d'utiliser cette commande")

############################################################################
