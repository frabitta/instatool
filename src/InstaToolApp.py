import tkinter as tk
import sys
import os
import threading
import time
import InstaTool
import FileUtils

# colours used
colour_bg = "#F2F2F2"
colour_bg2 = "#E3E3E3"
colour_text = "#0B2027"
colour_text_error = "red"
colour_text_success = "#70A9A1"
colour_azzurro = "#40798C"
colour_arancione = "#F05D23"

# file names
fileName_fan = None
fileName_unrequited = None
fileName_followers = None
fileName_followees = None
list_newFollow = None
list_newUnfollow = None
updateLabelText = InstaTool.getStatusCodes()

# a list of all the started threads
threads = []

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller
    source: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def openFile_asWindow(nomeFile):
    """
    open a file and displays its content in a new tkinter window
    """
    newWindow = tk.Tk()
    newWindow.geometry("300x600")
    newWindow.title(nomeFile)
    newWindow.resizable(True, True)
    newWindow.configure(bg=colour_bg)

    file = FileUtils.openFileFromDataDir(nomeFile,"r")

    scrollbar = tk.Scrollbar(newWindow)
    scrollbar.pack( side = tk.RIGHT, fill = tk.Y )
    text = tk.Text(newWindow, yscrollcommand = scrollbar.set, bg=colour_bg, fg=colour_text, font=("Arial", 15, "italic"))
    for line in file:
        text.insert(tk.END, str(line))
    text.pack( side = tk.LEFT, fill = tk.BOTH )
    text.config(state=tk.DISABLED)
    scrollbar.config(command = text.yview )

    newWindow.update()

def saveMemory(loggedUsername, usernameToAnalyze):
    """
    saves the usernames in a file
    """
    f = FileUtils.openFileFromDataDir("memory.txt","w")
    f.write(loggedUsername+"\n")
    f.write(usernameToAnalyze+"\n")
    f.close()

def readMemory():
    """
    reads the usernames from a file
    """
    try:
        f = FileUtils.openFileFromDataDir("memory.txt","r")
        loggedUsername = f.readline()[:-1]
        usernameToAnalyze = f.readline()[:-1]
        f.close()
    except:
        loggedUsername = "insert username"
        usernameToAnalyze = "insert username"
    return loggedUsername, usernameToAnalyze

class ReturnableThread(threading.Thread):
    """
    This class is a subclass of Thread that allows the thread to return a value.
    source: https://jackwhitworth.com/blog/return-values-from-a-python-thread/#htoc-how-to-return-values-from-a-python-thread
    """
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target
        self.result = None
    
    def run(self) -> None:
        self.result = self.target()

def StartAnalysis():
    """
    runs the InstaTool analysis
    """
    loggedUsername = box_nomeUtenteLoginato.get(1.0, "end-1c")
    usernameToAnalyze = box_nomeUtenteDaAnalizzare.get(1.0, "end-1c")
    saveMemory(loggedUsername, usernameToAnalyze)

    analyzer = ReturnableThread(target=lambda: InstaTool.executeAnalysis(loggedUsername, usernameToAnalyze, myApp = status))
    refresher = threading.Thread(target=lambda: Refresher(analyzer))
    analyzer.start()
    refresher.start()
    threads.append(analyzer)
    threads.append(refresher)

# status of the app
class AppStatus:
    def __init__(self):
        self.code = 0
        self.perc = 0.0
    def UpdateStatus(self, newStatus) -> None:
        self.code = newStatus
    def UpdatePerc(self, perc) -> None:
        self.perc = perc
status = AppStatus()

oldCode = 0
def UpdateLabel():
    """
    Updates the label with the status of the app
    """
    global oldCode
    try:
        if status.code != oldCode:
            color = colour_text
            if status.code>200 and status.code<400:
                color = colour_text_success
            elif status.code>400 and status.code<500:
                color = colour_text_error
            update.config(text = updateLabelText[status.code], fg=color)
            window.update()
            oldCode = status.code
        if status.code > 700:
            update.config(text = updateLabelText[status.code]+" "+str(round(status.perc))+"%")
            window.update()
    except:
        print("Error in updating the label")

def Refresher(analyzerThread):
    """
    Checks on the analysis thread, updates the label and gets the results once the analysis is done
    """
    global fileName_fan, fileName_unrequited, fileName_followers, fileName_followees, list_newFollow, list_newUnfollow
    oldCode = 0
    while analyzerThread.is_alive():
        UpdateLabel()
        print("still alive")
        time.sleep(0.1)
    print("Exited while")
    analyzerThread.join()
    print("Joined")
    UpdateLabel()
    try:
        fileName_fan, fileName_unrequited, fileName_followers, fileName_followees, list_newFollow, list_newUnfollow = analyzerThread.result
        list1.delete(0,tk.END)
        for line in list_newUnfollow:
            list1.insert(tk.END, str(line))
        list2.delete(0,tk.END)
        for line in list_newFollow:
            list2.insert(tk.END, str(line))
    except:
        print("Error in getting the results")
    print("Terminated")
    return


