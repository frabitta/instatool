import os
# Create a directory in the user's home directory to store data
home = os.path.expanduser("~")
data = os.path.join(home, ".instatool")
print(data)
os.makedirs(data, exist_ok=True)

"""
# Create a file in the data directory
f = open(os.path.join(data,"fileName"), mode="w")
f.write("toto")
"""

def openFileFromDataDir(nomeFile, m):
    f = open(os.path.join(data,nomeFile), mode=m)
    return f

def writeListToFile(nomeFile,lista,tot,status):
    """
    takes a list and print that on a file with the name specified
    """
    f = openFileFromDataDir(nomeFile, "w")
    i = 1
    for x in lista:
        f.write(str(x.username)+"\n")
        perc = i/tot * 100
        if status != None:
            status.UpdatePerc(perc)
        i += 1
    f.close()

def compareFiles_toFile(nomeFile1,nomeFile2,nomeFileOutput):
    """
    prints on nomeFileOutput every line of file2 that's not incuded in file1
    """
    file1 = openFileFromDataDir(nomeFile1, "r")
    file2 = openFileFromDataDir(nomeFile2, "r")
    list = file1.read()
    fileOutput = openFileFromDataDir(nomeFileOutput, "w")
    for line in file2:
        if line not in list:
            fileOutput.write(str(line))
    file1.close()
    file2.close()
    fileOutput.close()

def compareFiles_toList(nomeFile1,nomeFile2):
    """
    returns a list made of the lines in file2 not included in file1
    """
    file1 = openFileFromDataDir(nomeFile1, "r")
    file2 = openFileFromDataDir(nomeFile2, "r")
    list_f1 = file1.read()
    difference = []
    for line in file2:
        if line not in list_f1:
            difference.append(str(line))
    file1.close()
    file2.close()
    return difference

def copyFile(src_name, dst_name):
    """
    copies src content in dst
    """
    dst = openFileFromDataDir(dst_name, "w")
    try:
        src = openFileFromDataDir(src_name, "r")
    except:
        print("Update: no previous analysis on this account...")
        return
    else:    
        for line in src:
            dst.write(str(line))
        src.close()

    dst.close()
