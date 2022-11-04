#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#local host y creación de archivos
#barra de busqueda y resultados
#archivo user data extension
from curses.ascii import isalnum
from doctest import testfile
from pickle import FALSE
import re
from datetime import datetime
from sqlalchemy import null
from app import app
from app import database
from flask import render_template, request, url_for, redirect, session, flash
import json
import os
import sys
import hashlib
import random
from datetime import date


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    list_search = list()

    #busqueda
    if 'search' in request.form:

        if 'genre' in request.form:

            if request.form['genre'] == str("all"):
                if request.form['search'] != '':

                    for i in catalogue['peliculas']:
                        if request.form['search'].casefold() in str(i['titulo']).casefold():
                            list_search.append(i)
                else:
                    return render_template('index.html', title = "Film Search", movies=catalogue['peliculas'])
            else:
                    if request.form['search'] != '':
                        for i in catalogue['peliculas']:
                            if ((request.form['search'].casefold() in str(i['titulo']).casefold()) and
                                request.form['genre'].casefold() == str(i['categoria']).casefold()):
                                list_search.append(i)
                    else:
                        for i in catalogue['peliculas']:
                            if (request.form['genre'].casefold() == str(i['categoria']).casefold()):
                                list_search.append(i)


        return render_template('index.html', title = "Film Search", movies=list_search)

    #detalles de la pelicula
    if 'details_film' in request.form:

        detail =list()

        for i in catalogue['peliculas']:
            if i['id'] == int(request.form['details_film']):
                detail.append(i)

        

        return render_template('details.html', title = "Details", movies=detail)
        
    #añadir al carrito
    if 'add_to_cart' in request.form:
        
        if not session.get('carrito'):
            dict_aux = dict()
            dict_aux['peliculas'] = []
            session['carrito'] = dict_aux

        cart = session['carrito']

        aux_id = dict()

        aux_id['id'] = int(request.form['add_to_cart'])
        aux_id['cantidad'] = 1

        for i in cart['peliculas']:
            if i['id'] == aux_id['id']:
                aux_id['cantidad'] = 0
                i['cantidad'] += 1

        if aux_id['cantidad'] == 1:
            cart['peliculas'] += [aux_id]
            

        session['carrito'] = cart
        

    
    #establecer puntuación
    if 'submit' in request.form:
        if 'estrellas' in request.form:
            
            detail =list()


            for i in catalogue['peliculas']:
                if i['id'] == int(request.form['submit']):
                    puntuacion_aux = int ( i['puntuacion'] * i['valoraciones'])
                    puntuacion_aux += int(request.form['estrellas'])
                    i['valoraciones']+=1
                    i['puntuacion'] = float("{:.2f}".format(puntuacion_aux/i['valoraciones']))
                    detail.append(i)

        
            catalogue_f = open(os.path.join(app.root_path,'catalogue/inventario.json'), "w", encoding="utf-8")
            catalogue_f.write(json.dumps(catalogue, indent=4))
            catalogue_f.close()

            return render_template('details.html', title = "Details", movies=detail)



    
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:

        # aqui se deberia validar con fichero .dat del usuario
        if request.form['username'] != '': 
            
            if os.path.isdir(os.path.join(app.root_path,'../../si1users/' + request.form['username'])) == False:
                flash('Wrong username')
                return render_template('login.html', title = "Sign In")

            
            if 'password' in request.form:
                
                user = open(os.path.join(app.root_path,'../../si1users/' + request.form['username'] + '/userdata'), encoding="utf-8").read()
                user_info = json.loads(user)
               

                contra = hashlib.sha3_384()
                contra.update(request.form['password'].encode('utf-8'))
                                           
                if contra.hexdigest() == user_info['password']:
                
                    session['usuario'] = request.form['username']
                    session.modified=True

                    # se puede usar request.referrer para volver a la pagina desde la que se hizo login
                    return redirect(url_for('index'))
                else:
                    flash('Wrong password')
        else:
                flash('Invalid username')
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


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    
    if not session.get('carrito'):
        dict_aux = dict()
        dict_aux['peliculas'] = []
        session['carrito'] = dict_aux


    cart = session['carrito']
   
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    list_catalogue = list()
    list_cart = list()


    for i in cart['peliculas']:
        for j in catalogue['peliculas']:
            if i['id'] == j['id']:
                j['cantidad'] = i['cantidad']
                list_catalogue.append(j)
                list_cart.append(i)
    

    if 'delete' in request.form:

        for i in list_catalogue:
            if i['id'] == int(request.form['delete']):
                if i['cantidad'] == 1:
                    list_catalogue.remove(i)
                else:
                    i['cantidad'] -= 1
           
        for j in list_cart:
            if j['id'] == int(request.form['delete']):
                if j['cantidad'] == 1:
                    list_cart.remove(j)
                else:
                    j['cantidad'] -= 1


        dict_cart = dict()
        dict_cart['peliculas'] = list_cart

        session['carrito'] = dict_cart

        return render_template('cart.html', title = "Cart", movies=list_catalogue)

    
    if 'add' in request.form:
       
        aux_id = dict()

        aux_id['id'] = int(request.form['add'])

        for i in cart['peliculas']:
            if i['id'] == aux_id['id']:
                i['cantidad'] += 1


        for i in list_catalogue:
            if i['id'] == int(request.form['add']):
                i['cantidad'] += 1

        session['carrito'] = cart

        return render_template('cart.html', title = "Cart", movies=list_catalogue)

    if 'purchase' in request.form:

        total = 0
        for i in list_catalogue:
            total+=i['precio']*i['cantidad']


        user = open(os.path.join(app.root_path,'../../si1users/' + session['usuario'] + '/userdata'), encoding="utf-8").read()
        user_info = json.loads(user)
               
        if user_info['saldo'] < total:
            flash('Saldo insuficiente')
        else: 
            if (total <= 0):
                flash('No hay elementos en el carrito')
            else:
                user_info['saldo'] -= total        

                user_f = open(os.path.join(app.root_path,'../../si1users/' + session['usuario'] + '/userdata'), "w", encoding="utf-8")
                user_f.write(json.dumps(user_info, indent=4))
                user_f.close()
           
                compras = open(os.path.join(app.root_path,'../../si1users/' + session['usuario'] + '/compras.json'), encoding="utf-8").read()
                compras_info = json.loads(compras)


                aux_list = list()

                aux_dict = dict()

                aux_dict['total'] = "{:.2f}".format(total)
                aux_dict['fecha'] = date.today().strftime("%m/%d/%Y")
                
                aux_list.append(aux_dict)
            
                for i in list_catalogue:
                    aux_list.append(i)
        

                compras_info['compras'] += [aux_list]

                compras_f = open(os.path.join(app.root_path,'../../si1users/' + session['usuario'] + '/compras.json'), "w", encoding="utf-8")
                compras_f.write(json.dumps(compras_info, indent=4))
                compras_f.close()

                session['carrito'] = {"peliculas": []}
                return render_template('cart.html', title = "Cart",movies= session['carrito'])
   
    return render_template('cart.html', title = "Cart", movies=list_catalogue)


