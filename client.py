import socket
import ast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from huffman.decompression import Decompression

def getConnection():
    app = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    app.connect(("127.0.0.1", 1400))
    return app

fApi = FastAPI()

# Permettre les requêtes depuis toutes les origines
fApi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def messageInfo(app):
    type = taille = ""
    #Type
    while True:
        result = app.recv(1).decode()

        if result == "|":
            break
        
        type += result

    #Taille
    while True:
        result = app.recv(1).decode()

        if result == "|":
            break
        
        taille += result

    return type, int(taille)


def decompressFile(app):
    dictionnary = padded_text = ""
    
    # Récupérer le bytes array
    # while True:
    #     resultB = app.recv(1).decode('latin-1')
    #     if (resultB == '²'):
    #         break
    #     bytes_array += resultB

    # Récupérer le dictionnaire
    while True:
        resultD = app.recv(1).decode('latin-1')
        if (resultD == '²'):
            break
        dictionnary += resultD

    # Récupérer le padded_text
    while True:
        resultP = app.recv(1).decode('latin-1')
        if (resultP == '²'):
            break
        padded_text += resultP
    
    # Convertir dictionnary en dict
    dictionnary = ast.literal_eval(dictionnary)

    # Convertir Content en bytes
    # bytes_array = bytes_array.lstrip("b").strip("'\"")
    # bytes_array = bytes_array.encode("utf-8")
    
    actual_text = Decompression(dictionnary).decompress(padded_text)

    return actual_text


@fApi.get("/recup-files")
def getFiles():
    listFiles = []
    app = getConnection()

    app.send("0".encode())

    while True:
        type, taille = messageInfo(app)
        if type == "fini":
            break
        
        listFiles.append(app.recv(taille).decode()) 
    
    app.send("2".encode())

    return listFiles


@fApi.post("/download-file")
def downloadFile(file: str):
    app = getConnection()

    app.send("1".encode())

    lenFile = len(file)
    app.send(f'{lenFile}|{file}'.encode())

    actual_text = decompressFile(app)

    app.send("2".encode())
    return actual_text