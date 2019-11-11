import os, sys, urllib.request
from tkinter import *
from tkinter.messagebox import *

__version__ = 4
__filename__ = "ScanAllNet"
__basename__ = os.path.basename(sys.argv[0])
__savepath__ = os.path.join(os.environ['APPDATA'], "QuentiumPrograms")
__iconpath__ = __savepath__ + "/{}.ico".format(__filename__)
__picpath__ = __savepath__ + "/{}.png".format(__filename__)

try:urllib.request.urlopen("https://www.google.fr/", timeout=1); connection = True
except:connection = False
if not os.path.exists(__iconpath__) or not os.path.exists(__picpath__):
    try:os.mkdir(__savepath__)
    except:pass
    if connection == True:
        try:
            urllib.request.urlretrieve("http://quentium.fr/+++PythonDL/{}.ico".format(__filename__), __iconpath__)
            urllib.request.urlretrieve("http://quentium.fr/+++PythonDL/{}.png".format(__filename__), __picpath__)
        except:pass

if connection == True:
    try:script_version = int(urllib.request.urlopen("http://quentium.fr/programs/index.php").read().decode().split(__filename__ + "<!-- Version: ")[1].split(" --></h2>")[0])
    except:script_version = __version__
    if script_version > __version__:
        if os.path.exists(__iconpath__):popup = Tk(); popup.attributes("-topmost", 1); popup.iconbitmap(__iconpath__); popup.withdraw()
        ask_update = askquestion(__filename__ + " V" + str(script_version), "Une mise à jour à été trouvée, souhaitez vous la télécharger puis l'éxécuter ?", icon="question")
        if ask_update == "yes":
            try:os.rename(__basename__, __filename__ + "-old.exe")
            except:os.remove(__filename__ + "-old.exe"); os.rename(__basename__, __filename__ + "-old.exe")
            if "-32" in str(__basename__):urllib.request.urlretrieve("http://quentium.fr/download.php?file={}-32.exe".format(__filename__), __filename__ + ".exe")
            else:urllib.request.urlretrieve("http://quentium.fr/download.php?file={}.exe".format(__filename__), __filename__ + ".exe")
            showwarning(__filename__, "Le programme va redémarrer pour fonctionner sous la nouvelle version.", icon="warning")
            os.system("start " + __filename__ + ".exe"); os._exit(1)

__filename__ = __filename__ + " V" + str(__version__)

# Add a viewer at the end of scan

import socket, subprocess, threading
from tkinter.ttk import *
from tkinter import *
from PIL import Image, ImageTk

check_xbm = """
#define 1550156626092_width 11
#define 1550156626092_height 11
static char 1550156626092_bits[] = {
  0x00, 0x00, 0x00, 0x06, 0x00, 0x07, 0x80, 0x03, 0xC0, 0x01, 0xE3, 0x00, 
  0x77, 0x00, 0x3E, 0x00, 0x1C, 0x00, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00};
"""

cross_xbm = """
#define 1550158124104_width 11
#define 1550158124104_height 11
static char 1550158124104_bits[] = {
  0x03, 0x06, 0x07, 0x07, 0x8E, 0x03, 0xDC, 0x01, 0xF8, 0x00, 0x70, 0x00, 
  0xF8, 0x00, 0xDC, 0x01, 0x8E, 0x03, 0x07, 0x07, 0x03, 0x06, 0x00, 0x00};
"""

def start_init():
    global min_ip, max_ip, n_proc, base_ip
    try:
        min_ip = int(min_ip_ping.get())
    except:
        return showerror(__filename__, "Erreur : Mauvais argument dans Min IP ou non renseigné.")
    try:
        max_ip = int(max_ip_ping.get())
    except:
        return showerror(__filename__, "Erreur : Mauvais argument dans Max IP ou non renseigné.")
    try:
        n_proc = int(n_proc_ping.get())
    except:
        return showerror(__filename__, "Erreur : Mauvais argument dans le nombre de threads ou non renseigné.")
    if min_ip <= 254:
        if max_ip <= 255:
            if min_ip >= 1:
                if max_ip > 1:
                    if not min_ip == max_ip:
                        if min_ip < max_ip:
                            if int(str(base_ip.get()).count(".")) == 3:
                                if len([x for x in str(base_ip.get()).split(".")[:-1] if int(x) <= 255]) == 3:
                                    base_ip = base_ip.get()
                                    file = open("Networklist.txt", "w", encoding="utf-8")
                                    file.write("Liste de tout les périphériques connectés sur le réseau :" + "\n")
                                    file.write("------------------------------" + "\n")
                                    file.write("-     Votre ordinateur :     -" + "\n")
                                    file.write("Nom : " + my_hostname + "\n")
                                    file.write("IPV4 : " + my_addr + "\n")
                                    file.write("------------------------------" + "\n" + "\n")
                                    file.write("Test de ping sur toutes les IP demandées : " + "\n")
                                    file.close()
                                    
                                    max_ip += 1
                                    main_thread.start()
                                    Button1.configure(state="disabled")
                                else:
                                    showerror(__filename__, "Erreur : Les éléments de l'ip de base ne doivent pas dépasser 255.")
                            else:
                                showerror(__filename__, "Erreur : L'ip de base est fausse où incomplète (4 octets).")
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

