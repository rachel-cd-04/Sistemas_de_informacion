from flask import Flask, flash, redirect, render_template, request, session
from classes.usuario import UsuarioDAO, UsuarioVO
from classes.campeon import CampeonDAO, CampeonVO
from classes.composicion import ComposicionDAO, ComposicionVO
from classes.avatar import AvatarDAO, AvatarVO
from classes.emblema import EmblemaDAO, EmblemaVO
from classes.sinergia import SinergiaDAO, SinergiaVO
from classes.posee import PoseeDAO, PoseeVO
from classes.formadoPor import FormadoPorDAO, FormadoPorVO
from classes.vota import VotaDAO, VotaVO
from classes.reporta import ReportaDAO, ReportaVO

import sqlite3
import time
import os
import csv

app = Flask(__name__)
app.secret_key = 'secretita'  # Necesario para usar sesiones

DATABASE = '/app/src/db/database.db'
SCHEMA = '/app/src/db/schema.sql'
DATA_FILE = '/app/src/db/data.csv'

#-------------------------------------------------------------
@app.route('/', methods=['GET'])
def start():
    return render_template('index.html')

#-------------------------------------------------------------
@app.route('/index')
def index():
    return render_template('index.html')

#-------------------------------------------------------------
@app.route('/start_team')
def start_team():
    return render_template('start_team.html')

#-------------------------------------------------------------
@app.route('/help')
def help():
    return render_template('help.html')

#------------------------------------------------------------- 
@app.route("/login", methods=["GET", "POST"])
def login_user():
    session.clear()
    if request.method == "POST":
        mail = request.form.get("mail")
        password = request.form.get("password")
        if not mail or not password:
            return redirect("/login")

        user = UsuarioDAO().find_usuario_by_id_pssw(mail, password)
        if not user:
            return redirect("/login")

        session["mail"] = user.mail
        session["username"] = user.nombre
        session["avatar"] = user.avatar
        return redirect("/")

    return render_template("login.html")

#-------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register_user():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        mail = request.form.get("mail")
        password = request.form.get("password")
        confirmpssw = request.form.get("confirm_password")

        if not username or not mail or not password or not confirmpssw:
            return redirect("/register")

        if password != confirmpssw:
            return redirect("/register")

        user = UsuarioDAO().save_usuario(UsuarioVO(mail, username, password, '../static/images/avatars/avatar1.png'))
        if not user:
            return redirect("/help")

        session["mail"] = user.mail
        session["username"] = user.nombre
        session["avatar"] = user.avatar
        return redirect("/")

    return render_template("register.html")

#-------------------------------------------------------------
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    return redirect("/")

#-------------------------------------------------------------

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
