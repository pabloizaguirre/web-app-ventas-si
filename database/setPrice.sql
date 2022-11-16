-- Completar la columna price de la tabla orderdetail con los precios de la tabla products
-- que incrementan un 2% por cada año que pasa desde que se estrenó la película.
UPDATE
    public.orderdetail
SET
    price = public.products.price*(1 + 0.02*(EXTRACT(year FROM public.orders.orderdate) - cast(public.imdb_movies.year as int)))
from
    public.products, public.imdb_movies, public.orders

WHERE
public.orderdetail.prod_id = public.products.prod_id and
public.products.movieid = public.imdb_movies.movieid and
public.orderdetail.orderid = public.orders.orderid;