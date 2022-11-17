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

def movieHasGenre(idmovie, idgenre): 
    
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select * from imdb_movies where movieid in(Select movieid From imdb_moviegenres where "+ str(idgenre) +"= imdb_moviegenres.genre_id and " + str(idmovie) + " = imdb_moviegenres.movieid)")

        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def getGenreFromMovie(idmovie): 
    
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("Select genre_id from imdb_moviegenres where movieid = " + str(idmovie))

        return db_result.first()
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'


def getMovieFromGenre(genre): 
    
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("Select * from imdb_movies where movieid in (Select movieid From imdb_moviegenres where"+ str(genre) +"= imdb_moviegenres.genre_id) limit 10")
        return  list(db_result)
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
        return  list(db_result)
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
        return  list(db_result)
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
        db_result = db_conn.execute("select password from customers where username = " + username).one 
        db_conn.close()
        return list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def db_register(dictuser):
    username = ['username']
    password = dictuser['password']
    email = dictuser['email']
    tarjeta = dictuser['credit_card']
    direccion = dictuser['adress']
    balance = dictuser['saldo']

    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select * from customers where username= "+username)

        if len(list(db_result)) > 0:
            return 'Something is broken'

        if username != "" :
            customerid = db_conn.execute("select customerid from customers order by customerid desc limit 1;")
            db_result = db_conn.execute("insert into customers values('"+ str(customerid.fetchone() + 1) +"','"+str(direccion)+"','"+str(email)+ "','"+str(tarjeta)+"','"+str(username)+"','"+str(password)+"','"+str(balance)+"');" ) 
            db_conn.close()

        db_conn.close()
        return 1

    except:
        if db_conn is not None:
            db_conn.close()
        return 'Something is broken'

def topSales():
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("select * from getTopSales(2021,2022) limit 10;")
        db_conn.close()
        return  list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'
