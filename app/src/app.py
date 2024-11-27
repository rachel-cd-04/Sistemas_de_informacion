from flask import Flask, redirect, render_template, request, session, jsonify
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
import hashlib

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
    if not session.get("mail"):
        return redirect("/login")
    if 0 == UsuarioDAO().check_priviledge(session["mail"], session["contra"]):
            return redirect("/")
    
    team_comps = ComposicionDAO().get_all_composiciones()
    if team_comps:
        for comp in team_comps:
            personajes = FormadoPorDAO().get_champions_by_composicion_id(comp.usuario, comp.nombre)
            comp.champions = personajes

    return render_template('admin_comps_list.html', team_comps=team_comps, show_login_button=True)


@app.route('/delete_composition', methods=['POST'])
def delete_composition():
    data = request.get_json()
    usuario = data.get('usuario')
    nombre = data.get('nombre')

    try:
        ComposicionDAO().delete_composicion(usuario, nombre)
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500
    
#-------------------------------------------------------------
@app.route('/admin_users_list')
def admin_users_list():
        if not session.get("mail"):
            return redirect("/login")
        if 0 == UsuarioDAO().check_priviledge(session["mail"], session["contra"]):
            return redirect("/")
        
        users_list = UsuarioDAO().get_all_users()
    
        # Crear una lista a la que añadiremos los URLs de los avatares
        users_list_with_url = []

        
        for user in users_list:
            # Comprobamos si el privilegio del usuario es 0
            if user.privilegios == 0:
                
                avatar = AvatarDAO().find_avatar_by_id(user.avatar)  
                reports = ReportaDAO().find_reports_to(user.mail)  
            
                # Almacenamos los datos de usuario y la URL del avatar
                user_with_url = {
                    'mail': user.mail,
                    'nombre': user.nombre,
                    'contra': user.contra,
                    'reports': reports,
                    'avatar': avatar.URL_ if avatar else None  # Asignar el URL si existe
                }
                
                # Agregar el usuario con URL a la lista final
                users_list_with_url.append(user_with_url)
                
                # Pasar la lista de usuarios con URL al template
        return render_template('admin_users_list.html', users_list=users_list_with_url, show_login_button=True)


@app.route('/delete_user', methods=['POST'])
def delete_usuario():
    data = request.get_json()
    mail = data.get('mail')
    
    try:
        UsuarioDAO().delete_usuario(mail)
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500

#-------------------------------------------------------------
@app.route('/help')
def help():
    return render_template('help.html', show_login_button=True)

#-------------------------------------------------------------
@app.route('/settings')
def settings():
    avatars = AvatarDAO().get_all_avatars()
    return render_template('settings.html', avatars=avatars, show_login_button=True)


@app.route('/update_all', methods=['POST'])
def update_all():
    data = request.get_json()
    mail = session['mail']
    username = data.get('username')
    password = data.get('password')
    if password == "": # En caso de no modificar la memoria mantiene la previa
        password = session['contra']
    else:
        password = hashlib.sha256(password.encode('utf-8')).hexdigest() # Hashea la nueva contraseña

    avatar_id = data.get('avatar')
    if avatar_id == -1: #Obtenemos el id del avatar previo si no lo ha modificado
        avatar_id = UsuarioDAO().find_usuario_by_id_pssw(mail, session['contra']).avatar
    avatar_url = (AvatarDAO().find_avatar_by_id(avatar_id)).URL_

    try:
        UsuarioDAO().update_usuario(UsuarioVO(mail, username, password, avatar_id, 0))

        session['contra'] = password
        session['username'] = username
        session['avatar'] = avatar_url
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}),
   

#-------------------------------------------------------------
@app.route('/start_team')
def start_team():
    
    champs = CampeonDAO().get_all_champions()
    emblems = EmblemaDAO().get_all_emblems()
    synergies = SinergiaDAO().get_all_sinergias()

    # Creamos diccionarios con campeones, emblemas y sinergias
    champs_dict = [champ.to_dict() for champ in champs]
    emblems_dict = [emblem.to_dict() for emblem in emblems]
    synergies_dict = [synergie.to_dict() for synergie in synergies]

    return render_template('start_team.html', champs=champs_dict, emblems=emblems_dict, synergies=synergies_dict, show_login_button=True)

@app.route('/save_comp', methods=['POST'])
def save_comp():
    data = request.get_json()
    mail = session['mail']
    nombre = data.get('nombre')
    dificultad = data.get('dificultad')
    published = data.get('published')
    descr = data.get('descr')
    champions = data.get('champions')

    try:
        ComposicionDAO().save_composicion(ComposicionVO(mail, nombre, dificultad, published, descr))
        for champ in champions:
            FormadoPorDAO().add_campeon_to_composicion(FormadoPorVO(mail, nombre, champ))
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500

#-------------------------------------------------------------
@app.route('/my_team_comps')

def my_TC():
    if not session.get("mail"):
        return redirect("/login")
    
    mail = session['mail']

    # Obtenemos las composiciones del usuario logeado y sus campeones
    team_comps = ComposicionDAO().get_composiciones_by_usuario_id(mail)
    if team_comps:
        for comp in team_comps:
            personajes = FormadoPorDAO().get_champions_by_composicion_id(comp.usuario, comp.nombre)
            comp.champions = personajes

    return render_template('my_team_comps.html', team_comps=team_comps, show_login_button=True)

