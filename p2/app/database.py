# -*- coding: utf-8 -*-

import os
import sys, traceback
from sqlalchemy import and_, create_engine, update
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar una tabla
db_table_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)


def getGenreFromMovie(idmovie): 
    
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("Select genre_id from imdb_moviegenres where movieid = " + str(idmovie))

        return db_result.mappings().all()
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def getMovie(idmovie): 
    
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("Select * from imdb_movies where movieid = "+ str(idmovie))
        return  db_result.mappings().all()
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_listOfMovies(): 
    
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("Select * from imdb_movies LIMIT 10")
        return  db_result.mappings().all()
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'




def login(username):
    try:
        db_conn = None
        db_conn  = db_engine.connect()
        db_result = db_conn.execute("select password from customers where username = '" + username+"'")
        return db_result.mappings().all()
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def checkUsername(username): 
   
    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_result = db_conn.execute("select * from customers where username= '"+username+"' ")
        if(db_result.mappings().all()[0]['username'] == username):
            db_conn.close()
            return 'exists'
        
        db_conn.close()

        return 'notexists' 
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def register(dictuser): 
    username = dictuser['username']
    password = dictuser['password']
    email = dictuser['email']
    tarjeta = dictuser['credit_card']
    direccion = dictuser['adress']
    balance = dictuser['saldo']


    print(username, file=sys.stdout)
    print(password, file=sys.stdout)
    print(email, file=sys.stdout)
    print(tarjeta, file=sys.stdout)
    print(direccion, file=sys.stdout)
    print(balance, file=sys.stdout)
    
    try:
        db_conn = None
        db_conn = db_engine.connect()

        db_result = db_conn.execute("select customerid from customers order by customerid desc limit 1;")
        customid=db_result.mappings().all()
        db_result = db_conn.execute("insert into customers values('"+ str(int(customid[0]['customerid']) + 1) +"','"+str(direccion)+"','"+str(email)+ "','"+str(tarjeta)+"','"+str(username)+"','"+str(password)+"','"+str(balance)+"')" ) 

        db_conn.close()

        return 'good' 
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def topSales():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select * from getTopSales(2021,2022) limit 10;")
        db_conn.close()
        return  db_result.mappings().all()

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
