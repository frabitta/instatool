import instaloader
import tkinter as tk

# name of the generated files
BASE_nomeFileElencoFollowees = "Followees_list"
BASE_nomeFileElencoFollowers = "Followers_list"
BASE_nomeFileOutputUnrequited = "Unrequited_list"
BASE_nomeFileOutputFan = "Fan_list"

# colours used
colour_bg = "#F2F2F2"
colour_bg2 = "#E3E3E3"
colour_text = "#0B2027"
colour_text_error = "red"
colour_text_success = "#70A9A1"
colour_azzurro = "#40798C"
colour_arancione = "#F05D23"

#SAVE SESSION ----------------------https://instaloader.github.io/troubleshooting.html
from argparse import ArgumentParser
from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect

try:
    from instaloader import ConnectionException, Instaloader
except ModuleNotFoundError:
    raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")

def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
    return cookiefiles[0]


def import_session(cookiefile, sessionfile):
#    print("Using cookies from {}.".format(cookiefile))
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
        )
    instaloader = Instaloader(max_connection_attempts=1)
    instaloader.context._session.cookies.update(cookie_data)
    username = instaloader.test_login()
    if not username:
        raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
#    print("Imported session cookie for {}.".format(username))
    instaloader.context.username = username
    instaloader.save_session_to_file(sessionfile)

def saveSession():
    if __name__ == "__main__":
        p = ArgumentParser()
        p.add_argument("-c", "--cookiefile")
        p.add_argument("-f", "--sessionfile")
        args = p.parse_args()
        try:
            import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
        except (ConnectionException, OperationalError) as e:
            raise SystemExit("Cookie import failed: {}".format(e))
#END SAVE SESSION --------------------------------------------------------------

#UTILITIES----------------------------------------------------------------------
#takes a list and print that on a file with the name specified
def writeListToFile(nomefile,lista,tot,text):
    f = open(nomefile,"w")
    i = 1
    for x in lista:
        f.write(str(x.username)+"\n")
        perc = i/tot * 100
        update.config(text = "Update: loading "+text+" list...  "+str(round(perc))+"%")
        window.update()
        i += 1
    f.close()

#prints every line of file2 that's not incuded in file1
def compareFiles(nomeFile1,nomeFile2,nomeFileOutput):
    file1 = open(nomeFile1,"r")
    file2 = open(nomeFile2,"r")
    list = file1.read()
    fileOutput = open(nomeFileOutput,"w")
    for line in file2:
        if line not in list:
 #           print(line)
            fileOutput.write(str(line))
    file1.close()
    file2.close()
    fileOutput.close()

#by reading the old file he updates the list with the names of the new users: new followers and new unfollows
def compareFiles_forNewFollowUnfollow(nomeFile1,nomeFile2,list):
    file1 = open(nomeFile1,"r")
    file2 = open(nomeFile2,"r")
    list_f1 = file1.read()
    list.delete(0,tk.END)
    for line in file2:
        if line not in list_f1:
            list.insert(tk.END, str(line))
    file1.close()
    file2.close()

#open a file and displays its content in a new tkinter window
def openFile_asWindow(nomeFile):
    newWindow = tk.Tk()
    newWindow.geometry("300x600")
    newWindow.title(nomeFile)
    newWindow.resizable(True, True)
    newWindow.configure(bg=colour_bg)

    file = open(nomeFile,"r")

    scrollbar = tk.Scrollbar(newWindow)
    scrollbar.pack( side = tk.RIGHT, fill = tk.Y )
    text = tk.Text(newWindow, yscrollcommand = scrollbar.set, bg=colour_bg, fg=colour_text, font=("Arial", 15, "italic"))
    for line in file:
        text.insert(tk.END, str(line))
    text.pack( side = tk.LEFT, fill = tk.BOTH )
    scrollbar.config(command = text.yview )

    newWindow.update()

