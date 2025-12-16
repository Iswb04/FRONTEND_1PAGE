import sqlite3

conn = sqlite3.connect("login.db")
cursor = conn.cursor()

nome = "isabella gay" 

cursor.execute(
    "DELETE FROM usuarios WHERE nome = ?",
    (nome,)
)


"""cursor.execute(
    "DELETE FROM usuarios"
)
"""


conn.commit()
conn.close()

print("Usuário apagado com sucesso")
