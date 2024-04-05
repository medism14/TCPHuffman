import socket
import threading
import os
import json

from huffman.compression import Compression

app = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app.bind(("127.0.0.1", 1400))

app.listen()

class ThreadLaunch(threading.Thread): 
    def __init__(self, info):
        super().__init__()
        self.info = info

    def EventFiles(self, file):
        fileEncoded = file.encode()
        tailleMsg = len(fileEncoded)
        self.info.send(f'txt|{tailleMsg}|'.encode())
        self.info.send(fileEncoded)

    def recupLink(self):
        file = taille = ""
        while True:
            result = self.info.recv(1).decode()

            if (result == '|'):
                break

            taille += result
            
        taille = int(taille)
        file = self.info.recv(taille).decode()
        return file
    
    def run(self):
        
        while True:
            action = self.info.recv(1).decode()

            if action == "0":
                ##Recuperer les fichiers
                urlFichiers = "C:/Users/Etudiant/Desktop/Personnel/Université/M1/S2/Programmation parallèle/projet/files"
            
                for _, _, files in os.walk(urlFichiers):
                    for file in files:
                        self.EventFiles(file)

                self.info.send(f'fini|0|'.encode())

            elif action == "1":
                ## Télécharger un fichier
                file = self.recupLink()
                urlDowFile = f"C:/Users/Etudiant/Desktop/Personnel/Université/M1/S2/Programmation parallèle/projet/files/{file}"

                ## Compresser le fichier et l'envoyer à l'utilisateur
                dictionnary, padded_text = Compression(urlDowFile).compress()

                self.info.send(f"{dictionnary}²".encode('latin-1'))
                self.info.send(f"{padded_text}²".encode('latin-1'))

            elif action == "2":
                ##Déconnexion
                self.info.close()
                break

while True:
    info, _ = app.accept()
    ThreadLaunch(info).start()  
