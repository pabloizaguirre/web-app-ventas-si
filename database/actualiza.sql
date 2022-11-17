------- Modificaciones de la base de datos -------

-- Quitamos las filas de la tabla imdb_movies donde el valor de year es 1998-1999
update imdb_movies
set year = 1999
where year = '1998-1999';

-- AÑADIMOS FOREIGN KEY A ORDERS
ALTER TABLE customers
	ALTER COLUMN password TYPE VARCHAR(96);
	
ALTER TABLE imdb_movies 
	ADD COLUMN ratingmean NUMERIC,
	ADD COLUMN ratingcount NUMERIC;
	
	
--CREACION DE LA TABLA STATUS PARA EL ESTADO DEL PEDIDO
CREATE TABLE public.ratings( --usuario+pelicula = rating
	customerid integer NOT NULL,
	movieid	integer NOT NULL,
	rating NUMERIC
);

-- Setting customer username to be unique
ALTER TABLE customers
ADD CONSTRAINT email_unique
UNIQUE (email);

-- Adding foreign key in orders
ALTER TABLE orders
ADD CONSTRAINT orders_customerid_fkey
FOREIGN KEY (customerid) REFERENCES customers(customerid); -- no action

-- Adding primary key in actormovies
ALTER TABLE imdb_actormovies
ADD CONSTRAINT imdb_actormovies_pkey
PRIMARY KEY (actorid, movieid);

-- Adding foreign key in actormovies (actorid)
ALTER TABLE imdb_actormovies
ADD CONSTRAINT imdb_actormovies_actorid_fkey
FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid)
ON DELETE CASCADE;

-- Adding foreign key in actormovies (movieid)
ALTER TABLE imdb_actormovies
ADD CONSTRAINT imdb_actormovies_movieid_fkey
FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid)
ON DELETE CASCADE;

-- Deleting num_participation from directormovies PK
ALTER TABLE imdb_directormovies
DROP CONSTRAINT imdb_directormovies_pkey;

ALTER TABLE imdb_directormovies
ADD CONSTRAINT imdb_directormovies_pkey
PRIMARY KEY (directorid, movieid);

-- Getting tuples (orderid, prod_id) with no repetitions and the added quantity
SELECT orderid, prod_id, sum(quantity) INTO od_aux
FROM orderdetail
GROUP BY orderid, prod_id;

-- Deleting old orderdetail table
DROP TABLE orderdetail;

-- Creating a new one
CREATE TABLE public.orderdetail (
    orderid integer NOT NULL,
    prod_id integer NOT NULL,
    price numeric,
    quantity integer NOT NULL
);
ALTER TABLE public.orderdetail OWNER TO alumnodb;

-- Inserting tuples with no repetitions
INSERT INTO orderdetail (orderid, prod_id, quantity)
SELECT *
FROM od_aux;

-- Droping auxiliary table
DROP TABLE od_aux;

-- Adding primary key in orderdetail
ALTER TABLE orderdetail
ADD CONSTRAINT orderdetail_pkey
PRIMARY KEY (orderid, prod_id);

-- Adding foreign key in orderdetail (orderid)
ALTER TABLE orderdetail
ADD CONSTRAINT orderdetail_orderid_fkey
FOREIGN KEY (orderid) REFERENCES orders(orderid)
ON DELETE CASCADE;

-- Adding foreign key in actormovies (movieid)
ALTER TABLE orderdetail
ADD CONSTRAINT imdb_prod_id_fkey
FOREIGN KEY (prod_id) REFERENCES products(prod_id); -- no action
-------------------------------------------------------------------------


-------------------------------------------------------------------------
-- MERGING INVENTORY TABLE WITH PRODUCTS TABLE (1-1 relation)

-- Creating new columns stock and sales in products' table
ALTER TABLE products
ADD COLUMN stock integer DEFAULT 0;

ALTER TABLE products
ADD COLUMN sales integer DEFAULT 0;

-- Merging stock values
UPDATE products
SET stock=inventory.stock
FROM inventory
WHERE products.prod_id=inventory.prod_id;

-- Merging sales values
UPDATE products
SET sales=inventory.sales
FROM inventory
WHERE products.prod_id=inventory.prod_id;

-- Deleting deprecated inventory table
DROP TABLE inventory;
-------------------------------------------------------------------------


-------------------------------------------------------------------------
-- IMPROVING RELATIONS OF MULTIVALUED ATTRIBUTES

-- IMDB_MOVIELANGUAGES
-- Creating new languages table
CREATE TABLE public.languages(
    language_id integer PRIMARY KEY NOT NULL,
    language character varying(32) NOT NULL
);
ALTER TABLE public.languages OWNER TO alumnodb;

-- Creating sequence of the id (PK) before inserting
CREATE SEQUENCE public.languages_language_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.languages_language_id_seq OWNER TO alumnodb;

ALTER SEQUENCE public.languages_language_id_seq OWNED BY public.languages.language_id;

ALTER TABLE ONLY public.languages ALTER COLUMN language_id SET DEFAULT nextval('public.languages_language_id_seq'::regclass);

-- Inserting languages
INSERT INTO public.languages(language)
SELECT DISTINCT language
FROM public.imdb_movielanguages;

-- Adding new language_id column
ALTER TABLE public.imdb_movielanguages
ADD COLUMN language_id integer;

-- Updating column with languages ids
UPDATE imdb_movielanguages
SET language_id=languages.language_id
FROM languages
WHERE imdb_movielanguages.language=languages.language;

-- Deleting column with languages strings
ALTER TABLE imdb_movielanguages
DROP COLUMN language;

-- Setting up new PK's and FK's
ALTER TABLE ONLY public.imdb_movielanguages
ADD CONSTRAINT imdb_movielanguages_pkey PRIMARY KEY (movieid, language_id);

