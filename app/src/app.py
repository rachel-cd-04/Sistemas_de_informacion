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
    return render_template('index.html', show_login_button=True)

#-------------------------------------------------------------
@app.route('/index')
def index():
    return render_template('index.html', show_login_button=True)

#-------------------------------------------------------------
@app.route('/admin_comps_list')
def admin_comps_list():
    team_comps = ComposicionDAO().get_all_public_composiciones()
    if team_comps:
        for comp in team_comps:
            personajes = FormadoPorDAO().get_champions_by_composicion_id(comp.usuario, comp.nombre)
            comp.champions = personajes

    return render_template('admin_comps_list.html', team_comps=team_comps, show_login_button=True)

#-------------------------------------------------------------
@app.route('/admin_users_list')
def admin_users_list():
    users_list = UsuarioDAO().get_all_users()

    return render_template('admin_users_list.html', users_list=users_list, show_login_button=True)

#-------------------------------------------------------------
@app.route('/help')
def help():
    return render_template('help.html', show_login_button=True)

#-------------------------------------------------------------
@app.route('/settings')
def settings():
    return render_template('settings.html', show_login_button=True)

#-------------------------------------------------------------
@app.route('/start_team')
#@login_required(login_url="/login")
def start_team():
    champs = CampeonDAO().get_all_champions()
    if champs:
        for champ in champs:
            synergies = PoseeDAO().get_sinergias_by_champion_id(champ.nombre)
            champ.synergies = synergies

    return render_template('start_team.html', champs=champs, show_login_button=True)

#-------------------------------------------------------------
@app.route('/my_team_comps')
#@login_required(login_url="/login")
def my_TC():
    mail = session['mail']
    team_comps = ComposicionDAO().get_composiciones_by_usuario_id(mail)
    if team_comps:
        for comp in team_comps:
            personajes = FormadoPorDAO().get_champions_by_composicion_id(comp.usuario, comp.nombre)
            comp.champions = personajes

    return render_template('my_team_comps.html', team_comps=team_comps, show_login_button=True)


@app.route('/set_publicado', methods=['POST'])
def set_publicado():
    data = request.get_json()
    usuario = data.get('usuario')
    nombre = data.get('nombre')
    publicado = data.get('publicado')

    try:
        ComposicionDAO().set_publicado(usuario, nombre, publicado)
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500

#------------------------------------------------------------- 
@app.route('/community_comps')
#@login_required(login_url="/login")
def comComps():
    team_comps = ComposicionDAO().get_all_public_composiciones()
    if team_comps:
        for comp in team_comps:
            personajes = FormadoPorDAO().get_champions_by_composicion_id(comp.usuario, comp.nombre)
            comp.champions = personajes

    return render_template('community_comps.html', team_comps=team_comps, show_login_button=True)

@app.route('/save_composition', methods=['POST'])
def save_composition():
    data = request.get_json()
    try:
        ComposicionDAO.save_composicion(ComposicionVO(session['mail'], data.get('nombre'), data.get('dificultad'), "N", data.get('descr')))
        for champ in data.get('champions'):
            FormadoPorDAO.add_campeon_to_composicion(FormadoPorVO(session['mail'], data.get('nombre'), champ.nombre))

        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500


#------------------------------------------------------------- 
@app.route("/login", methods=["GET", "POST"])
def login_user():
    CORREO_ADMIN = "admin@gmail.com"
    CONTRASENA_ADMIN = "admin"
    session.clear()
    if request.method == "POST":
        mail = request.form.get("mail")
        password = request.form.get("password")
        if not mail or not password:
            return redirect("/login")
        
        if mail == CORREO_ADMIN and password == CONTRASENA_ADMIN:
            return redirect("admin_comps_list")

        user = UsuarioDAO().find_usuario_by_id_pssw(mail, password)
        if not user:
            return redirect("/login")

        session["mail"] = user.mail
        session["username"] = user.nombre
        session["avatar"] = user.avatar
        return redirect("/")

    return render_template("login.html", show_login_button=False)

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

    return render_template("register.html", show_login_button=False)

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
