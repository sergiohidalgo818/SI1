#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#local host y creación de archivos
#barra de busqueda y resultados
#archivo user data extension
from curses.ascii import isalnum
from doctest import testfile
from pickle import FALSE
import re
from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys
import hashlib
import random


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    if 'details_film' in request.form:

        detail =list()

        for i in catalogue['peliculas']:
            if i['id'] == int(request.form['details_film']):
                detail.append(i)

        

        return render_template('details.html', title = "Details", movies=detail)
        
    
    if 'add_to_cart' in request.form:
        
        cart_data = open(os.path.join(app.root_path,'catalogue/cart.json'), encoding="utf-8").read()
        cart = json.loads(cart_data)
    
        cart_dict = dict(cart)

        aux_id = dict()

        aux_id['id'] = int(request.form['add_to_cart'])

        cart_dict['peliculas'] += [aux_id]


        cart_f = open(os.path.join(app.root_path,'catalogue/cart.json'), "w", encoding="utf-8")
        cart_f.write(json.dumps(cart_dict, indent=4))
        cart_f.close()
  
    
    return render_template('index.html', title = "Home", movies=catalogue['peliculas'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        # aqui se deberia validar con fichero .dat del usuario
        if os.path.isdir(os.path.join(app.root_path,'../../../si1users/' + request.form['username'])) == True:
            


            
            if 'password' in request.form:
                
                user = open(os.path.join(app.root_path,'../../../si1users/' + request.form['username'] + '/userdata'), encoding="utf-8").read()
                user_info = json.loads(user)
               
                if request.form['password'] == user_info['password']:
                
                    session['usuario'] = request.form['username']
                    session.modified=True

                    # se puede usar request.referrer para volver a la pagina desde la que se hizo login
                    return redirect(url_for('index'))

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

    list_search = list()

    if 'search' in request.form:

        if 'genre' in request.form:

            if request.form['genre'] == str("all"):
                if request.form['search'] != '':

                    for i in catalogue['peliculas']:
                        if (request.form['search'].casefold() == str(i['titulo']).casefold() or 
                        request.form['search'].casefold() == str(i['director']).casefold()):
                            list_search.append(i)
                else:
                    return render_template('seeker.html', title = "Film Search", movies=catalogue['peliculas'])
            else:
                    if request.form['search'] != '':
                        for i in catalogue['peliculas']:
                            if ((request.form['search'].casefold() == str(i['titulo']).casefold() or 
                                request.form['search'].casefold() == str(i['director']).casefold()) and
                                request.form['genre'].casefold() == str(i['categoria']).casefold()):
                                list_search.append(i)
                    else:
                        for i in catalogue['peliculas']:
                            if (request.form['genre'].casefold() == str(i['categoria']).casefold()):
                                list_search.append(i)


    return render_template('seeker.html', title = "Film Search", movies=list_search)

  
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    print (url_for('static', filename='css/si1.css'), file=sys.stderr)
    cart_data = open(os.path.join(app.root_path,'catalogue/cart.json'), encoding="utf-8").read()
    cart = json.loads(cart_data)
   
    catalogue_data = open(os.path.join(app.root_path,'catalogue/inventario.json'), encoding="utf-8").read()
    catalogue = json.loads(catalogue_data)

    list_catalogue = list()
    list_cart = list()


    for i in cart['peliculas']:
        for j in catalogue['peliculas']:
            if i['id'] == j['id']:
                list_catalogue.append(j)
                list_cart.append(i)
    

    if 'delete' in request.form:
        for i in list_catalogue:
            if i['id'] == int(request.form['delete']):
                list_catalogue.remove(i)

           
        for j in list_cart:
            if j['id'] == int(request.form['delete']):
               list_cart.remove(j)



        dict_cart = dict()
        dict_cart['peliculas'] = list_cart

        cart_f = open(os.path.join(app.root_path,'catalogue/cart.json'), "w", encoding="utf-8")
        cart_f.write(json.dumps(dict_cart, indent=4))
        cart_f.close()
        
        
    
    return render_template('cart.html', title = "Home", movies=list_catalogue)


@app.route('/details', methods=['GET', 'POST'])
def details():

    

    return render_template('details.html', title = "Home")

@app.route('/register', methods=['GET', 'POST'])
def register():

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    dict_user = dict()

    if os.path.isdir(os.path.join(app.root_path,'../../../si1users')) == False:
        os.mkdir(os.path.join(app.root_path,'../../../si1users'))

    if 'username' in request.form:
        if len(request.form['username']) >= 5:
            for i in request.form['username']:
                if (i == ' ' or i == '[' or i == '@' or i == '_' or i == '!' or i =='#' 
                or i == '$' or i == '%' or i == '^' or i == '&' or i == '*' or i == '('
                or i == ')' or i == '<' or i == '>' or i == '?' or i == '/' or i == '\\'
                or i == '|' or i == '}' or i =='{' or i =='~' or i==':' or i ==']'):
                    return render_template('register.html', title = "Home")

            if os.path.isdir(os.path.join(app.root_path,'../../../si1users/' + request.form['username'])) == True:
                return render_template('register.html', title = "Home")

            os.mkdir(os.path.join(app.root_path,'../../../si1users/' + request.form['username']))
            
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
                                           
                                            dict_user['password'] = request.form['password']
                                            

                                            if 'credit_card' in request.form:
                                                if len(request.form['credit_card']) == 16:
                                                    
                                                    dict_user['credit_card'] = request.form['credit_card']
                                                    
                                                    dict_user['saldo'] = random.randint(0, 50)

                                                    user_f = open(os.path.join(app.root_path,'../../../si1users/' + request.form['username'] + '/userdata'), "w", encoding="utf-8")
                                                    user_f.write(json.dumps(dict_user, indent=4))
                                                    user_f.close()
        
                                                    return render_template('index.html', title = "Home")

        else:            
            return render_template('register.html', title = "Home")
        

    return render_template('register.html', title = "Home")