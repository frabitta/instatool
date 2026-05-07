#SAVE SESSION ---------------------- source: https://instaloader.github.io/troubleshooting.html
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

def import_session(cookiefile):
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
    instaloader.context.username = username
    instaloader.save_session_to_file()

def saveSession():
    import_session(get_cookiefile())
#END SAVE SESSION --------------------------------------------------------------

import instaloader
import FileUtils
import sys

# name of the generated files
BASE_nomeFileElencoFollowees = "Followees_list"
BASE_nomeFileElencoFollowers = "Followers_list"
BASE_nomeFileOutputUnrequited = "Unrequited_list"
BASE_nomeFileOutputFan = "Fan_list"

def getStatusCodes():
    return statusCodes

statusCodes = {
    0: "Update: waiting",
    1: "Update: initialising analysis...",
    2: "Update: saving session...",
    3: "Update: loading session...",
    4: "Update: opening profile...",
    5: "Update: loading followees list...",
    6: "Update: loading followers list...",
    7: "Update: creating unrequited users list...",
    8: "Update: creating fans list...",
    201: "Update: session saved",
    202: "Update: session loaded",
    203: "Update: profile opened",
    204: "Update: unrequited users list created",
    205: "Update: fan users list created",
    209: "Update: finished!",
    401: "Error: unable to save the session.",
    402: "Error: unable to load the session.",
    403: "Error: unable to open the profile.",
    404: "Error: unable to create unrequited users list.",
    405: "Error: unable to create fan users list.",
    701: "Update: loading followees list...",
    702: "Update: loading followers list...",
}

appStatus = None
def updateStatus(code):
    """
    Prints the status of the analysis and
    updates the status of the app if present
    """
    print(statusCodes[code])
    if appStatus != None:
        appStatus.UpdateStatus(code)

def generateFilesNames(username):
    """
    Generates the names of the files that will be created
    """
    fileName_followees = username+"_"+BASE_nomeFileElencoFollowees+".txt"
    fileName_followers = username+"_"+BASE_nomeFileElencoFollowers+".txt"
    fileName_unrequited = username+"_"+BASE_nomeFileOutputUnrequited+".txt"
    fileName_fan = username+"_"+BASE_nomeFileOutputFan+".txt"
    return fileName_followees, fileName_followers, fileName_unrequited, fileName_fan

def executeAnalysis(loggedUsername, usernameToAnalyze, myApp = None):
    """
    Executes the analysis of the user, takes as arguments:
    - usernames of the logged user and the user to analyze
    - app status if ran by the gui app
    """
    global appStatus
    appStatus = myApp

    updateStatus(1)
    # gets the usernames fron the text boxes in the window
    nomeUtenteLoginato = loggedUsername
    nomeUtenteDaAnalizzare = usernameToAnalyze
    
    fileName_followees, fileName_followers, fileName_unrequited, fileName_fan = generateFilesNames(nomeUtenteDaAnalizzare)
    list_newFollow = []
    list_newUnfollow = []

    # saves the current firefox session to access instagram
    updateStatus(2)
    try:
        saveSession()
    except:
        updateStatus(401)
        return
    else:
        updateStatus(201)

    # load the instagram session saved before with instaloader
    updateStatus(3)
    L = instaloader.Instaloader()
    try:
        L.load_session_from_file(nomeUtenteLoginato)
    except:
        updateStatus(402)
        return
    else:
        updateStatus(202)

    # opens the profile we want to do the analysis on
    updateStatus(4)
    try:
        profile = instaloader.Profile.from_username(L.context,nomeUtenteDaAnalizzare)
    except:
        updateStatus(403)
        return
    else:
        updateStatus(203)

    # creates a file with a list of all the followees of that user
    updateStatus(701)
    followeesList = profile.get_followees()
    FileUtils.writeListToFile(fileName_followees,followeesList,followeesList.count,appStatus)

    # creates a file with a list of all the followers of that user
    updateStatus(702)
    followersList = profile.get_followers()
    FileUtils.copyFile(fileName_followers,"old.txt")
    FileUtils.writeListToFile(fileName_followers,followersList,followersList.count,appStatus)

    #updates the two displayed lists with the new followers and unfollows
    list_newFollow = FileUtils.compareFiles_toList("old.txt",fileName_followers)
    list_newUnfollow = FileUtils.compareFiles_toList(fileName_followers,"old.txt")

    # compares the two files generated before and creates another one with the list of all the unrequited users
    updateStatus(7)
    try:
        FileUtils.compareFiles_toFile(fileName_followers,fileName_followees,fileName_unrequited)
    except:
        updateStatus(404)
        return
    else:
        updateStatus(204)

    # compares the two files generated before and creates another one with the list of all the users that our user don't follow back
    updateStatus(8)
    try:
        FileUtils.compareFiles_toFile(fileName_followees,fileName_followers,fileName_fan)
    except:
        updateStatus(405)
        return
    else:
        updateStatus(205)
    
    FileUtils.deleteFileFromDataDir("old.txt")
    updateStatus(209)
    print("Nome file followees: "+fileName_followees)
    print("Nome file followers: "+fileName_followers)
    print("Nome file unrequited: "+fileName_unrequited)
    print("Nome file fan: "+fileName_fan)
    print("Nuovi follow: "+str(list_newFollow))
    print("Nuovi unfollow: "+str(list_newUnfollow))
    return fileName_fan, fileName_unrequited, fileName_followers, fileName_followees, list_newFollow, list_newUnfollow

# decomment this to run the script from the terminal
"""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: InstaTool.py <loggedUsername> <usernameToAnalyze>")
    else:
        executeAnalysis(sys.argv[1],sys.argv[2])
"""