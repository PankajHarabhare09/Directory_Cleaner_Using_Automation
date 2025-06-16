import os
import sys
import schedule
import time
import hashlib

#This function is perform for make ensure the data is preent in that file
def CalculateCheckSum(path , BlockSize = 1024):
    #open file in reading binary mode
    fobj = open(path , "rb")#rb means READING BINARY

    #creating object of hashlib with the help of md5 class
    #md5 class helps to  create a 32-characters hash number
    hobj = hashlib.md5()

    buffer = fobj.read(BlockSize)

    while(len(buffer) > 0):
        hobj.update(buffer)
        buffer = fobj.read(BlockSize)

    fobj.close()

    #hexdigest method use to represent created 32-character hash number
    return hobj.hexdigest()


#This function perform for detect the files or changes of that file(DirectoryWatcher)
def DirectoryWatcher(DirName = "Test"):

    #check is given directory is absolute or relative
    chkDir = os.path.isabs(DirName)
    #if path is not absolute then convert it into absolute
    if chkDir == False:
        DirName = os.path.abspath(DirName)
        
    #check the given directory is exists or not
    chkDirExists = os.path.exists(DirName)
    if chkDirExists == False:
        print("--> Given Path is Not Exists <--")
        exit()

    #check the given directory is using the path or not
    chkDirPath = os.path.isdir(DirName)
    if chkDirPath == False:
        print("--> The Path is Valid But The Target Not In A Directory <--")
        exit()

     #os.walk use to traverse the given directory
    for FolderName , SubFolderNames , FileNames in os.walk(DirName):
        for fname in FileNames:
            fname = os.path.join(FolderName , fname)
            chksum = CalculateCheckSum(fname)

            print("File Name Is: ",fname)
            print("CheckSum Is: ",chksum)

            print()
    timestamp = time.ctime()

    filename = "TestLog%s.Log"%(timestamp) #(%) used to formating time in string
    filename = filename.replace(" " ,"_")
    filename = filename.replace(":" ,"_")

    fobj = open(filename , "w")

    Border = "-" * 54

    fobj.write(Border + "\n")
    fobj.write("---------> This is Directory Cleaner Script <---------\n")
    fobj.write(Border + "\n")

    fobj.write(Border + "\n")
    fobj.write("This Log File Created At: \n" + timestamp + "\n")
    fobj.write(Border + "\n")


#This Function is perform for find duplicate files 
def FindDuplicate(DirName = "Test"):
    chkDir = os.path.isabs(DirName)
    if chkDir == False:
        chkDir = os.path.abspath(DirName)
    
    chkDirExists = os.path.exists(DirName)
    if chkDirExists == False:
        print("--> Given Path is Not Exists <--")
        exit()
    
    chkDirPath = os.path.isdir(DirName)
    if chkDirPath == False:
        print("--> The Path is Valid But The Target Not In A Directory <--")
        exit()

    #creating dictonary for stroing duplicate files
    Duplicate = {}

    for FolderName , SubFolderNames , FileNames in os.walk(DirName):
        for fname in FileNames:
            #join the path
            fname = os.path.join(FolderName , fname)
            chksum = CalculateCheckSum(fname)

            #if checksum is already present then this file is duplicate
            #so its  added in list
            if chksum in Duplicate:
                Duplicate[chksum].append(fname)
            #else its create new list with the path
            else:
                Duplicate[chksum] = [fname]

    return Duplicate

#This Fuction is perform for display duplicate file Name And its count
def DisplayResult(MyDictonary):

    #we using filter because it collect only those file which is  duplicated
    Result = list(filter(lambda x: len(x) > 1 , MyDictonary.values()))
    
    #Count is used to count the dupplicate values
    count = 0

    #loop for each group of duplicate files
    for value in Result:
        #loop for each file in group of duplicate files
        for subvalue in value:
            #increment when the duplicate file found
            count = count + 1
            print(subvalue)
        print("<-------------------------------->")
        print("Count of Duplicate Files: ",count)
        print("<-------------------------------->")
        #Resets the value of count for new Group of Duplicate file
        count = 0

#This Function perform for delete the Duplicates Files
def DeleteDuplicates(MyPath = "Test"):
    #storing the Duplicates in MyDictonary Variable
    MyDictonary = FindDuplicate(MyPath)

    #we using filter because it collect only those file which is  duplicated
    Result = list(filter(lambda Dict: len(Dict) > 1 , MyDictonary.values()))

    #Count is used to count the dupplicate values
    count = 0

    #DeletedCount is used for count the deleted files
    DeletedCount = 0

    ##loop for each group of duplicate files
    for value in Result:
        #loop for each file in group of duplicate files
        for subvalue in value:
            #increment when the duplicate file found
            count = count + 1

            #if the count of file is greater than 1 then me remove the file
            if count > 1:
                print("Deleted File: ",subvalue)
                os.remove(subvalue)
                DeletedCount = DeletedCount + 1

        #Resets the value of count for new Group of Duplicate file  
        count = 0
    print("Deleted File Count is: ",DeletedCount)

#MAIN FUNCTION
def main():
    Border = "-"*54
 
    print(Border)
    print("----------------- Directory Cleaner ------------------")
    print(Border)

    if len(sys.argv) ==  2:
        # --h means HELP Its Provide Information to new User
        if ((sys.argv[1] == "--h") or (sys.argv[1] == "--H")): 
            print("--> This Is Application Is Used To Perform Directory Cleaning <--")
            print("--> This is Automation Script <--")
            
        #--u Means How To Use Like (Manual of Any Toy)
        elif((sys.argv[1] == "--u") or (sys.argv[1] == "--U")):
            print("--> USE THE GIVEN SCRIPT AS <--")
            print("--> ScriptName.py NameOfDirectory TimeTraversal <--")
            print("--> NOTE: \n PLEASE PROVIDE VALID ABSOLUTE PATH")

        '''
        USED FOR TESTING THE FUNCTIONS
        else:
            
            DirectoryWatcher(sys.argv[1])
            Result = FindDuplicate(sys.argv[1])
            DeleteDuplicates(Result)
        '''

    if len(sys.argv) == 3:
        schedule.every(int(sys.argv[2])).minutes.do(DeleteDuplicates)

        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("--> INVALID NUMBER OF COMMAND LINE ARGUMENTS <--")
        print("--> USE THE GIVEN FLAGS AS <--")
        print("--> --h Used To Display The HELP <--")
        print("--> --u Used To Display The USAGE <--")

        print(Border)
        print("----------- Thank You For Using This Script -----------")
        print(Border)

if __name__ == "__main__":
    main()

'''
OUTPUT

    ------------------------------------------------------
    ----------------- Directory Cleaner ------------------
    ------------------------------------------------------
    Deleted File:  Test\Automation1 - Copy.py
    Deleted File:  Test\Automation1.py
    Deleted File:  Test\Automation2 - Copy.py
    Deleted File:  Test\Automation2.py
    Deleted File:  Test\Automation3 - Copy.py
    Deleted File:  Test\Automation3.py
    Deleted File:  Test\Automation4 - Copy.py
    Deleted File:  Test\Automation4.py
    Deleted File:  Test\WhatsApp Video 2025-06-13 at 19.34.56_f00b4837 - Copy (3).mp4
    Deleted File:  Test\WhatsApp Video 2025-06-13 at 19.34.56_f00b4837 - Copy.mp4
    Deleted File:  Test\WhatsApp Video 2025-06-13 at 19.34.56_f00b4837.mp4
    Deleted File Count is:  11

'''