@app.route('/edit_comp', methods=['POST'])
def edit_comp():
    data = request.get_json()
    mail = session['mail']
    nombre = data.get('nombre')
    dificultad = data.get('dificultad')
    descr = data.get('descr')

    # Obtiene la composición a editar
    old_comp = ComposicionDAO().find_composicion_by_id(mail, nombre)

    try:
        # Sube editada la composición
        ComposicionDAO().update_composicion(ComposicionVO(mail, nombre, dificultad, old_comp.publicado, descr))

        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500

@app.route('/set_publicado', methods=['POST'])
def set_publicado(): # Publica o despublica la composición
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

def comComps():

    team_comps = ComposicionDAO().get_all_public_composiciones()
    if team_comps:
        for comp in team_comps:
            # Obtenemos los votos positivos y negativos y el contador total de votos
            votosPositivos = VotaDAO().find_good_votes_to_comp(comp.usuario, comp.nombre) 
            votosNegativos = VotaDAO().find_bad_votes_to_comp(comp.usuario, comp.nombre)
            comp.votos = votosPositivos - votosNegativos

            # Obtenemos el voto específico del usuario actualmente logueado
            if not session.get("mail"):
                comp.votoUser = 0
            else:
                comp.votoUser = VotaDAO().find_vota_by_id(session['mail'], comp.usuario, comp.nombre)

            # Obtenemos los campeones de cada composición
            personajes = FormadoPorDAO().get_champions_by_composicion_id(comp.usuario, comp.nombre)
            comp.champions = personajes
            
    return render_template('community_comps.html', team_comps=team_comps, show_login_button=True)


@app.route('/save_composition', methods=['POST'])
def save_composition():
    data = request.get_json()
    nombre = data.get('nombre')
    user = data.get('user')
    dificultad = data.get('dificultad')
    descr = data.get('descr')

    try:
        ComposicionDAO().save_composicion(ComposicionVO(session['mail'], nombre, dificultad, "N", descr))

        # Obtenemos los campeones de la composición que queremos copiar
        champions = FormadoPorDAO().get_champions_by_composicion_id(user, data.get('nombre'))
        for champ in champions:
            # Añadimos los campeones a la nueva composición
            FormadoPorDAO().add_campeon_to_composicion(FormadoPorVO(session['mail'], nombre, champ.nombre))
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500
    
    
@app.route('/report_composition', methods=['POST'])
def report_composition():
    data = request.get_json()
    user = data.get('user')
    try:
        ReportaDAO().save_reporta(ReportaVO(session['mail'], user))
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500
    

@app.route('/delete_vote', methods=['POST'])
def delete_vote():
    data = request.get_json()
    mailVotante = session['mail']
    mail = data.get('mail')
    nombre = data.get('nombre')
    try:
        VotaDAO().delete_vota(mailVotante, mail, nombre)
        
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}), 500
    

    
    
@app.route('/save_vote', methods=['POST'])
def save_vote():
    data = request.get_json()
    try:
        VotaDAO().save_vota(VotaVO(session['mail'], data.get('mail'), data.get('nombre'), data.get('voto')))

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

        # Obtenemos la versión hasheada de la contraseña 
        hashed_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Comprobamos campos
        if not mail or not password:
            return redirect("/login")
        
        # Obtenemos el usuario que coincida en mail y contraseña
        user = UsuarioDAO().find_usuario_by_id_pssw(mail, hashed_pass)
        if not user:
            return redirect("/login")

        session["mail"] = user.mail
        session["username"] = user.nombre
        avatar = AvatarDAO().find_avatar_by_id(user.avatar) # Guardamos la URL, no el id
        session["avatar"] = avatar.URL_
        session["contra"] = user.contra

        if user.privilegios != 0:
            return redirect("admin_comps_list")
        return redirect("/")

    return render_template("login.html", session=session, show_login_button=False)

#-------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register_user():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        mail = request.form.get("mail")
        password = request.form.get("password")
        confirmpssw = request.form.get("confirm_password")

        # Hashea la contraseña
        hashed_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()


        # Comprueba que los valores de los campos sean correctos (Comprobaciones extra en el html)
        if not username or not mail or not password or not confirmpssw:
            return redirect("/register")

        if password != confirmpssw:
            return redirect("/register")

        user = UsuarioDAO().save_usuario(UsuarioVO(mail, username, hashed_pass, 6, 0)) # Privilegios siempre a 0
        if not user:
            return redirect("/help")

        session["mail"] = user.mail
        session["username"] = user.nombre
        avatar = AvatarDAO().find_avatar_by_id(user.avatar) # Guardamos la URL, no el id
        session["avatar"] = avatar.URL_
        session["contra"] = user.contra
        return redirect("/")

    return render_template("register.html", show_login_button=False)

#-------------------------------------------------------------
# Permite salir de la cuenta
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    return redirect("/")

#-------------------------------------------------------------
# Comprueba si el usuario esta loggeado
@app.route('/check_logged', methods=['POST'])
def check_logged():
    if not session.get("mail"):
        return jsonify({"success": True})

#-------------------------------------------------------------

if __name__ == '__main__':
    print("Hello")

    ## Test de DAO y VO
    #UsuarioDAO().save_usuario(UsuarioVO("mail@mail", "pepe", "contra", "avatar"))
    #user = UsuarioDAO().find_usuario_by_id("mail@mail")
    #print(user.nombre)

    ## Lanzar Web
    app.run(host="0.0.0.0", port=4000, debug=True)
    print("Bye")
