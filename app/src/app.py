from flask import Flask, redirect, render_template, request, session, jsonify
#from django.contrib.auth.decorators import login_required
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
@app.route('/settings')
def settings():
    return render_template('settings.html')

#-------------------------------------------------------------
@app.route('/my_team_comps')
#@login_required(login_url="/login")
def my_TC():
    mail = session['mail']
    team_comps = ComposicionDAO().get_composiciones_by_usuario_id(mail)
    if team_comps:
        for comp in team_comps:
            compName = comp.nombre
            personajes = FormadoPorDAO().get_champions_by_composicion_id(mail, compName)
            comp.champions = personajes

    return render_template('my_team_comps.html', team_comps=team_comps)


@app.route('/set_publicado', methods=['POST'])
def set_publicado():
    data = request.get_json()
    usuario = data.get('usuario')
    nombre = data.get('nombre')
    publicado = data.get('publicado')
    print(f"usuario: {usuario}, nombre: {nombre}, publicado: {publicado}")

    try:
        ComposicionDAO().set_publicado(usuario, nombre, publicado)
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500

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
