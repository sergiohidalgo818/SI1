--B)CONSULTA SET PRICE
UPDATE orderdetail
SET price = setprice.pricetoset
FROM (
SELECT orderdetail.prod_id , orderdetail.orderid,(orderdetail.quantity * products.price * POW(1.02 , extract(year FROM NOW()) - extract(year FROM orders.orderdate))) AS pricetoset
FROM products, orders, orderdetail
WHERE orderdetail.prod_id = products.prod_id AND orders.orderid = orderdetail.orderid) AS setprice
WHERE orderdetail.prod_id = setprice.prod_id AND setprice.orderid = orderdetail.orderid;

--C)PROCEDIMIENTO ALMACENADO QUE INDICA EL VALOR DE LAS PELICULAS CON UN INCREMENTO DEL 2% CON EL PASO DE LOS AÑOS
CREATE OR REPLACE FUNCTION setOrderAmount() returns void as $$ 
BEGIN
UPDATE orders
SET netamount = sumorder.price :: NUMERIC :: MONEY
FROM(
        SELECT SUM(orderdetails.price * orderdetails.quantity) AS price, orderid 
		FROM orderdetails
        GROUP BY orderdetails.orderid
) AS sumorder WHERE orders.orderid = sumorder.orderid;

-- EN ESTA PARTE SE CALCULA EL TOTALAMOUNT
UPDATE orders 
SET totalamount = (netamount :: FLOAT :: NUMERIC * (1.0 :: FLOAT + (tax :: FLOAT :: NUMERIC/100 :: FLOAT :: NUMERIC))) :: MONEY :: NUMERIC;

END;
$$ LANGUAGE 'plpgsql';
