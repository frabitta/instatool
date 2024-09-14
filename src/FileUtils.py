def writeListToFile(nomefile,lista,tot,status):
    """
    takes a list and print that on a file with the name specified
    """
    f = open(nomefile,"w")
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
    file1 = open(nomeFile1,"r")
    file2 = open(nomeFile2,"r")
    list = file1.read()
    fileOutput = open(nomeFileOutput,"w")
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
    file1 = open(nomeFile1,"r")
    file2 = open(nomeFile2,"r")
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
    dst = open(dst_name, "w")
    try:
        src = open(src_name, "r")
    except:
        print("Update: no previous analysis on this account...")
        return
    else:    
        for line in src:
            dst.write(str(line))
        src.close()

    dst.close()
