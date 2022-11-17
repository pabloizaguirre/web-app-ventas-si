dropdb -U alumnodb -h localhost si1
createdb -U alumnodb -h localhost si1 
gunzip -c dump_v1.7.sql.gz | psql -U alumnodb -h localhost si1
psql si1 -U alumnodb -h localhost -f actualiza.sql
psql si1 -U alumnodb -h localhost -f setPrice.sql
psql si1 -U alumnodb -h localhost -f setOrderAmount.sql
psql si1 -U alumnodb -h localhost -f getTopSales.sql
psql si1 -U alumnodb -h localhost -f getTopActors.sql
psql si1 -U alumnodb -h localhost -f updOrders.sql
psql si1 -U alumnodb -h localhost -f updInventoryAndCustomer.sql