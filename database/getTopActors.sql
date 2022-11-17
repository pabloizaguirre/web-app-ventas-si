create or replace function getTopActors(
    genre char,
    out actor varchar,
    out num bigint,
    out debut text,
    out film varchar,
    out director varchar
) returns setof record as $$ begin return query (
    select
        actorname as actor,
        numfilms as num,
        year as debut,
        movietitle as film,
        directorname as director
    from
        (
            select
                actorid,
                min(year) as minyear,
                numfilms
            from
                (
                    select
                        count(*) as numfilms,
                        actorid
                    from
                        imdb_actormovies 
                        natural join imdb_moviegenres 
                        natural join genres
                    where
                        genres.genre = $1
                    group by
                        actorid
                    having
                        count(*) > 4
                    order by
                        count(*) desc
                ) as topactors 
                natural join imdb_actormovies 
                natural join imdb_movies 
                natural join imdb_moviegenres 
                natural join genres
            where
                genres.genre = $1
            group by
                actorid,
                numfilms
        ) as actoryeardebut 
        natural join imdb_actors 
        natural join imdb_actormovies 
        natural join imdb_movies 
        natural join imdb_directormovies 
        natural join imdb_directors
    where
        year = minyear
    order by
        numfilms desc
);

end;

$$ language plpgsql;