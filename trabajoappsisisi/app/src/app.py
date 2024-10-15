from flask import Flask, render_template
from classes.usuario import *
from classes.campeon import *
from classes.composicion import *
from classes.avatar import *
from classes.emblema import *
from classes.sinergia import *
from classes.posee import *
from classes.formadoPor import *
from classes.vota import *
from classes.reporta import *

import sqlite3
import time
import os
import csv

app = Flask(__name__)

DATABASE = '/app/src/db/database.db'
SCHEMA = '/app/src/db/schema.sql'
DATA_FILE = '/app/src/db/data.csv'

@app.route('/', methods=['GET'])
def start():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/start_team')
def start_team():
    return render_template('start_team.html')
#----------------------------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("mail"):
            return redirect("/login")

        elif not request.form.get("contra"):
            return redirect("/login")

        user = find_usuario_by_id(request.form.get("mail"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("contra")
        ):
            return redirect("/login")

        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")
#-----------------------------------------------------------------------------------------


if __name__ == '__main__':
    print("Hello")

    ## Crear Base de Datos (antiguo)
    #init_db()
    #populate_db()

    ## Test de DAO y VO
    #UsuarioDAO().save_usuario(UsuarioVO("mail@mail", "pepe", "contra", "avatar"))
    #user = UsuarioDAO().find_usuario_by_id("mail@mail")
    #print(user.nombre)

    ## Lanzar Web
    app.run(host="0.0.0.0", port=4000, debug=True)
    time.sleep(20)
    print("Bye")
