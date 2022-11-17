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