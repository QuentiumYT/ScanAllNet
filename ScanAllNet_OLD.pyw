import os, sys, urllib.request
from tkinter import *
from tkinter.messagebox import *

__version__ = 2
__filename__ = "ScanAllNet"
__savepath__ = os.path.join(os.environ['APPDATA'], "QuentiumPrograms")
__iconpath__ = __savepath__ + "/{}.ico".format(__filename__)

try:urllib.request.urlopen("https://www.google.fr/", timeout=1); connection = True
except:connection = False
if not os.path.exists(__iconpath__):
    try:os.mkdir(__savepath__)
    except:pass
    if connection == True:
        try:urllib.request.urlretrieve("https://quentium.fr/+++PythonDL/{}.ico".format(__filename__), __iconpath__)
        except:pass

if connection == True:
    try:script_version = int(urllib.request.urlopen("https://quentium.fr/programs/index.php").read().decode().split(__filename__ + "<!-- Version: ")[1].split(" --></h2>")[0])
    except:script_version = __version__
    if script_version > __version__:
        if os.path.exists(__iconpath__):popup = Tk(); popup.attributes("-topmost", 1); popup.iconbitmap(__iconpath__); popup.withdraw()
        ask_update = askquestion(__filename__ + " V" + str(script_version), "Une mise à jour à été trouvée, souhaitez vous la télécharger puis l'installer ?", icon="question")
        if ask_update == "yes":
            os.rename(os.path.basename(sys.argv[0]), __filename__ + "-old.exe")
            urllib.request.urlretrieve("https://quentium.fr/download.php?file={}.exe".format(__filename__), __filename__ + ".exe")
            showwarning(__filename__, "Le programme va redémarrer pour fonctionner sous la nouvelle version.", icon="warning")
            os.system("start " + __filename__ + ".exe")
            os._exit(1)

__filename__ = __filename__ + " V" + str(__version__)

import socket, subprocess, threading
from tkinter.ttk import *
from tkinter import *

hosts = []

def start_thread():
    global min_ip, max_ip
    try:
        min_ip = int(min_ip_ping.get())
        min_ip_status = True
    except:
        min_ip_status = False
        showerror(__filename__, "Erreur : Mauvais argument dans Min IP ou non renseigné.")
    try:
        max_ip = int(max_ip_ping.get())
        max_ip_status = True
    except:
        max_ip_status = False
        showerror(__filename__, "Erreur : Mauvais argument dans Max IP ou non renseigné.")
    if min_ip_status and max_ip_status == True:
        if min_ip <= 254:
            if max_ip <= 255:
                if min_ip >= 1:
                    if max_ip > 1:
                        if not min_ip == max_ip:
                            if min_ip < max_ip:
                                button.configure(state="disabled")
                                thread.start()
                                labeltext.set("Status : Recherche")
                            else:
                                showerror(__filename__, "Erreur : Min IP ne dois pas être supérieur à Max IP.")
                        else:
                            showerror(__filename__, "Erreur : Min IP ne doit pas être égal à Max IP.")
                    else:
                        showerror(__filename__, "Erreur : Max IP doit être supérieur à 1.")
                else:
                    showerror(__filename__, "Erreur : Min IP doit être supérieur ou égal à 1.")
            else:
                showerror(__filename__, "Erreur : Max IP ne doit pas dépasser 255.")
        else:
            showerror(__filename__, "Erreur : Min IP ne doit pas dépasser 254.")