# the following 4 functions call openFile_asWindow with the respective name file required
def openFanFile_asWindow():
    nomeUtenteDaAnalizzare = box_nomeUtenteDaAnalizzare.get(1.0, "end-1c")
    openFile_asWindow(nomeUtenteDaAnalizzare+"_"+BASE_nomeFileOutputFan+".txt")

def openUnrequitedFile_asWindow():
    nomeUtenteDaAnalizzare = box_nomeUtenteDaAnalizzare.get(1.0, "end-1c")
    openFile_asWindow(nomeUtenteDaAnalizzare+"_"+BASE_nomeFileOutputUnrequited+".txt")

def openFollowersFile_asWindow():
    nomeUtenteDaAnalizzare = box_nomeUtenteDaAnalizzare.get(1.0, "end-1c")
    openFile_asWindow(nomeUtenteDaAnalizzare+"_"+BASE_nomeFileElencoFollowers+".txt")

def openFolloweesFile_asWindow():
    nomeUtenteDaAnalizzare = box_nomeUtenteDaAnalizzare.get(1.0, "end-1c")
    openFile_asWindow(nomeUtenteDaAnalizzare+"_"+BASE_nomeFileElencoFollowees+".txt")

#copies src content in dst
def copyFile(src_name, dst_name):
    dst = open(dst_name, "w")
    try:
        src = open(src_name, "r")
    except:
        update.config(text = "Update: no previous analysis on this account...")
        window.update()
    else:    
        for line in src:
            dst.write(str(line))
        src.close()

    dst.close()

#END UTILITIES-------------------------------------------------------------------

#TOOL----------------------------------------------------------------------------
def executeAnalysis():
    update.config(text = "Update: initialising analysis...", fg=colour_text)
    window.update()

    # gets the usernames fron the text boxes in the window
    nomeUtenteLoginato = box_nomeUtenteLoginato.get(1.0, "end-1c")
    nomeUtenteDaAnalizzare = box_nomeUtenteDaAnalizzare.get(1.0, "end-1c")
    
    nomeFileElencoFollowees = nomeUtenteDaAnalizzare+"_"+BASE_nomeFileElencoFollowees+".txt"
    nomeFileElencoFollowers = nomeUtenteDaAnalizzare+"_"+BASE_nomeFileElencoFollowers+".txt"
    nomeFileOutputUnrequited = nomeUtenteDaAnalizzare+"_"+BASE_nomeFileOutputUnrequited+".txt"
    nomeFileOutputFan = nomeUtenteDaAnalizzare+"_"+BASE_nomeFileOutputFan+".txt"

    update.config(text = "Update: saving session...")
    window.update()

    # saves the current firefox session to access instagram
    try:
        saveSession()
    except:
#        print("Impossibile salvare la sessione")
        update.config(text = "Error: unable to save the session.", fg=colour_text_error)
        return
    else:
#       print("Sessione salvata")
        update.config(text = "Update: session saved")
    window.update()

    update.config(text = "Update: loading session...")
    window.update()

    # load the instagram session saved before with instaloader
    L = instaloader.Instaloader()
    try:
        L.load_session_from_file(nomeUtenteLoginato)
    except:
#        print("Impossibile caricare la sessione")
        update.config(text = "Error: unable to load the session.", fg=colour_text_error)
        return
    else:
#        print("Sessione caricata")
        update.config(text = "Update: session loaded")
    window.update()

    update.config(text = "Update: opening profile...")
    window.update()

    # opens the profile we want to do the analysis on
    try:
        profile = instaloader.Profile.from_username(L.context,nomeUtenteDaAnalizzare)
    except:
#        print("Impossibile aprire profilo")
        update.config(text = "Error: unable to open the profile.", fg=colour_text_error)
        return
    else:
#        print("Profilo di "+str(profile.username)+" aperto")
        update.config(text = "Update: "+str(profile.username)+"'s profile opened") #LU E' CORRETTO????????????????????????????
    window.update()

    update.config(text = "Update: loading followees list...")
    window.update()

    # creates a file with a list of all the followees of that user
    followeesList = profile.get_followees()
