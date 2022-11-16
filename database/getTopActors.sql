CREATE OR REPLACE FUNCTION getTopActors(
    genre CHAR,
    OUT Actor varchar,
    OUT Num bigINT,
    OUT Debut text,
    OUT Film varCHAR,
    OUT Director varCHAR
) RETURNS SETOF record AS $$ BEGIN RETURN QUERY (
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
                MIN(year) as minyear,
                numfilms
            from
                (
                    select
                        Count(*) as numfilms,
                        actorid
                    from
                        imdb_actormovies natural
                        join imdb_moviegenres natural
                        join genres
                    where
                        genres.genre = $1
                    group by
                        actorid
                    having
                        Count(*) > 4
                    order by
                        count(*) desc
                ) as topactors natural
                join imdb_actormovies natural
                join imdb_movies natural
                join imdb_moviegenres natural
                join genres
            where
                genres.genre = $1
            group by
                actorid,
                numfilms
        ) as actoryeardebut natural
        join imdb_actors natural
        join imdb_actormovies natural
        join imdb_movies natural
        join imdb_directormovies natural
        join imdb_directors
    where
        year = minyear
    order by
        numfilms desc
);

END;

$$ LANGUAGE plpgsql;