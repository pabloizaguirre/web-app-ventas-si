create or replace function updOrders() returns trigger as $$
begin 
	if (tg_op = 'INSERT') then 
		update public.orders 
		set 
			orderdate = NOW(),
			netamount = netamount + new.price,
			totalamount = ROUND(netamount * (100 + tax) / 100, 2)
		where 
			orderid = new.orderid;
		return new;
	end if;
			
end;
$$ language plpgsql;

create or replace trigger t_updOrders after insert or update or delete on orderdetail
for each row execute function updOrders();