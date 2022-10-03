#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys

@app.route('/')
@app.route('/index')
def index():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        # aqui se deberia validar con fichero .dat del usuario
        if request.form['username'] == 'pp':
            session['usuario'] = request.form['username']
            session.modified=True
            # se puede usar request.referrer para volver a la pagina desde la que se hizo login
            return redirect(url_for('index'))
        else:
            # aqui se le puede pasar como argumento un mensaje de login invalido
            return render_template('login.html', title = "Sign In")
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen']=request.referrer
        session.modified=True        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login.html', title = "Sign In")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))


@app.route('/seeker', methods=['GET', 'POST'])
def seeker():

    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
     # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'search' in request.form:

        catalogue_search ={}

        
        catalogue_search['peliculas'] ={}

        catalogue_search['peliculas'].clear

        for i in catalogue['peliculas']:
            catalogue_search['peliculas'] = i
        


        return render_template('seeker.html', title = "Film Search", movies=json.dumps(catalogue_search['peliculas'], False))

    else:

        return render_template('seeker.html', title = "Film Search")

@app.route('/cart')
def cart():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)
    return render_template('cart.html', title = "Home", movies=catalogue['peliculas'])

