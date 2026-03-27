from telethon import TelegramClient, events, sync
# from telethon.tl.types import InputMessagesFilterRoundVoice
import telethon.tl.types
import os.path
#from os.path import exists
import logging
import cleanup_filename
'''
Notice:
This program uses the Telegram API and is part of the Telegram ecosystem.
Downloader with archiving functionality and media filter option 
'''

# Input parameter:
fullpath = r"f:\path\to\your\targetfolder"  # The folder where your files and the ID repository file are to be saved.
channel = "channelname"  # Type here in the channel's name. The full link  https://t.me/channelname should work too.
limit = 10  # value which indicates how many files you want to download, set it to <None> for no limit
media_filter = None  # Possible options: "Audio" | "Speech" | "Video" | "Photo" | "PhotoVideo"
api_id = 1234567  # get your api_id from https://core.telegram.org/api/obtaining_api_id#obtaining-api-id
api_hash = 'pasteHereYourAPIhash'  # get your api_hash from https://core.telegram.org/api/obtaining_api_id#obtaining-api-id
# --- You're done now. Start the program. --- 

os.chdir(fullpath)  # Change working directory to target directory
logging.basicConfig(filename='telegram-downloader-log.log', filemode='w', level=logging.INFO)

media_dict = {
"Audio":telethon.tl.types.InputMessagesFilterMusic,
"Speech":telethon.tl.types.InputMessagesFilterVoice,
"Video":telethon.tl.types.InputMessagesFilterVideo,
"Photo":telethon.tl.types.InputMessagesFilterPhotos,
"PhotoVideo":telethon.tl.types.InputMessagesFilterPhotoVideo  # Filter for messages containing photos or videos.
# "Alles":telethon.tl.types.TypeMessageMedia
}

filter_selected = media_dict.get(media_filter)  # Modus-Filter für Telegram wird aus Dict selektiert, Achtung: get_messages-Funktion nimmt nur MessagesFilter, kein z.B. telethon.tl.types.TypeMessageMedia!
print("Media modus selected:", str(media_filter))

client = TelegramClient('Telegram-Downloader', api_id, api_hash)
print("Starting Client")
client.start()
logging.info("Client startet")

print("Collect entries")
msgs = client.get_messages(entity=channel, limit=limit, filter=filter_selected)
print(len(msgs), "entries collected")

errlist = []  # Not downloaded message-names due to error
skipped = []  # Not downloaded message-names due to already downloaded
counter = 0  # Counter how many messages are left
counter_unknown = 0  # Counter for messages left which have no name attribute

# Establishing list of voice message IDs to prevent downloading duplicates
# if not os.path.isfile('id_list.txt'):  # Prüfen ob Datei vorhanden, sonst erzeugen
#     open('id_list.txt', 'a').close()
id_rep_file = open('id_list.txt', 'a+')  # List with saved IDs, a+ for establishing as required, read + write
id_rep_file.seek(0)  # Zeiger zum Anfang setzen
id_rep = id_rep_file.read().splitlines()  # id repository

id_container = []  # List with IDs, which are being requested from Telegram
for msg in msgs:  # Collect IDs
    id_container.append(str(msg.id))

missing_id_list = list(set(id_container).difference(id_rep))  # Filtering of duplicate entries from the two lists. Result is the files to be downloaded.

for msg in msgs:
    counter += 1

    file_id = msg.id
    title = msg.text  # or possible: msg.message
    if str(file_id) in missing_id_list:  # File id is not in list, therefore download it

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

        filename = cleanup_filename.sanitize(path=fullpath, filename=filename, replace_dict=None)

        try:  # File is not yet in directory. Attempt to download it
            print("\nDownloading of No.", counter, "of", len(msgs), "\n", filename, "File ID:", msg.id)
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

        id_rep_file.write(str(file_id)+"\n")  # add downloaded file ID

    else:  # File is there, therefore do not download:
        # logging.info("Skipping title: %s, ID: %s" % (title, file_id))
        print("Skipping title: %s, ID: %s" % (title, file_id))
        # print(len(msgs) - counter, " left", "\n")
        skipped.append(title)  # Fill list of skipped files
        skipped.append(str(file_id))  # Fill list of skipped files

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

