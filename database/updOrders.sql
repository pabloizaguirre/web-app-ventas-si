create or replace function updOrders() returns trigger as $$
begin 
	if (tg_op = 'INSERT') then 
		update public.orders 
		set 
			orderdate = NOW(),
			netamount = netamount + new.price * new.quantity
		where 
			orderid = new.orderid;
		update public.orders 
		set 
			totalamount = ROUND(netamount * (100 + tax) / 100, 2)
		where 
			orderid = new.orderid;
		return new;
	elsif (tg_op = 'UPDATE') then
		update public.orders
		set
			orderdate = NOW(),
			netamount = netamount + (new.quantity - old.quantity) * new.price
		where
			orderid = new.orderid;
		update public.orders
		set
			totalamount = ROUND(netamount * (100 + tax)/100, 2)
		where
			orderid = new.orderid;
		return new;
	else 
		update public.orders 
		set
			orderdate = NOW(),
			netamount = netamount - old.quantity * old.price
		where 
			orderid = old.orderid;
		update public.orders 
		set
			totalamount = ROUND(netamount * (100 + tax)/100, 2)
		where 
			orderid = old.orderid;
		return old;
	end if;
end;
$$ language plpgsql;

create or replace trigger t_updOrders after insert or update or delete on orderdetail
for each row execute function updOrders();