def start_scan():
    global min_ip, max_ip
    my_hostname = socket.gethostname()
    my_addr = socket.gethostbyname(my_hostname)
    file = open("Networklist.txt", "w", encoding="utf-8")
    file.write("Liste de tout les périphériques connectés sur le réseau :" + "\n")
    file.write("------------------------------" + "\n")
    file.write("-     Votre ordinateur :     -" + "\n")
    file.write("Nom : " + my_hostname + "\n")
    file.write("IPV4 : " + my_addr + "\n")
    file.write("------------------------------" + "\n" + "\n")
    file.write("Test de ping sur toutes les IP demandées : " + "\n")
    file.close()
    file = open("Networklist.txt", "a", encoding="utf-8")

    ip = my_addr
    ip = ip.split(".", 3)[:-1]
    ip = str([ip + "." for ip in ip])
    base_ip = ip.replace("[", "").replace("]", "").replace("', '", "").replace("'", "")

    progress_var.set(0)
    scanallnet.update_idletasks()
    max_ip += 1
    for i in range(min_ip, max_ip):
        hostname = base_ip + str(i)
        try:
            subprocess.check_output("ping " + hostname + " -n 1 -l 1 -w 1", stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            hosts.append(hostname)
            file.write("[+] Trouvé " + hostname + "\n")
        except:
            file.write("[-] Vérifié " + hostname + "\n")
        i = round((1000 / (max_ip - min_ip)) * (i - min_ip + 1))
        progress_var.set(i)
        scanallnet.update_idletasks()

    progress_var.set(0)
    scanallnet.update_idletasks()
    file.write("\n" + "------------------------------" + "\n")
    file.write("-         Résultats :        -" + "\n")
    for i in range(0, len(hosts)):
        labeltext.set("Status : Résolution du nom d'hôte")
        try:
            name, _, _ = socket.gethostbyaddr(hosts[i])
        except:
            name = "Nom introuvable !"
        file.write(hosts[i] + " | " + name + "\n")
        i = round((1000 / len(hosts)) * (i + 1))
        progress_var.set(i)
        scanallnet.update_idletasks()

    if not hosts:
         file.write("Aucuns résultats." + "\n")
    file.write("------------------------------" + "\n")
    file.close()
    try:os.system("start notepad Networklist.txt")
    except:pass
    os._exit(1)
    scanallnet.destroy()

scanallnet = Tk()
width = 750
height = 500
scanallnet.update_idletasks()
x = (scanallnet.winfo_screenwidth() - width) // 2
y = (scanallnet.winfo_screenheight() - height) // 2
scanallnet.geometry("{}x{}+{}+{}".format(width , height, int(x), int(y)))
scanallnet.resizable(width=False, height=False)
scanallnet.configure(bg="lightgray")
if os.path.exists(__iconpath__):
    scanallnet.iconbitmap(__iconpath__)
scanallnet.title(__filename__)

thread = threading.Thread(target=start_scan)
Label(scanallnet, text="Bienvenue dans le programme de Scan !", font="impact 30", fg="red", bg="lightgray").pack(pady=70)

def character_limit(txt):
    try:
        if len(str(txt.get())) >= 0:
            txt.set(str(txt.get())[:3])
        if int(txt.get()) >= 255:
            txt.set(255)
    except:
        pass

Label1 = Label(scanallnet, font="impact 20", text="Min IP :", bg="lightgray")
Label1.place(relx=0.2, rely=0.36, height=28, width=100)
Label2 = Label(scanallnet, font="impact 20", text="Max IP :", bg="lightgray")
Label2.place(relx=0.55, rely=0.36, height=28, width=100)
labeltext = StringVar()
Label3 = Label(scanallnet, font="impact 14", textvar=labeltext, bg="lightgray")
Label3.place(relx=0.32, rely=0.76, height=28, width=260)
labeltext.set("Status :  Attente")

min_ip_ping = IntVar()
min_ip_ping.set("1")
max_ip_ping = IntVar()
max_ip_ping.set("255")
Entry1 = Entry(scanallnet, font="impact 20", textvariable=min_ip_ping, width=5)
Entry1.place(relx=0.35, rely=0.36, relheight=0.05, relwidth=0.1)
min_ip_ping.trace("w", lambda *args: character_limit(min_ip_ping))
Entry2 = Entry(scanallnet, font="impact 20", textvariable=max_ip_ping, width=5)
Entry2.place(relx=0.7, rely=0.36, relheight=0.05, relwidth=0.1)
max_ip_ping.trace("w", lambda *args: character_limit(max_ip_ping))

button = Button(scanallnet, text="Commencer à scan", command=start_thread, relief=GROOVE, width=25, font="impact 20", fg="black")
button.pack(pady=50)

progress_var = DoubleVar()
progressbar = Progressbar(scanallnet, orient='horizontal', variable=progress_var, mode='determinate', length=500, maximum=1000)
progressbar.pack()

scanallnet.mainloop()
