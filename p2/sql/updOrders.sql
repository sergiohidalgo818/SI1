--G)PROCEDIMIENTO ALMACENADO QUE GUARDE INFORMACION A CERCA DE ORDERS CUANDO SE ACTUALIZA EL CARRITO
CREATE OR REPLACE FUNCTION updOrderFun() RETURNS trigger AS $$ begin 
IF (TG_OP = 'UPDATE') THEN 
IF (OLD.quantity <> NEW.quantity) THEN
UPDATE orders 
SET totalamount = ( netamount :: FLOAT :: NUMERIC * (  1 :: FLOAT +(tax :: FLOAT :: NUMERIC / 100:: FLOAT :: NUMERIC ))) :: MONEY :: NUMERIC
WHERE NEW.orderid = orders.orderid ;
UPDATE orders 
SET totalamount = ( netamount::NUMERIC::FLOAT * (1 :: FLOAT +(tax :: FLOAT :: NUMERIC / 100 :: FLOAT :: NUMERIC))) :: MONEY :: NUMERIC 
WHERE o.orderid = NEW.orderid;
END IF;

ELSIF (TG_OP = 'INSERT') THEN
UPDATE orders
SET netamount = ( netamount :: NUMERIC + NEW.price :: NUMERIC * NEW.quantity :: NUMERIC ) :: MONEY :: NUMERIC
WHERE NEW.orderid = orders.orderid ;
UPDATE orders
SET totalamount = ( netamount :: FLOAT :: NUMERIC * (1 :: FLOAT +(tax :: FLOAT :: NUMERIC/100 :: FLOAT :: NUMERIC))) :: MONEY :: NUMERIC
WHERE NEW.orderid = orders.orderid ;

ELSIF (TG_OP = 'DELETE') THEN
UPDATE orders
SET netamount = (netamount :: NUMERIC - OLD.price :: NUMERIC * OLD.quantity :: NUMERIC) :: MONEY :: NUMERIC 
WHERE OLD.orderid = orders.orderid;
UPDATE orders
SET totalamount = (netamount :: FLOAT :: NUMERIC * (1 :: FLOAT + (tax :: FLOAT :: NUMERIC/100 :: FLOAT :: NUMERIC))) :: MONEY :: NUMERIC
WHERE OLD.orderid = orders.orderid;
END IF;
RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updOrders
AFTER UPDATE OR INSERT OR DELETE on orderdetail FOR EACH ROW EXECUTE PROCEDURE updOrderFun();
