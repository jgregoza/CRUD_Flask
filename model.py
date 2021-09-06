import json

def load_db():
    with open("flahscards_db.json") as f:
        return json.load(f)


# la fucion load_db lee el archivo con las tarjetas y luego esto
# se almacena en la variable "db"


def save_db():
    with open("flahscards_db.json", 'w') as f:
        return json.dump(db, f, indent=4, sort_keys=True)   # los parametos de ident y sort_key ordenan el objeto o diccionario


# Writing JSON content to a file using the dump method
# #Use dumps to convert the object to a serialized string
# se pasa como parametro "db" ya que ahi se almacenan las cartas(lista/diccionario)

db = load_db()

# se esta usando un file Json para simular la capa de BD en Flask.