def starting_thread():
    global ips, count_ips, count_hosts, threads, n_proc
    ips = [x for x in range(min_ip, max_ip)]
    if n_proc > len(ips):
        n_proc = len(ips)
    for i in range(n_proc):
        lists_split = ips[i::n_proc]
        th = threading.Thread(target=start_scan, args=lists_split, daemon=True)
        threads.append(th)
    count_ips = 0
    labeltext.set("Status : Recherche")
    Label4.configure(width=18)
    for x in threads:x.start()
    for x in threads:x.join()

    threads = []

    if n_proc > len(hosts):
        n_proc = len(hosts)
    for i in range(n_proc):
        lists_split = hosts[i::n_proc]
        th = threading.Thread(target=start_resolve, args=lists_split, daemon=True)
        threads.append(th)
    count_hosts = 0
    labeltext.set("Status : Résolution du nom d'hôte")
    Label4.configure(width=30)
    for x in threads:x.start()
    for x in threads:x.join()
    finish_scan()

def start_scan(*liste):
    global count_ips, base_ip
    progress_var.set(0)
    scanallnet.update_idletasks()
    liste = list(liste)
    for i in liste:
        count_ips += 1
        p_stat = round((1000 / len(ips)) * count_ips)
        progress_var.set(p_stat)
        scanallnet.update_idletasks()

        hostname = ".".join(base_ip.split(".")[:3]) + "." + str(i)
        try:
            subprocess.check_output("ping " + hostname + " -n 1 -l 1 -w 1", stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            ip_check.append(hostname)
            hosts.append(hostname)
        except:
            ip_check.append(hostname)

def start_resolve(*liste):
    global count_hosts
    progress_var.set(0)
    scanallnet.update_idletasks()
    liste = list(liste)
    for i in liste:
        count_hosts += 1
        p_stat = round((1000 / len(hosts)) * count_hosts)
        progress_var.set(p_stat)
        scanallnet.update_idletasks()

        try:
            name, _, _ = socket.gethostbyaddr(i)
        except:
            name = "Nom introuvable !"
        ip_hosts.append(i)
        if ".home" in str(name):
            name = name.replace(".home", "")
        name_hosts.append(" | " + name)

def finish_scan():
    global verif
    def sort_ips(liste):
        return sorted(liste, key=lambda x: int("".join((lambda a:lambda v:a(a,v))(lambda s,x: x if len(x) == 3 else s(s, "0"+x))(i) for i in x.split("."))))
    file = open("Networklist.txt", "a", encoding="utf-8")
    for item in sort_ips(ip_check):
        if hosts:
            for x in hosts:
                if item == x:
                    file.write("[+] Trouvé " + item + "\n")
                    verif = False
                    break
                else:
                    verif = True
        else:
           verif = True 
        if verif == True:
            file.write("[-] Vérifié " + item + "\n")
    file.write("\n" + "------------------------------" + "\n")
    file.write("-         Résultats :        -" + "\n")
    if not hosts:
        file.write("Aucuns résultats." + "\n")
    else:
        sorted_ips = sort_ips(ip_hosts)
        sorted_names = [x for _, x in sorted(zip(ip_hosts, name_hosts))]
        for i in range(len(sorted_ips)):
            file.write(sorted_ips[i] + sorted_names[i] + "\n")
    file.write("------------------------------" + "\n")
    file.close()
    answer = askyesno(__filename__, "Souhaitez vous ouvrir le résultat avec notepad ?")
    if answer:
        subprocess.call("notepad Networklist.txt", shell=False)
    os._exit(1)
    scanallnet.destroy()

threads = []
hosts = []
ip_hosts = []
name_hosts = []
ip_check = []
temp_txt = "0"
verif = False

my_hostname = socket.gethostname()
my_addr = socket.gethostbyname(my_hostname)

scanallnet = Tk()
width = 750
height = 500
scanallnet.update_idletasks()
x = (scanallnet.winfo_screenwidth() - width) // 2
y = (scanallnet.winfo_screenheight() - height) // 2
scanallnet.geometry("{}x{}+{}+{}".format(width , height, int(x), int(y)))
scanallnet.resizable(width=False, height=False)
scanallnet.title(__filename__)
scanallnet.configure(bg="lightgray")

main_thread = threading.Thread(target=starting_thread, daemon=True)

if os.path.exists(__iconpath__):
    scanallnet.iconbitmap(__iconpath__)

if os.path.exists(__picpath__):
    BG = Image.open(__picpath__)
    img = ImageTk.PhotoImage(BG)
    BGL = Label(scanallnet, image=img)
    BGL.place(relx=0, rely=0, relheight=1, relwidth=1)

def character_limit(txt):
    global temp_txt
    try:
        if len(str(txt.get())) >= 0:
            txt.set(str(txt.get())[:3])
        if int(txt.get()) >= 255:
            txt.set(255)
        temp_txt = txt.get()
    except Exception as e:
        if not "got \"\"" in str(e):
            txt.set(temp_txt)

def len_entry(long):
    long += 1
    if long <= 3:
        Entry4.configure(width=3)
    else:
        Entry4.configure(width=int(long * 0.91))

is_activated = False
def toogle_active():
    global is_activated, Checkbutton1, bitmap
    if is_activated == True:
        Entry4.configure(state="disabled")
        if os.path.exists(__picpath__):
            bitmap = BitmapImage(data=check_xbm)
            Checkbutton1.configure(image=bitmap)
        is_activated = False
    else:
        Entry4.configure(state="normal")
        if os.path.exists(__picpath__):
            bitmap = BitmapImage(data=cross_xbm)
            Checkbutton1.configure(image=bitmap, anchor="nw")
        is_activated = True

if not os.path.exists(__picpath__):
    LabelMain = Label(scanallnet, text="Bienvenue dans le programme de Scan !", font="impact 30", fg="red", bg="lightgray")
    LabelMain.place(relx=0.5, rely=0.1, anchor=CENTER)

    Label1 = Label(scanallnet, font="impact 20", text="Min IP :", bg="lightgray")
    Label1.place(relx=0.28, rely=0.25, height=28, width=100, anchor=CENTER)

    Label2 = Label(scanallnet, font="impact 20", text="Max IP : ", bg="lightgray")
    Label2.place(relx=0.58, rely=0.25, height=28, width=100, anchor=CENTER)

    Label3 = Label(scanallnet, font="impact 16", text="Threads :", bg="lightgray")
    Label3.place(relx=0.27, rely=0.38, anchor=CENTER)

    check_var = IntVar()
    Checkbutton1 = Checkbutton(scanallnet, variable=check_var, command=toogle_active, bg="lightgray", activebackground="lightgray")
    Checkbutton1.place(relx=0.54, rely=0.38, anchor=CENTER)
else:
    check_var = IntVar()
    bitmap = BitmapImage(data=check_xbm)
    Checkbutton1 = Checkbutton(scanallnet, variable=check_var, command=toogle_active, indicatoron=0, borderwidth=2, height=11, width=11, image=bitmap)
    Checkbutton1.place(relx=0.54, rely=0.38, anchor=CENTER)

min_ip_ping = IntVar()
min_ip_ping.set("1")
Entry1 = Entry(scanallnet, font="impact 20", textvariable=min_ip_ping, width=5)
Entry1.place(relx=0.38, rely=0.25, height=30, width=55, anchor=CENTER)
min_ip_ping.trace("w", lambda *args: character_limit(min_ip_ping))

max_ip_ping = IntVar()
max_ip_ping.set("255")
Entry2 = Entry(scanallnet, font="impact 20", textvariable=max_ip_ping, width=5)
Entry2.place(relx=0.68, rely=0.25, height=30, width=55, anchor=CENTER)
max_ip_ping.trace("w", lambda *args: character_limit(max_ip_ping))

n_proc_ping = IntVar()
n_proc_ping.set("16")
Entry3 = Entry(scanallnet, font="impact 16", textvariable=n_proc_ping, width=5)
Entry3.place(relx=0.38, rely=0.38, anchor=CENTER)

base_ip = StringVar()
base_ip.set(".".join(my_addr.split(".")[:3]) + "." + "IP")
Entry4 = Entry(scanallnet, font="impact 16", textvariable=base_ip, state="disabled", width=5)
Entry4.place(relx=0.58, rely=0.38, anchor=W)
Entry4.configure(width=int(len(my_addr) * 0.9))
base_ip.trace("w", lambda *args: len_entry(len(base_ip.get())))

Button1 = Button(scanallnet, text="Commencer à scan", command=start_init, relief=GROOVE, width=25, font="impact 20", fg="black")
Button1.place(relx=0.5, rely=0.58, anchor=CENTER)

labeltext = StringVar()
Label4 = Label(scanallnet, font="impact 14", textvar=labeltext, relief="solid", bg="lightgray", bd=4, width=15)
Label4.place(relheight=0.08, relx=0.5, rely=0.88, anchor=CENTER)
labeltext.set("Status :  Attente")

progress_var = DoubleVar()
progressbar = Progressbar(scanallnet, orient="horizontal", variable=progress_var, mode="determinate", length=500, maximum=1000)
progressbar.place(relx=0.5, rely=0.75, anchor=CENTER)

scanallnet.mainloop()
