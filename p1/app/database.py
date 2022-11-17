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



def db_listOfMovies(): 
    
    try:
        db_conn = None
        db_conn = db_engine.connect()
        db_result = db_conn.execute("Select * from imdb_movies")
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def genres(): 
    
    try: 
        db_conn=None
        db_conn=db_engine.connect()
        string=" * from imdb_genres"
        query=select(text(string))
        db_result = db_conn.execute(query)
        db_conn.close()
        return list(db_result)

    except:
        if db_conn is not None:
            db_conn.close()
            print("Exception in DB access: ")
            print("-"*60)
            traceback.print_exc(file=sys.stderr)
            print("-"*60)

        return 'Something is broken'

def filmstoshow(year1,  year2,  limitnum):
        try: 
            db_conn=None
            string="getTopSales("+str(year1)+","+str(year2)+") limit "+ str(limitnum)
            db_conn=db_engine.connect()
            db_movies_1949=select(text(string))
            db_result = db_conn.execute(db_movies_1949)
            db_conn.close()

            return list(db_result)

        except:
            if db_conn is not None:
                db_conn.close()
                print("Exception in DB access: ")
                print("-"*60)
                traceback.print_exc(file=sys.stderr)
                print("-"*60)

                return 'Something is broken'