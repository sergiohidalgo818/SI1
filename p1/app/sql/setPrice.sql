-- Tomi
UPDATE orderdetail
SET total2 =  quantity * natural_join.price/power(1.02, (2020 - natural_join.year))
FROM (  SELECT orderid, prod_id, price, EXTRACT(YEAR FROM (DATE(orders.orderdate))) AS year
	FROM products NATURAL JOIN orderdetail NATURAL JOIN orders) AS natural_join
WHERE natural_join.orderid = orderdetail.orderid;

-- Miguel
update orderdetail
set price = s1.price_setted
from
(select o.prod_id ,o.orderid,(p.price * o.quantity * power(1.02, extract(year from now()) - extract(year from o2.orderdate)))as price_setted
from products as p, orders as o2, orderdetail as o
where o.prod_id = p.prod_id and o2.orderid = o.orderid) as s1
where s1.prod_id=orderdetail.prod_id and s1.orderid=orderdetail.orderid;