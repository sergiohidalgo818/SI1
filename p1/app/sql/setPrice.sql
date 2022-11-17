--B)CONSULTA SET PRICE
UPDATE orderdetail
SET price = setprice.pricetoset
FROM (
SELECT orderdetail.prod_id , orderdetail.orderid,(orderdetail.quantity * products.price * POW(1.02 , extract(year from now()) - extract(year from orders.orderdate))) as pricetoset
from products, orders, orderdetail
where orderdetail.prod_id = products.prod_id and orders.orderid = orderdetail.orderid) as setprice
where orderdetail.prod_id = setprice.prod_id and setprice.orderid = orderdetail.orderid;

--C)PROCEDIMIENTO ALMACENADO
CREATE FUNCTION setOrderAmount() returns void as $$ 
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
SET totalamount = (netamount :: FLOAT :: NUMERIC * (1.0 :: FLOAT + (tax :: FLOAT :: NUMERIC/100 :: FLOAT :: NUMERIC))) :: NUMERIC :: MONEY;

END;
$$ LANGUAGE 'plpgsql';
