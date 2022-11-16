CREATE OR REPLACE FUNCTION updOrders()
RETURNS TRIGGER
AS $$
BEGIN
	-- Para insertar en ordertails
	IF (TG_OP = 'INSERT') THEN
		NEW.total2 = (SELECT price FROM products WHERE products.prod_id = NEW.prod_id) * NEW.quantity;

		UPDATE orders
		SET netamount = netamount + NEW.total2
		WHERE orders.orderid = NEW.orderid;

		UPDATE orders
		SET totalamount = netamount + (netamount * (tax/100))
		WHERE orders.orderid = NEW.orderid;
		RETURN NEW;
		
	-- Borrar en ordertails
	ELSIF (TG_OP = 'DELETE') THEN
		UPDATE orders
		SET netamount = netamount - OLD.total2
		WHERE orders.orderid = OLD.orderid;
		
		UPDATE orders
		SET totalamount = netamount + (netamount * (tax/100))
		WHERE orders.orderid = OLD.orderid;
		RETURN OLD;
		
	-- Update en ordertails
	ELSE
		NEW.total2 = (SELECT price FROM products WHERE products.prod_id = OLD.prod_id) * NEW.quantity;

		UPDATE orders
		SET netamount = netamount + (NEW.total2 - OLD.total2)
		WHERE orders.orderid = NEW.orderid;

		UPDATE orders
		SET totalamount = netamount + (netamount * (tax/100))
		WHERE orders.orderid = NEW.orderid;
		RETURN NEW;		
	END IF;
	
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_updOrders BEFORE INSERT OR UPDATE OR DELETE
ON orderdetail FOR EACH ROW 
EXECUTE PROCEDURE updOrders();


--Miguel
create or replace function updOrders()
returns trigger as 
$$

    begin
        if (TG_OP = 'DELETE') then
            update orders set netamount = netamount - (old.price * old.quantity) where orderid = old.orderid;
            update orders set totalamount = netamount + (netamount * tax/100) where orderid = old.orderid;
            return old;
        END IF;
        
        if (TG_OP = 'INSERT') then
            update orders set netamount = netamount + (new.price * new.quantity) where orderid = new.orderid;
            update orders set totalamount = netamount + (netamount * tax/100) where orderid = new.orderid;
            return new;
        END IF;
        if (TG_OP = 'UPDATE') then
            update orders set netamount = netamount - (old.price * old.quantity) where orderid = new.orderid;
            update orders set netamount = netamount + (new.price * new.quantity) where orderid = new.orderid;
            update orders set totalamount = netamount + (netamount * tax/100) where orderid = new.orderid;
            return new;
        END IF;

        return NULL;
    end
$$ LANGUAGE 'plpgsql';


create trigger updOrders before insert or update or delete on orderdetail
  for each row execute procedure updOrders();

--delete from orderdetail where orderid='1' and prod_id='1938'
--insert into orderdetail values('1', '1938','11.444','1')
--update orderdetail set price='11.444' where orderid='1' and prod_id='1938'