#    print("Followees: "+str(followeesList.count))
    writeListToFile(nomeFileElencoFollowees,followeesList,followeesList.count,"followees")

    update.config(text = "Update: loading followers list...")
    window.update()

    # creates a file with a list of all the followers of that user
    followersList = profile.get_followers()
#    print("Followers: "+str(followersList.count))
    copyFile(nomeFileElencoFollowers,"old.txt")
    writeListToFile(nomeFileElencoFollowers,followersList,followersList.count,"followers")

    #updates the two displayed lists with the new followers and unfollows
    compareFiles_forNewFollowUnfollow("old.txt",nomeFileElencoFollowers,list1)
    compareFiles_forNewFollowUnfollow(nomeFileElencoFollowers,"old.txt",list2)

    update.config(text = "Update: creating unrequited users list...")
    window.update()

    # compares the two files generated before and creates another one with the list of all the unrequited users
    try:
        compareFiles(nomeFileElencoFollowers,nomeFileElencoFollowees,nomeFileOutputUnrequited)
    except:
#        print("Impossibile creare file non ricambianti")
        update.config(text = "Error: unable to create unrequited users list.", fg=colour_text_error)
        return
    else:
#        print("File non ricambianti creato")
        update.config(text = "Update: unrequited users list created")
    window.update()

    update.config(text = "Update: creating fans list...")
    window.update()

    # compares the two files generated before and creates another one with the list of all the users that our user don't follow back
    try:
        compareFiles(nomeFileElencoFollowees,nomeFileElencoFollowers,nomeFileOutputFan)
    except:
#        print("Impossibile creare file fan")
        update.config(text = "Error: unable to create fan users list.", fg=colour_text_error)
        return
    else:
#        print("File dei fan creato")
        update.config(text = "Update: fan users list created")
    window.update()

    update.config(text = "Update: finished!", fg=colour_text_success)

    window.update()
#END TOOL------------------------------------------------------------------------


# initialising window
window = tk.Tk()
window.geometry("750x580")
window.title("Insta tool")
window.resizable(False, False)
window.configure(background=colour_bg)

try:
    icon = tk.PhotoImage(file = 'InstaTool_icon.png')
except:
    print("impossible to load icon")
else:
    window.iconphoto(False,icon)

#Instructions
title = tk.Label(master=window,text="Welcome to Insta-Tool",fg=colour_text_error,bg=colour_bg,font=("Arial", 14))
title.pack(side=tk.TOP)
text = tk.Label(master=window,text="To run the program you need to login to your Instagram account using the Firefox web browser\n"+
                    "-In the 'Logged username' box you need to insert your username\n"+
                    "-In the 'Username to analyze' box you have to insert the username of the account you want to analyze\n"+
                    "In order for it to work this account must be public or followed by the logged in user (it can be yourself if you want to analyze your account)\n"+
                    "Once you put the correct usernames in the boxes click 'Run' and wait for the results wich will be saved in 4 text files",bg=colour_bg,fg=colour_text)
text.pack(side=tk.TOP)

# textbox to input usernames
frame_input = tk.Frame(window, bg=colour_bg2,height=40)
frame_input.pack(side = tk.TOP,pady=15,fill=tk.Y)
text_nomeUtenteLoginato = tk.Label(frame_input, text="Logged username:",bg=colour_bg2,fg=colour_text, font=("Arial", 11))
text_nomeUtenteLoginato.grid(row=0,column=0,pady=3, padx=3)
box_nomeUtenteLoginato = tk.Text(frame_input, height = 1, width = 20)
box_nomeUtenteLoginato.insert(0.0,"francescobittasi")
box_nomeUtenteLoginato.grid(row=0,column=1,pady=3,padx = 5)

