from flask import Flask, jsonify

from utils import search_by_title, search_by_date, find_film_by_rating, find_film_by_genre

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/movie/<title>")
def get_film_page(title):
    res = search_by_title(title)
    return jsonify(res)


@app.route("/movie/<int:year_1>/to/<int:year_2>")
def search_year_page(year_1, year_2):
    result = search_by_date(year_1, year_2)
    return jsonify(result)


@app.route("/rating/<rating>")
def search_rating_page(rating):
    result = find_film_by_rating(rating)
    return jsonify(result)


@app.route("/genre/<genre>")
def search_genre_page(genre):
    result = find_film_by_genre(genre)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
