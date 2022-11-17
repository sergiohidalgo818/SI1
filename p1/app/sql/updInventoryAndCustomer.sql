CREATE OR REPLACE FUNCTION updInventoryAndCustomerFunction() RETURNS trigger AS $$ BEGIN
	 IF (NEW.status = 'Paid' ) THEN
	 UPDATE customers
	 SET balance = balance - NEW.totalamount
	 WHERE customerid = NEW.customerid;
	 UPDATE imdb_products 
	 SET stock = stock -(SELECT sum(quantity) FROM orderdetail WHERE prod_id = imdb_products.prod_id AND orderid = NEW.orderid ),
        sales = sales + (SELECT sum(quantity) FROM orderdetail WHERE prod_id = imdb_products.prod_id AND orderid = NEW.orderid )
     WHERE prod_id in (SELECT prod_id FROM orderdetail WHERE orderid = NEW.orderid);	
	 END IF;
    RETURN NULL;
END;
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updInventoryAndCustomer
AFTER UPDATE  ON  orders FOR EACH ROW EXECUTE PROCEDURE updInventoryAndCustomerFunction();