text_nomeUtenteDaAnalizzare = tk.Label(frame_input, text="Username to analyze:",bg=colour_bg2,fg=colour_text, font=("Arial", 11))
text_nomeUtenteDaAnalizzare.grid(row=1,column=0,pady=3,padx=3)
box_nomeUtenteDaAnalizzare = tk.Text(frame_input, height = 1, width = 20)
box_nomeUtenteDaAnalizzare.insert(0.0,"francescobittasi")
box_nomeUtenteDaAnalizzare.grid(row=1,column=1,pady=3,padx = 5)

# button to start the analysis
run_button = tk.Button(master=window,text="Run", command=executeAnalysis,bg=colour_text_success)
run_button.pack(side = tk.TOP)

# update label (used when the analysis runs)
update = tk.Label(window, text="Update: waiting", background=colour_bg, fg=colour_text, font=("Arial", 11))
update.pack(side=tk.TOP)

# frame and buttons to open the lists
frame_FileButtons = tk.Frame(window, bg = colour_azzurro)
frame_FileButtons.pack(side=tk.TOP,pady=10)

followers_button = tk.Button(master=frame_FileButtons,text="Followers list", command=openFollowersFile_asWindow)
followers_button.grid(row=0, column=0, sticky="nsew", padx = 20, pady=10)
followees_button = tk.Button(master=frame_FileButtons,text="Followees list", command=openFolloweesFile_asWindow)
followees_button.grid(row=0, column=1, sticky="nsew", padx = 20, pady=10)
fans_button = tk.Button(master=frame_FileButtons,text="Fans list", command=openFanFile_asWindow)
fans_button.grid(row=1, column=0, sticky="nsew", padx = 20, pady=10)
unrequited_button = tk.Button(master=frame_FileButtons,text="Unrequited list", command=openUnrequitedFile_asWindow)
unrequited_button.grid(row=1, column=1, sticky="nsew", padx = 20, pady=10)

# frame and lists to show new follows/unfollows
frame_newFollowUnfollows = tk.Frame(window, bg = colour_bg2, width=300, height=70)
frame_newFollowUnfollows.pack(side = tk.TOP)

frame_unfollow = tk.Frame(frame_newFollowUnfollows, bg = colour_bg2)
frame_unfollow.pack(side=tk.LEFT, pady=10,padx=25, fill=tk.X)
list1_title = tk.Label(frame_unfollow, text="New followers: ", bg=colour_bg2, fg=colour_text, font=("Arial", 11))
list1_title.pack(side = tk.TOP)
frame_unfollow_list = tk.Frame(frame_unfollow, bg = colour_bg2)
frame_unfollow_list.pack(side = tk.TOP)
list1_scrollbar = tk.Scrollbar(frame_unfollow_list)
list1 = tk.Listbox(frame_unfollow_list, yscrollcommand = list1_scrollbar.set)
list1_scrollbar.config(command = list1.yview)
list1.pack(side = tk.LEFT)
list1_scrollbar.pack(side = tk.RIGHT, fill = tk.Y )

frame_follow = tk.Frame(frame_newFollowUnfollows,bg = colour_bg2)
frame_follow.pack(side=tk.RIGHT, pady=10,padx=25, fill=tk.X)
list2_title = tk.Label(frame_follow, text="New unfollows: ", bg=colour_bg2, fg=colour_text, font=("Arial", 11))
list2_title.pack(side = tk.TOP)
frame_follow_list = tk.Frame(frame_follow,bg = colour_bg2)
frame_follow_list.pack(side = tk.TOP)
list2_scrollbar = tk.Scrollbar(frame_follow_list)
list2 = tk.Listbox(frame_follow_list,  yscrollcommand = list2_scrollbar.set)
list2_scrollbar.config(command = list2.yview)
list2.pack(side = tk.LEFT)
list2_scrollbar.pack(side = tk.RIGHT,  fill = tk.Y )

# credits
crediti = tk.Label(window,text="2023 CC BY-SA Francesco Bittasi")
crediti.pack(side = tk.RIGHT)

# main loop (runs the program)
if __name__ == "__main__":
    window.mainloop()

#pyinstaller --name InstaTool --onefile --windowed --icon=InstaTool_icon.ico main.py