# Import Module
import ftplib
import time
import Data_Buffer
import CheckSync

# Fill Required Information
import Setings

HOSTNAME = "ftp.dlptest.com"
USERNAME = "dlpuser@dlptest.com"
PASSWORD = "rNrKYTX9g7z3RgJRmxWuGHbeu"
# check site https://dlptest.com/ftp-test/ for see password

def makeFileSyncr():
    import json

    aList = Data_Buffer.data
    jsonString = json.dumps(aList)
    jsonFile = open("data" + str(Setings.server_nr) + ".json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def sendFile(filename):
    while True:
        time.sleep(5)

        makeFileSyncr()

        # Connect FTP Server
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

        # force UTF-8 encoding
        ftp_server.encoding = "utf-8"

        print(filename, " is Send by tcp")

        # Read file in binary mode
        with open(filename, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR {filename}", file)

        # Get list of files
        ftp_server.dir()

        # Close the Connection
        ftp_server.quit()

def donwldFile(filename):
    while True:
        time.sleep(6)
        # Connect FTP Server
        ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

        # force UTF-8 encoding
        ftp_server.encoding = "utf-8"

        # Write file in binary mode
        with open(filename, "wb") as file:
            # Command for Downloading the file "RETR filename"
            ftp_server.retrbinary(f"RETR {filename}", file.write)

        # Get list of files
        ftp_server.dir()

        # Display the content of downloaded file
        file = open(filename, "r")
        print('File Content:', file.read())

        # Close the Connection
        ftp_server.quit()

        sync = CheckSync.checkSync()
        if sync > 0:
            print("Sincronizing ")
