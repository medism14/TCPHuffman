import socket
import threading
import os

from huffman.compression import Compression

app = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app.bind(("127.0.0.1", 1400))

app.listen()

class ThreadLaunch(threading.Thread): 
    def __init__(self, info):
        super().__init__()
        self.conn = conn

    def EventFiles(self, file):
        fileEncoded = file.encode()
        tailleMsg = len(fileEncoded)
        self.conn.send(f'txt|{tailleMsg}|'.encode())
        self.conn.send(fileEncoded)

    def recupLink(self):
        file = taille = ""
        while True:
            result = self.conn.recv(1).decode()

            if (result == '|'):
                break

            taille += result
            
        taille = int(taille)
        file = self.conn.recv(taille).decode()
        return file
    
    def run(self):
        while True:
            action = self.conn.recv(1).decode()

            if action == "0":
                ##Recuperer les fichiers
                urlFichiers = "C:/Users/Etudiant/Desktop/Personnel/Université/M1/S2/Programmation parallèle/projet/files"
            
                for _, _, files in os.walk(urlFichiers):
                    for file in files:
                        self.EventFiles(file)

                self.conn.send(f'fini|0|'.encode())

            elif action == "1":
                ##Télécharger un fichier
                file = self.recupLink()
                urlDowFile = f"C:/Users/Etudiant/Desktop/Personnel/Université/M1/S2/Programmation parallèle/projet/files/{file}"

                ##Compresser le fichier et l'envoyer à l'utilisateur
                dictionnary, padded_text = Compression(urlDowFile).compress()

                self.conn.send(f"{dictionnary}²".encode('latin-1'))
                self.conn.send(f"{padded_text}²".encode('latin-1'))

            elif action == "2":
                ##Déconnexion
                self.conn.close()
                break

while True:
    conn, _ = app.accept()
    ThreadLaunch(conn).start()  
