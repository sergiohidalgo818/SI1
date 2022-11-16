CREATE OR REPLACE FUNCTION setAmountOrder() RETURNS VOID
AS $$
BEGIN
	UPDATE orders
	SET amount = sum
	FROM 	(SELECT orderid, SUM(total2)
			FROM orderdetail GROUP BY orderid) AS aux
	WHERE orders.orderid = aux.orderid;
	UPDATE orders
	SET total = amount + (amount * (tax/100));	
END;
$$ LANGUAGE plpgsql;

SELECT setAmountOrder();

--Miguel
update orderdetail
set price = s1.price_setted
from
(select o.prod_id ,o.orderid,(p.price * o.quantity * power(1.02, extract(year from now()) - extract(year from o2.orderdate)))as price_setted
from products as p, orders as o2, orderdetail as o
where o.prod_id = p.prod_id and o2.orderid = o.orderid) as s1
where s1.prod_id=orderdetail.prod_id and s1.orderid=orderdetail.orderid;



create or replace procedure setOrderAmount()
AS $$
begin

    update orders 
    set netamount=s1.suma , totalamount= s1.suma + (s1.suma * (orders.tax/100) )
    from(
    select o.orderid, sum(od.price * od.quantity) as suma
    from orders o join orderdetail od on od.orderid = o.orderid
    group by o.orderid) as s1
    where s1.orderid = orders.orderid;

end
$$ LANGUAGE 'plpgsql';
call setOrderAmount();
