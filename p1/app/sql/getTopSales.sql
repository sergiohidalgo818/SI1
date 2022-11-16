CREATE OR REPLACE FUNCTION getTopsales(integer) 
RETURNS TABLE(
	año int, 
	pelicula varchar(255), 
	ventas numeric
    ) 
AS $$
BEGIN
	RETURN QUERY 
	SELECT DISTINCT ON (year) EXTRACT(YEAR FROM orderdate)::int AS year, movietitle, SUM(quantity) AS sales
	FROM imdb_movies NATURAL JOIN products NATURAL JOIN orderdetail NATURAL JOIN orders
	WHERE EXTRACT(YEAR FROM orderdate)::int >= $1
	GROUP BY imdb_movies.movieid, EXTRACT(YEAR FROM (DATE(orders.orderdate)))
	ORDER BY year, sales DESC;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM getTopVentas(2015);

--Miguel
create or replace function getTopSales(year1 integer, year2 integer, out year integer, out film char, out sales bigint)
    RETURNS Setof record as
$$
    declare
    begin
        return query
        select cast(s3.año as integer), s3.film, s3.sales from(
        select s2.ano as año, s2.film as film , s2.sales as sales, ROW_NUMBER() OVER (partition by s2.ano order by s2.ano desc, s2.sales desc) as contador from(
        select s1.ano,cast(s1.Film as bpchar) as film, cast(s1.Sales as bigint)as sales from(
        select im.movietitle as Film,date_part('year', o2.orderdate) as ano, im.movieid, sum(o.quantity) as Sales , im.year as Año 
        from imdb_movies im join products p on im.movieid  = p.movieid 
            join orderdetail o on p.prod_id = o.prod_id 
            join orders o2 on o.orderid = o2.orderid
        where date_part('year', o2.orderdate) between year1 and year2
        group by im.movieid, date_part('year', o2.orderdate)) as s1
        order by s1.ano desc, s1.sales desc) as s2
        order by s2.ano desc , s2.sales desc) as s3
        where contador='1'
        order by sales desc;
    end
    
$$ LANGUAGE 'plpgsql';

select * from getTopSales(2016,2022);
create or replace function getTopSales(year1 integer, year2 integer, out year integer, out film char, out sales bigint)
    RETURNS Setof record as
$$
    declare
    begin
        return query
        select cast(s3.año as integer), s3.film, s3.sales from(
        select s2.ano as año, s2.film as film , s2.sales as sales, ROW_NUMBER() OVER (partition by s2.ano order by s2.ano desc, s2.sales desc) as contador from(
        select s1.ano,cast(s1.Film as bpchar) as film, cast(s1.Sales as bigint)as sales from(
        select im.movietitle as Film,date_part('year', o2.orderdate) as ano, im.movieid, sum(o.quantity) as Sales , im.year as Año 
        from imdb_movies im join products p on im.movieid  = p.movieid 
            join orderdetail o on p.prod_id = o.prod_id 
            join orders o2 on o.orderid = o2.orderid
        where date_part('year', o2.orderdate) between year1 and year2
        group by im.movieid, date_part('year', o2.orderdate)) as s1
        order by s1.ano desc, s1.sales desc) as s2
        order by s2.ano desc , s2.sales desc) as s3
        where contador='1'
        order by sales desc;
    end
    
$$ LANGUAGE 'plpgsql';

select * from getTopSales(2016,2022);