@app.route('/register', methods=['GET', 'POST'])
def register():


    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    dict_user = dict()

    if os.path.isdir(os.path.join(app.root_path,'../../si1users')) == False:
        os.mkdir(os.path.join(app.root_path,'../../si1users'), mode=0o777)

    if 'username' in request.form:
        if len(request.form['username']) >= 5:
            for i in request.form['username']:
                if (i == ' ' or i == '[' or i == '@' or i == '_' or i == '!' or i =='#' 
                or i == '$' or i == '%' or i == '^' or i == '&' or i == '*' or i == '('
                or i == ')' or i == '<' or i == '>' or i == '?' or i == '/' or i == '\\'
                or i == '|' or i == '}' or i =='{' or i =='~' or i==':' or i ==']'):
                    flash('Wrong username')
                    return render_template('register.html', title = "Register")

            if os.path.isdir(os.path.join(app.root_path,'../../si1users/' + request.form['username'])) == True:
                flash('Username already exists')
                return render_template('register.html', title = "Register")

            
            dict_user['username'] = request.form['username']

            if 'email' in request.form:

                if(re.fullmatch(regex, request.form['email'])):
                    
                    dict_user['email'] = request.form['email']

                    if 'adress' in request.form:
                        if len(request.form['adress']) <= 50:
                            
                            dict_user['adress'] = request.form['adress']


                            if 'password' in request.form:
                                if len(request.form['password']) >= 6:

                                    if 'confirm_password' in request.form:
                                        if request.form['password'] == request.form['confirm_password']:
                                            
                                            contra = hashlib.sha3_384()
                                            contra.update(request.form['password'].encode('utf-8'))
                                           
                                            dict_user['password'] = contra.hexdigest()
                                            

                                            if 'credit_card' in request.form:
                                                if len(request.form['credit_card']) == 16:
                                                    
                                                    dict_user['credit_card'] = request.form['credit_card']
                                                    
                                                    dict_user['saldo'] = random.randint(0, 50)
                                                    
                                                    os.mkdir(os.path.join(app.root_path,'../../si1users/' + request.form['username']), mode=0o777)
                                                    
                                                    open(os.path.join(app.root_path,'../../si1users/' + request.form['username'] + '/userdata'), "x", encoding="utf-8")

                                                    user_f = open(os.path.join(app.root_path,'../../si1users/' + request.form['username'] + '/userdata'), "w", encoding="utf-8")
                                                    user_f.write(json.dumps(dict_user, indent=4))
                                                    user_f.close()

                                                    user_f = open(os.path.join(app.root_path,'../../si1users/' + request.form['username'] + '/compras.json'), "w", encoding="utf-8")
                                                    
                                                    dict_compras= dict()
                                                    dict_compras['compras'] = []
                                                    
                                                    user_f.write(json.dumps(dict_compras, indent=4))
                                                    user_f.close()
                                                    return redirect(url_for('login'))
                                                
                                                else:
                                                    flash('Invalid credit card')            
                                        else:
                                            flash('Passwords dont match')                                
                                else:
                                    flash('Short password')
                        else:
                            flash('Too long adress')

                else:
                    flash('Invalid email')

        else:            
            flash('Short username')


    return render_template('register.html', title = "Register")
        
@app.route('/history', methods=['GET', 'POST'])
def history():

    if not session.get('usuario'):
        return render_template('history.html', title = "History")



    if 'details_film' in request.form:

        detail =list()

        catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
        catalogue = json.loads(catalogue_data)

        for i in catalogue['peliculas']:
            if i['id'] == int(request.form['details_film']):
                detail.append(i)
        
        return render_template('details.html', title = "Details", movies=detail)


    if session.get('usuario'):
        compras = open(os.path.join(app.root_path,'../../si1users/' + session['usuario'] + '/compras.json'), encoding="utf-8").read()
        compras_info = json.loads(compras)

        return render_template('history.html', title = "History", compras = compras_info['compras'])

#EJEMPLO DATABASE MOODLE
@app.route('/list_movies')
def list_movies():
    movies = database.db_listOfMovies()
    return render_template('list_movies.html', title = "Movies from Postgres Database", movies = movies)
