# Face_recognition
Projet de reconnaissance faciale python
il faut crée tout d'abord la base de donnée pour éxecuter le code
----------------------------------------------------------------
#creation d'une base de donnée
import sqlite3

fichierD = "C:/bd/image.sq3"

conn = sqlite3.connect(fichierD)
curr = conn.cursor()

curr.execute("CREATE TABLE IF NOT EXISTS ImageData ( id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,img BLOP);")


conn.commit()

#il faut ajouter en suite les information des personnes 
#exemple
import sqlite3

fichierD = "C:/bd/image.sq3"
name="louay"
conn = sqlite3.connect(fichierD)
curr = conn.cursor()
with open("C:\Users\loayk\PycharmProjects\pythonProject3\ImagesAttendAnce", "rb") as f:
    data = f.read()
m=curr.execute("""
INSERT INTO ImageData VALUES(?,?,?)""",(50,name,data))

conn.commit()
curr.close()
conn.close()


