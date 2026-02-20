from telethon import TelegramClient, events, sync
from telethon.tl.types import InputMessagesFilterRoundVoice
import os.path
#from os.path import exists
import logging

'''
Notice:
This program uses the Telegram API and is part of the Telegram ecosystem.
'''

# Input parameter:
folder = r"f:\path\to\your\targetfolder"  # The folder where your files and the ID repository file are to be saved.
channel = "channelname"  # Type here in the channel's name. The full link  https://t.me/channelname should work too.
limit = 100  # value which indicates how many files you want to download, set it to <None> for no limit
api_id = 1234567  # get your api_id from https://core.telegram.org/api/obtaining_api_id#obtaining-api-id
api_hash = 'pasteHereYourAPIhash'  # get your api_hash from https://core.telegram.org/api/obtaining_api_id#obtaining-api-id
# --- You're done now. Start the program. --- 

os.chdir(folder)  # Change working directory to target directory
logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)

client = TelegramClient('session_name', api_id, api_hash)
print("Starting Client")
client.start()
logging.info("Client startet")

print("Collect entries")
msgs = client.get_messages(entity=channel, limit=limit, filter=InputMessagesFilterRoundVoice)
print(len(msgs), "entries collected")

errlist = []  # Not downloaded message-names due to error
skipped = []  # Not downloaded message-names due to already downloaded
counter = 0  # Counter how many messages are left
counter_unknown = 0  # Counter for messages left which have no name attribute

# Establishing list of voice message IDs to prevent downloading duplicates
id_rep_file = open('id_list.txt', 'a')  # List with saved IDs, a+ for establishing as required, read + write
id_rep = id_rep_file.read().splitlines()  # id repository
id_container = []  # List with IDs, which are being requested from Telegram

for msg in msgs:  # Collect IDs
    id_container.append(msg.file.id)

missingidlist = list(set(id_container).difference(id_rep))  # Filtering of duplicate entries from the two lists. Result is the files to be downloaded.

for msg in msgs:
    counter += 1

    file_id = msg.file.id
    title = msg.text  # or possible: msg.message
    if any(file_id in s for s in missingidlist):  # File id is not in list, therefore download it

        ext = msg.file.ext
        creatime = msg.date.date().isoformat()  # Date format: yyyy-mm-dd
        views = msg.views  # save views
        views = round(views / 100) * 100  # Round to hundreds
        views = str(views)  # convert into string

        if title:  # oder möglich: msg.message
            filename = creatime + " " + title + " " + views + "views" + ext  # Name + file extension
        else:
            filename = creatime + " unknown" + str(counter_unknown) + " " + views + "views" + ext
            counter_unknown += 1

        # Replace characters which are not supported in Windows
        filename = filename.replace("\n", " - ")
        filename = filename.replace("\\", "-")
        filename = filename.replace("/", "-")
        filename = filename.replace("?", "-")
        filename = filename.replace("\"", "!")
        filename = filename.replace(r"*", " ! ")
        filename = filename.replace(r"<", " ! ")
        filename = filename.replace(r">", " ! ")
        filename = filename.replace(r":", " - ")

        try:  # File is not yet in directory. Attempt to download it
            print("Downloading of No.", counter, "of", len(msgs) - counter, "\n", filename, "File ID:", msg.file.id)
            msg.download_media(filename)
            print("msg:", filename, "downloaded")
            # print(len(msgs) - counter, " left", "\n")
        except Exception as inst:
            print(type(inst))  # the exception instance
            print(inst.args)  # arguments stored in .args
            print(inst)  # __str__ allows args to be printed directly,
            # print ("msg:\n", filename, "\ncould not be downloaded")
            logging.info("msg:", filename, "ID:", file_id, "could not be downloaded\n")
            errlist.append(filename)

        id_rep_file.write(file_id+"\n")  # add downloaded file ID

    else:  # File is there, therefore do not download:
        logging.debug("Skipping title: %s, ID: %s" % (title, file_id))

        print(len(msgs) - counter, " left", "\n")
        skipped.append(title)  # Fill list of skipped files
        skipped.append(file_id)  # Fill list of skipped files

id_rep_file.close()
client.disconnect()

errlist_string = "\n".join(errlist)  # Convert in string for logger
skipped_string = "\n".join(skipped)  # Convert in string for logger

# print("Downloading entries finished\n")
logging.info("\nDownloading entries finished")
# print("Could not be downloaded:", errlist, "\n")
logging.info("Could not be downloaded:\n + %s" % errlist_string)
# print("Number of skipped files:", len(skipped), "\n", "Files:", skipped)
logging.info("Skipped files:\n %s" % skipped_string)

# os.system("shutdown -s -t 10")  # Shutdown computer, last number is timer in seconds

