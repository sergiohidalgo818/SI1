--E)PROCEDIMIENTO ALMACENADO PARA CONSEGUIR LOS ARTISTAS QUE MÁS HAN TRABAJADO
CREATE OR replace FUNCTION getTopActors( genreactor VARCHAR) RETURNS TABLE (actors VARCHAR, num INT,debut VARCHAR , film VARCHAR,director VARCHAR)AS $$
BEGIN
RETURN QUERY
SELECT tablejoin.actorname,tablejoin.num, tablejoin.debut, imdb_movies.movietitle, imdb_directors.directorname  FROM(
SELECT imdb_actors.actorid, imdb_actors.actorname,  min(imdb_movies."year") :: VARCHAR AS debut, count(imdb_actors.actorname) :: INT AS num FROM imdb_actors
JOIN imdb_actormovies imdb_actormovies ON imdb_actormovies.actorid = imdb_actors.actorid
JOIN imdb_movies imdb_movies ON imdb_actormovies.movieid = imdb_movies.movieid
JOIN imdb_moviegenres mg ON imdb_movies.movieid = mg.movieid
JOIN imdb_genres ON mg.genre_id = imdb_genres.genre_id
WHERE genreactor = imdb_genres.genre
GROUP BY imdb_actors.actorname,imdb_actors.actorid
ORDER BY count(imdb_actors.actorname) DESC )AS tablejoin 
JOIN imdb_actormovies ON imdb_actormovies.actorid = tablejoin.actorid
JOIN imdb_movies ON imdb_movies.year = tablejoin.debut AND imdb_actormovies.movieid = imdb_movies.movieid 
JOIN imdb_directormovies ON imdb_movies.movieid = imdb_directormovies.movieid 
JOIN imdb_directors ON imdb_directormovies.directorid = imdb_directors.directorid
WHERE tablejoin.num>4
ORDER BY tablejoin.debut DESC;
END;
$$ LANGUAGE plpgsql;

