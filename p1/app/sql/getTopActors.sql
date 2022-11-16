create or replace function getTopActors(genre CHAR, OUT Actor char, OUT Num INT, OUT Debut INT, OUT Film CHAR, OUT Director CHAR)
RETURNS Setof record as
$$
    declare
    begin
        return query
        select * from(
        select cast(s1.actorname as bpchar) as Actor, s2.Num as Num, cast(s1.year as int) as Debut , cast(s1.movietitle as bpchar) as Film, cast(s1.directorname as bpchar) as Director from(
        select actorname, movietitle,directorname,ROW_NUMBER() OVER (partition by actorname order by actorname) as contador, year
        from imdb_actors ia natural join imdb_actormovies ia2 natural join imdb_movies natural join imdb_moviegenres im natural join imdb_directormovies id natural join imdb_directors id2  
        where im.genre=getTopActors.genre
        group by actorname, movietitle, directorname,year 
        order by actorname asc, year asc) as s1 join 
        (select * from(
        select actorname, cast(count(*) as int) as Num
        from imdb_actors ia natural join imdb_actormovies ia2 natural join imdb_movies natural join imdb_moviegenres im natural join imdb_directormovies id natural join imdb_directors id2
        where im.genre=getTopActors.genre
        group by actorname
        order by actorname asc) as prueba
        where prueba.Num > '4') as s2 on s1.actorname=s2.actorname and s1.contador=s2.Num) as fin
        order by fin.Num desc;
    end
$$ LANGUAGE 'plpgsql';

select * from getTopActors('Romance');