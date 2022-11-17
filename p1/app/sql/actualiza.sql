-- ARREGLO DIRECTORMOVIES
ALTER TABLE imdb_directormovies DROP CONSTRAINT imdb_directormovies_pkey;
ALTER TABLE imdb_directormovies ADD CONSTRAINT imdb_directormovies_pkey PRIMARY KEY (movieid, directorid);
ALTER TABLE imdb_directormovies DROP COLUMN numpartitipation;

-- ARREGLO INVENTORY
ALTER TABLE inventory ADD CONSTRAINT inventory_fkey FOREIGN KEY (prod_id) REFERENCES products(prod_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;


-- ARREGLO ACTORMOVIES
ALTER TABLE imdb_actormovies ADD CONSTRAINT imdb_actormovies_pkey FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE imdb_actormovies ADD CONSTRAINT imdb_actormovies_fkey FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;


-- ARREGLO ORDERDETAIL
-- SE CREA OTRA TABLA PARA PODER TENER LA SUMA DE LA CANTIDAD DE TODAS LAS CANTIDADES
-- IGUALES EN ORDERDETAIL
CREATE TABLE orderdetailsum AS
SELECT orderid, orderdetail.prod_id, sum(quantity) AS quantity
FROM orderdetail 
INNER JOIN products ON orderdetail.prod_id = products.prod_id
group by orderid, orderdetail.prod_id;

ALTER TABLE orderdetailsum ADD CONSTRAINT orderdetail_pkey PRIMARY KEY (orderid, prod_id);
ALTER TABLE orderdetailsum ADD FOREIGN KEY (orderid) REFERENCES orders(orderid) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE orderdetailsum ADD CONSTRAINT orderdetail_fkey FOREIGN KEY (prod_id) REFERENCES products(prod_id) ON DELETE CASCADE ON UPDATE CASCADE;

DROP TABLE orderdetail;

ALTER TABLE orderdetailsum RENAME TO orderdetail;


--SECUENCIAS DE CUSTOMERS Y ORDERS
CREATE SEQUENCE customers_sequence;
ALTER TABLE customers ALTER COLUMN customerid SET NOT NULL;
ALTER TABLE  customers  ALTER COLUMN customerid SET DEFAULT nextval('customers_sequence');
select setval('customers_sequence', (SELECT MAX(customerid) FROM customers));

CREATE SEQUENCE orders_sequence;
ALTER TABLE orders ALTER COLUMN orderid SET NOT NULL;
ALTER TABLE  orders  ALTER COLUMN orderid SET DEFAULT nextval('orders_sequence');
select setval('orders_sequence', (SELECT MAX(orderid) FROM orders));


-- CAMPO ‘balance’ EN LA TABLA ‘customers’
ALTER TABLE customers ADD COLUMN balance money default 0;

-- PROCEDIMIENTO PARA CREAR UN NUMERO ALEATORIO ENTRE 0 Y N:
CREATE FUNCTION setCustomersBalance(IN N bigint) returns void as $$ 
BEGIN
UPDATE customers
  SET balance =(random() * N) :: NUMERIC :: MONEY;
END;
$$ LANGUAGE 'plpgsql';
-- LLAMADA AL PROCEDIMIENTO CON N = 100
SELECT setCustomersBalance(100) as n;

-- CREAR CAMPOS ‘ratingcount' Y 'ratingmean'
ALTER TABLE imdb_movies ADD COLUMN ratingmean FLOAT;
ALTER TABLE imdb_movies ADD COLUMN ratingcount INTEGER;
UPDATE imdb_movies SET ratingcount='0';
UPDATE imdb_movies SET ratingmean='0';

-- CREAR TABLA RATINGS
create table ratings(
  customerid SERIAL NOT NULL,
  movieid SERIAL NOT NULL,
  rating decimal NOT NULL,
  constraint ratings_pk primary key (customerid,movieid),
  constraint ratings_customerid_fk foreign key(customerid) references customers(customerid)  MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE,
  constraint ratings_movieid_fk foreign key(movieid) references imdb_movies(movieid)  MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE
);

--CREAR TABLA MOVIELANGUAGES
CREATE TABLE imdb_languages AS
SELECT DISTINCT "language"
FROM imdb_movielanguages;

ALTER TABLE imdb_languages ADD CONSTRAINT language UNIQUE ("language");
ALTER TABLE imdb_languages ADD language_id SERIAL NOT NULL;
ALTER TABLE imdb_languages ADD CONSTRAINT imdb_languages_pk PRIMARY KEY (language_id);


UPDATE imdb_movielanguages l2 
SET language = l1.language_id 
FROM imdb_languages l1
WHERE l2.language = l1.language;

ALTER TABLE imdb_movielanguages RENAME COLUMN language TO language_id;

ALTER TABLE imdb_movielanguages ALTER COLUMN language_id TYPE INT USING language_id :: INTEGER;

-- ARREGLO MOVIELANGUAGES
ALTER TABLE imdb_movielanguages ADD CONSTRAINT imdb_movielanguages_fkey FOREIGN KEY (language_id) REFERENCES imdb_languages(language_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;

--CREAR TABLA MOVIECOUNTRIES
CREATE TABLE imdb_countries AS
SELECT DISTINCT "country"
FROM imdb_moviecountries;

ALTER TABLE imdb_countries ADD CONSTRAINT country UNIQUE ("country");
ALTER TABLE imdb_countries ADD country_id SERIAL NOT NULL;
ALTER TABLE imdb_countries ADD CONSTRAINT imdb_countries_pk PRIMARY KEY (country_id);

UPDATE imdb_moviecountries c2 
SET country = c1.country_id 
FROM imdb_countries c1
WHERE c2.country = c1.country;

ALTER TABLE imdb_moviecountries RENAME COLUMN country TO country_id;

ALTER TABLE imdb_moviecountries ALTER COLUMN country_id TYPE INT USING country_id :: INTEGER;

-- ARREGLO MOVIECOUNTRIES
ALTER TABLE imdb_moviecountries ADD CONSTRAINT imdb_moviecountries_fkey FOREIGN KEY (country_id) REFERENCES imdb_countries(country_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;


--CREAR TABLA MOVIEGENRES
CREATE TABLE imdb_genres AS
SELECT DISTINCT "genre"
FROM imdb_moviegenres;

ALTER TABLE imdb_genres ADD CONSTRAINT genre UNIQUE ("genre");
ALTER TABLE imdb_genres ADD genre_id SERIAL NOT NULL;
ALTER TABLE imdb_genres ADD CONSTRAINT imdb_genres_pk PRIMARY KEY (genre_id);

UPDATE imdb_moviegenres g2 
SET genre = g1.genre_id 
FROM imdb_genres g1
WHERE g2.genre = g1.genre;

ALTER TABLE imdb_moviegenres RENAME COLUMN genre TO genre_id;

ALTER TABLE imdb_moviegenres ALTER COLUMN genre_id TYPE INT USING genre_id :: INTEGER;



-- ARREGLO MOVIEGENRES
ALTER TABLE imdb_moviegenres ADD CONSTRAINT imdb_moviegenres_fkey FOREIGN KEY (genre_id) REFERENCES imdb_genres(genre_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE CASCADE;

ALTER TABLE orders ALTER COLUMN netamount TYPE MONEY;
ALTER TABLE orders ALTER COLUMN totalamount TYPE MONEY;
ALTER TABLE products ALTER COLUMN price TYPE MONEY;



