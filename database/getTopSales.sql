CREATE OR REPLACE FUNCTION getTopSales(year INT, year2 INT)
    RETURNS TABLE (
        Years integer,
        Film varchar,
        sales bigint)
    AS $$

    BEGIN
        RETURN QUERY
        SELECT cast(yr as integer), movietitle, cast(MaxSalesYear as bigint) 

            FROM
                imdb_movies,
                (
                    SELECT AUX.movieid, MaxSalesPerYearTable.MaxSalesYear, MaxSalesPerYearTable.yr, AUX.prod_id as prod_id
                    FROM (
                        SELECT movieid, DATE_PART('year', orderdate) as yr, sum(quantity) as Sales_per_year, products.prod_id as prod_id
                        FROM orders, orderdetail, products
                        WHERE orders.orderid=orderdetail.orderid
                            AND orderdetail.prod_id=products.prod_id
                            AND DATE_PART('year', orderdate) BETWEEN $1 AND $2
                            GROUP BY yr, products.prod_id
                    ) AUX
                    INNER JOIN
                        (SELECT yr, max(Sales_per_year) as MaxSalesYear
                        FROM
                            (
                                SELECT movieid, DATE_PART('year', orderdate) as yr, sum(quantity) as Sales_per_year
                                FROM orders, orderdetail, products
                                WHERE orders.orderid=orderdetail.orderid
                                    AND orderdetail.prod_id=products.prod_id
                                    AND DATE_PART('year', orderdate) BETWEEN $1 AND $2
                                    GROUP BY yr, products.prod_id
                            ) AUX2
                        GROUP BY yr) MaxSalesPerYearTable
                    ON AUX.yr=MaxSalesPerYearTable.yr
                    AND AUX.Sales_per_year=MaxSalesPerYearTable.MaxSalesYear
                ) AS Auxiliar

            WHERE
                imdb_movies.movieid=Auxiliar.movieid;

    END;
$$ LANGUAGE plpgsql;
