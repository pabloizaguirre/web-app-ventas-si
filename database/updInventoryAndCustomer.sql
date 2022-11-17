
CREATE OR REPLACE FUNCTION updInventoryAndCustomer()
RETURNS TRIGGER AS $$
DECLARE
    rec RECORD;
BEGIN

    -- Updating products (inventory) information and customer's balance information
    FOR rec IN
        SELECT products.prod_id as prod_id, quantity, products.price as price, customerid 
        FROM orderdetail, orders, products
        WHERE OLD.orderid=orderdetail.orderid 
        AND products.prod_id=orderdetail.prod_id
    LOOP
        UPDATE products
        SET stock=stock-rec.quantity,
            sales=sales+rec.quantity
        WHERE prod_id=rec.prod_id;
        
        UPDATE customer
        SET balance = balance-rec.price
        WHERE customerid=rec2.customerid;

    END LOOP;
   
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER updInventoryAndCustomer
AFTER UPDATE
ON orders
FOR EACH ROW
WHEN (OLD.status IS DISTINCT FROM NEW.status)
EXECUTE PROCEDURE updInventoryAndCustomer();