# APP GUI -----------------------------------------------------------------------------------------------
# initialising window
window = tk.Tk()
window.geometry("750x580")
window.title("Insta tool")
window.resizable(True, True)
window.configure(background=colour_bg)

# loading icon
icon_path = resource_path("rsc/InstaTool_icon.png")
try:
    icon = tk.PhotoImage(file = icon_path)
except:
    print("impossible to load icon")
else:
    window.iconphoto(False,icon)

# Instructions
title = tk.Label(master=window,text="InstaTool",fg=colour_text_error,bg=colour_bg,font=("Arial", 14))
title.pack(side=tk.TOP)
text = tk.Label(master=window,text="To run the program you need to login to your Instagram account using the Firefox web browser\n"+
                    "-In the 'Logged username' box you need to insert your username\n"+
                    "-In the 'Username to analyze' box you have to insert the username of the account you want to analyze\n"+
                    "In order for it to work this account must be public or followed by the logged in user (it can be yourself if you want to analyze your account)\n"+
                    "Once you put the correct usernames in the boxes click 'Run' and wait for the results wich will be saved in 4 text files",bg=colour_bg,fg=colour_text)
text.pack(side=tk.TOP)

# textbox to input usernames
loggedUsername, usernameToAnalyze  = readMemory()
frame_input = tk.Frame(window, bg=colour_bg2,height=40)
frame_input.pack(side = tk.TOP,pady=15,fill=tk.Y)
text_nomeUtenteLoginato = tk.Label(frame_input, text="Logged username:",bg=colour_bg2,fg=colour_text, font=("Arial", 11))
text_nomeUtenteLoginato.grid(row=0,column=0,pady=3, padx=3)
box_nomeUtenteLoginato = tk.Text(frame_input, height = 1, width = 20)
box_nomeUtenteLoginato.insert(0.0,loggedUsername)
box_nomeUtenteLoginato.grid(row=0,column=1,pady=3,padx = 5)

text_nomeUtenteDaAnalizzare = tk.Label(frame_input, text="Username to analyze:",bg=colour_bg2,fg=colour_text, font=("Arial", 11))
text_nomeUtenteDaAnalizzare.grid(row=1,column=0,pady=3,padx=3)
box_nomeUtenteDaAnalizzare = tk.Text(frame_input, height = 1, width = 20)
box_nomeUtenteDaAnalizzare.insert(0.0,usernameToAnalyze)
box_nomeUtenteDaAnalizzare.grid(row=1,column=1,pady=3,padx = 5)

# button to start the analysis
run_button = tk.Button(master=window,text="Run", command=StartAnalysis,bg=colour_text_success)
run_button.pack(side = tk.TOP)    

# update label (used when the analysis runs)
update = tk.Label(window, text="Update: waiting", background=colour_bg, fg=colour_text, font=("Arial", 11))
updateStatus = 0
update.pack(side=tk.TOP)

# frame and buttons to open the lists
frame_FileButtons = tk.Frame(window, bg = colour_azzurro)
frame_FileButtons.pack(side=tk.TOP,pady=10)

followers_button = tk.Button(master=frame_FileButtons,text="Followers list", command=lambda: openFile_asWindow(fileName_followers))
followers_button.grid(row=0, column=0, sticky="nsew", padx = 20, pady=10)
followees_button = tk.Button(master=frame_FileButtons,text="Followees list", command=lambda: openFile_asWindow(fileName_followees))
followees_button.grid(row=0, column=1, sticky="nsew", padx = 20, pady=10)
fans_button = tk.Button(master=frame_FileButtons,text="Fans list", command=lambda: openFile_asWindow(fileName_fan))
fans_button.grid(row=1, column=0, sticky="nsew", padx = 20, pady=10)
unrequited_button = tk.Button(master=frame_FileButtons,text="Unrequited list", command=lambda: openFile_asWindow(fileName_unrequited))
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
crediti = tk.Label(window,text="2024 Francesco Bittasi")
crediti.pack(side = tk.RIGHT)

# handles the closing of the window
def on_closing():
    window.destroy()
    print("closing...")
    for t in threads:
        t.join()
    print("all threads closed")
    sys.exit(0)
window.protocol("WM_DELETE_WINDOW", on_closing)

# main loop (runs the program)
if __name__ == "__main__":
    window.mainloop()

# pyinstaller InstaTool.spec