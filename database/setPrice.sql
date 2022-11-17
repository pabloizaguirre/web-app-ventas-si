-- Completar la columna price de la tabla orderdetail con los precios de los productos en el 
-- momento de compra, teniendo en cuenta que el precio ha ido aumentando un 2% anualmente.
UPDATE
    public.orderdetail
SET
    price = ROUND(public.products.price/POW(1.02, EXTRACT (year FROM NOW()) - EXTRACT(year FROM public.orders.orderdate)), 2)
FROM
    public.products, public.imdb_movies, public.orders

WHERE
    public.orderdetail.prod_id = public.products.prod_id AND
    public.products.movieid = public.imdb_movies.movieid AND
    public.orderdetail.orderid = public.orders.orderid;