create or replace function updRatings() returns trigger as $$
begin 
	if (tg_op = 'DELETE') then
		update imdb_movies
		set ratingmean = (ratingmean * ratingcount - old.rating) / (ratingcount - 1),
			ratingcount = ratingcount - 1
		where movieid = old.movieid;
		return old;
	elsif (tg_op = 'INSERT') then
		update imdb_movies 
		set ratingmean = (ratingmean*ratingcount + new.rating)/(ratingcount + 1),
			ratingcount = ratingcount + 1
		where movieid = new.movieid
			and ratingcount is not NULL;
		
		update imdb_movies 
		set ratingmean = new.rating,
			ratingcount = 1
		where movieid = new.movieid
			and ratingcount is NULL;
		return new;
		
	else -- update
		update imdb_movies 
		set ratingmean = (ratingmean*ratingcount - old.rating + new.rating)/ratingcount
		where movieid = new.movieid;
		return new;
		
	end if;
end;
$$ language plpgsql;

create or replace trigger t_updRatings after insert or update or delete on ratings
for each row execute function updRatings();
