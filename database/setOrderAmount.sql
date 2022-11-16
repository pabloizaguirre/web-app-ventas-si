create or replace procedure setOrderAmount()
language plpgsql
as $$
declare
begin 
	-- Updating netamount values of orders table
        UPDATE orders
        SET netamount=S.sum_price
        FROM (
            SELECT orderid, sum(totalprice) AS sum_price
            FROM (select orderid, price * quantity as totalprice from orderdetail) as totalpriceorder
            GROUP BY orderid
        ) S
        WHERE orders.orderid=S.orderid;

        -- Updating totalamount values of orders table (netamount + taxes)
        UPDATE orders
        SET totalamount=T.ta
        FROM (
            SELECT orderid, ROUND(
                                ((netamount*(tax/100)) + netamount)
                                , 2) AS ta
            FROM orders
        ) T
        WHERE orders.orderid=T.orderid;
end; $$