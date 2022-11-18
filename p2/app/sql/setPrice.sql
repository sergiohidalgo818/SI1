--B)CONSULTA SET PRICE
UPDATE orderdetail
SET price = setprice.pricetoset
FROM (
SELECT orderdetail.prod_id , orderdetail.orderid,(orderdetail.quantity * products.price * POW(1.02 , extract(year FROM NOW()) - extract(year FROM orders.orderdate))) AS pricetoset
FROM products, orders, orderdetail
WHERE orderdetail.prod_id = products.prod_id AND orders.orderid = orderdetail.orderid) AS setprice
WHERE orderdetail.prod_id = setprice.prod_id AND setprice.orderid = orderdetail.orderid;


