#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Para ejecutar sin Apache/mod_wsgi, en directorio con .wsgi:
# PYTHONPATH=. python3 -m app

from app import app
import json

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)


    with open("public_html/SI1/p1/app/catalogue/catalogue.json") as archivo:
        datos = json.load(archivo)
 
    archivo.close()