from flask import render_template, request, url_for, redirect, session
import json
import os
import sys

if __name__ == "__main__":

    with open('catalogue/inventario.json') as json_file:
        catalogue = json.load(json_file)
    
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    list_search = list()
    
    for i in catalogue['peliculas']:
            print (i['title'])
