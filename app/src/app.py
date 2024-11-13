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
    
        # Crear una lista enriquecida con los URLs de los avatares
        users_list_with_url = []
        
        # Iterar sobre cada usuario y buscar la URL del avatar
        for user in users_list:
            # Usar `find_avatar_by_id` para obtener el objeto AvatarVO del avatar
            avatar = AvatarDAO().find_avatar_by_id(user.avatar)  # Acceso a `user.avatar` como propiedad
            reports = ReportaDAO().find_reports_to(user.mail) 
            
            # Crear un diccionario para almacenar los datos de usuario y la URL del avatar
            enriched_user = {
                'mail': user.mail,
                'nombre': user.nombre,
                'contra': user.contra,
                'reports': reports,
                'avatar': avatar.URL_ if avatar else None  # Asignar el URL si existe
            }
            
            # Agregar el usuario enriquecido a la lista final
            users_list_with_url.append(enriched_user)
            # Pasar la lista de usuarios enriquecida al template
        return render_template('admin_users_list.html', users_list=users_list_with_url, show_login_button=True)


@app.route('/delete_user', methods=['POST'])
def delete_usuario():
    data = request.get_json()
    mail = data.get('mail')
    
    try:
        # Llama a la función del DAO que borra el usuario por su mail
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
def update_avatar():
    data = request.get_json()
    mail = session['mail']
    username = data.get('username')
    password = data.get('password')
    avatar_id = data.get('avatar')
    avatar_url = (AvatarDAO().find_avatar_by_id(avatar_id)).URL_

    try:
        UsuarioDAO().update_usuario(UsuarioVO(mail, username, password, avatar_id))
        session['username'] = username
        session['contra'] = password
        session['avatar'] = avatar_url
        return jsonify({"success": True})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False}),
   

#-------------------------------------------------------------
@app.route('/start_team')
#@login_required(login_url="/login")
def start_team():
    
    champs = CampeonDAO().get_all_champions()
    emblems = EmblemaDAO().get_all_emblems()
    synergies = SinergiaDAO().get_all_sinergias()

    champs_dict = [champ.to_dict() for champ in champs]
    emblems_dict = [emblem.to_dict() for emblem in emblems]
    synergies_dict = [synergie.to_dict() for synergie in synergies]

    return render_template('start_team.html', champs=champs_dict, emblems=emblems_dict, synergies=synergies_dict, show_login_button=True)

#-------------------------------------------------------------
@app.route('/my_team_comps')
#@login_required(login_url="/login")
def my_TC():
    if not session.get("mail"):
        return redirect("/login")
    
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
            votosPositivos = VotaDAO().find_good_votes_to_comp(comp.usuario, comp.nombre) 
            votosNegativos = VotaDAO().find_bad_votes_to_comp(comp.usuario, comp.nombre)
            comp.votos = votosPositivos - votosNegativos
            if not session.get("mail"):
                comp.votoUser = 0
            else:
                comp.votoUser = VotaDAO().find_vota_by_id(session['mail'], comp.usuario, comp.nombre)

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
        champions = FormadoPorDAO().get_champions_by_composicion_id(user, data.get('nombre'))
        for champ in champions:
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
        if not mail or not password:
            return redirect("/login")
        

        user = UsuarioDAO().find_usuario_by_id_pssw(mail, password)
        if not user:
            return redirect("/login")

        session["mail"] = user.mail
        session["username"] = user.nombre
        avatar = AvatarDAO().find_avatar_by_id(user.avatar)
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

        if not username or not mail or not password or not confirmpssw:
            return redirect("/register")

        if password != confirmpssw:
            return redirect("/register")

        user = UsuarioDAO().save_usuario(UsuarioVO(mail, username, password, 6, 0))
        if not user:
            return redirect("/help")

        session["mail"] = user.mail
        session["username"] = user.nombre
        avatar = AvatarDAO().find_avatar_by_id(user.avatar)
        session["avatar"] = avatar.URL_
        session["contra"] = user.contra
        return redirect("/")

    return render_template("register.html", show_login_button=False)

#-------------------------------------------------------------
@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    return redirect("/")

#-------------------------------------------------------------
@app.route('/check_logged', methods=['POST'])
def not_logged():
    if not session.get("mail"):
        return jsonify({"success": False})
    return jsonify({"success": True})

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
