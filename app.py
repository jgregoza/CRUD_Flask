#from datetime import datetime
from flask import (Flask, render_template, abort, jsonify, request, redirect, url_for)

from model import db, save_db
# se importa los datos del archivo json almacenados en la variable "db"

# Creando al app

app = Flask(__name__)

# Main de la pagina

@app.route("/")
def welcome():
    return render_template( 
    "welcome.html", #   muestra el HTML con la informacion de la bd
    cards = db  # variable que contiene todas las tarjetas de la bd
    )

# Establece la vista para cada indice o carta

@app.route("/card/<int:index>") # representa "View" del patron MTV. El parametro del decorador presenta la ruta o el indice en la URL.
def card_view(index):   # muestra pagina con el indice de la tarjeta creada
    try:    # para manejar si se ingresa un indice que no esta en la base de datos.
        card = db[index]    # representa "Model" del patron MTV. Index toma como valor el 1er elemento de la base de datos. 
        return render_template("card.html", # representa "Template" del modelo MTV
                               card=card,   # muestra el indixe 1 de la BD en el HTML
                               index=index,
                               max_index=len(db)-1) # muestra el indice de la ultima tarjeta en la bd   
    except IndexError:  #   fin del bloque que maneja el error del indice
        abort(404)  # mensaje que se mostrara tras el error de indice

# Agregar cartas

@app.route('/add_card', methods=["GET", "POST"])    # se pasa como parametros los metodos HTTP a admitir debido a que se usa un Form.
def add_card():
    if request.method == "POST":    # instruccion para probar el tipo de metodo HTTP (sera POST).
        # form has been submitted, process data
        card = {"question": request.form['question'],   # request.form = atributo del modulo "request" que permite recuperar los datos para la entrada: "question".
                "answer": request.form['answer']}   ## request.form = atributo del modulo "request" que permite recuperar los datos para la entrada: "answer". Al final se unen creando un dicccionario llamado: card
        db.append(card) # escribe el diccionario en la base de datos.
        save_db()   # guarda los datos en el disco para la bd.
        return redirect(url_for('card_view', index=len(db) -1)) # funcion "redirec" toma un URL como argumento. Y para generar esa URL se usa la fun. "url_for" lo cual retoranra a la vista "card_view". Y como indice le pasamos la longitud de la bd -1 que seria el indice de la tarjeta recien creada.
    else:   # se confirma el metodo GET y con lo cual se desea retornar al formulario
        return render_template("add_card.html")

# Remover cartas

@app.route('/remove_card/<int:index>', methods=["GET", "POST"])
def remove_card(index):
    try:
        if request.method == "POST":
            del db[index]
            save_db()
            return redirect(url_for('welcome'))
        else:
            return render_template("remove_card.html", card=db[index])
    except IndexError:
        abort(404)

#simulado una API REST con Flask..

@app.route("/api/card/")
def api_card_list():
    return jsonify(db)  #   se agrega "jsonify" because "db" es una lista y no esta permitido en Flask para Api REST. Con lo cual se agrega 
                        #   la funcion jsonyfy para serializar la lista en un JSON y mostrarlo por pantalla.

@app.route('/api/card/<int:index>') # funcion REST   que toma un Indice como argumento.
def api_card_detail(index):
    try:
        return db[index]    # retorna el objeto de la tarjeta desde la BD y lo retornara como JSON y eso devolvera una respuesta RESTful.
    except IndexError:      # 
        abort(404)

# Contando views..

'''
@app.route("/date")
def date():
    return "This page was served at: " + str(datetime.now())

counter = 0

@app.route("/count_views")
def count_views():
    global counter
    counter += 1
    return "This page was served at: " + str(counter) + " times."
'''

# Inicializando la app

if __name__ == "__main__":
    app.run(debug=True)