CREATE OR REPLACE FUNCTION updRatingsFun() RETURNS trigger AS $$ BEGIN
    IF (TG_OP = 'DELETE') THEN 
        UPDATE imdb_movies SET ratingmean = ((ratingmean * ratingcount) - OLD.rating) / (ratingcount - 1) WHERE ratingcount >'1' AND movieid = OLD.movieid;
        UPDATE imdb_movies SET ratingmean = '0' WHERE  ratingcount >'1' AND movieid = OLD.movieid;        
        UPDATE imdb_movies SET ratingcount = ratingcount - 1 WHERE movieid = OLD.movieid;
        RETURN OLD;
    END IF;

        IF (TG_OP = 'INSERT') THEN
            UPDATE imdb_movies SET ratingmean = ((ratingmean * ratingcount) + NEW.rating) / (ratingcount + 1) WHERE movieid = NEW.movieid;
            UPDATE imdb_movies SET ratingcount =  ratingcount + 1 WHERE movieid = NEW.movieid;
            RETURN NEW;
        END IF;
        
        IF (TG_OP = 'UPDATE') THEN
            UPDATE imdb_movies SET ratingmean = ((ratingmean * ratingcount) - OLD.rating) / (ratingcount - 1) WHERE ratingcount >'1' AND movieid = NEW.movieid;
            UPDATE imdb_movies SET ratingmean = NEW.rating WHERE ratingcount >'1' AND movieid = NEW.movieid;
            UPDATE imdb_movies SET ratingmean = ((ratingmean * ratingcount) + NEW.rating) / (ratingcount + 1) WHERE movieid = NEW.movieid;
            RETURN NEW;
        END IF;

        RETURN NULL;
    END
$$ LANGUAGE 'plpgsql';

CREATE TRIGGER updRatings
AFTER UPDATE OR INSERT OR DELETE on ratings FOR EACH ROW EXECUTE PROCEDURE updRatingsFun();
