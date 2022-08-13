import json
import sqlite3


# Структура таблицы
# -----------------------
# show_id — id тайтла
# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание
# -----------------------

def connect_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(sql).fetchall()

        return result


def search_by_title(title):
    """Функция, которая возвращает самый свежий фильм по названию фильма из БД"""
    sql_quary = f"""
            SELECT "title","country","release_year","listed_in","description"
            FROM netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC
            LIMIT 1
                """
    result = connect_db(sql_quary)

    for item in result:
        return dict(item)


def search_by_date(year1, year2):
    """Функция, которая возвращает названия фильмов в диапазоне между year1 и year2"""

    sql = f'''
           SELECT "title","release_year"
           FROM netflix
           WHERE "release_year" BETWEEN '{year1}' AND '{year2}'
           LIMIT 100
     '''

    result = connect_db(sql)
    dict_movies = []
    for item in result:
        dict_movies.append(dict(item))
    return dict_movies


def find_film_by_rating(rating):
    my_dict = {"children": ("G", "G"), "family": ("G", "PG", "PG-13"), "adult": ("R", "NC-17")}
    sql = f"""select "title","rating","description"
            FROM netflix
            where rating in {my_dict.get(rating, "R")}
            """
    dict_film = []
    result = connect_db(sql)
    for res in result:
        dict_film.append(dict(res))
    return dict_film


def find_film_by_genre(genre):
    sql = f"""select "title","description"
            from netflix
            where "listed_in" like "%{genre}"
            order by date_added desc
            limit 10
            """
    dict_film = []
    result = connect_db(sql)
    for res in result:
        dict_film.append(dict(res))
    return dict_film


def step_5(name1, name2):
    sql = f"""select "cast"
            FROM netflix
            where "cast" like "%{name1}%" and "cast" like "%{name2}%"
            
            """
    result = connect_db(sql=sql)
    actors_all = []
    # Собираем полный список всех актеров
    for movie in result:
        actors = movie[0].split(", ")
        actors_all.extend(actors)
    print(actors_all)

    # Оставляем тех, кто встречается дважды
    actors_seen_twice = {actor for actor in actors_all if actors_all.count(actor) > 2} - {name1, name2}
    print(actors_seen_twice)


def step_6(type, year, genre):
    """Функция, которая принимает три параметра и возвращает по ним фильмы"""

    sql = f'''
          SELECT title,description,listed_in
          FROM netflix
          WHERE type = '{type}'
          AND release_year = '{year}'
          AND listed_in LIKE '%{genre}%'
    '''
    dict_movies = []
    for item in connect_db(sql=sql):
        dict_movies.append(item)
    return dict_movies
