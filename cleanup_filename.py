"""
Umbenennen von Dateinamen
Gemäß max_len_path werden die letzten Stellen des Dateinamens (ohne Dateiendung) abgeschnitten
"""

import unicodedata
import pathlib
import os
import re

max_len_path = 180 #259

# def remove_signature(split_word)  # Entfernt ein wiederkehrendes Muster, Signatur 


def sanitize(path, filename, replace_dict=None):

    if replace_dict:
        for regkey, replval in replace_dict.items():
            filename = regkey.sub(replval, filename)
    
    # ASCII-Zeichen ersetzen
    filename = unicodedata.normalize('NFKC', filename).encode('latin-1', 'ignore').decode("latin-1")  # Nur Ascii-Zeichen, NFC und NFKC lassen ß sowie Umlaute unberührt
    # filename = filename.replace(",", " ")  
    filename = filename.replace("\n", " - ")  # "\n" ersetzen mit Bindestrich
    filename = filename.replace("\\", "-")  
    filename = filename.replace("/", "-")  
    filename = filename.replace("?", "-") 
    filename = filename.replace("\"", "!")  
    filename = filename.replace("*", " ! ")  
    filename = filename.replace("<", " ! ")  
    filename = filename.replace(">", " ! ")  
    filename = filename.replace(":", " - ")  
    filename = filename.replace("  ", " ")  # doppelte Leerzeichn mit einem ersetzen
    filename = filename.strip()

    #  Pfadlänge auf ggf. unter 260 kürzen
    pathges = path + filename
    lenpathges = len(pathges)
    if lenpathges > max_len_path:
        name = os.path.splitext(filename)[0]  # Dateiname ohne Dateiendung
        ext = os.path.splitext(filename)[-1]  # Dateiendung
        len_name = len(name)
        new_len_file = lenpathges - max_len_path  # Berücksichtigung des Punktes am Ende und der Dateiendung: max. 4 Zeichen
        len_name -= new_len_file
        name = name[:len_name]

        # filename = os.path.join(name, ext)
        filename = name + ext
        # print("len filename", len(path+name+ext))

    return filename


if __name__ == "__main__":

    targetpath = r"f:\Hörbücher + Podcasts\Diplomateninterviews"
    # targetpath = r"f:\Hörbücher + Podcasts\Diplomateninterviews\test"
    # replace_dict=None

    # Umbenennen der Dateien
    files = os.listdir(targetpath)
    for index, file in enumerate(files):
        print("Bearbeite Index:", index)
        new_filename = sanitize(path=targetpath, filename=file)
        os.rename(src=os.path.join(targetpath, file), dst=os.path.join(targetpath, new_filename))
    # os.rename(, os.path.join(path, ''.join([str(index), '.jpg'])))