ALTER TABLE ONLY public.imdb_movielanguages
ADD CONSTRAINT imdb_movielanguages_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.languages(language_id);


-- IMDB_MOVIECOUNTRIES
-- Creating new countries table
CREATE TABLE public.countries(
    country_id integer PRIMARY KEY NOT NULL,
    country character varying(32) NOT NULL
);
ALTER TABLE public.countries OWNER TO alumnodb;

-- Creating sequence of the id (PK) before inserting
CREATE SEQUENCE public.countries_country_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.countries_country_id_seq OWNER TO alumnodb;

ALTER SEQUENCE public.countries_country_id_seq OWNED BY public.countries.country_id;

ALTER TABLE ONLY public.countries ALTER COLUMN country_id SET DEFAULT nextval('public.countries_country_id_seq'::regclass);

-- Inserting countries
INSERT INTO public.countries(country)
SELECT DISTINCT country
FROM public.imdb_moviecountries;

-- Adding new language_id column
ALTER TABLE public.imdb_moviecountries
ADD COLUMN country_id integer;

-- Updating column with countries ids
UPDATE imdb_moviecountries
SET country_id=countries.country_id
FROM countries
WHERE imdb_moviecountries.country=countries.country;

-- Deleting column with countries strings
ALTER TABLE imdb_moviecountries
DROP COLUMN country;

-- Setting up new PK's and FK's
ALTER TABLE ONLY public.imdb_moviecountries
ADD CONSTRAINT imdb_moviecountries_pkey PRIMARY KEY (movieid, country_id);

ALTER TABLE ONLY public.imdb_moviecountries
ADD CONSTRAINT imdb_moviecountries_country_id_fkey FOREIGN KEY (country_id) REFERENCES public.countries(country_id);


-- IMDB_MOVIEGENRES
-- Creating new genres table
CREATE TABLE public.genres(
    genre_id integer PRIMARY KEY NOT NULL,
    genre character varying(32) NOT NULL
);
ALTER TABLE public.genres OWNER TO alumnodb;

-- Creating sequence of the id (PK) before inserting
CREATE SEQUENCE public.genres_genre_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.genres_genre_id_seq OWNER TO alumnodb;

ALTER SEQUENCE public.genres_genre_id_seq OWNED BY public.genres.genre_id;

ALTER TABLE ONLY public.genres ALTER COLUMN genre_id SET DEFAULT nextval('public.genres_genre_id_seq'::regclass);

-- Inserting genres
INSERT INTO public.genres(genre)
SELECT DISTINCT genre
FROM public.imdb_moviegenres;

-- Adding new genre_id column
ALTER TABLE public.imdb_moviegenres
ADD COLUMN genre_id integer;

-- Updating column with genres ids
UPDATE imdb_moviegenres
SET genre_id=genres.genre_id
FROM genres
WHERE imdb_moviegenres.genre=genres.genre;

-- Deleting column with genres strings
ALTER TABLE imdb_moviegenres
DROP COLUMN genre;

-- Setting up new PK's and FK's
ALTER TABLE ONLY public.imdb_moviegenres
ADD CONSTRAINT imdb_moviegenres_pkey PRIMARY KEY (movieid, genre_id);

ALTER TABLE ONLY public.imdb_moviegenres
ADD CONSTRAINT imdb_moviegenres_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genres(genre_id);

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (customerid, movieid); 

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_customer_id_fkey FOREIGN KEY (customerid) REFERENCES public.customers(customerid),
    ADD CONSTRAINT ratings_movie_id_fkey FOREIGN KEY (movieid) REFERENCES public.imdb_movies(movieid);

-------------------------------------------------------------------------
-- INSERTING BALANCE COLUMN IN CUSTOMERS TABLE

CREATE OR REPLACE FUNCTION setCostumersBalance(initialBalance integer) 
   RETURNS INTEGER AS
$$
BEGIN
   RETURN floor(random()* (initialBalance-0 + 1) + 0);
END;
$$ language 'plpgsql' STRICT;



-- Creating column
ALTER TABLE public.customers
ADD COLUMN balance INTEGER NOT NULL DEFAULT setCostumersBalance(100);


 
-----------------------------------------------------------------------


-----------------------------------------------------------------------
-- RESOLVING INCONSISTENCY WITH PRODUCTS.SALES AND ORDERS

UPDATE products
SET sales=S.sum_q
FROM (
    SELECT prod_id, sum(quantity) AS sum_q
    FROM orderdetail
    GROUP BY prod_id
) S
WHERE products.prod_id=S.prod_id;
-----------------------------------------------------------------------


-----------------------------------------------------------------------
-- CREATING NEW ALERTAS TABLE

--CREATE TABLE public.alerts(
--    prod_id integer PRIMARY KEY NOT NULL
--);
--ALTER TABLE public.alerts OWNER TO alumnodb;

--ALTER TABLE ONLY public.alerts
--ADD CONSTRAINT alertas_prod_id_fkey FOREIGN KEY (prod_id) REFERENCES public.products(prod_id);
-----------------------------------------------------------------------


-----------------------------------------------------------------------

-- Creating a auxliary table (view) to set updated price (setPrice.sql file)
CREATE VIEW new_price_table AS
SELECT orderdetail.orderid,
       orderdetail.prod_id,
       -- Current_price / ((1.02)^(current_year - order_year)) -> casted to numeric to be rounded later
       ROUND(
            CAST(
                (products.price * POWER(1.02, -(DATE_PART('year', now()::date) - DATE_PART('year', orderdate))))
            AS numeric),
        2) AS new_price
FROM products, orders, orderdetail
WHERE products.prod_id=orderdetail.prod_id
    AND orders.orderid=orderdetail.orderid;

