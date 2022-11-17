create or replace function updRatings()
returns trigger as 
$$

    begin
        if (TG_OP = 'DELETE') then 
            update imdb_movies set ratingmean = ((ratingmean * ratingcount) - old.rating) / (ratingcount - 1) where movieid = old.movieid and ratingcount >'1';
            update imdb_movies set ratingmean = '0' where movieid = old.movieid and ratingcount ='1';        
            update imdb_movies set ratingcount = ratingcount - 1 where movieid = old.movieid;
            return old;
        END IF;

        if (TG_OP = 'INSERT') then
            update imdb_movies set ratingmean = ((ratingmean * ratingcount) + new.rating) / (ratingcount + 1) where movieid = new.movieid;
            update imdb_movies set ratingcount =  ratingcount + 1 where movieid = new.movieid;
            return new;
        END IF;

        if (TG_OP = 'UPDATE') then
            update imdb_movies set ratingmean = ((ratingmean * ratingcount) - old.rating) / (ratingcount - 1) where movieid = new.movieid and ratingcount >'1';
            update imdb_movies set ratingmean = new.rating where movieid = new.movieid and ratingcount ='1';
            update imdb_movies set ratingmean = ((ratingmean * ratingcount) + new.rating) / (ratingcount + 1) where movieid = new.movieid;
            return new;
        END IF;

        return NULL;
    end
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updRatings
AFTER UPDATE OR INSERT OR DELETE on ratings FOR EACH ROW EXECUTE PROCEDURE updRatingsFun();
