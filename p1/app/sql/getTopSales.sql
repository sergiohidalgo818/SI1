--D)PROCEDIMIENTO ALMACENADO PARA OBTENER LAS PELÍCULAS MAS VENDIDAS DE CADA AÑO
CREATE OR REPLACE FUNCTION getTopSales( "primeranyo" int, "ultimoanyo" int) 
RETURNS table (year text, film varchar, sales int)AS $$
BEGIN
RETURN QUERY
SELECT * FROM (
SELECT DISTINCT ON (DATEPART(year, o.orderdate))
    imdb_movies.movietitle :: VARCHAR AS title,
    DATEPART(year, orders.orderdate) :: TEXT AS year,
    sum(orderdetail.quantity) :: INT AS copies
FROM imdb_movies
JOIN orders ON orderdetail.orderid = orders.orderid 
JOIN imdb_products ON imdb_products.movieid = imdb_movies.movieid 
JOIN orderdetail ON imdb_products.prod_id = orderdetail.prod_id
WHERE DATEPART(year, orders.orderdate) :: int between "primeranyo" and "ultimoanyo"
GROUP BY imdb_movies.movietitle, DATEPART(year, orders.orderdate)
ORDER BY DATEPART(year, orders.orderdate) desc, sum(op.quantity) desc) as film_select
order by film_select.copies desc;
END;
$$ LANGUAGE plpgsql;