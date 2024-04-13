import socket
import ast
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Content(BaseModel):
    content: str
    fileName: str

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
    allow_methods=["GET", "POST", "DELETE"],
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
     
    app.send("3".encode())

    return listFiles


@fApi.post("/download-file")
def downloadFile(file: str):
    app = getConnection()

    app.send("1".encode())

    fileEncoded = file.encode()
    lenFile = len(fileEncoded)
    app.send(f'{lenFile}|{file}'.encode())

    lenContent = ""
    while True:
        result = app.recv(1).decode()

        if result == '|':
            break
            
        lenContent += result

    lenContent = int(lenContent)
    content = app.recv(lenContent).decode()

    app.send("3".encode())
    return content

@fApi.post("/save-file")
def saveFile(content: Content):

    app = getConnection()

    app.send("2".encode())

    fileName = content.fileName
    content = content.content

    fileNameEncoded = fileName.encode()
    contentEncoded = content.encode()

    contentLen = len(contentEncoded)
    fileNameLen = len(fileNameEncoded)

    app.send(f'{contentLen}|{content}'.encode())
    app.send(f'{fileNameLen}|{fileName}'.encode())

    app.send("3".encode())

@fApi.delete("/remove-file")
def RemoveFile(file: str):

    app = getConnection()

    app.send("4".encode())

    lenFile = len(file.encode())

    app.send(f"{lenFile}|{file}".encode())

    app.send("3".encode())